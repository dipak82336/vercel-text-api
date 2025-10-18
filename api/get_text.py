from http.server import BaseHTTPRequestHandler
from vercel_kv import KV
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # સાચી રીત: KV() ને કોઈ આર્ગ્યુમેન્ટની જરૂર નથી.
            # તે આપોઆપ પાસવર્ડ શોધી લે છે.
            kv_instance = KV() 
            
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
