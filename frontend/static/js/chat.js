// ═══════════════════════════════════════════
// College AI Assistant - Full Featured JS
// Features: Voice, Multilang, Feedback, Typing Animation
// ═══════════════════════════════════════════

let isLoading   = false;
let recognition = null;
let currentLang = 'en';

// ── THEME ──────────────────────────────────
function toggleTheme() {
  const html  = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  document.getElementById('themeToggle').textContent = isDark ? '🌙' : '☀️';
  localStorage.setItem('theme', isDark ? 'light' : 'dark');
}
function loadTheme() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  document.getElementById('themeToggle').textContent = saved === 'dark' ? '☀️' : '🌙';
}

// ── LANGUAGE ───────────────────────────────
const langLabels = { en: '🇬🇧 EN', ta: '🇮🇳 தமிழ்' };

function toggleLanguage() {
  currentLang = currentLang === 'en' ? 'ta' : 'en';
  const btn = document.getElementById('langBtn');
  btn.textContent = langLabels[currentLang];
  if (recognition) recognition.lang = currentLang === 'ta' ? 'ta-IN' : 'en-IN';
  // Show toast
  showToast(currentLang === 'ta' ? '🇮🇳 Tamil mode enabled' : '🇬🇧 English mode enabled');
}

function getLanguagePromptSuffix() {
  return currentLang === 'ta' ? ' (Please answer in Tamil language)' : '';
}

// ── TOAST ──────────────────────────────────
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

// ── STATUS ─────────────────────────────────
async function loadStatus() {
  try {
    const res  = await fetch('/api/status');
    const data = await res.json();
    const dot  = document.querySelector('.status-dot');
    const txt  = document.getElementById('statusText');
    if (data.index_ready) {
      dot.className   = 'status-dot ready';
      txt.textContent = `Ready · ${data.document_count} docs`;
    } else {
      dot.className   = 'status-dot error';
      txt.textContent = 'No documents';
    }
  } catch {
    document.getElementById('statusText').textContent = 'Offline';
  }
}

// ── SEND MESSAGE ───────────────────────────
async function sendMessage() {
  const input = document.getElementById('userInput');
  const text  = input.value.trim();
  if (!text || isLoading) return;

  const question = text + getLanguagePromptSuffix();
  appendUserMessage(text);
  input.value = '';
  autoResize(input);
  showTyping(true);
  setLoading(true);

  try {
    const res  = await fetch('/api/chat', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ question })
    });
    const data = await res.json();
    showTyping(false);
    if (data.answer) {
      appendBotMessage(data.answer, data.sources || [], data.model_used || '');
    } else {
      appendBotMessage('Sorry, something went wrong. Please try again.', [], '');
    }
  } catch {
    showTyping(false);
    appendBotMessage('Connection error. Is the server running?', [], '');
  }

  setLoading(false);
  scrollToBottom();
}

// ── APPEND USER MESSAGE ────────────────────
function appendUserMessage(text) {
  const msgs = document.getElementById('messages');
  const now  = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const div  = document.createElement('div');
  div.className = 'message user-message';
  div.innerHTML = `
    <div class="avatar">👤</div>
    <div>
      <div class="bubble">${escapeHtml(text)}</div>
      <div class="msg-time">${now}</div>
    </div>`;
  msgs.appendChild(div);
  scrollToBottom();
}

// ── APPEND BOT MESSAGE WITH TYPING ANIMATION ──
function appendBotMessage(answer, sources, model) {
  const msgs    = document.getElementById('messages');
  const now     = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const msgId   = 'msg_' + Date.now();
  const div     = document.createElement('div');
  div.className = 'message bot-message';

  // Sources HTML
  let sourcesHtml = '';
  if (sources && sources.length > 0) {
    const tags = sources.map(s => `<span class="source-tag">📄 ${s}</span>`).join('');
    sourcesHtml = `<div class="sources-box"><div class="sources-title">📚 Sources</div><div class="source-tags">${tags}</div></div>`;
  }

  // Model badge
  let badgeHtml = '';
  if (model) {
    const cls   = model.includes('groq') ? 'groq' : model.includes('gemini') ? 'gemini' : '';
    const label = model.includes('groq') ? '⚡ Groq' : model.includes('gemini') ? '✨ Gemini' : '📝 Context';
    badgeHtml   = `<span class="model-badge ${cls}">${label}</span>`;
  }

  div.innerHTML = `
    <div class="avatar">🤖</div>
    <div style="max-width:680px">
      <div class="bubble">
        <span id="${msgId}" class="typed-text"></span>
        ${sourcesHtml}
        <div class="msg-actions">
          ${badgeHtml}
          <button class="action-micro" onclick="toggleSpeech(this,'${msgId}')" title="Read aloud">🔊</button>
          <button class="action-micro feedback-btn" onclick="sendFeedback(this,'${msgId}','good')" title="Good answer">👍</button>
          <button class="action-micro feedback-btn" onclick="sendFeedback(this,'${msgId}','bad')"  title="Bad answer">👎</button>
        </div>
      </div>
      <div class="msg-time">${now}</div>
    </div>`;
  msgs.appendChild(div);
  scrollToBottom();

  // Typing animation
  typeText(msgId, answer);
}

