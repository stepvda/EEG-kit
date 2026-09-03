/*
 * protocol.js -- the EEG field kit wire format.  COBS framing, the 10-byte header, CRC-32.
 *
 * THIS FILE IS NOT TEST CODE.  It is the protocol layer of the production browser client,
 * written here first because the connectivity tester needs exactly the same thing and there
 * must never be two implementations of a wire format.  TOOL-EEG-022 uses it with an
 * inspector sink; the study runner will use it with a WebSocket sink to the TI One Voice
 * server.  Nothing in this file knows which.
 *
 * Normative source: FW-EEG-001 Rev C section 5.  Where this file and that document
 * disagree, the document governs and this file is wrong.
 *
 * Licence: MIT (firmware and its host tools).
 */

export const PROTO_VERSION = 1;

export const FrameType = {
  DATA: 1,
  STATUS: 2,
  EVENT: 3,
  GAP: 4,
  SIGNATURE: 5,
  CMD_ACK: 6,
  CMD: 16,          // host to device
};

export const FRAME_TYPE_NAME = Object.fromEntries(
  Object.entries(FrameType).map(([k, v]) => [v, k]));

export const Cmd = {
  START_SESSION: 0x01, STOP_SESSION: 0x02, BLOCK_START: 0x03, BLOCK_END: 0x04,
  SET_RATE: 0x05, SET_GAIN: 0x06, IMPEDANCE: 0x07, RETRANSMIT: 0x08,
  TIMING_SELFTEST: 0x09, LIGHTS: 0x0A, CLOCK_XCHG: 0x0B, PLAY_AT: 0x0C,
  FW_UPDATE_BEGIN: 0x0D, PROVISION: 0x0E,
  // connectivity self-test -- neither touches the converters or the electrodes
  IDENTIFY: 0x0F, LOOPBACK: 0x10,
};

export const RATE_HZ = { 0: 250, 1: 500, 2: 1000 };
export const HEADER_BYTES = 10;
export const SAMPLE_RECORD_BYTES = 50;

/* ------------------------------------------------------------------ CRC-32
 * IEEE 802.3, the same polynomial zlib uses, over the header and payload but not over
 * itself.  Table built once at module load.
 */
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let i = 0; i < 256; i++) {
    let c = i;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[i] = c >>> 0;
  }
  return t;
})();

