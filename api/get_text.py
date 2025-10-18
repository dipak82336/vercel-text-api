from http.server import BaseHTTPRequestHandler
from vercel_kv import KV
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # પાસવર્ડ જાતે જ os.environ માંથી લોડ કરો
            kv_instance = KV(
                url=os.environ.get('KV_URL'),
                rest_api_url=os.environ.get('KV_REST_API_URL'),
                rest_api_token=os.environ.get('KV_REST_API_TOKEN'),
                rest_api_read_only_token=os.environ.get('KV_REST_API_READ_ONLY_TOKEN')
            )
            
            current_text = kv_instance.get("current_text") or "Default text"
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
        return
