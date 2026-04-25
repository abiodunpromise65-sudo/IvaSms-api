from flask import Flask, jsonify
import requests

app = Flask(__name__)

# --- YOUR CONFIG ---
TELEGRAM_TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q"
TELEGRAM_CHAT_ID = "-1003126309534"

@app.route('/')
def home():
    # This automatically sends a test to Telegram as soon as you open the link
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": "✅ Bridge is LIVE, Salvation!"}
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        return jsonify({
            "status": "Online",
            "telegram_response": res.json(),
            "message": "If you don't see a Telegram message, check your Chat ID!"
        })
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()
    
