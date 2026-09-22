"""
NEURALFLOW — Unified Vercel Serverless Entrypoint & Local Launcher
==================================================================
Exports 'app', 'application', and 'handler' for the Vercel Python runtime.
Captures all exceptions and returns informative tracebacks.
"""

import os
import sys
import mimetypes
import traceback
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RENDER_BACKEND_URL = "https://neuralflow-backend-epbh.onrender.com"

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".txt": "text/plain; charset=utf-8"
}


def _resolve_static_file(path):
    clean = path.split("?")[0].lstrip("/")
    if not clean or clean == "index.html":
        clean = "index.html"

    # Search current directory
    candidate = os.path.join(BASE_DIR, clean)
    if os.path.isfile(candidate):
        return candidate

    # Search frontend directory
    candidate = os.path.join(BASE_DIR, "frontend", clean)
    if os.path.isfile(candidate):
        return candidate

    # SPA index fallback
    fallback = os.path.join(BASE_DIR, "index.html")
    if os.path.isfile(fallback):
        return fallback

    fallback = os.path.join(BASE_DIR, "frontend", "index.html")
    if os.path.isfile(fallback):
        return fallback

    return None


def _proxy_api_request(method, path, body=None, headers=None):
    target_url = f"{RENDER_BACKEND_URL}{path}"
    req = urllib.request.Request(target_url, data=body, method=method)
    if headers:
        for k, v in headers.items():
            if k.lower() not in ("host", "content-length"):
                req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            resp_headers = [(k, v) for k, v in resp.getheaders() if k.lower() not in ("transfer-encoding", "content-encoding")]
            return resp.status, resp_headers, data
    except urllib.error.HTTPError as e:
        data = e.read()
        resp_headers = [(k, v) for k, v in e.headers.items() if k.lower() not in ("transfer-encoding", "content-encoding")]
        return e.code, resp_headers, data
    except Exception as e:
        return 502, [("Content-Type", "application/json")], f'{{"error":"Backend unavailable: {e}"}}'.encode()


# ---------------------------------------------------------------------------
# Robust WSGI Handler
# ---------------------------------------------------------------------------
def _wsgi_handler(environ, start_response):
    try:
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = environ.get("PATH_INFO", "/")

        # Reverse proxy to Render for any /api/* route
        if path.startswith("/api/"):
            body = None
            try:
                content_length = int(environ.get("CONTENT_LENGTH", 0) or 0)
                if content_length > 0:
                    body = environ["wsgi.input"].read(content_length)
            except Exception:
                body = None

            forward_headers = {}
            for key, value in environ.items():
                if key.startswith("HTTP_"):
                    header_name = key[5:].replace("_", "-").title()
                    forward_headers[header_name] = value
                elif key in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                    forward_headers[key.replace("_", "-").title()] = value

            status_code, resp_headers, resp_data = _proxy_api_request(method, path, body, forward_headers)
            status_text = f"{status_code} {'OK' if status_code == 200 else 'Response'}"
            start_response(status_text, resp_headers)
            return [resp_data]

        # Serve static assets
        file_path = _resolve_static_file(path)
        if file_path and os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            content_type = MIME_TYPES.get(ext, mimetypes.guess_type(file_path)[0] or "application/octet-stream")
            with open(file_path, "rb") as f:
                data = f.read()
            headers = [
                ("Content-Type", content_type),
                ("Content-Length", str(len(data))),
                ("Cache-Control", "public, max-age=3600")
            ]
            start_response("200 OK", headers)
            return [data]

        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Not Found"]
    except Exception:
        err = traceback.format_exc()
        start_response("500 Internal Server Error", [("Content-Type", "text/plain; charset=utf-8")])
        return [f"WSGI Handler Error:\n{err}".encode("utf-8")]


# Universal callable
def app(environ, start_response):
    return _wsgi_handler(environ, start_response)


# WSGI standard alias
application = app


# ---------------------------------------------------------------------------
# BaseHTTPRequestHandler subclass for Vercel Function runtime
# ---------------------------------------------------------------------------
class handler(BaseHTTPRequestHandler):
    """Vercel Python Serverless HTTP Request Handler."""

    def do_GET(self):
        try:
            path = self.path
            if path.startswith("/api/"):
                headers = {k: v for k, v in self.headers.items()}
                status_code, resp_headers, data = _proxy_api_request("GET", path, None, headers)
                self.send_response(status_code)
                for k, v in resp_headers:
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(data)
                return

            file_path = _resolve_static_file(path)
            if file_path and os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                content_type = MIME_TYPES.get(ext, mimetypes.guess_type(file_path)[0] or "application/octet-stream")
                with open(file_path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "public, max-age=3600")
                self.end_headers()
                self.wfile.write(data)
                return

            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Not Found")
        except Exception:
            err = traceback.format_exc()
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Handler GET Error:\n{err}".encode("utf-8"))

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", 0) or 0)
            body = self.rfile.read(length) if length > 0 else None
            headers = {k: v for k, v in self.headers.items()}
            status_code, resp_headers, data = _proxy_api_request("POST", self.path, body, headers)
            self.send_response(status_code)
            for k, v in resp_headers:
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)
        except Exception:
            err = traceback.format_exc()
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"Handler POST Error:\n{err}".encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.end_headers()


# Local development launcher
if __name__ == "__main__":
    import runpy
    BACKEND_DIR = os.path.join(BASE_DIR, "backend")
    BACKEND_APP = os.path.join(BACKEND_DIR, "app.py")
    if os.path.isfile(BACKEND_APP):
        os.chdir(BACKEND_DIR)
        if BACKEND_DIR not in sys.path:
            sys.path.insert(0, BACKEND_DIR)
        runpy.run_path(BACKEND_APP, run_name="__main__")
