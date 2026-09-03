/*
 * diagnostics.js -- the connectivity test sequence, TOOL-EEG-022.
 *
 * WHAT THIS TESTS, AND WHAT IT DELIBERATELY DOES NOT.
 *
 * It tests that the chain
 *
 *     EEG device --USB--> this computer --WebSerial--> this browser tab
 *
 * is whole, in both directions, and that the frame contract is honoured.  It is the chain
 * the study runner depends on, minus the server.
 *
 * It does NOT start a session, read an electrode, touch the ADS1299 converters, write to
 * the microSD card or connect to any network.  A unit on a bench with nothing plugged into
 * it must pass every one of these steps.  If a step here fails, the fault is in the cable,
 * the enclosure connector, the USB stack, the firmware build or the browser -- not in the
 * analogue front end, and not in the study protocol.
 *
 * Every step returns the same shape so the report is uniform and machine-readable:
 *   { id, title, state: 'pass'|'fail'|'skip'|'warn', detail, evidence, ms }
 *
 * Licence: MIT.
 */

import { Cmd, FrameType, crc32, cobsEncode, cobsDecode, parseFrame, buildCommand,
         PROTO_VERSION } from './protocol.js';
import { DeviceLink, decodeIdentity } from './transport.js';

const now = () => performance.now();

function result(id, title, state, detail, evidence, t0) {
  return { id, title, state, detail, evidence: evidence ?? null,
           ms: t0 === undefined ? null : Math.round(now() - t0) };
}

/* ------------------------------------------------------------------ offline self-checks
 *
 * These need no device.  They run first because if the protocol layer in THIS BROWSER is
 * wrong, every later result is meaningless -- and because they let an operator confirm the
 * tool itself is sound before blaming a unit.
 */
export function selfChecks() {
  const out = [];

  let t = now();
  // CRC-32 against the standard check vector: "123456789" -> 0xCBF43926.
  const v = new TextEncoder().encode('123456789');
  const got = crc32(v);
  out.push(result('S1', 'CRC-32 implementation', got === 0xCBF43926 ? 'pass' : 'fail',
    got === 0xCBF43926 ? 'matches the standard check value'
                       : `got 0x${got.toString(16)}, the check value is 0xCBF43926`,
    `crc32("123456789") = 0x${got.toString(16).toUpperCase()}`, t));

  t = now();
  // COBS must survive the cases that actually break naive implementations: a payload of
  // zeros, a run longer than 254 bytes, and an empty payload.
  const cases = [
    new Uint8Array(0),
    new Uint8Array([0, 0, 0]),
    new Uint8Array(300).fill(0x41),
    Uint8Array.from({ length: 300 }, (_, i) => i % 256),
  ];
  let cobsOk = true, why = '';
  for (const c of cases) {
    const enc = cobsEncode(c);
    if (enc.indexOf(0) !== enc.length - 1) { cobsOk = false; why = 'a 0x00 appears inside the encoded frame'; break; }
    const dec = cobsDecode(enc.subarray(0, enc.length - 1));
    if (!dec || dec.length !== c.length || dec.some((b, i) => b !== c[i])) {
      cobsOk = false; why = `round trip failed for a ${c.length}-byte payload`; break;
    }
  }
  out.push(result('S2', 'COBS round trip', cobsOk ? 'pass' : 'fail',
    cobsOk ? 'four payloads including all-zero and >254-byte runs' : why,
    `${cases.length} cases`, t));

  t = now();
  // A frame this tool builds must be one this tool can parse.  If the two halves disagree,
  // nothing downstream is trustworthy.
  let frameOk = false, fdetail = '';
  try {
    const wire = buildCommand(Cmd.LOOPBACK, new Uint8Array([1, 2, 3, 0, 255]));
    const body = cobsDecode(wire.subarray(0, wire.length - 1));
    const f = parseFrame(body);
    frameOk = f.type === FrameType.CMD && f.version === PROTO_VERSION;
    fdetail = frameOk ? `type ${f.typeName}, version ${f.version}`
                      : `parsed as type ${f.type}, version ${f.version}`;
  } catch (e) { fdetail = e.message; }
  out.push(result('S3', 'Frame build and parse agree', frameOk ? 'pass' : 'fail', fdetail,
    'CMD_LOOPBACK with an embedded 0x00', t));

  t = now();
  const supported = DeviceLink.supported;
  out.push(result('S4', 'Browser supports Web Serial', supported ? 'pass' : 'fail',
    supported ? `${browserName()} exposes navigator.serial`
              : `${browserName()} does not. Use Chrome or Edge on desktop.`,
    navigator.userAgent, t));

  t = now();
  const secure = window.isSecureContext;
  out.push(result('S5', 'Secure context', secure ? 'pass' : 'fail',
    secure ? `origin ${location.origin === 'null' ? 'file://' : location.origin} is trusted`
           : 'Web Serial needs a secure context: open the file directly, or serve it over ' +
             'http://localhost or https://',
    `isSecureContext = ${secure}`, t));

  return out;
}

