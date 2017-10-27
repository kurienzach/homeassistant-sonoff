from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json
from SimpleWebSocketServer import SimpleWebSocketServer, SimpleSSLWebSocketServer, WebSocket
import threading

server_ip = "192.168.1.10"
server_port = "5000"


class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        print(self.address, 'closed')
        clients.remove(self)


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        print(self.path)
        self.wfile.write("<html><body><h1>hi!</h1></body></html>".encode())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        if self.path == "/":
            response = json.dumps({"error": 0, "reason": "ok", "IP": server_ip, "port": server_port})
            self.wfile.write(response.encode())
        elif self.path == "/on":
            clients[0].sendMessage("hi")
            response = json.dumps({"status": "on"})
            self.wfile.write(response.encode())
        elif self.path == "/off":
            response = json.dumps({"status": "on"})
            self.wfile.write(response.encode())
        elif self.path == "/toggle":
            response = json.dumps({"status": "on"})
            self.wfile.write(response.encode())


server = HTTPServer(('localhost', 9091), S)
server.socket = ssl.wrap_socket (server.socket, certfile='selfsigned.crt', keyfile='selfsigned.key', server_side=True)
thread = threading.Thread(target=server.serve_forever)
thread.daemon = True

clients = []
wsserver = SimpleSSLWebSocketServer('localhost', 9092, SimpleEcho, 'selfsigned.crt', 'selfsigned.key')
wsthread = threading.Thread(target=wsserver.serveforever)
wsthread.daemon = True

thread.start()
wsthread.start()

print('Server Started')

while 1:
    try:
        pass
    except KeyboardInterrupt:
        server.shutdown()
        wsserver.close()
        break