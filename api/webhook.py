from http.server import BaseHTTPRequestHandler
import requests
import os
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h2>🚨 Webhook Server Running! ✅</h2>')

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            bot_token = os.environ.get('BOT_TOKEN')
            chat_id = os.environ.get('CHAT_ID')
            
            if not bot_token or not chat_id:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing credentials')
                return

            symbol = data.get('symbol', 'Unknown')
            price = data.get('price', 'Unknown')
            msg = data.get('message', 'Alert triggered')
            telegram_message = f"🚨 ALERT 🚨\nSymbol: {symbol}\nPrice: {price}\nMessage: {msg}"
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, data={'chat_id': chat_id, 'text': telegram_message})
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

def handler(request):
    # This function is retained for Vercel's serverless environment
    # but the actual logic is handled by the BaseHTTPRequestHandler above.
    # Vercel will use the class-based approach automatically.
    pass
