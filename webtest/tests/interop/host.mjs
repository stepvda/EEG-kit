/* HOST: the real webtest protocol module against the compiled firmware. */
import { execFileSync } from 'node:child_process';
const P = await import(process.env.WT + '/js/protocol.js');
const T = await import(process.env.WT + '/js/transport.js');
const { buildCommand, FrameDecoder, Cmd, FrameType, PROTO_VERSION, HEADER_BYTES, parseAck, ACK_STATUS } = P;
const DEV = process.env.SC + "/device";

function exchange(op, payload = new Uint8Array(0), opts = []) {
  const out = execFileSync(DEV, opts, { input: Buffer.from(buildCommand(op, payload)), maxBuffer: 1 << 24 });
  const dec = new FrameDecoder();
  const frames = [...(dec.push(new Uint8Array(out)) ?? [])];
  return { frames, stats: dec.stats, bytes: out.length };
}

let pass = 0, fail = 0;
const check = (name, ok, detail = '') => {
  (ok ? pass++ : fail++);
  console.log(`  ${ok ? 'ok  ' : 'FAIL'}  ${name}${detail ? '   ' + detail : ''}`);
};

console.log('=== 1. every frame the device sends is well-formed ===');
{
  const r = exchange(Cmd.IDENTIFY);
  check('device answered IDENTIFY with exactly one frame', r.frames.length === 1, `${r.frames.length} frame(s), ${r.bytes} bytes`);
  check('CRC accepted by the host decoder', r.stats.crcErrors === 0, `crcErrors=${r.stats.crcErrors}`);
  check('no version errors', r.stats.versionErrors === 0);
  check('no short/oversize frames', r.stats.shortFrames === 0 && r.stats.oversizeDiscards === 0);
  const f = r.frames[0];
  if (f) check('frame type is CMD_ACK', f.type === FrameType.CMD_ACK, `type=${f.type}`);
}

console.log('\n=== 2. IDENTIFY decodes with the shipped decoder ===');
{
  const f = exchange(Cmd.IDENTIFY).frames[0];
  let id = null;
  try { id = T.decodeIdentity(parseAck(f).result); check('decodeIdentity() parsed the result', true); }
  catch (e) { check('decodeIdentity() parsed the payload', false, e.message); }
  if (id) {
    console.log('        ' + JSON.stringify({ proto: id.protoVersion, fw: id.firmware, rev: id.boardRev,
      ring: id.ringBytes, rate: id.rateCode, rates: id.rateCount, serial: id.unitSerial }));
    console.log('        caps ' + JSON.stringify(id.capabilities));
    check('protocol version matches the host', id.protoVersion === PROTO_VERSION, `device=${id.protoVersion} host=${PROTO_VERSION}`);
    check('unit serial is present and NUL-terminated', /^TIOV-/.test(id.unitSerial), `"${id.unitSerial}"`);
    check('ring buffer is the 6 MiB of FW-D13', id.ringBytes === 6 * 1024 * 1024, `${id.ringBytes} bytes`);
    check('capability: CDC advertised', id.capabilities.cdc);
    check('capability: WebUSB advertised', id.capabilities.webusb);
    check('capability: microSD advertised', id.capabilities.microSD);
    check('capability: codec advertised', id.capabilities.codec);
    check('capability: ATECC advertised', id.capabilities.atecc);
    check('rateCount is non-zero', id.rateCount > 0, `${id.rateCount}`);
  }
}

console.log('\n=== 3. LOOPBACK echoes exactly ===');
for (const n of [1, 4, 32, 64]) {
  const sent = Uint8Array.from({ length: n }, (_, i) => (i * 7 + 3) & 0xff);
  const f = exchange(Cmd.LOOPBACK, sent).frames[0];
  const got = f ? parseAck(f).result : new Uint8Array(0);
  const same = got.length === sent.length && sent.every((b, i) => got[i] === b);
  check(`loopback ${n} byte(s)`, same, same ? '' : `sent ${sent.length}, got ${got.length}`);
}

const ackOf = r => { const f = r.frames.find(f => f.type === FrameType.CMD_ACK); return f ? parseAck(f) : null; };
console.log('\n=== 4. commands are dispatched to the right handler ===');
for (const [name, op] of [['STOP_SESSION',0x02],['BLOCK_START',0x03],['BLOCK_END',0x04],
                          ['RETRANSMIT',0x08],['TIMING_SELFTEST',0x09],['LIGHTS',0x0a],
                          ['READ_PROVISION_STATE',0x48]]) {
  const f = ackOf(exchange(op));
  const echo = f ? f.opcode : null;
  const known = echo === op;
  check(`${name} (0x${op.toString(16).padStart(2,'0')}) acked its own opcode`, known,
        known ? '' : `ack carried 0x${echo === null ? '--' : echo.toString(16)}`);
  if (known && f.status !== 0x00)
    console.log(`        note: ${name} -> status 0x${f.status.toString(16).padStart(2,'0')} (${ACK_STATUS[f.status] ?? '?'})`);
}

