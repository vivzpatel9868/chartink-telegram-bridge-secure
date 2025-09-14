from vercel import Request, Response
import json
import requests
import os

def handler(request: Request) -> Response:
    if request.method != 'POST':
        return Response('<h2>🚨 Webhook Server Running! ✅</h2><p>Ready for Chartink alerts!</p>', 200, headers={'content-type': 'text/html'})
    
    try:
        # Get request data
        if hasattr(request, 'json') and request.json:
            data = request.json
        else:
            data = {}
        
        # Bot credentials
        bot_token = os.environ.get('BOT_TOKEN')
        chat_id = os.environ.get('CHAT_ID')
        
        if not bot_token or not chat_id:
            return Response('Missing credentials', 400)
        
        # Create message
        symbol = data.get('symbol', 'Unknown')
        price = data.get('price', 'Unknown')
        msg = data.get('message', 'Alert triggered')
        
        telegram_message = f"🚨 TRADING ALERT 🚨\nSymbol: {symbol}\nPrice: {price}\nMessage: {msg}"
        
        # Send to Telegram
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {'chat_id': chat_id, 'text': telegram_message}
        requests.post(url, data=payload)
        
        return Response('Alert sent!', 200)
        
    except Exception as e:
        return Response(f'Error: {str(e)}', 500)
