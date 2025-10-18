# api/get_text.py
from http.server import BaseHTTPRequestHandler
import json
import os
import traceback

# Try multiple import/initialization strategies for vercel_kv
kv_client = None
init_error = None

try:
    # preferred if package exports a ready instance named `kv`
    from vercel_kv import kv as _kv
    kv_client = _kv
except Exception as e1:
    try:
        # fallback: import KV class and instantiate (it will read env vars)
        from vercel_kv import KV as _KV
        try:
            kv_client = _KV()  # may raise if env vars missing / invalid
        except Exception as e2:
            init_error = f"KV() init error: {e2}"
            kv_client = None
    except Exception as e3:
        init_error = f"import error: {e1}; fallback import error: {e3}"
        kv_client = None

def _kv_get(key):
    if kv_client is None:
        raise RuntimeError("KV client not initialized")
    val = kv_client.get(key)
    if isinstance(val, bytes):
        return val.decode("utf-8")
    return val

class handler(BaseHTTPRequestHandler):
    def _json_response(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        try:
            if kv_client is None:
                # helpful diagnostic message
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

            current_text = _kv_get("current_text") or "Default text"
            return self._json_response(200, {"text": current_text})
        except Exception as e:
            tb = traceback.format_exc()
            return self._json_response(500, {"error": str(e), "traceback": tb})
