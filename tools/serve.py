"""Siteyi yerelde önizlemek için küçük statik sunucu.

    python tools/serve.py            # http://localhost:8080
    python tools/serve.py 8000       # başka bir port

`python -m http.server` de çalışır; ancak bu sunucu eşzamanlı istekleri
(yüzlerce ders görseli) bağlantı sıfırlamadan karşılar ve IPv4/IPv6'yı birlikte dinler.
"""
import contextlib
import functools
import http.server
import os
import socket
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Server(http.server.ThreadingHTTPServer):
    address_family = socket.AF_INET6
    request_queue_size = 128
    daemon_threads = True

    def server_bind(self):
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        # Önizlemede tarayıcı her istekte dosyanın güncel olup olmadığını sorsun (eski CSS/JS kalmasın).
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"Önizleme: http://localhost:{port}/  (durdurmak için Ctrl+C)")
    try:
        Server(("::", port), functools.partial(Handler, directory=ROOT)).serve_forever()
    except KeyboardInterrupt:
        pass
