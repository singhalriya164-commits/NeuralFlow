from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'NeuralFlow Edge Gateway: Operational. Frontend served from static edge.')
        return

    def do_POST(self):
        self.do_GET()

# Export for WSGI/ASGI compatibility if inspected
app = handler
application = handler