export function crc32(bytes, from = 0, to = bytes.length) {
  let c = 0xFFFFFFFF;
  for (let i = from; i < to; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}

/* ------------------------------------------------------------------ COBS
 * Consistent Overhead Byte Stuffing.  The point of it here is that 0x00 never appears
 * inside a frame, so a decoder that joins a live stream mid-frame -- which is the normal
 * case when a browser tab opens on a device that is already running -- resynchronises at
 * the next 0x00 and loses at most one frame.
 */
export function cobsEncode(src) {
  const out = new Uint8Array(src.length + Math.ceil(src.length / 254) + 2);
  let codeIdx = 0, w = 1, code = 1;
  for (let i = 0; i < src.length; i++) {
    if (src[i] === 0) { out[codeIdx] = code; codeIdx = w++; code = 1; }
    else {
      out[w++] = src[i];
      if (++code === 0xFF) { out[codeIdx] = code; codeIdx = w++; code = 1; }
    }
  }
  out[codeIdx] = code;
  out[w++] = 0x00;                        // delimiter
  return out.subarray(0, w);
}

export function cobsDecode(src) {
  const out = new Uint8Array(src.length);
  let r = 0, w = 0;
  while (r < src.length) {
    const code = src[r];
    if (code === 0) return null;          // a 0 inside the body is malformed
    r++;
    for (let i = 1; i < code && r < src.length; i++) out[w++] = src[r++];
    if (code < 0xFF && r < src.length) out[w++] = 0;
  }
  return out.subarray(0, w);
}

/* ------------------------------------------------------------------ frames */
export class Frame {
  constructor(version, type, seq, firstSample, rateCode, nSamples, payload) {
    Object.assign(this, { version, type, seq, firstSample, rateCode, nSamples, payload });
  }
  get typeName() { return FRAME_TYPE_NAME[this.type] || `0x${this.type.toString(16)}`; }
  get rateHz() { return RATE_HZ[this.rateCode] ?? null; }
}

export class FrameError extends Error {
  constructor(reason, detail) { super(reason); this.reason = reason; this.detail = detail; }
}

/** Parse one already-COBS-decoded frame.  Throws FrameError; never returns a bad frame. */
export function parseFrame(buf) {
  if (buf.length < HEADER_BYTES + 4)
    throw new FrameError('short', `${buf.length} bytes, need at least ${HEADER_BYTES + 4}`);

  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const version = dv.getUint8(0);
  // A host that sees another version must REJECT the frame, not parse it (section 5.1).
  if (version !== PROTO_VERSION)
    throw new FrameError('version', `frame says version ${version}, this client speaks ${PROTO_VERSION}`);

  const want = dv.getUint32(buf.length - 4, true);
  const got = crc32(buf, 0, buf.length - 4);
  if (want !== got)
    throw new FrameError('crc', `header says ${want.toString(16)}, computed ${got.toString(16)}`);

  return new Frame(
    version,
    dv.getUint8(1),
    dv.getUint16(2, true),
    dv.getUint32(4, true),
    dv.getUint8(8),
    dv.getUint8(9),
    buf.subarray(HEADER_BYTES, buf.length - 4),
  );
}

/** Build a host-to-device command frame, COBS-encoded and delimited, ready to write. */
export function buildCommand(opcode, payload = new Uint8Array(0)) {
  const body = new Uint8Array(HEADER_BYTES + 1 + payload.length + 4);
  const dv = new DataView(body.buffer);
  dv.setUint8(0, PROTO_VERSION);
  dv.setUint8(1, FrameType.CMD);
  dv.setUint16(2, 0, true);          // the device does not check the host's sequence
  dv.setUint32(4, 0, true);
  dv.setUint8(8, 0);
  dv.setUint8(9, 0);
  body[HEADER_BYTES] = opcode;
  body.set(payload, HEADER_BYTES + 1);
  dv.setUint32(body.length - 4, crc32(body, 0, body.length - 4), true);
  return cobsEncode(body);
}

/**
 * Decode a CMD_ACK payload per FW-EEG-001 section 6.2:
 *
 *     0  opcode echoed   1  reserved, zero   2  status   3  result length   4..  result
 *
 * The opcode echo is what lets a host tell which command an acknowledgement answers.
 * Before this existed on the wire, IDENTIFY, LOOPBACK and CLOCK_XCHG returned their
 * result at offset 0 with no echo at all, and the host matched replies by arrival order.
 */
export function parseAck(frame) {
  const p = frame.payload;
  if (p.length < 4)
    throw new FrameError('ack', `CMD_ACK payload is ${p.length} bytes, section 6.2 needs at least 4`);
  const len = p[3];
  if (4 + len > p.length)
    throw new FrameError('ack', `CMD_ACK claims ${len} result bytes but carries ${p.length - 4}`);
  return {
    opcode: p[0],
    status: p[2],
    result: p.subarray(4, 4 + len),
    frame,
  };
}

export const ACK_STATUS = {
  0x00: 'ok', 0x01: 'unknown opcode', 0x02: 'bad length', 0x03: 'argument out of range',
  0x04: 'wrong state', 0x05: 'interlock: charger connected (S-01)', 0x06: 'not provisioned',
  0x07: 'hardware fault', 0x08: 'payload CRC or hash mismatch', 0x09: 'ATECC already locked',
  0x0A: 'timeout', 0x0B: 'not implemented in this build',
};

/* ------------------------------------------------------------------ stream decoder
 *
 * Feed it whatever arrives from the port, in whatever sized chunks the browser gives you,
 * and it yields whole frames.  It counts what it had to throw away, because on a long
 * recording those counters are the evidence that the link was clean.
 */
export class FrameDecoder {
  constructor({ maxFrameBytes = 4096 } = {}) {
    this.buf = new Uint8Array(0);
    this.maxFrameBytes = maxFrameBytes;
    this.stats = { frames: 0, crcErrors: 0, versionErrors: 0, shortFrames: 0,
                   oversizeDiscards: 0, resyncs: 0, bytesIn: 0 };
  }

  push(chunk) {
    this.stats.bytesIn += chunk.length;
    const merged = new Uint8Array(this.buf.length + chunk.length);
    merged.set(this.buf); merged.set(chunk, this.buf.length);
    this.buf = merged;

    const frames = [];
    let start = 0;
    for (;;) {
      const zero = this.buf.indexOf(0, start);
      if (zero < 0) break;
      const slice = this.buf.subarray(start, zero);
      start = zero + 1;
      if (slice.length === 0) continue;            // back-to-back delimiters
      const decoded = cobsDecode(slice);
      if (!decoded) { this.stats.resyncs++; continue; }
      try {
        frames.push(parseFrame(decoded));
        this.stats.frames++;
      } catch (e) {
        if (e.reason === 'crc') this.stats.crcErrors++;
        else if (e.reason === 'version') this.stats.versionErrors++;
        else this.stats.shortFrames++;
      }
    }
    this.buf = this.buf.subarray(start);
    // A run of noise with no delimiter must not grow without bound.
    if (this.buf.length > this.maxFrameBytes) {
      this.stats.oversizeDiscards++;
      this.buf = new Uint8Array(0);
    }
    return frames;
  }
}

/* ------------------------------------------------------------------ sequence tracking
 *
 * F-07: silent loss is not permitted.  The device emits a GAP frame when it drops, but the
 * host must also notice gaps the device could not report -- a USB stall, a closed tab, a
 * cable pulled and replaced.  This is the host half of that, and the production client
 * needs it exactly as written; the connectivity tester just displays it.
 */
export class SequenceTracker {
  constructor() { this.last = null; this.gaps = []; this.received = 0; this.missing = 0; }

  observe(frame) {
    this.received++;
    if (this.last !== null) {
      const expected = (this.last + 1) & 0xFFFF;
      if (frame.seq !== expected) {
        const lost = (frame.seq - expected) & 0xFFFF;
        // A huge jump is far more likely a resync than 60 000 genuinely lost frames.
        if (lost < 0x8000) {
          this.missing += lost;
          this.gaps.push({ from: expected, to: (frame.seq - 1) & 0xFFFF, lost });
        }
      }
    }
    this.last = frame.seq;
  }
}
