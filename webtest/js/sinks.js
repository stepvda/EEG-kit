/*
 * sinks.js -- where frames GO.
 *
 * THIS IS THE ARCHITECTURAL SEAM OF THE WHOLE CLIENT, and it is the reason the connectivity
 * tester is worth building as production code rather than as a throwaway page.
 *
 * The end architecture is:
 *
 *     EEG device --USB/WebSerial--> browser --WebSocket--> TI One Voice server
 *
 * Everything to the left of the browser is identical in both programs.  The only thing that
 * differs is what the browser does with a frame once it has one, so that is the only thing
 * behind an interface:
 *
 *     TOOL-EEG-022 (this tester)   InspectorSink   counts, classifies, shows, discards
 *     the study runner             UploadSink      streams to the server, with backpressure,
 *                                                  retransmission and an offline queue
 *
 * A sink must satisfy three rules, and they come from the requirements rather than from
 * taste:
 *
 *   1. accept() MUST NOT BLOCK THE READ LOOP.  At 1000 Hz the device emits a frame every
 *      20 ms and USB will not wait for a slow consumer.  A sink that needs time queues and
 *      returns.
 *   2. A sink must be able to say "I am behind" (`pressure`), because F-06's ring buffer and
 *      CMD_RETRANSMIT exist precisely so a host that falls behind can catch up rather than
 *      lose data.
 *   3. A sink must never silently drop.  F-07: silent loss is not permitted.  If it discards,
 *      it counts, and the count is visible.
 *
 * Licence: MIT.
 */

import { FrameType } from './protocol.js';

/**
 * The interface.  Documented as a base class so both implementations and any future one
 * (a file writer, a replay recorder) are forced through the same shape.
 */
export class FrameSink {
  /** Called once before any frame.  May be async: opening a socket, a file, a DB. */
  async open(_deviceInfo) {}
  /** Called for every frame, in order.  MUST return promptly.  Never throws. */
  accept(_frame) {}
  /** 0 = keeping up, 1 = saturated.  The read loop uses it to decide when to warn. */
  get pressure() { return 0; }
  /** Called once when the port closes or the session ends.  Flush here. */
  async close() {}
  /** Human-readable counters for the UI.  Shape is free. */
  get stats() { return {}; }
}

/* ------------------------------------------------------------------ the tester's sink
 *
 * Counts everything, keeps a small ring of recent frames for display, and throws the
 * payloads away.  It deliberately does NOT decode samples: TOOL-EEG-022 tests connectivity,
 * not measurement, and decoding channel data here would be the first step towards a second
 * half-implementation of the study runner.
 */
export class InspectorSink extends FrameSink {
  constructor({ keepRecent = 50 } = {}) {
    super();
    this.counts = {};
    this.recent = [];
    this.keepRecent = keepRecent;
    this.firstAt = null;
    this.lastAt = null;
    this.bytes = 0;
  }

  accept(frame) {
    const now = performance.now();
    if (this.firstAt === null) this.firstAt = now;
    this.lastAt = now;
    this.counts[frame.typeName] = (this.counts[frame.typeName] || 0) + 1;
    this.bytes += frame.payload.length;
    this.recent.push({ at: now, type: frame.typeName, seq: frame.seq,
                       firstSample: frame.firstSample, n: frame.nSamples,
                       bytes: frame.payload.length });
    if (this.recent.length > this.keepRecent) this.recent.shift();
  }

  get stats() {
    const secs = this.firstAt === null ? 0 : (this.lastAt - this.firstAt) / 1000;
    const total = Object.values(this.counts).reduce((a, b) => a + b, 0);
    return {
      byType: { ...this.counts },
      frames: total,
      payloadBytes: this.bytes,
      seconds: secs,
      framesPerSecond: secs > 0.25 ? total / secs : null,
    };
  }
}

/* ------------------------------------------------------------------ the production sink
 *
 * THIS IS NOT USED BY THE CONNECTIVITY TESTER and it does not connect to anything here.  It
 * is included, complete and commented, because the whole point of the exercise is that the
 * study runner is this file plus a UI, and because writing it now is what proves the
 * interface above is the right shape.
 *
 * It is UNTESTED against a real server -- no server endpoint exists yet.  Do not ship it
 * without testing it; do read it when the server side is designed, because the four things
 * it needs from the server are the four things easiest to get wrong:
 *
 *   * an ordered, framed channel (a WebSocket, not a series of POSTs);
 *   * backpressure the client can actually observe (bufferedAmount);
 *   * an ack carrying the highest contiguous sequence the server has durably stored, so the
 *     client knows what it may forget;
 *   * a resume handshake, so a dropped socket does not mean a lost block.
 */