// ── TYPING ANIMATION ───────────────────────
function typeText(elementId, text) {
  const el    = document.getElementById(elementId);
  if (!el) return;
  const words = text.split(' ');
  let i       = 0;
  el.textContent = "";
  el.classList.add("typing");

  const iv = setInterval(() => {
    if (i < words.length) {
      el.textContent += (i === 0 ? '' : ' ') + words[i];
      i++;
      scrollToBottom();
    } else {
      clearInterval(iv);
      el.classList.remove("typing");
      // Auto speak after typing done
      speakText(text);
    }
  }, 40); // 40ms per word = natural reading speed
}

// ── FEEDBACK ───────────────────────────────
function sendFeedback(btn, msgId, type) {
  // Visual feedback
  const parent = btn.closest('.msg-actions');
  const allBtns = parent.querySelectorAll('.feedback-btn');
  allBtns.forEach(b => b.style.opacity = '0.4');
  btn.style.opacity  = '1';
  btn.style.transform = 'scale(1.3)';

  showToast(type === 'good' ? '👍 Thanks for the feedback!' : '👎 We\'ll improve this answer!');

  // Log feedback (can be sent to server later)
  console.log('Feedback:', type, 'for message:', msgId);
}

// ── SUGGESTED QUESTIONS ────────────────────
function askSuggestion(question) {
  const input = document.getElementById('userInput');
  input.value = question;
  autoResize(input);
  sendMessage();
}

function filterSuggestions(query) {
  document.querySelectorAll('.suggestion-btn').forEach(btn => {
    const text = btn.dataset.q || btn.textContent;
    btn.classList.toggle('hidden', !text.toLowerCase().includes(query.toLowerCase()));
  });
}

function filterCategory(cat, el) {
  document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.suggestion-btn').forEach(btn => {
    btn.classList.toggle('hidden', cat !== 'all' && btn.dataset.cat !== cat);
  });
}

// ── CHAT HISTORY ───────────────────────────
async function loadHistory() {
  try {
    const res  = await fetch('/api/history?limit=10');
    const data = await res.json();
    const list = document.getElementById('historyList');
    if (!data.history || data.history.length === 0) {
      list.innerHTML = '<p class="no-history">No history yet</p>';
      return;
    }
    list.innerHTML = data.history.map(item => `
      <div class="history-item" onclick="askSuggestion(${JSON.stringify(item.question)})">
        <div class="history-q">${escapeHtml(item.question)}</div>
        <div class="history-t">${item.timestamp || ''}</div>
      </div>`).join('');
  } catch {
    document.getElementById('historyList').innerHTML = '<p class="no-history">Failed to load</p>';
  }
}

// ── CLEAR CHAT ─────────────────────────────
function clearChat() {
  const msgs    = document.getElementById('messages');
  const welcome = msgs.querySelector('.welcome-msg');
  msgs.innerHTML = '';
  if (welcome) msgs.appendChild(welcome);
  showToast('🗑️ Chat cleared');
}

// ── VOICE INPUT ────────────────────────────
function initVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return;
  recognition              = new SR();
  recognition.lang         = 'en-IN';
  recognition.interimResults   = false;
  recognition.maxAlternatives  = 1;

  recognition.onstart  = () => { document.getElementById('micBtn').textContent = '🔴'; };
  recognition.onresult = (e) => {
    const text = e.results[0][0].transcript;
    document.getElementById('userInput').value = text;
    autoResize(document.getElementById('userInput'));
    sendMessage();
  };
  recognition.onend   = () => { document.getElementById('micBtn').textContent = '🎤'; };
  recognition.onerror = ()  => { document.getElementById('micBtn').textContent = '🎤'; };
}

function toggleVoice() {
  if (!recognition) { alert('Use Chrome for voice input.'); return; }
  document.getElementById('micBtn').textContent === '🔴'
    ? recognition.stop()
    : recognition.start();
}

// ── VOICE OUTPUT ───────────────────────────
function speakText(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const clean     = text.replace(/[\[\]📄📚⚡✨🔊👍👎]/g, '').trim();
  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.lang  = currentLang === 'ta' ? 'ta-IN' : 'en-IN';
  utterance.rate  = 0.95;
  window.speechSynthesis.speak(utterance);
}

function toggleSpeech(btn, msgId) {
  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
    btn.textContent = '🔊';
  } else {
    const el = document.getElementById(msgId);
    if (el) speakText(el.innerText);
    btn.textContent = '⏹️';
  }
}

// ── HELPERS ────────────────────────────────
function showTyping(show) {
  document.getElementById('typingIndicator').style.display = show ? 'flex' : 'none';
}
function setLoading(state) {
  isLoading = state;
  document.getElementById('sendBtn').disabled = state;
}
function scrollToBottom() {
  const msgs = document.getElementById('messages');
  setTimeout(() => msgs.scrollTop = msgs.scrollHeight, 50);
}
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}
function handleKeyDown(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}
function escapeHtml(text) {
  return String(text)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
}

// ── INIT ───────────────────────────────────
loadTheme();
loadStatus();
initVoice();
setInterval(loadStatus, 30000);
