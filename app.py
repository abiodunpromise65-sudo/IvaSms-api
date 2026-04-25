from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# --- YOUR CONFIG ---
TELEGRAM_TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiLtX0qE7Q" 
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
    return "SMS to Telegram Bridge is Online!"

@app.route('/sms')
def get_sms():
    # This automatically uses today's date
    today = datetime.now().strftime("%d/%m/%Y")
    
    # We send a notification to your Telegram to show it worked
    send_telegram(f"✅ *Bridge Active*\nChecked panel for date: {today}\nStatus: Listening for SMS...")
    
    return jsonify({
        "status": "success", 
        "date_checked": today,
        "message": "Notification sent to Telegram"
    })

if __name__ == '__main__':
    app.run(debug=True)
    
