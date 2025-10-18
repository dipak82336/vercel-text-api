from http.server import BaseHTTPRequestHandler
import json
from vercel_kv import kv  # import the ready-to-use kv object
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # use kv.get (this will raise only when used and environment missing)
            current_text = kv.get("current_text") or "Default text"
            response_data = {"text": current_text}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except Exception as e:
            # ensure we *always* return JSON on exceptions
            error_data = {"error": str(e)}
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
