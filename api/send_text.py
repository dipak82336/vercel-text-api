from http.server import BaseHTTPRequestHandler
from vercel_kv import KV  # 'kv' ને બદલે 'KV' इम्पोर्ट કરો
import json
import os  # 'os' લાઇબ્રેરી इम्पोर्ट કરો

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # પાસવર્ડ જાતે જ os.environ માંથી લોડ કરો
            kv = KV(
                url=os.environ.get('KV_URL'),
                rest_api_url=os.environ.get('KV_REST_API_URL'),
                rest_api_token=os.environ.get('KV_REST_API_TOKEN'),
                rest_api_read_only_token=os.environ.get('KV_REST_API_READ_ONLY_TOKEN')
            )

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            new_text = data.get('text')
            
            if new_text is not None:
                kv.set("current_text", new_text)
                response_data = {"message": "Text updated successfully!"}
                self.send_response(200)
            else:
                response_data = {"error": "Text not provided"}
                self.send_response(400)
                
        except Exception as e:
            response_data = {"error": str(e)}
            self.send_response(500)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
