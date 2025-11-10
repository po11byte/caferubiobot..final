from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot SIMPLE funcionando"

@app.route('/health')
def health():
    return jsonify({"status": "ok", "simple": True})

@app.route('/webhook', methods=['POST'])
def webhook():
    return jsonify({"status": "received"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)