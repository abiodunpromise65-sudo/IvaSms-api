from flask import Flask, jsonify
import requests

app = Flask(__name__)

# --- YOUR CONFIG ---
# Ensure these match exactly. I added the -100 for your group.
TELEGRAM_TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q"
TELEGRAM_CHAT_ID = "-1003126309534"

@app.route('/')
def home():
    # This tries to send a message the moment you open the link
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    text = "🔔 *Bridge Status:* System is Online!\nSalvation, if you see this, the connection is fixed."
    
    try:
        response = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
        res_data = response.json()
        return jsonify({
            "status": "Vercel Updated",
            "telegram_sent": res_data.get("ok", False),
            "details": res_data
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
    
