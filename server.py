#!/usr/bin/env python3
"""LazyDesk local server. Uses only Python's standard library."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path
import json, urllib.request, urllib.error, os, mimetypes

ROOT = Path(__file__).resolve().parent
OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
PORT = int(os.environ.get("PORT", "8000"))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def _json(self, code, payload):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/status":
            try:
                with urllib.request.urlopen(OLLAMA + "/api/tags", timeout=1.8) as r:
                    info = json.loads(r.read().decode("utf-8"))
                models = [m.get("name", "") for m in info.get("models", [])]
                return self._json(200, {"server": True, "ollama": bool(models), "models": models,
                                        "model": models[0] if models else None})
            except Exception:
                return self._json(200, {"server": True, "ollama": False, "models": [], "model": None})
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/ai":
            return self._json(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 1_000_000:
                return self._json(400, {"error": "Request must be under 1 MB"})
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            prompt = str(payload.get("prompt", "")).strip()
            model = str(payload.get("model", "llama3.2")).strip()
            if not prompt:
                return self._json(400, {"error": "Please enter a prompt"})
            if len(prompt) > 20000:
                return self._json(400, {"error": "Prompt is too long (20,000 characters max)"})
            if not model or len(model) > 100:
                return self._json(400, {"error": "Invalid model name"})
            messages = []
            for item in payload.get("history", [])[-8:]:
                role = item.get("role")
                content = str(item.get("content", ""))[:20000]
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": prompt})
            body = json.dumps({"model": model, "messages": messages, "stream": False,
                               "options": {"temperature": 0.4}}).encode("utf-8")
            req = urllib.request.Request(OLLAMA + "/api/chat", data=body,
                                         headers={"Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    result = json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")[:500]
                return self._json(502, {"error": "Ollama returned an error: " + detail})
            response = result.get("message", {}).get("content", "")
            return self._json(200, {"response": response, "model": model})
        except urllib.error.URLError:
            return self._json(503, {"error": "Can't reach Ollama at " + OLLAMA + ". Is Ollama running?"})
        except (ValueError, UnicodeDecodeError):
            return self._json(400, {"error": "Invalid JSON request"})
        except Exception as e:
            return self._json(500, {"error": "Local request failed: " + str(e)[:200]})

    def log_message(self, fmt, *args):
        # Keep local logs quiet; uncomment next line while debugging.
        # super().log_message(fmt, *args)
        pass

if __name__ == "__main__":
    print(f"LazyDesk AI is starting at http://127.0.0.1:{PORT}")
    print("Keep this terminal open while using the app. Press Ctrl+C to stop.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
