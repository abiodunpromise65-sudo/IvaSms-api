import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8668872857:AAFKr-vAtAA_Jc5tiL_nM_upVHZStX0qE7Q"
CHAT_ID = "-1003126309534"

# Extracted from your screenshot 1000651479.jpg
XSRF = "eyJpdiI6IlkrRnhXWlE9PSIsInZhbHVlIjozWk5xRTJleW1lZ1UWNmwBdz00aml6ZDNvMHhMzdTZ000YkZLU0lRdmIzdVlvMo4aml6NUw4MIZpenRnBfIlamFzeWh2bkVbkVQdmdlckPW2w4RVNRSENXOTPb1k1QnFhM2R1M2RkOUdoZEC0RGkyOGdJTUQI LCJtYWMiOiI2Njc1ZjA3NGU3ZTYzZTgyZTgyYmNhNjE2NjR4QlJzW1zXyJE2G13_tcXU8ng1MzS-I7TUqnf6WsiZN_f6wacZbhUSUAtrw7nXiriCsg2AfKKYA_f-g"

@app.route('/sms')
def fetch_sms():
    date = request.args.get('date', '25/04/2026')
    # Using the path confirmed in your screenshot
    url = "https://ivasms.com/portal/live/get-otp-messages"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36',
        'X-XSRF-TOKEN': XSRF.replace('%3D', '='),
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json',
        'Cookie': f'XSRF-TOKEN={XSRF}'
    }
    
    try:
        # We send the request with the token headers
        response = requests.get(url, headers=headers, params={'date': date}, timeout=15)
        
        # Check if we got a valid response
        if response.status_code != 200:
            return jsonify({"status": "Error", "http_code": response.status_code, "detail": "Token might be expired"})

        data = response.json()
        messages = data.get('otp_messages', [])
        
        if messages:
            for msg in messages:
                text = f"📩 *New SMS Detected*\n\n*Sender:* {msg.get('sender')}\n*OTP:* `{msg.get('otp')}`\n*Time:* {msg.get('time')}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
            return jsonify({"status": "Success", "sent": len(messages)})
        
        return jsonify({"status": "Connected", "msg": "No new messages for this date", "debug": data})

    except Exception as e:
        return jsonify({"status": "Error", "detail": str(e)})

@app.route('/')
def home():
    return "SMS Bridge is Active."
    
