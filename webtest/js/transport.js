/*
 * transport.js -- the WebSerial link to the device, and the command/response layer above it.
 *
 * Production code, shared with the study runner.  The connectivity tester and the runner
 * open the port the same way, read it the same way and recover from the same faults; only
 * the sink differs.
 *
 * WHY WEBSERIAL AND NOT WEBUSB.  The device presents both (FW-EEG-001 F-01): a CDC-ACM
 * interface and a vendor interface with a WebUSB descriptor.  WebSerial is used here because
 * it works on Windows, macOS, Linux and ChromeOS without a driver install, and because on
 * Windows the CDC-ACM interface binds to the in-box usbser.sys driver, which WebUSB cannot
 * then claim.  RFQ F-13 asks for WebSerial on desktop and WebUSB on Android for exactly
 * that reason.  The frame layer is identical either way; only openPort() changes.
 *
 * Licence: MIT.
 */

import { FrameDecoder, SequenceTracker, buildCommand, Cmd, FrameType, parseAck, ACK_STATUS } from './protocol.js';

/** pid.codes.  The PID is a placeholder until the programme's application is granted. */
export const USB_FILTERS = [{ usbVendorId: 0x1209 }];

export class TransportError extends Error {}

export class DeviceLink {
  constructor({ sink, onFrame = () => {}, onLog = () => {}, onState = () => {} } = {}) {
    this.sink = sink;
    this.onFrame = onFrame;
    this.onLog = onLog;
    this.onState = onState;
    this.port = null;
    this.reader = null;
    this.writer = null;
    this.decoder = new FrameDecoder();
    this.sequence = new SequenceTracker();
    this.reading = false;
    this.pending = [];            // command round trips awaiting their CMD_ACK
    this.state = 'closed';
  }

  static get supported() {
    // `'serial' in navigator` is true when the key exists with an undefined value, which is
    // exactly what a shim or a stubbed test environment produces.  Check the object.
    return typeof navigator !== 'undefined' && navigator.serial != null;
  }

  #setState(s) { this.state = s; this.onState(s); }

  /**
   * Ask the user for a port.  MUST be called from a user gesture -- a click -- because
   * Chromium will not show the chooser otherwise.  That is not a quirk to work around; it
   * is the permission model, and the study runner is bound by it too.
   */
  async requestPort() {
    if (!DeviceLink.supported)
      throw new TransportError(
        'This browser has no Web Serial API. Use Chrome, Edge or another Chromium browser ' +
        'on Windows, macOS, Linux or ChromeOS. Safari and Firefox do not implement it.');
    return navigator.serial.requestPort({ filters: USB_FILTERS });
  }

  /** Ports the user has already authorised: this is what makes reconnection one click. */
  async knownPorts() {
    if (!DeviceLink.supported) return [];
    return navigator.serial.getPorts();
  }

  async open(port) {
    this.port = port;
    // The device is USB CDC-ACM; the baud rate is not meaningful over USB but the API
    // requires one, and 921600 is what FW-EEG-001 names so host and device agree on paper.
    await this.port.open({ baudRate: 921600, bufferSize: 64 * 1024 });
    this.writer = this.port.writable.getWriter();
    this.#setState('open');
    this.onLog('port opened');
    this.#readLoop();
  }

  async close() {
    this.reading = false;
    try { if (this.reader) await this.reader.cancel(); } catch { /* already gone */ }
    try { if (this.writer) this.writer.releaseLock(); } catch { /* already gone */ }
    try { if (this.port) await this.port.close(); } catch { /* already gone */ }
    this.port = this.reader = this.writer = null;
    this.#setState('closed');
    this.onLog('port closed');
  }

