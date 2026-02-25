from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response = {
            "status": "ok",
            "message": "Servidor funcionando 🔥",
            "port": 6969
        }

        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(("0.0.0.0", 6969), Handler)
print("Servidor corriendo en puerto 6969...")
server.serve_forever()
