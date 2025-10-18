from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # આપણે તપાસીશું કે પાસવર્ડ કોડ સુધી પહોંચી રહ્યા છે કે નહીં
            debug_info = {
                "MESSAGE": "This is a debug response.",
                "ARE_WE_IN_VERCEL": "VERCEL" in os.environ,
                "KV_URL_EXISTS": "KV_URL" in os.environ,
                "KV_REST_API_URL_EXISTS": "KV_REST_API_URL" in os.environ,
                "KV_REST_API_TOKEN_EXISTS": "KV_REST_API_TOKEN" in os.environ,
                # સુરક્ષા માટે, આપણે માત્ર ટોકનની લંબાઈ તપાસીશું
                "KV_REST_API_TOKEN_LENGTH": len(os.environ.get("KV_REST_API_TOKEN", ""))
            }
            
            self.wfile.write(json.dumps(debug_info).encode('utf-8'))

        except Exception as e:
            # જો અહીં પણ એરર આવે, તો તે બતાવો
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {"FATAL_ERROR": str(e)}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))
        return
