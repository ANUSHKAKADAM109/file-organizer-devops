// ── Tab navigation ────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', e => {
    e.preventDefault();
    const tab = item.dataset.tab;

    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

    item.classList.add('active');
    document.getElementById('tab-' + tab).classList.add('active');

    if (tab === 'history') loadHistory();
  });
});

// ── Status helper ─────────────────────────────────────
function setStatus(state, text) {
  const dot = document.getElementById('statusDot');
  const label = document.getElementById('statusText');
  dot.className = 'status-dot ' + state;
  label.textContent = text;
}

// ── Organize ──────────────────────────────────────────
async function organizeFiles() {
  const folderPath = document.getElementById('folderPath').value.trim();
  const btn = document.getElementById('organizeBtn');
  const btnLabel = document.getElementById('btnLabel');
  const resultsCard = document.getElementById('resultsCard');
  const errorCard = document.getElementById('errorCard');
  const logList = document.getElementById('logList');
  const resultCount = document.getElementById('resultCount');

  // Hide old results
  resultsCard.style.display = 'none';
  errorCard.style.display = 'none';

  if (!folderPath) {
    showError('Please enter a folder path.');
    return;
  }

  // Loading state
  btn.disabled = true;
  btnLabel.textContent = 'Running…';
  setStatus('running', 'Organizing…');

  try {
    const res = await fetch('/organize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ folder_path: folderPath }),
    });
    const data = await res.json();

    if (!data.success) {
      showError(data.error);
      setStatus('error', 'Error');
      return;
    }

    // Render log items with staggered animation
    logList.innerHTML = '';
    if (data.logs.length === 0) {
      logList.innerHTML = '<p style="color:var(--muted);font-size:13px;">No files found to organize.</p>';
    } else {
      data.logs.forEach((entry, i) => {
        const el = document.createElement('div');
        el.className = 'log-item';
        el.style.animationDelay = (i * 40) + 'ms';
        el.innerHTML = `
          <span class="log-file" title="${entry.file}">${entry.file}</span>
          <span class="log-arrow">→</span>
          <span class="log-dest">${entry.destination}</span>
        `;
        logList.appendChild(el);
      });
    }

    resultCount.textContent = data.total + ' file' + (data.total !== 1 ? 's' : '');
    resultsCard.style.display = 'block';
    setStatus('done', 'Done');

  } catch (err) {
    showError('Network error: ' + err.message);
    setStatus('error', 'Error');
  } finally {
    btn.disabled = false;
    btnLabel.textContent = 'Run';
  }
}

function showError(msg) {
  const errorCard = document.getElementById('errorCard');
  document.getElementById('errorMsg').textContent = msg;
  errorCard.style.display = 'flex';
  setStatus('error', 'Error');
}

// Allow Enter key in path input
document.getElementById('folderPath').addEventListener('keydown', e => {
  if (e.key === 'Enter') organizeFiles();
});

// ── History ───────────────────────────────────────────
async function loadHistory() {
  const tbody = document.getElementById('historyBody');
  tbody.innerHTML = '<tr><td colspan="4" class="empty-row">Loading…</td></tr>';

  try {
    const res = await fetch('/history');
    const data = await res.json();

    if (!data.logs.length) {
      tbody.innerHTML = '<tr><td colspan="4" class="empty-row">No history yet.</td></tr>';
      return;
    }

    tbody.innerHTML = '';
    // Show newest first
    [...data.logs].reverse().forEach(row => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="color:var(--muted);font-size:12px;">${row.Timestamp}</td>
        <td>${row.File}</td>
        <td><span class="log-dest">${row.Destination}</span></td>
        <td style="color:var(--accent);font-size:12px;">${row.Status}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="4" class="empty-row">Failed to load history.</td></tr>';
  }
}

async function clearHistory() {
  if (!confirm('Clear all history? This cannot be undone.')) return;
  await fetch('/clear-history', { method: 'POST' });
  loadHistory();
}