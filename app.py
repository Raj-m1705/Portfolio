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