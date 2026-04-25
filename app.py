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
    
    # We will try both common URL versions automatically
    urls = [
        f"https://ivasms.com/portal/live-sms/get-otp-messages?date={date}",
        f"https://ivasms.com/portal/liv-sms/get-otp-messages?date={date}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json'
    }
    
    cookies = get_cookies()
    last_error = ""

    for url in urls:
        try:
            response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
            data = response.json()
            
            # If we find messages, send them to Telegram!
            messages = data.get('otp_messages', [])
            if messages:
                for msg in messages:
                    text = f"📩 *New SMS*\n*From:* {msg.get('sender')}\n*Code:* `{msg.get('otp')}`\n*Time:* {msg.get('time')}"
                    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                  json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
                return jsonify({"status": "Success", "messages_sent": len(messages)})
            
            # If the link works but no messages are found
            if "otp_messages" in data:
                return jsonify({"status": "Connected", "info": "No messages for this date", "raw": data})
                
            last_error = data.get('message', 'Unknown Error')
        except Exception as e:
            last_error = str(e)

    return jsonify({"status": "Error", "detail": last_error, "help": "Try refreshing your cookies.json"})

@app.route('/')
def home():
    return "Bridge is Online. Use /sms?date=25/04/2026"
        
