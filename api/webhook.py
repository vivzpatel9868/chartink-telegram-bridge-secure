from http.server import BaseHTTPRequestHandler
import json
import requests
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the request data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        # Get tokens from environment variables (SECURE!)
        BOT_TOKEN = os.environ.get('BOT_TOKEN')
        CHAT_ID = os.environ.get('CHAT_ID')
        
        if not BOT_TOKEN or not CHAT_ID:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Missing environment variables')
            return
        
        # Create message
        message = f"🚨 TRADING ALERT 🚨\n"
        message += f"Symbol: {data.get('symbol', 'Unknown')}\n"
        message += f"Price: {data.get('price', 'Unknown')}\n"
        message += f"Message: {data.get('message', 'Alert triggered')}\n"
        message += f"Time: {data.get('timestamp', 'Now')}"
        
        # Send to Telegram
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }
        
        requests.post(telegram_url, data=payload)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
