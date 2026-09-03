import { crc32, cobsEncode, cobsDecode, buildCommand, parseFrame, FrameDecoder,
         SequenceTracker, Cmd, FrameType } from '../js/protocol.js';
let fails = 0;
const ok = (c, m) => { if (!c) { console.log('  FAIL', m); fails++; } else console.log('  ok  ', m); };

ok(crc32(new TextEncoder().encode('123456789')) === 0xCBF43926, 'CRC-32 check vector');

for (const c of [new Uint8Array(0), new Uint8Array([0,0,0]), new Uint8Array(300).fill(0x41),
                 Uint8Array.from({length:600},(_,i)=>i%256)]) {
  const e = cobsEncode(c);
  ok(e.indexOf(0) === e.length-1, `COBS: no interior zero (${c.length}B)`);
  const d = cobsDecode(e.subarray(0, e.length-1));
  ok(d && d.length===c.length && d.every((b,i)=>b===c[i]), `COBS round trip (${c.length}B)`);
}

// build -> decode through the streaming decoder, in awkward chunk sizes
const wire = buildCommand(Cmd.LOOPBACK, Uint8Array.from({length:240},(_,i)=>(i*7)&0xFF));
const dec = new FrameDecoder();
let got = [];
for (let i = 0; i < wire.length; i += 7) got = got.concat(dec.push(wire.subarray(i, i+7)));
ok(got.length === 1, 'streaming decoder reassembles across chunk boundaries');
ok(got[0] && got[0].type === FrameType.CMD, 'frame type survives');
ok(got[0] && got[0].payload.length === 241, `payload length ${got[0]?.payload.length} (opcode + 240)`);

// a corrupted frame must be counted, not returned
const bad = Uint8Array.from(wire); bad[5] ^= 0xFF;
const d2 = new FrameDecoder(); const r2 = d2.push(bad);
ok(r2.length === 0 && d2.stats.crcErrors === 1, 'CRC error is caught and counted');

// sequence tracking
const st = new SequenceTracker();
[0,1,2,7].forEach(seq => st.observe({seq}));
ok(st.missing === 4 && st.gaps.length === 1, `gap detected: missing=${st.missing}`);
const stw = new SequenceTracker();
[65534,65535,0,1].forEach(seq => stw.observe({seq}));
ok(stw.missing === 0, 'sequence wrap at 0xFFFF is not a gap');

console.log(fails ? `\n${fails} FAILED` : '\nall protocol tests passed');
process.exit(fails ? 1 : 0);