{
  const f = ackOf(exchange(0x0b));
  check('CLOCK_XCHG returns a 12-byte timing result', f && f.result.length === 12,
        f ? `${f.result.length} bytes` : 'no ack');
  check('CLOCK_XCHG echoes its own opcode', f && f.opcode === 0x0b,
        f ? `0x${f.opcode.toString(16)}` : 'no ack');
}

console.log('\n=== 4b. the provisioning family uses the same envelope ===');
{
  // The provisioning path built its own {opcode,status,result} and called frame_emit()
  // directly, so it kept the pre-6.2 shape after everything else moved. provision.py reads
  // the status at payload offset 2, which under the old shape was the first RESULT byte --
  // and on READ_PROVISION_STATE that byte is the config-zone lock flag, so an unlocked unit
  // reported 0 and read as success. Checking the opcode echo alone did NOT catch it.
  const f = ackOf(exchange(0x48));                      // READ_PROVISION_STATE
  check('READ_PROVISION_STATE echoes its opcode', f && f.opcode === 0x48);
  check('READ_PROVISION_STATE reports status OK', f && f.status === 0x00,
        f ? `status=0x${f.status.toString(16)}` : 'no ack');
  check('READ_PROVISION_STATE returns 2 result bytes (locked, prov_open)',
        f && f.result.length === 2, f ? `${f.result.length} bytes` : 'no ack');
  // the simulated ATECC is unlocked and provisioning is closed, so both flags read 0
  check('an unlocked part reports locked=0 in the RESULT, not in the status',
        f && f.result.length === 2 && f.result[0] === 0 && f.status === 0,
        f ? `result=[${[...f.result]}] status=${f.status}` : 'no ack');
  const g = ackOf(exchange(0x41));                      // GENKEY, outside provisioning mode
  check('a provisioning command outside prov mode is refused with status 0x01',
        g && g.opcode === 0x41 && g.status === 0x01,
        g ? `op=0x${g.opcode.toString(16)} status=0x${g.status.toString(16)}` : 'no ack');
  check('a refusal carries no result bytes', g && g.result.length === 0,
        g ? `${g.result.length} bytes` : 'no ack');
}

console.log('\n=== 4c. calibration read-back (T6 acceptance) ===');
{
  // T6's acceptance limit is that the unit reads back what was written, and until
  // CMD_READ_CALIBRATION existed nothing could read it back at all.
  const req = (off, len) => {
    const p = new Uint8Array(3);
    p[0] = off & 0xff; p[1] = (off >> 8) & 0xff; p[2] = len;
    return ackOf(exchange(0x4a, p));
  };
  const a = req(0, 32);
  check('CMD_READ_CALIBRATION echoes its opcode', a && a.opcode === 0x4a);
  check('returns the requested length', a && a.result.length === 32,
        a ? `${a.result.length} bytes` : 'no ack');
  const patternOk = a && [...a.result].every((b, i) => b === ((i * 3 + 1) & 0xff));
  check('returns the stored bytes at offset 0', patternOk);
  const b = req(64, 16);
  const offsetOk = b && [...b.result].every((v, i) => v === (((64 + i) * 3 + 1) & 0xff));
  check('a non-zero offset returns that slice, not the start', offsetOk,
        b ? `first byte 0x${b.result[0].toString(16)}` : 'no ack');
  const c2 = req(0, 3);
  check('a short request is not padded', c2 && c2.result.length === 3);
  const d2 = ackOf(exchange(0x4a, new Uint8Array([0])));
  check('a malformed request is refused with bad-length', d2 && d2.status === 0x02,
        d2 ? `status=0x${d2.status.toString(16)}` : 'no ack');
}

