import json, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIG ---
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
    url = f"https://ivasms.com/portal/liv-sms/get-otp-messages?date={date}"
    
    cookies = get_cookies()
    response = requests.get(url, cookies=cookies)
    
    try:
        messages = response.json().get('otp_messages', [])
        if messages:
            for msg in messages:
                text = f"📩 *New SMS*\n*From:* {msg.get('sender')}\n*Code:* `{msg.get('otp')}`\n*Time:* {msg.get('time')}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
        return jsonify({"status": "Success", "count": len(messages)})
    except:
        return jsonify({"status": "Error", "detail": "Check cookies/session"})

@app.route('/')
def status():
    return "Bridge is Online. Use /sms?date=DD/MM/YYYY to fetch."
                
