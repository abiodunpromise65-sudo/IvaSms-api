import json, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q"
CHAT_ID = "-1003126309534"

def get_cookies():
    try:
        with open('cookies.json', 'r') as f:
            data = json.load(f)
            return {c['name']: c['value'] for c in data}
    except:
        return {}

@app.route('/sms')
def fetch_sms():
    date = request.args.get('date', '25/04/2026')
    # EXACT URL FROM YOUR SCREENSHOT
    url = "https://ivasms.com/portal/live/get-otp-messages"
    
    params = {'date': date}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json'
    }
    
    try:
        cookies = get_cookies()
        response = requests.get(url, cookies=cookies, headers=headers, params=params, timeout=15)
        
        # Check if the response is actually JSON
        try:
            data = response.json()
        except:
            return jsonify({"status": "Error", "detail": "Site didn't return JSON. Are you logged in?", "url_tried": response.url})

        messages = data.get('otp_messages', [])
        if messages:
            for msg in messages:
                text = f"📩 *New SMS*\n*From:* {msg.get('sender')}\n*Code:* `{msg.get('otp')}`\n*Time:* {msg.get('time')}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
            return jsonify({"status": "Success", "count": len(messages)})
        
        return jsonify({"status": "Connected", "msg": "No messages for this date", "site_response": data})

    except Exception as e:
        return jsonify({"status": "Error", "detail": str(e)})

@app.route('/')
def home():
    return "Bridge is Online."
    
