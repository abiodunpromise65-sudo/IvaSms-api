import json, requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q"
CHAT_ID = "-1003126309534"

def get_cookies():
    try:
        with open('cookies.json', 'r') as f:
            data = json.load(f)
            # This extracts the cookies into the format the website expects
            return {c['name']: c['value'] for c in data}
    except Exception as e:
        print(f"Cookie Error: {e}")
        return {}

@app.route('/sms')
def fetch_sms():
    date = request.args.get('date', '25/04/2026')
    url = f"https://ivasms.com/portal/liv-sms/get-otp-messages?date={date}"
    
    # These headers make the bot look like a real mobile browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://ivasms.com/portal/liv-sms',
    }
    
    try:
        cookies = get_cookies()
        response = requests.get(url, cookies=cookies, headers=headers, timeout=15)
        data = response.json()
        
        messages = data.get('otp_messages', [])
        
        if messages:
            for msg in messages:
                # This sends each SMS to your Telegram group
                text = f"📩 *New SMS Detected*\n\n*Sender:* {msg.get('sender')}\n*OTP:* `{msg.get('otp')}`\n*Time:* {msg.get('time')}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
            return jsonify({"status": "Success", "messages_sent": len(messages)})
        else:
            return jsonify({"status": "Connected", "message": "No new SMS found for this date.", "raw_response": data})
            
    except Exception as e:
        return jsonify({"status": "Error", "detail": str(e)})

@app.route('/')
def home():
    return "Bridge is active. Use /sms?date=25/04/2026"
                