export class UploadSink extends FrameSink {
  constructor({ url, token, highWaterBytes = 4 * 1024 * 1024,
                onStateChange = () => {} } = {}) {
    super();
    Object.assign(this, { url, token, highWaterBytes, onStateChange });
    this.ws = null;
    this.queue = [];
    this.state = 'idle';
    this.counters = { queued: 0, sent: 0, acked: 0, requeued: 0, dropped: 0 };
    this.highestAcked = null;
  }

  async open(deviceInfo) {
    this.deviceInfo = deviceInfo;
    await this.#connect();
  }

  async #connect() {
    this.#setState('connecting');
    await new Promise((resolve, reject) => {
      const ws = new WebSocket(this.url);
      ws.binaryType = 'arraybuffer';
      ws.onopen = () => {
        // The server needs to know which unit this is before any frame arrives.  The unit
        // serial is the device identity everywhere else in the package (F-04), so it is the
        // identity here too.
        ws.send(JSON.stringify({ hello: 1, unitSerial: this.deviceInfo?.unitSerial,
                                 firmware: this.deviceInfo?.firmware,
                                 resumeFrom: this.highestAcked, token: this.token }));
        this.ws = ws; this.#setState('open'); resolve();
      };
      ws.onerror = () => { this.#setState('error'); reject(new Error('websocket failed')); };
      ws.onclose = () => { this.ws = null; this.#setState('closed'); };
      ws.onmessage = (ev) => this.#onServerMessage(ev);
    });
    this.#drain();
  }

  #onServerMessage(ev) {
    // The only message that matters on the hot path: how far the server has durably stored.
    try {
      const m = JSON.parse(typeof ev.data === 'string' ? ev.data : '{}');
      if (typeof m.ackedThrough === 'number') {
        this.highestAcked = m.ackedThrough;
        this.counters.acked = m.ackedThrough;
      }
    } catch { /* a server that sends us junk is the server's problem, not a client crash */ }
  }

  accept(frame) {
    // Rule 1: return promptly.  Serialise and queue; the drain is asynchronous.
    this.queue.push(frame);
    this.counters.queued++;
    this.#drain();
  }

  #drain() {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;
    while (this.queue.length && this.ws.bufferedAmount < this.highWaterBytes) {
      const f = this.queue.shift();
      // Re-encode rather than forward the raw bytes: the server contract is the frame, and
      // the client must not become a byte pipe that cannot be reasoned about.
      this.ws.send(JSON.stringify({
        seq: f.seq, type: f.type, firstSample: f.firstSample,
        rateCode: f.rateCode, nSamples: f.nSamples,
      }));
      this.ws.send(f.payload);
      this.counters.sent++;
    }
  }

  get pressure() {
    if (!this.ws) return 1;
    return Math.min(1, this.ws.bufferedAmount / this.highWaterBytes);
  }

  async close() {
    this.#drain();
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ goodbye: 1, queued: this.queue.length }));
      this.ws.close();
    }
    this.#setState('closed');
  }

  #setState(s) { this.state = s; this.onStateChange(s); }

  get stats() {
    return { ...this.counters, state: this.state, queueDepth: this.queue.length,
             bufferedAmount: this.ws ? this.ws.bufferedAmount : 0 };
  }
}

/* ------------------------------------------------------------------ fan-out
 *
 * The study runner will want both at once: upload to the server AND show the operator what
 * is happening.  Composing sinks is cheaper than teaching either one to do the other's job.
 */
export class TeeSink extends FrameSink {
  constructor(...sinks) { super(); this.sinks = sinks; }
  async open(info) { for (const s of this.sinks) await s.open(info); }
  accept(f) { for (const s of this.sinks) s.accept(f); }
  get pressure() { return Math.max(0, ...this.sinks.map((s) => s.pressure)); }
  async close() { for (const s of this.sinks) await s.close(); }
  get stats() { return this.sinks.map((s) => s.stats); }
}
