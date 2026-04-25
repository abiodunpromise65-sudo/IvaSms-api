from flask import Flask, jsonify
import requests

app = Flask(__name__)

# --- YOUR CONFIG ---
TELEGRAM_TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q"
# I am using the ID you provided. If this fails, we will know why.
TELEGRAM_CHAT_ID = "-1003126309534" 

@app.route('/')
def home():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": "🚨 *Bridge Alert:* If you see this, Telegram is WORKING!",
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        return jsonify({
            "bridge_status": "Active",
            "telegram_connected": res_data.get("ok", False),
            "telegram_error_details": res_data if not res_data.get("ok") else "None! Check your phone."
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
    
