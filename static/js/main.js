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