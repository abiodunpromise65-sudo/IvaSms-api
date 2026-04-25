from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# --- YOUR CONFIGURATION ---
TELEGRAM_TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q" # Make sure this is your full token
TELEGRAM_CHAT_ID = "1003126309534"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

@app.route('/')
def home():
    return "API and Telegram Bridge is Live!"

@app.route('/sms')
def get_sms():
    # This triggers the message to your Telegram
    send_telegram("🚀 *Bot is checking for new SMS messages!*")
    return jsonify({"status": "success", "message": "Telegram notified"})

if __name__ == '__main__':
    app.run(debug=True)
    
