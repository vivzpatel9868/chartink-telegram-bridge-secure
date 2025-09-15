# webhook.py

import json
import os
import requests

def handler(request):
    if request.method == "GET":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": "<h2>🚨 Webhook Server Running! ✅</h2>"
        }
    try:
        data = request.json or {}

        bot_token = os.environ.get('BOT_TOKEN')
        chat_id = os.environ.get('CHAT_ID')
        if not bot_token or not chat_id:
            return {
                "statusCode": 400,
                "body": "Missing credentials"
            }
        symbol = data.get('symbol', 'Unknown')
        price = data.get('price', 'Unknown')
        msg = data.get('message', 'Alert triggered')
        telegram_message = f"🚨 ALERT 🚨\nSymbol: {symbol}\nPrice: {price}\nMessage: {msg}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        requests.post(url, data={'chat_id': chat_id, 'text': telegram_message})
        return {
            "statusCode": 200,
            "body": "OK"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
