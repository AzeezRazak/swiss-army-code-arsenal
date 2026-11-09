/* Purpose: Connect dashboard navigation, scope form, findings table and exports to app.py. */
/* Location: projects/python-security-research/security-research-dashboard/static/app.js */
/* Input/output: user interactions and local JSON API responses to rendered dashboard state. */
/* Requirements: modern browser JavaScript; no external libraries or network services. */
/* Usage from root: loaded by static/index.html. */
/* Limits: communicates only with the same loopback dashboard origin. */
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

function showView(name) {
  $$('.view').forEach((view) => view.classList.toggle('active-view', view.id === name));
  $$('.nav-link').forEach((button) => button.classList.toggle('active', button.dataset.view === name));
}

async function getJson(path) {
  const response = await fetch(path);
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || 'Request failed');
  return body;
}

function lines(value) { return value.split('\n').map((line) => line.trim()).filter(Boolean); }

async function loadScope() {
  const scope = await getJson('/api/scope');
  $('#targets').value = (scope.targets || []).join('\n');
  $('#methods').value = (scope.methods || []).join('\n');
  $('#accounts').value = (scope.accounts || []).join('\n');
  $('#callbacks').value = (scope.callbacks || []).join('\n');
  $('#notes').value = scope.notes || '';
}

async function loadSummary() {
  const summary = await getJson('/api/summary');
  const values = [summary.total, summary.web, summary.php, summary.high];
  $('#stats').querySelectorAll('strong').forEach((node, index) => { node.textContent = values[index]; });
}

async function loadResults() {
  const scanner = $('#scanner-filter').value;
  const severity = $('#severity-filter').value;
  const findings = await getJson(`/api/findings?scanner=${encodeURIComponent(scanner)}`);
  const visible = severity === 'all' ? findings : findings.filter((finding) => finding.severity === severity);
  const body = $('#results-body');
  if (!visible.length) { body.innerHTML = '<tr><td colspan="6" class="empty">No findings in this view yet.</td></tr>'; return; }
  body.innerHTML = visible.map((finding) => `<tr><td>${escapeHtml(finding.scanner)}</td><td>${escapeHtml(finding.module)}</td><td>${escapeHtml(finding.summary || '')}</td><td><span class="badge badge-${escapeHtml(finding.severity || 'informational')}">${escapeHtml(finding.severity || '—')}</span></td><td>${escapeHtml(finding.confidence || '—')}</td><td><span class="badge badge-signal">${escapeHtml(finding.status || '—')}</span></td></tr>`).join('');
}

function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (character) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[character])); }

$$('.nav-link').forEach((button) => button.addEventListener('click', () => showView(button.dataset.view)));
$$('[data-view-target]').forEach((button) => button.addEventListener('click', () => showView(button.dataset.viewTarget)));
$('#scanner-filter').addEventListener('change', loadResults);
$('#severity-filter').addEventListener('change', loadResults);

$('#scope-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const status = $('#scope-status');
  status.textContent = 'Saving…';
  try {
    await fetch('/api/scope', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({targets: lines($('#targets').value), methods: lines($('#methods').value), accounts: lines($('#accounts').value), callbacks: lines($('#callbacks').value), notes: $('#notes').value})}).then(async (response) => { const body = await response.json(); if (!response.ok) throw new Error(body.error); return body; });
    status.textContent = 'Saved locally';
  } catch (error) { status.textContent = error.message; }
});

$$('[data-export]').forEach((button) => button.addEventListener('click', () => { window.location.href = `/api/export?format=${button.dataset.export}&scanner=${$('#scanner-filter').value}`; }));

Promise.all([loadScope(), loadSummary(), loadResults()]).catch((error) => { $('#scope-status').textContent = error.message; });
