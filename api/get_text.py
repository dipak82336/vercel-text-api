from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # ચાલો ચકાસીએ કે આપણને પાસવર્ડ મળે છે કે નહીં
            kv_url_from_env = os.environ.get('KV_URL')

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            if kv_url_from_env:
                # જો પાસવર્ડ મળે, તો આ સંદેશ બતાવો
                response_data = {"text": "SUCCESS: Environment Variable read successfully!"}
            else:
                # જો પાસવર્ડ ન મળે, તો આ સંદેશ બતાવો
                response_data = {"text": "ERROR: Could NOT read Environment Variable!"}
            
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        
        except Exception as e:
            # જો કોઈ બીજી એરર આવે, તો તે બતાવો
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {"text": f"A server error occurred: {str(e)}"}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
        return
