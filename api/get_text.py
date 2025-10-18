from http.server import BaseHTTPRequestHandler
import json
import traceback
from vercel_kv import kv

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            current_text = kv.get("current_text") or "Default text"
            response = {"text": current_text}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        except Exception as e:
            # Return full traceback (for temporary debugging only)
            tb = traceback.format_exc()
            error_data = {"error": str(e), "traceback": tb}
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(error_data).encode("utf-8"))
