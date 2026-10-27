"""Local training server. Run: python server.py --port 8765."""

import argparse
import json
import secrets
import time
from functools import partial
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SESSIONS = set()


class TrainingServer(ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True


class Handler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        mime = super().guess_type(path)
        if mime.startswith("text/") or mime in ("application/javascript", "application/json"):
            return mime + "; charset=utf-8"
        return mime

    def log_message(self, format, *args):
        pass

    def send_json(self, status, body, cookie=None):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/health":
            time.sleep(0.005)
            return self.send_json(HTTPStatus.OK, {"status": "ok", "service": "training-api"})
        if self.path == "/api/session":
            cookies = SimpleCookie(self.headers.get("Cookie", ""))
            token = cookies.get("session")
            active = token is not None and token.value in SESSIONS
            return self.send_json(200 if active else 401, {"authenticated": active})
        return super().do_GET()

    def do_POST(self):
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= 8192:
                return self.send_json(400, {"error": "Некорректный размер запроса"})
            payload = json.loads(self.rfile.read(size))
            if not isinstance(payload, dict):
                raise ValueError("Expected a JSON object")
        except (ValueError, json.JSONDecodeError):
            return self.send_json(400, {"error": "Некорректный JSON"})
        if self.path == "/api/login":
            if payload.get("username") == "student" and payload.get("password") == "Study123!":
                token = secrets.token_urlsafe(24)
                SESSIONS.add(token)
                return self.send_json(200, {"message": "Вход выполнен"},
                                      f"session={token}; HttpOnly; SameSite=Strict; Path=/")
            return self.send_json(401, {"error": "Неверный логин или пароль"})
        if self.path == "/api/logout":
            cookies = SimpleCookie(self.headers.get("Cookie", ""))
            token = cookies.get("session")
            if token:
                SESSIONS.discard(token.value)
            return self.send_json(200, {"message": "Вы вышли"}, "session=; Max-Age=0; Path=/")
        if self.path == "/api/contact":
            errors = {}
            for field, title in (("name", "Имя"), ("email", "Email"), ("message", "Сообщение")):
                if not isinstance(payload.get(field), str) or not payload[field].strip():
                    errors[field] = f"{title}: обязательное поле"
            email = payload.get("email", "")
            import re
            if isinstance(email, str) and email.strip() and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()):
                errors["email"] = "Введите корректный email"
            if errors:
                return self.send_json(422, {"errors": errors})
            return self.send_json(200, {"message": "Сообщение успешно принято"})
        return self.send_json(404, {"error": "Endpoint not found"})


def make_server(port=0):
    return TrainingServer(("127.0.0.1", port), partial(Handler, directory=str(ROOT)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with make_server(args.port) as server:
        print(f"Training server: http://127.0.0.1:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
