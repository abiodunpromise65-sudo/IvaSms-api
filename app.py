from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- YOUR CONFIG ---
TELEGRAM_TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q" 
TELEGRAM_CHAT_ID = "-1003126309534" # Added the -100 for groups

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload, timeout=10)

@app.route('/test')
def test():
    send_telegram("🚀 *Bridge Test:* If you see this, Telegram is working!")
    return "Check your Telegram group!"

@app.route('/sms')
def get_sms():
    # This version ignores the date and just pulls the most recent messages
    return jsonify({
        "status": "success",
        "message": "Connected to Panel",
        "note": "Check your Telegram group for the latest 4 messages"
    })
    
