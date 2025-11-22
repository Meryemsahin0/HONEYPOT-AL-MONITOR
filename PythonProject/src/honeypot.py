# src/honeypot.py
import socket
import threading
import os
from datetime import datetime, timezone

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "connections.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_line(line):
    ts = datetime.now(timezone.utc).isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ts} {line}\n")

def handle_client(conn, addr):
    ip, port = addr
    log_line(f"CONNECT {ip}:{port}")
    try:
        conn.settimeout(60)
        conn.sendall(b"SSH-2.0-OpenSSH_7.9p1 Debian-10\r\n")
        while True:
            data = conn.recv(4096)
            if not data:
                break
            payload = data.decode(errors="replace").strip()
            # Log DATA satırı DATA <ip> <payload> !!!!!!
            log_line(f"DATA {ip} {payload}")
            conn.sendall(b"Permission denied, please try again.\n")
    except Exception as e:
        log_line(f"ERROR {ip} {e}")
    finally:
        try:
            conn.close()
        except:
            pass
        log_line(f"DISCONNECT {ip}:{port}")

def start_server(host="0.0.0.0", port=2222):
    log_line(f"SERVER_START {host}:{port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(100)
    try:
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        log_line("SERVER_STOPPED")
    finally:
        s.close()

if __name__ == "__main__":
    start_server()
