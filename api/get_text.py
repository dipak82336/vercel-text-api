from http.server import BaseHTTPRequestHandler
import json
from vercel_kv import kv  # lowercase 'kv' object imported directly

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            current_text = kv.get("current_text") or "Default text"
            response_data = {"text": current_text}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except Exception as e:
            error_data = {"error": str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
