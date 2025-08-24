# Portfolio Website (Flask) — Complete Project

This document contains a ready-to-run, responsive portfolio website built with **HTML / CSS / JS** and **Python Flask**, plus a lightweight integration layer for a **local LLM** (optional). It's structured for easy deployment to **PythonAnywhere** or a similar host.

---

## Project structure

```
portfolio-flask/
├── app.py
├── requirements.txt
├── README.md
├── runtime.txt
├── .env.example
├── templates/
│   ├── base.html
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── local_llm/
    └── local_llm.py
```

---

## Files (copy each file into the matching path)

### `app.py`
```python
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# optional local llm wrapper
from local_llm.local_llm import generate_reply

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Simple homepage with portfolio and chat widget
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for chatbot
@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Empty message'}), 400

    # Mode: local or fallback
    try:
        mode = os.getenv('CHAT_MODE', 'LOCAL')  # LOCAL or OPENAI
        if mode == 'OPENAI':
            # If user chooses OPENAI, fall back to OpenAI API (optional)
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            resp = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role":"user","content":message}],
                max_tokens=256,
            )
            text = resp.choices[0].message.content
        else:
            # LOCAL: call local LLM wrapper
            text = generate_reply(message)

    except Exception as e:
        text = f"[Error generating reply: {str(e)}]"

    return jsonify({'reply': text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
```

---

### `local_llm/local_llm.py`
```python
"""
Lightweight local LLM helper.

This uses Hugging Face `transformers` text-generation pipeline when available.
- Default model: `gpt2` (small) — works on CPU but limited quality.
- If you have a larger local model (llama.cpp, local server), adapt this file to call it.

Note: For deployment on PythonAnywhere, heavy model libraries (torch) may not be allowed. Use OPENAI mode for hosted inference.
"""

import os

# Try to import transformers; if unavailable, provide a deterministic fallback.
try:
    from transformers import pipeline, set_seed
    _has_transformers = True
except Exception:
    _has_transformers = False

_model = os.getenv('LOCAL_LLM_MODEL', 'gpt2')

if _has_transformers:
    try:
        _generator = pipeline('text-generation', model=_model)
    except Exception:
        _generator = None
else:
    _generator = None


def generate_reply(prompt: str, max_length: int = 150) -> str:
    """Generate a reply using local HF pipeline if available, else echo fallback."""
    if _generator:
        try:
            out = _generator(prompt, max_length=max_length, do_sample=True, top_k=50, num_return_sequences=1)
            text = out[0]['generated_text']
            # crude trimming: return the part after the prompt
            if text.startswith(prompt):
                return text[len(prompt):].strip()
            return text.strip()
        except Exception as e:
            return f"[Local generation error: {e}]"

    # Fallback: simple rule-based/echo reply
    if len(prompt) < 40:
        return "Nice! Tell me more — I can also run locally if you install Hugging Face transformers."
    return "I received your message. To enable smarter replies, install `transformers` and set LOCAL_LLM_MODEL in your environment."
```

---

### `requirements.txt`
```
Flask>=2.0
python-dotenv
# Optional for local LLM (CPU):
transformers>=4.0.0
# Torch is optional but recommended for better model support. On PythonAnywhere this may not be available.
torch>=1.13.0; extra == 'torch'
# Optional OpenAI fallback
openai>=1.0.0
```

> **Note:** `torch` is large and may be incompatible with PythonAnywhere's environment. Keep the local-llm stack for local development. For deployment use `CHAT_MODE=OPENAI` with an API key.

---

### `templates/base.html`
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Portfolio — {{ title if title else 'My Portfolio' }}</title>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
  <nav class="nav">
    <div class="container nav-inner">
      <a class="logo" href="/">MyPortfolio</a>
      <div class="nav-links">
        <a href="#about">About</a>
        <a href="#projects">Projects</a>
        <a href="#contact">Contact</a>
      </div>
    </div>
  </nav>
  <main>
    {% block content %}{% endblock %}
  </main>
  <script src="/static/js/main.js"></script>
</body>
</html>
```

---

### `templates/index.html`
```html
{% extends 'base.html' %}
{% block content %}
<section class="hero">
  <div class="container hero-inner">
    <div class="hero-left">
      <h1>Hi — I'm Your Name</h1>
      <p>AI engineer • Web developer • Problem solver</p>
      <a class="btn" href="#projects">See my work</a>
    </div>
    <div class="hero-right">
      <img src="/static/img/placeholder-profile.png" alt="profile" class="profile-img">
    </div>
  </div>
</section>

<section id="about" class="container section">
  <h2>About me</h2>
  <p>Short bio — background, skills, and what you're building.</p>
</section>

<section id="projects" class="container section projects">
  <h2>Selected Projects</h2>
  <div class="grid">
    <!-- repeat project cards -->
    <article class="card">
      <h3>Project One</h3>
      <p>Short description</p>
    </article>
  </div>
</section>

