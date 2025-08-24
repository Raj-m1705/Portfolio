# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message']
    bot_reply = get_rag_reply(user_msg)  # connect to your RAG model
    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
