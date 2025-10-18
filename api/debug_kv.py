# api/debug_kv.py
from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        keys = ["KV_REST_API_URL","KV_REST_API_TOKEN","KV_REST_API_READ_ONLY_TOKEN","KV_URL","REDIS_URL"]
        status = {k: bool(os.getenv(k)) for k in keys}
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(status).encode("utf-8"))
