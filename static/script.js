/* ====== AcadBot – Frontend Logic ====== */

const chatMessages = document.getElementById('chatMessages');
const userInput    = document.getElementById('userInput');
const sendBtn      = document.getElementById('sendBtn');
const resetBtn     = document.getElementById('resetBtn');
const resetBtnHeader = document.getElementById('resetBtnHeader');
const menuToggle   = document.getElementById('menuToggle');
const sidebar      = document.querySelector('.sidebar');

// ---- Sidebar toggle (mobile) ----
menuToggle?.addEventListener('click', () => sidebar.classList.toggle('open'));
document.addEventListener('click', (e) => {
  if (sidebar.classList.contains('open') &&
      !sidebar.contains(e.target) &&
      !menuToggle.contains(e.target)) {
    sidebar.classList.remove('open');
  }
});

// ---- Auto-resize textarea ----
userInput.addEventListener('input', () => {
  userInput.style.height = 'auto';
  userInput.style.height = Math.min(userInput.scrollHeight, 160) + 'px';
});

// ---- Send on Enter (Shift+Enter for newline) ----
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

sendBtn.addEventListener('click', sendMessage);

// ---- Quick topic buttons ----
document.querySelectorAll('.quick-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    userInput.value = btn.dataset.msg;
    sidebar.classList.remove('open');
    sendMessage();
  });
});

// ---- Chips on welcome screen ----
document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => {
    userInput.value = chip.dataset.msg;
    sendMessage();
  });
});

// ---- Reset ----
[resetBtn, resetBtnHeader].forEach(btn => btn?.addEventListener('click', resetChat));

async function resetChat() {
  try {
    await fetch('/reset', { method: 'POST' });
    chatMessages.innerHTML = '';
    appendWelcome();
    userInput.value = '';
    userInput.style.height = 'auto';
  } catch (err) {
    console.error('Reset failed:', err);
  }
}

// ---- Main send function ----
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text || sendBtn.disabled) return;

  removeWelcome();
  appendMessage('user', text);
  userInput.value = '';
  userInput.style.height = 'auto';

  setSending(true);
  const typingEl = appendTyping();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    typingEl.remove();

    if (data.reply) {
      appendMessage('bot', data.reply);
    } else {
      appendMessage('bot', `⚠️ Error: ${data.error || 'Unknown error'}`);
    }
  } catch (err) {
    typingEl.remove();
    appendMessage('bot', '⚠️ Could not connect to server. Make sure the Flask app is running.');
  } finally {
    setSending(false);
    userInput.focus();
  }
}

// ---- Helpers ----
function setSending(state) {
  sendBtn.disabled = state;
  userInput.disabled = state;
}

function removeWelcome() {
  document.querySelector('.welcome-block')?.remove();
}

function appendMessage(role, text) {
  const row = document.createElement('div');
  row.className = `message-row ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'user' ? '👤' : '🎓';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = formatText(text);

  const ts = document.createElement('div');
  ts.className = 'timestamp';
  ts.textContent = now();

  const wrapper = document.createElement('div');
  wrapper.style.display = 'flex';
  wrapper.style.flexDirection = 'column';
  wrapper.style.alignItems = role === 'user' ? 'flex-end' : 'flex-start';
  wrapper.appendChild(bubble);
  wrapper.appendChild(ts);

  row.appendChild(avatar);
  row.appendChild(wrapper);

  chatMessages.appendChild(row);
  scrollBottom();
  return row;
}

function appendTyping() {
  const row = document.createElement('div');
  row.className = 'message-row bot';

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = '🎓';

  const bubble = document.createElement('div');
  bubble.className = 'bubble typing-bubble';
  bubble.innerHTML = '<span></span><span></span><span></span>';

  row.appendChild(avatar);
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  scrollBottom();
  return row;
}

function appendWelcome() {
  const el = document.createElement('div');
  el.className = 'welcome-block';
  el.innerHTML = `
    <div class="welcome-avatar">🎓</div>
    <h1 class="welcome-title">Hi, I'm your AI Course Advisor!</h1>
    <p class="welcome-sub">Ask me anything about courses, study strategies, career paths, or academic planning.</p>
    <div class="welcome-chips">
      <span class="chip" data-msg="What should I study in 2nd year CS?">What to study in 2nd year?</span>
      <span class="chip" data-msg="How do I get into machine learning?">How to get into ML?</span>
      <span class="chip" data-msg="Best projects for my resume?">Best resume projects?</span>
    </div>`;
  chatMessages.appendChild(el);
  el.querySelectorAll('.chip').forEach(c => {
    c.addEventListener('click', () => { userInput.value = c.dataset.msg; sendMessage(); });
  });
}

function formatText(text) {
  // Basic markdown-like formatting
  return text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^#{1,3} (.+)$/gm, '<strong>$1</strong>')
    .replace(/^\* (.+)$/gm, '<li>$1</li>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    .replace(/\n\n+/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^(.+)$/, '<p>$1</p>');
}

function scrollBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function now() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}
