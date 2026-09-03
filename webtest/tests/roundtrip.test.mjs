/* Drives the real DeviceLink against a SIMULATED DEVICE that speaks the firmware's wire
   format, so the D-series checks are exercised end to end without hardware.  If this
   passes, the tool and the firmware agree about framing, CRC, the header layout and the
   two self-test opcodes. */
import { buildCommand, cobsDecode, cobsEncode, crc32, parseFrame, parseAck, Cmd, FrameType,
         PROTO_VERSION, HEADER_BYTES } from '../js/protocol.js';

let fails = 0;
const ok = (c, m) => { if (!c) { console.log('  FAIL', m); fails++; } else console.log('  ok  ', m); };

/* --- the simulated device: exactly what main.c does, written independently --- */
let seq = 0;
function emit(type, payload) {
  const body = new Uint8Array(HEADER_BYTES + payload.length + 4);
  const dv = new DataView(body.buffer);
  dv.setUint8(0, PROTO_VERSION); dv.setUint8(1, type);
  dv.setUint16(2, seq++ & 0xFFFF, true); dv.setUint32(4, 0, true);
  dv.setUint8(8, 1); dv.setUint8(9, 0);
  body.set(payload, HEADER_BYTES);
  dv.setUint32(body.length - 4, crc32(body, 0, body.length - 4), true);
  return cobsEncode(body);
}
function identityPayload(serial) {
  const d = new Uint8Array(14 + serial.length + 1);
  const dv = new DataView(d.buffer);
  dv.setUint8(0, PROTO_VERSION); dv.setUint8(1, 0); dv.setUint8(2, 3);
  dv.setUint8(3, 'B'.charCodeAt(0));
  dv.setUint32(4, 6 * 1024 * 1024, true);
  dv.setUint32(8, 0b111111, true);
  dv.setUint8(12, 1); dv.setUint8(13, 3);
  d.set(new TextEncoder().encode(serial), 14);
  return d;
}
/* FW-EEG-001 section 6.2: 0 opcode echoed, 1 reserved, 2 status, 3 result length, 4.. result.
   This simulation used to answer { opcode, 0xFF } with the identity and the loopback echo at
   offset 0 -- a THIRD shape, agreeing with neither the document nor main.c, which is how
   these tests stayed green while the firmware dispatched every command as START_SESSION. */
function ack(op, status, result = new Uint8Array(0)) {
  const p = new Uint8Array(4 + result.length);
  p[0] = op; p[1] = 0; p[2] = status; p[3] = result.length;
  p.set(result, 4);
  return emit(FrameType.CMD_ACK, p);
}
function deviceRespond(hostWire) {
  const body = cobsDecode(hostWire.subarray(0, hostWire.length - 1));
  const f = parseFrame(body);
  if (f.type !== FrameType.CMD) return null;
  const op = f.payload[0];
  if (op === Cmd.IDENTIFY) return ack(op, 0x00, identityPayload('TIOV-B-0007'));
  if (op === Cmd.LOOPBACK) return ack(op, 0x00, f.payload.subarray(1));
  return ack(op, 0x01);                    /* 0x01 = unknown opcode, section 6.2 */
}

/* --- exercise it --- */
const { decodeIdentity } = await import('../js/transport.js');

const idWire = deviceRespond(buildCommand(Cmd.IDENTIFY));
const idFrame = parseFrame(cobsDecode(idWire.subarray(0, idWire.length - 1)));
const idAck = parseAck(idFrame);
ok(idAck.opcode === Cmd.IDENTIFY, 'ack echoes the IDENTIFY opcode');
ok(idAck.status === 0x00, 'ack status is OK');
const id = decodeIdentity(idAck.result);
ok(id.unitSerial === 'TIOV-B-0007', `identity serial round trip: ${id.unitSerial}`);
ok(id.firmware === '0.3', `firmware version: ${id.firmware}`);
ok(id.boardRev === 'B', `board revision: ${id.boardRev}`);
ok(id.ringBytes === 6291456, `ring bytes: ${id.ringBytes}`);
ok(id.capabilities.provisioned === true, 'capability flags decode');

for (const pat of [new Uint8Array([0,1,2,0xFE,0xFF]),
                   Uint8Array.from({length:240},(_,i)=>(i*7)&0xFF),
                   new Uint8Array(200).fill(0)]) {
  const w = deviceRespond(buildCommand(Cmd.LOOPBACK, pat));
  const f = parseFrame(cobsDecode(w.subarray(0, w.length - 1)));
  const r = parseAck(f).result;
  const same = r.length === pat.length && r.every((b,i)=>b===pat[i]);
  ok(same, `loopback ${pat.length} bytes returned unchanged`);
}

// the full 256-value sweep the tool's D6 step performs
let sweep = true;
for (let base = 0; base < 256; base += 64) {
  const pat = Uint8Array.from({length:64},(_,i)=>(base+i)&0xFF);
  const w = deviceRespond(buildCommand(Cmd.LOOPBACK, pat));
  const f = parseFrame(cobsDecode(w.subarray(0, w.length - 1)));
  const r = parseAck(f).result;
  if (!(r.length === 64 && r.every((b,i)=>b===pat[i]))) sweep = false;
}
ok(sweep, 'all 256 byte values survive the round trip (step D6)');

console.log(fails ? `\n${fails} FAILED` : '\nround-trip against the simulated device passed');
process.exit(fails ? 1 : 0);
