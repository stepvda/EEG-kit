/*
 * ui.js -- TOOL-EEG-022, the operator-facing half.
 *
 * Deliberately small.  Everything that matters is in protocol.js, transport.js and
 * diagnostics.js, which the study runner will reuse; this file only decides what to put on
 * the screen.  Keep it that way: logic that creeps in here has to be written twice.
 *
 * Licence: MIT.
 */

import { DeviceLink, USB_FILTERS } from './transport.js';
import { InspectorSink } from './sinks.js';
import { selfChecks, deviceChecks, integritySummary, overallVerdict, browserName }
  from './diagnostics.js';

const $ = (id) => document.getElementById(id);
const STATE_ICON = { pass: '✓', fail: '✗', warn: '!', skip: '–' };

let link = null;
let sink = null;
let report = { startedAt: null, self: [], device: [], identity: null, integrity: null };

function log(msg) {
  const el = $('log');
  const t = new Date().toISOString().substring(11, 19);
  el.textContent += `${t}  ${msg}\n`;
  el.scrollTop = el.scrollHeight;
}

function renderSteps(containerId, steps) {
  const el = $(containerId);
  el.innerHTML = '';
  for (const s of steps) {
    const row = document.createElement('div');
    row.className = `step ${s.state}`;
    row.innerHTML = `
      <span class="icon">${STATE_ICON[s.state] || '?'}</span>
      <span class="id">${s.id}</span>
      <span class="title">${escapeHtml(s.title)}</span>
      <span class="ms">${s.ms === null ? '' : s.ms + ' ms'}</span>
      <div class="detail">${escapeHtml(s.detail || '')}</div>`;
    el.appendChild(row);
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function setVerdict(v) {
  const el = $('verdict');
  el.className = `verdict ${v}`;
  el.textContent = {
    pass: 'PASS — the link is whole',
    warn: 'PASS WITH WARNINGS — read them before you rely on the link',
    fail: 'FAIL — the link is not usable',
    skip: 'not run',
  }[v] || v;
}

function renderIdentity(id) {
  const el = $('identity');
  if (!id) { el.innerHTML = '<p class="muted">No device identified yet.</p>'; return; }
  const cap = Object.entries(id.capabilities)
    .map(([k, v]) => `<span class="cap ${v ? 'on' : 'off'}">${k}</span>`).join(' ');
  el.innerHTML = `
    <table>
      <tr><th>Unit serial</th><td>${escapeHtml(id.unitSerial || '(not provisioned)')}</td></tr>
      <tr><th>Firmware</th><td>${escapeHtml(id.firmware)}</td></tr>
      <tr><th>Board revision</th><td>${escapeHtml(id.boardRev)}</td></tr>
      <tr><th>Protocol</th><td>v${id.protoVersion}</td></tr>
      <tr><th>Ring buffer</th><td>${(id.ringBytes / 1048576).toFixed(2)} MiB</td></tr>
      <tr><th>Reports</th><td>${cap}</td></tr>
    </table>`;
}

function renderIntegrity(s) {
  if (!s) return;
  $('integrity').innerHTML = `
    <table>
      <tr><th>Bytes received</th><td>${s.bytesIn.toLocaleString()}</td></tr>
      <tr><th>Frames decoded</th><td>${s.framesDecoded.toLocaleString()}</td></tr>
      <tr><th>CRC errors</th><td class="${s.crcErrors ? 'bad' : ''}">${s.crcErrors}</td></tr>
      <tr><th>Version errors</th><td class="${s.versionErrors ? 'bad' : ''}">${s.versionErrors}</td></tr>
      <tr><th>Short frames</th><td class="${s.shortFrames ? 'bad' : ''}">${s.shortFrames}</td></tr>
      <tr><th>Resyncs</th><td>${s.resyncs}</td></tr>
      <tr><th>Sequence gaps</th><td class="${s.sequenceGaps ? 'bad' : ''}">${s.sequenceGaps}</td></tr>
      <tr><th>Frames missing</th><td class="${s.framesMissing ? 'bad' : ''}">${s.framesMissing}</td></tr>
    </table>`;
}

/* ------------------------------------------------------------------ actions */

async function runSelfChecks() {
  report.self = selfChecks();
  renderSteps('selfSteps', report.self);
  const bad = report.self.filter((s) => s.state === 'fail');
  log(`self-checks: ${report.self.length - bad.length}/${report.self.length} passed`);
  if (bad.length) log('the tool cannot be trusted until the self-checks pass');
  $('connectBtn').disabled = !DeviceLink.supported;
  return bad.length === 0;
}

async function connect() {
  try {
    sink = new InspectorSink();
    link = new DeviceLink({
      sink,
      onLog: log,
      onState: (s) => { $('portState').textContent = s; },
    });
    const port = await link.requestPort();
    await link.open(port);
    $('connectBtn').disabled = true;
    $('disconnectBtn').disabled = false;
    $('runBtn').disabled = false;
    log('connected; press "Run the connectivity test"');
  } catch (e) {
    // A user who closes the chooser is not an error worth shouting about.
    if (e?.name === 'NotFoundError') { log('no port chosen'); return; }
    log(`connect failed: ${e.message}`);
  }
}

async function disconnect() {
  if (link) await link.close();
  $('connectBtn').disabled = false;
  $('disconnectBtn').disabled = true;
  $('runBtn').disabled = true;
}

async function runTest() {
  $('runBtn').disabled = true;
  report.startedAt = new Date().toISOString();
  report.device = [];
  renderSteps('deviceSteps', []);
  log('running device checks');
  const { steps, identity } = await deviceChecks(link, {
    onStep: (r) => { report.device.push(r); renderSteps('deviceSteps', report.device); },
  });
  report.device = steps;
  report.identity = identity;
  report.integrity = integritySummary(link);
  renderIdentity(identity);
  renderIntegrity(report.integrity);
  setVerdict(overallVerdict([...report.self, ...report.device]));
  $('runBtn').disabled = false;
  $('saveBtn').disabled = false;
  log('done');
}

function saveReport() {
  const body = {
    tool: 'TOOL-EEG-022 EEG field kit connectivity test',
    toolVersion: '1.0',
    startedAt: report.startedAt,
    browser: `${browserName()} — ${navigator.userAgent}`,
    platform: navigator.platform,
    verdict: overallVerdict([...report.self, ...report.device]),
    identity: report.identity,
    selfChecks: report.self,
    deviceChecks: report.device,
    linkIntegrity: report.integrity,
    note: 'Connectivity only. No measurement was taken and no server was contacted.',
  };
  const blob = new Blob([JSON.stringify(body, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  const sn = report.identity?.unitSerial || 'unidentified';
  a.download = `connectivity-${sn}-${(report.startedAt || '').replace(/[:.]/g, '-')}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
  log(`report saved as ${a.download}`);
}

/* ------------------------------------------------------------------ boot */
export function boot() {
  $('browserName').textContent = browserName();
  $('connectBtn').addEventListener('click', connect);
  $('disconnectBtn').addEventListener('click', disconnect);
  $('runBtn').addEventListener('click', runTest);
  $('saveBtn').addEventListener('click', saveReport);
  renderIdentity(null);
  runSelfChecks();

  // A device unplugged mid-test is a thing that happens in a field kit, and the operator
  // should see it on the screen rather than wonder why the numbers stopped.
  if (DeviceLink.supported) {
    navigator.serial.addEventListener('disconnect', () => {
      log('device disconnected from USB');
      $('portState').textContent = 'unplugged';
    });
    navigator.serial.addEventListener('connect', () => log('a serial device was plugged in'));
  }
}