export function browserName() {
  const ua = navigator.userAgent;
  if (/Edg\//.test(ua)) return 'Edge';
  if (/OPR\//.test(ua)) return 'Opera';
  if (/Chrome\//.test(ua)) return 'Chrome';
  if (/Firefox\//.test(ua)) return 'Firefox';
  if (/Safari\//.test(ua)) return 'Safari';
  return 'this browser';
}

/* ------------------------------------------------------------------ device checks */

export async function deviceChecks(link, { onStep = () => {} } = {}) {
  const out = [];
  const push = (r) => { out.push(r); onStep(r); return r; };

  // D1 -- the port is open and the device answers at all.
  let t = now(); let identity = null;
  try {
    identity = await link.identify();
    push(result('D1', 'Device answers CMD_IDENTIFY', 'pass',
      `firmware ${identity.firmware}, board Rev ${identity.boardRev}, protocol v${identity.protoVersion}`,
      JSON.stringify(identity), t));
  } catch (e) {
    push(result('D1', 'Device answers CMD_IDENTIFY', 'fail', e.message, null, t));
    // Everything below needs a talking device.  Stop rather than emit a cascade of
    // failures that all have the same single cause.
    push(result('D2', 'Protocol version matches', 'skip', 'no reply to CMD_IDENTIFY'));
    push(result('D3', 'Unit serial is provisioned', 'skip', 'no reply to CMD_IDENTIFY'));
    push(result('D4', 'Loopback, small payload', 'skip', 'no reply to CMD_IDENTIFY'));
    push(result('D5', 'Loopback, full-size payload', 'skip', 'no reply to CMD_IDENTIFY'));
    push(result('D6', 'Loopback, byte-pattern sweep', 'skip', 'no reply to CMD_IDENTIFY'));
    push(result('D7', 'Round-trip latency', 'skip', 'no reply to CMD_IDENTIFY'));
    push(result('D8', 'Link is quiet when idle', 'skip', 'no reply to CMD_IDENTIFY'));
    return { steps: out, identity: null };
  }

  // D2 -- version agreement, which decides whether anything else can be believed.
  t = now();
  push(identity.protoVersion === PROTO_VERSION
    ? result('D2', 'Protocol version matches', 'pass',
        `both speak version ${PROTO_VERSION}`, null, t)
    : result('D2', 'Protocol version matches', 'fail',
        `device speaks v${identity.protoVersion}, this tool speaks v${PROTO_VERSION}. ` +
        'Update whichever is older; do not interpret the frames.', null, t));

  // D3 -- provisioning.  A blank serial is not a fault in the link, so it is a warning:
  // an unprovisioned unit communicates perfectly well and simply is not identifiable yet.
  t = now();
  const sn = identity.unitSerial || '';
  const provisioned = /^TIOV-[A-Z]-\d{4}$/.test(sn) && sn !== 'TIOV-B-0000';
  push(result('D3', 'Unit serial is provisioned', provisioned ? 'pass' : 'warn',
    provisioned ? sn
      : `the device reports "${sn || '(empty)'}". End-of-line provisioning has not run, so ` +
        'the browser cannot bind a persistent authorisation to this unit (F-04). ' +
        'Connectivity is unaffected.',
    sn, t));

  // D4/D5/D6 -- the loopback ladder.  Small, then a full frame, then a pattern sweep.  The
  // sweep is the one that catches a transport that mangles particular byte values, which is
  // exactly what a COBS bug or a driver doing newline translation looks like.
  t = now();
  const small = new Uint8Array([0x00, 0x01, 0x02, 0xFE, 0xFF]);
  let r = await safeLoopback(link, small);
  push(result('D4', 'Loopback, small payload', r.ok ? 'pass' : 'fail',
    r.ok ? '5 bytes including 0x00 and 0xFF returned unchanged' : r.why, null, t));

  t = now();
  const big = Uint8Array.from({ length: 240 }, (_, i) => (i * 7) & 0xFF);
  r = await safeLoopback(link, big);
  push(result('D5', 'Loopback, full-size payload', r.ok ? 'pass' : 'fail',
    r.ok ? '240 bytes returned unchanged' : r.why, null, t));

  t = now();
  let sweepOk = true, sweepWhy = '';
  for (let base = 0; base < 256 && sweepOk; base += 64) {
    const pat = Uint8Array.from({ length: 64 }, (_, i) => (base + i) & 0xFF);
    const rr = await safeLoopback(link, pat);
    if (!rr.ok) { sweepOk = false; sweepWhy = `bytes ${base}..${base + 63}: ${rr.why}`; }
  }
  push(result('D6', 'Loopback, byte-pattern sweep', sweepOk ? 'pass' : 'fail',
    sweepOk ? 'all 256 byte values survive the round trip' : sweepWhy, null, t));

  // D7 -- latency.  Not a performance test; a sanity check that the link is not being
  // buffered by something that would ruin the stimulus timing later.
  t = now();
  const samples = [];
  for (let i = 0; i < 20; i++) {
    const a = now();
    const rr = await safeLoopback(link, new Uint8Array([i]));
    if (rr.ok) samples.push(now() - a);
  }
  if (samples.length < 5) {
    push(result('D7', 'Round-trip latency', 'fail',
      `only ${samples.length} of 20 round trips completed`, null, t));
  } else {
    samples.sort((a, b) => a - b);
    const med = samples[Math.floor(samples.length / 2)];
    const p95 = samples[Math.min(samples.length - 1, Math.floor(samples.length * 0.95))];
    push(result('D7', 'Round-trip latency', med < 50 ? 'pass' : 'warn',
      `median ${med.toFixed(1)} ms, p95 ${p95.toFixed(1)} ms over ${samples.length} round trips` +
      (med < 50 ? '' : '. That is slow for USB; suspect a hub, a virtual COM driver or a busy machine.'),
      JSON.stringify({ median: +med.toFixed(2), p95: +p95.toFixed(2), n: samples.length }), t));
  }

  // D8 -- silence when idle.  No session has been started, so the device must not be
  // streaming.  If frames arrive here, something started a session, and the operator needs
  // to know before they interpret anything else.
  t = now();
  const before = link.decoder.stats.frames;
  await new Promise((res) => setTimeout(res, 1000));
  const during = link.decoder.stats.frames - before;
  push(result('D8', 'Link is quiet when idle', during === 0 ? 'pass' : 'warn',
    during === 0 ? 'no unsolicited frames in one second, as expected with no session running'
                 : `${during} unsolicited frames arrived in one second. A session is already ` +
                   'running, or the firmware is streaming without being asked.',
    `${during} frames/s`, t));

  return { steps: out, identity };
}

async function safeLoopback(link, bytes) {
  try { return await link.loopback(bytes); }
  catch (e) { return { ok: false, why: e.message }; }
}

/* ------------------------------------------------------------------ integrity summary */
export function integritySummary(link) {
  const d = link.decoder.stats;
  const s = link.sequence;
  return {
    bytesIn: d.bytesIn,
    framesDecoded: d.frames,
    crcErrors: d.crcErrors,
    versionErrors: d.versionErrors,
    shortFrames: d.shortFrames,
    resyncs: d.resyncs,
    oversizeDiscards: d.oversizeDiscards,
    sequenceGaps: s.gaps.length,
    framesMissing: s.missing,
  };
}

export function overallVerdict(steps) {
  if (steps.some((s) => s.state === 'fail')) return 'fail';
  if (steps.some((s) => s.state === 'warn')) return 'warn';
  if (steps.every((s) => s.state === 'skip')) return 'skip';
  return 'pass';
}