console.log('\n=== 4d. the ATECC config-zone write (0x4B) ===');
{
  // 0x4A was allocated twice on the same day -- here for the config write, in main.c for
  // the calibration reader. A collision answers a config write with a calibration slice
  // and reports success, so the opcode is exercised here to keep the two apart.
  const good = new Uint8Array(1 + 32 + 32);
  good[0] = 0;                                  // block 0
  for (let i = 0; i < 32; i++) good[1 + i] = (i < 4) ? 0xff : 0x00;   // mask word 0 only

  // The write is gated on provisioning mode, so it must follow ENTER_PROV. Both frames go
  // into one stream: the device's receive loop consumes whatever arrives, exactly as it
  // would from a station that opened the port once.
  const two = (opA, pA, opB, pB) => {
    const a = buildCommand(opA, pA), b = buildCommand(opB, pB);
    const wire = new Uint8Array(a.length + b.length);
    wire.set(a, 0); wire.set(b, a.length);
    const out = execFileSync(DEV, [], { input: Buffer.from(wire), maxBuffer: 1 << 24 });
    const dec = new FrameDecoder();
    return [...(dec.push(new Uint8Array(out)) ?? [])]
      .filter(f => f.type === FrameType.CMD_ACK).map(parseAck);
  };
  const gated = ackOf(exchange(0x4b, good));
  check('a config write outside provisioning mode is refused', gated && gated.status === 0x01,
        gated ? `status=0x${gated.status.toString(16)}` : 'no ack');
  const seq = two(0x40, new Uint8Array(0), 0x4b, good);
  const a = seq.find(x => x.opcode === 0x4b);
  check('CMD_ATECC_WRITE_CONFIG echoes its own opcode', a && a.opcode === 0x4b,
        a ? `0x${a.opcode.toString(16)}` : 'no ack');
  check('a well-formed config write is accepted after ENTER_PROV', a && a.status === 0x00,
        a ? `status=0x${a.status.toString(16)}` : 'no ack');
  const shortSeq = two(0x40, new Uint8Array(0), 0x4b, new Uint8Array([0, 1, 2]));
  const short = shortSeq.find(x => x.opcode === 0x4b);
  check('a short config write is refused with bad-length', short && short.status === 0x02,
        short ? `status=0x${short.status.toString(16)}` : 'no ack');
  const cal = ackOf(exchange(0x4a, new Uint8Array([0, 0, 8])));
  check('0x4A is still the calibration reader, not the config write',
        cal && cal.opcode === 0x4a && cal.result.length === 8,
        cal ? `op=0x${cal.opcode.toString(16)} ${cal.result.length} bytes` : 'no ack');
}

console.log('\n=== 4b. CMD_LIGHTS answers honestly about the modes it has (FW-D18) ===');
{
  // This used to take the mode byte as a plain enable and answer 0x00 OK to every value,
  // so a host asking to force red was told it had succeeded while the device carried on
  // showing automatic colour. The forced modes are implemented now, and a mode the
  // firmware does not have must come back UNIMPLEMENTED rather than OK.
  const lights = (payload) => ackOf(exchange(0x0a, new Uint8Array(payload)));
  for (const [mode, name] of [[0, 'off'], [1, 'auto'], [2, 'force green'],
                              [3, 'force red'], [4, 'force amber']]) {
    const a = lights([mode]);
    check(`CMD_LIGHTS mode ${mode} (${name}) is accepted`,
          a && a.opcode === 0x0a && a.status === 0x00,
          a ? `status=0x${a.status.toString(16)}` : 'no ack');
  }
  const masked = lights([3, 0x0f]);
  check('CMD_LIGHTS takes an optional site mask', masked && masked.status === 0x00,
        masked ? `status=0x${masked.status.toString(16)}` : 'no ack');
  const bogus = lights([5]);
  check('a mode the firmware does not have is refused, not silently accepted',
        bogus && bogus.status === 0x0b,
        bogus ? `status=0x${bogus.status.toString(16)}` : 'no ack');
  const stunted = lights([]);
  check('CMD_LIGHTS with no mode byte is refused with bad-length',
        stunted && stunted.status === 0x02,
        stunted ? `status=0x${stunted.status.toString(16)}` : 'no ack');
}

console.log('\n=== 5. S-01 interlock: refuse to start while charging ===');
{
  const norm = ackOf(exchange(0x01));
  const chg  = ackOf(exchange(0x01, new Uint8Array(0), ['--vbus']));
  check('START_SESSION accepted on battery', norm && norm.status === 0x00, `status=0x${(norm?.status??255).toString(16)}`);
  check('START_SESSION refused with VBUS present', chg && chg.status === 0x05, `status=0x${(chg?.status??255).toString(16)} = ${ACK_STATUS[chg?.status] ?? '?'}`);
}

console.log('\n=== 6. the device ignores malformed traffic ===');
{
  const good = buildCommand(Cmd.IDENTIFY);
  const bad = Uint8Array.from(good); bad[bad.length - 2] ^= 0xff;       // corrupt the CRC
  const r1 = execFileSync(DEV, [], { input: Buffer.from(bad), maxBuffer: 1<<24 });
  check('a corrupted CRC produces no reply', r1.length === 0, `${r1.length} bytes back`);
  const noise = Buffer.from([0x01,0x02,0x03,0x00,0xff,0xfe,0x00]);
  const r2 = execFileSync(DEV, [], { input: noise, maxBuffer: 1<<24 });
  check('random noise produces no reply', r2.length === 0, `${r2.length} bytes back`);
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