<section id="contact" class="container section">
  <h2>Chat & Contact</h2>
  <div class="chat-wrap">
    <div id="chatLog" class="chat-log"></div>
    <form id="chatForm" class="chat-form">
      <input id="chatInput" autocomplete="off" placeholder="Say hi...">
      <button type="submit">Send</button>
    </form>
  </div>
</section>

<footer class="container footer">
  <p>© Your Name • Built with Flask</p>
</footer>
{% endblock %}
```

---

### `static/css/style.css`
```css
:root{
  --max-width: 1100px;
  --accent: #4f46e5;
  --muted: #6b7280;
}
*{box-sizing:border-box}
body{font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; margin:0; color:#111}
.container{max-width:var(--max-width);margin:0 auto;padding:1rem}
.nav{background:#fff;box-shadow:0 1px 4px rgba(0,0,0,0.06)}
.nav-inner{display:flex;align-items:center;justify-content:space-between;padding:0.75rem 1rem}
.logo{font-weight:700;color:var(--accent);text-decoration:none}
.nav-links a{margin-left:1rem;color:var(--muted);text-decoration:none}
.hero{padding:3rem 0}
.hero-inner{display:flex;gap:2rem;align-items:center}
.hero-left h1{font-size:2rem;margin:0}
.btn{display:inline-block;padding:0.5rem 0.9rem;background:var(--accent);color:#fff;border-radius:8px;text-decoration:none}
.profile-img{width:220px;border-radius:12px}
.section{padding:2rem 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}
.card{padding:1rem;border-radius:8px;border:1px solid #eee}
.footer{padding:1rem 0;color:var(--muted)}

/* Chat styles */
.chat-wrap{max-width:700px}
.chat-log{min-height:160px;border:1px solid #eee;padding:0.75rem;border-radius:6px;overflow:auto;background:#fafafa}
.chat-log .msg{margin-bottom:0.5rem}
.chat-log .me{font-weight:600}
.chat-form{display:flex;gap:0.5rem;margin-top:0.5rem}
.chat-form input{flex:1;padding:0.5rem;border:1px solid #ddd;border-radius:6px}
.chat-form button{padding:0.5rem 0.9rem;border-radius:6px;border:none;background:var(--accent);color:#fff}

/* Responsive */
@media (max-width:800px){
  .hero-inner{flex-direction:column}
  .profile-img{width:160px}
}
```

---

### `static/js/main.js`
```javascript
document.addEventListener('DOMContentLoaded', ()=>{
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');
  const log = document.getElementById('chatLog');

  function append(role, text){
    const div = document.createElement('div');
    div.className = 'msg ' + (role === 'me' ? 'me' : 'bot');
    div.textContent = (role === 'me' ? 'You: ' : 'Bot: ') + text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  }

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const msg = input.value.trim();
    if(!msg) return;
    append('me', msg);
    input.value = '';

    append('bot', '...');
    const placeholder = log.lastChild;

    try{
      const resp = await fetch('/api/chat', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({message: msg})
      });
      const data = await resp.json();
      placeholder.textContent = 'Bot: ' + (data.reply || data.error || 'No reply');
    }catch(err){
      placeholder.textContent = 'Bot: [Error connecting]';
    }
  });
});
```

---

### `README.md` (short)
```md
# Portfolio Flask App

Run locally:

1. python -m venv venv
2. source venv/bin/activate (or venv\Scripts\activate on Windows)
3. pip install -r requirements.txt
4. export FLASK_APP=app.py
5. flask run

Environment variables (see .env.example):

- CHAT_MODE=LOCAL or OPENAI
- OPENAI_API_KEY=... (optional)
- LOCAL_LLM_MODEL=gpt2

Deploy to PythonAnywhere:
- Upload files
- Create a virtualenv and install requirements (avoid heavy torch)
- Point WSGI to `app:app`
- Use OPENAI fallback for chatbot on server, or keep CHAT_MODE=LOCAL if you have lightweight model installed.
```

---

### `.env.example`
```env
FLASK_ENV=development
CHAT_MODE=LOCAL
LOCAL_LLM_MODEL=gpt2
# OPENAI_API_KEY=
```

---

### `runtime.txt` (optional for PythonAnywhere)
```
python-3.10
```

---

## Notes & Next steps

- **Local LLM:** The `local_llm` helper is intentionally minimal. If you plan to use heavier models:
  - For CPU inference consider `gpt2`, `distilgpt2` or optimized CPU builds.
  - For Llama-family models use an external local server (llama.cpp or llama.cpp-based HTTP server) and adapt `generate_reply` to call it over `requests`.
- **PythonAnywhere:** They often restrict installing `torch` and heavy packages. Use `CHAT_MODE=OPENAI` and an API key for server hosting. Locally you can test with `transformers`.
- **Security:** Never commit secrets. Put API keys in environment variables (PythonAnywhere has a web UI to add them).


---

That's the complete scaffolding. Copy files into a project folder and follow the README to run locally. Enjoy building the portfolio!

