import base64
import random
import socket
import threading
import time
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler

DECOY_PORT = 80
COLLECTOR_PORT = 47820
RELAY_PORT = 5140
BASE_SPORT = 40000
NOISE_SPORT = 39999
CHUNK = 6
FLAG = "QMCTF{rn_l00ks_l1k3_m}"


def send_relay(dst_ip):
    time.sleep(2)
    encoded = base64.b64encode(FLAG.encode()).decode()
    chunks = [encoded[i:i + CHUNK] for i in range(0, len(encoded), CHUNK)]
    packets = [(BASE_SPORT + i, c.encode()) for i, c in enumerate(chunks)]
    packets += [(NOISE_SPORT, b"HB") for _ in range(5)]
    random.shuffle(packets)
    for sport, payload in packets:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", sport))
        s.sendto(payload, (dst_ip, RELAY_PORT))
        s.close()
        time.sleep(0.2)


class CollectorHandler(BaseHTTPRequestHandler):
    server_version = "QCollector/0.3"
    sys_version = ""

    def send_text(self, code, text):
        body = text.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_text(200, "Quillrnarsh collector v0.3\nEndpoints: /status\n")
        elif self.path == "/status":
            self.send_text(200, "status: online\nharvested sessions: 3\nrelay: enabled (test with GET /relay)\n")
        elif self.path == "/relay":
            client_ip = self.client_address[0]
            threading.Thread(target=send_relay, args=(client_ip,), daemon=True).start()
            self.send_text(200, f"relay test queued -> {client_ip} udp/{RELAY_PORT}\nfragments dispatch in 2s\n")
        else:
            self.send_text(404, "not found\n")


def run_decoy():
    handler = partial(SimpleHTTPRequestHandler, directory="/srv/www")
    HTTPServer(("0.0.0.0", DECOY_PORT), handler).serve_forever()


def run_collector():
    HTTPServer(("0.0.0.0", COLLECTOR_PORT), CollectorHandler).serve_forever()


if __name__ == "__main__":
    threading.Thread(target=run_decoy, daemon=True).start()
    run_collector()
