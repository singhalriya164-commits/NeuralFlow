from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'NeuralFlow API Edge: Operational. Proxying to Render backend.')
        return

    def do_POST(self):
        self.do_GET()

app = handler
application = handler
