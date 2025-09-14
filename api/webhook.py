from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return '<h2>🚨 Webhook Server Running! ✅</h2>'
    
    try:
        data = request.get_json() or {}
        
        bot_token = os.environ.get('BOT_TOKEN')
        chat_id = os.environ.get('CHAT_ID')
        
        if not bot_token or not chat_id:
            return 'Missing credentials', 400
        
        symbol = data.get('symbol', 'Unknown')
        price = data.get('price', 'Unknown')
        msg = data.get('message', 'Alert triggered')
        
        telegram_message = f"🚨 ALERT 🚨\nSymbol: {symbol}\nPrice: {price}\nMessage: {msg}"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': telegram_message}
        requests.post(url, data=payload)
        
        return 'OK', 200
        
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    app.run()
