// Admin Panel JS

// ── DRAG & DROP ────────────────────────────
function handleDragOver(e) {
  e.preventDefault();
  document.getElementById('uploadZone').classList.add('dragover');
}
function handleDragLeave(e) {
  document.getElementById('uploadZone').classList.remove('dragover');
}
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('uploadZone').classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) uploadFile(file);
}

// ── UPLOAD ─────────────────────────────────
async function uploadFile(file) {
  if (!file) return;
  if (!file.name.endsWith('.pdf')) {
    showUploadResult('error', '❌ Only PDF files are supported.');
    return;
  }

  showProgress(true);
  showUploadResult('', '');
  animateProgress();

  const formData = new FormData();
  formData.append('file', file);

  try {
    const res  = await fetch('/api/upload', { method: 'POST', body: formData });
    const data = await res.json();
    showProgress(false);
    if (data.status === 'success') {
      showUploadResult('success', `✅ ${data.message}`);
      loadDocuments();
    } else {
      showUploadResult('error', `❌ Error: ${data.message || data.error}`);
    }
  } catch (err) {
    showProgress(false);
    showUploadResult('error', '❌ Upload failed. Is the server running?');
  }
}

function animateProgress() {
  const fill = document.getElementById('progressFill');
  let w = 0;
  const iv = setInterval(() => {
    w = Math.min(w + Math.random() * 15, 85);
    fill.style.width = w + '%';
    if (w >= 85) clearInterval(iv);
  }, 300);
}

function showProgress(show) {
  document.getElementById('progressWrap').style.display = show ? 'block' : 'none';
  if (!show) document.getElementById('progressFill').style.width = '100%';
}

function showUploadResult(type, msg) {
  const el = document.getElementById('uploadResult');
  el.className = `upload-result ${type}`;
  el.textContent = msg;
  el.style.display = msg ? 'block' : 'none';
}

// ── DOCUMENTS ──────────────────────────────
async function loadDocuments() {
  try {
    const res  = await fetch('/api/documents');
    const data = await res.json();
    const list = document.getElementById('docList');

    if (!data.documents || data.documents.length === 0) {
      list.innerHTML = '<div class="no-docs">📭 No documents uploaded yet. Upload a PDF to get started.</div>';
      return;
    }

    list.innerHTML = data.documents.map(doc => `
      <div class="doc-item">
        <div class="doc-info">
          <span class="doc-icon">📄</span>
          <div>
            <div class="doc-name">${doc}</div>
            <div class="doc-size">PDF Document</div>
          </div>
        </div>
        <button class="delete-btn" onclick="deleteDocument('${doc}')">🗑️ Delete</button>
      </div>`).join('');
  } catch {
    document.getElementById('docList').innerHTML = '<div class="no-docs">❌ Failed to load documents.</div>';
  }
}

async function deleteDocument(filename) {
  if (!confirm(`Delete "${filename}"? This will rebuild the index.`)) return;
  try {
    const res  = await fetch(`/api/documents/${encodeURIComponent(filename)}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.status === 'success') {
      showActionResult('success', `✅ ${data.message}`);
      loadDocuments();
    } else {
      showActionResult('error', `❌ ${data.message}`);
    }
  } catch {
    showActionResult('error', '❌ Delete failed.');
  }
}

// ── REBUILD ────────────────────────────────
async function rebuildIndex() {
  showActionResult('success', '⏳ Rebuilding index...');
  try {
    const res  = await fetch('/api/rebuild', { method: 'POST' });
    const data = await res.json();
    if (data.status === 'success') {
      showActionResult('success', `✅ ${data.message}`);
    } else {
      showActionResult('error', `❌ ${data.message}`);
    }
  } catch {
    showActionResult('error', '❌ Rebuild failed.');
  }
}

// ── STATS ──────────────────────────────────
async function loadStats() {
  try {
    const res  = await fetch('/api/status');
    const data = await res.json();
    const grid = document.getElementById('statsGrid');
    grid.style.display = 'grid';
    grid.innerHTML = `
      <div class="stat-card">
        <div class="stat-value">${data.document_count || 0}</div>
        <div class="stat-label">📄 Documents</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${data.vector_count || 0}</div>
        <div class="stat-label">🔢 Vectors</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${data.index_ready ? '✅' : '❌'}</div>
        <div class="stat-label">🚦 Index Status</div>
      </div>`;
    showActionResult('success', '✅ Stats loaded successfully.');
  } catch {
    showActionResult('error', '❌ Failed to load stats.');
  }
}

function showActionResult(type, msg) {
  const el = document.getElementById('actionResult');
  el.className = `action-result ${type}`;
  el.textContent = msg;
  el.style.display = 'block';
}

// ── HISTORY ────────────────────────────────
async function loadAdminHistory() {
  try {
    const res  = await fetch('/api/history?limit=20');
    const data = await res.json();
    const div  = document.getElementById('adminHistory');

    if (!data.history || data.history.length === 0) {
      div.innerHTML = '<p class="no-docs">No conversations yet.</p>';
      return;
    }

    const rows = data.history.map(item => {
      const model = item.model_used || '';
      const cls   = model.includes('groq') ? 'groq' : model.includes('gemini') ? 'gemini' : 'ctx';
      const label = model.includes('groq') ? '⚡ Groq' : model.includes('gemini') ? '✨ Gemini' : '📝 Context';
      return `<tr>
        <td>${escapeHtml(item.question)}</td>
        <td>${escapeHtml((item.answer || '').substring(0, 80))}...</td>
        <td><span class="badge ${cls}">${label}</span></td>
        <td style="font-size:11px;color:var(--text2)">${item.timestamp || ''}</td>
      </tr>`;
    }).join('');

    div.innerHTML = `
      <table class="history-table">
        <thead><tr><th>Question</th><th>Answer</th><th>Model</th><th>Time</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>`;
  } catch {
    document.getElementById('adminHistory').innerHTML = '<p class="no-docs">❌ Failed to load history.</p>';
  }
}

function escapeHtml(text) {
  return String(text || '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// Auto-load on page open
loadDocuments();
