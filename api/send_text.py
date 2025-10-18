# api/send_text.py
from http.server import BaseHTTPRequestHandler
import json
import os
import traceback

kv_client = None
init_error = None

try:
    from vercel_kv import kv as _kv
    kv_client = _kv
except Exception as e1:
    try:
        from vercel_kv import KV as _KV
        try:
            kv_client = _KV()
        except Exception as e2:
            init_error = f"KV() init error: {e2}"
            kv_client = None
    except Exception as e3:
        init_error = f"import error: {e1}; fallback import error: {e3}"
        kv_client = None

def _kv_set(key, value):
    if kv_client is None:
        raise RuntimeError("KV client not initialized")
    return kv_client.set(key, value)

class handler(BaseHTTPRequestHandler):
    def _json_response(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            if kv_client is None:
                env_status = {k: bool(os.getenv(k)) for k in (
                    "KV_REST_API_URL", "KV_REST_API_TOKEN", "KV_REST_API_READ_ONLY_TOKEN",
                    "KV_URL", "REDIS_URL"
                )}
                payload = {
                    "error": "KV client not initialized",
                    "init_error": init_error,
                    "env_present": env_status,
                    "hint": "Make sure KV_REST_API_URL and KV_REST_API_TOKEN are set in Vercel, then redeploy."
                }
                return self._json_response(500, payload)

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length or 0)
            data = json.loads(body or b"{}")
            new_text = data.get("text")
            if new_text is None:
                return self._json_response(400, {"error": "Text not provided"})
            _kv_set("current_text", new_text)
            return self._json_response(200, {"message": "Text updated successfully!"})
        except Exception as e:
            tb = traceback.format_exc()
            return self._json_response(500, {"error": str(e), "traceback": tb})
