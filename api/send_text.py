from http.server import BaseHTTPRequestHandler
import json
from vercel_kv import kv  # lowercase kv import (no need for KV())

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
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