  async #readLoop() {
    this.reading = true;
    while (this.reading && this.port?.readable) {
      this.reader = this.port.readable.getReader();
      try {
        for (;;) {
          const { value, done } = await this.reader.read();
          if (done) break;
          if (!value) continue;
          for (const frame of this.decoder.push(value)) this.#dispatch(frame);
        }
      } catch (e) {
        // A physically unplugged device lands here.  It is not an error condition to hide:
        // the operator needs to know the cable moved.
        this.onLog(`read stopped: ${e.message}`);
        this.#setState('lost');
      } finally {
        try { this.reader.releaseLock(); } catch { /* already released */ }
      }
      if (this.reading) await new Promise((r) => setTimeout(r, 100));
    }
  }

  #dispatch(frame) {
    this.sequence.observe(frame);
    if (frame.type === FrameType.CMD_ACK) {
      const ack = parseAck(frame);
      // FW-EEG-001 section 6.2 gives every ack the opcode it answers, so match on it
      // rather than assuming the next reply belongs to the oldest question.  Without
      // that, one command timing out made every later reply answer the wrong promise:
      // the late ack arrived, the queue shifted, and the next command resolved with the
      // previous command's result.
      const i = this.pending.findIndex((p) => p.opcode === ack.opcode);
      if (i >= 0) {
        const [p] = this.pending.splice(i, 1);
        clearTimeout(p.timer);
        p.resolve(ack);
        return;             // an ack answers a question; it is not stream data
      }
      // An ack nobody is waiting for: the command it belongs to already timed out, or
      // the device volunteered it.  Count it and drop it -- never hand it to a caller.
      this.stats.orphanAcks = (this.stats.orphanAcks ?? 0) + 1;
      this.onLog(`unmatched ack for opcode 0x${ack.opcode.toString(16).padStart(2, '0')}`
                 + ` (status 0x${ack.status.toString(16).padStart(2, '0')})`);
      return;
    }
    try { this.sink?.accept(frame); } catch (e) { this.onLog(`sink error: ${e.message}`); }
    this.onFrame(frame);
  }

  /** Send a command and wait for its CMD_ACK.  Rejects on timeout rather than hanging. */
  async command(opcode, payload = new Uint8Array(0), { timeoutMs = 2000 } = {}) {
    if (!this.writer) throw new TransportError('the port is not open');
    const wait = new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        const i = this.pending.findIndex((p) => p.timer === timer);
        if (i >= 0) this.pending.splice(i, 1);
        reject(new TransportError(
          `no reply to command 0x${opcode.toString(16).padStart(2, '0')} within ${timeoutMs} ms`));
      }, timeoutMs);
      this.pending.push({ opcode, resolve, reject, timer });
    });
    await this.writer.write(buildCommand(opcode, payload));
    return wait;
  }

  /* ---------------------------------------------------------------- self-test commands
   * Neither of these touches the converters, the electrodes or the card, so both are safe
   * on a bare bench unit.  They are the two the connectivity tester is built around.
   */

  /** CMD_IDENTIFY -- who are you?  Returns a decoded description. */
  async identify() {
    const ack = await this.command(Cmd.IDENTIFY);
    if (ack.status !== 0x00)
      throw new TransportError(`IDENTIFY returned status 0x${ack.status.toString(16).padStart(2, '0')}`);
    return decodeIdentity(ack.result);
  }

  /** CMD_LOOPBACK -- echo this back.  Proves COBS, CRC, both endpoints and the ack path. */
  async loopback(bytes) {
    const ack = await this.command(Cmd.LOOPBACK, bytes);
    const echoed = ack.result;
    if (echoed.length !== bytes.length)
      return { ok: false, why: `sent ${bytes.length} bytes, got ${echoed.length} back` };
    for (let i = 0; i < bytes.length; i++)
      if (echoed[i] !== bytes[i])
        return { ok: false, why: `byte ${i} came back 0x${echoed[i].toString(16)}, sent 0x${bytes[i].toString(16)}` };
    return { ok: true, bytes: bytes.length };
  }
}

/** Decode the CMD_IDENTIFY payload.  Layout is fixed by FW-EEG-001; see main.c. */
export function decodeIdentity(p) {
  if (p.length < 14) throw new TransportError(`identity payload is ${p.length} bytes, expected at least 14`);
  const dv = new DataView(p.buffer, p.byteOffset, p.byteLength);
  const caps = dv.getUint32(8, true);
  let end = 14;
  while (end < p.length && p[end] !== 0) end++;
  return {
    protoVersion: dv.getUint8(0),
    firmware: `${dv.getUint8(1)}.${dv.getUint8(2)}`,
    boardRev: String.fromCharCode(dv.getUint8(3)),
    ringBytes: dv.getUint32(4, true),
    capabilities: {
      cdc:        !!(caps & (1 << 0)),
      webusb:     !!(caps & (1 << 1)),
      microSD:    !!(caps & (1 << 2)),
      codec:      !!(caps & (1 << 3)),
      atecc:      !!(caps & (1 << 4)),
      provisioned:!!(caps & (1 << 5)),
    },
    rateCode: dv.getUint8(12),
    rateCount: dv.getUint8(13),
    unitSerial: new TextDecoder().decode(p.subarray(14, end)),
  };
}
