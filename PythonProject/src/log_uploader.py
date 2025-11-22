# src/log_uploader.py
import os
from supabase_client import supabase

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "connections.log")

def upload_logs_to_db():
    if not os.path.exists(LOG_FILE):
        print("Log dosyası yok:", LOG_FILE)
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format: <timestamp> <TYPE> rest...
            parts = line.split(" ", 3)
            if len(parts) < 3:
                continue
            timestamp = parts[0]
            typ = parts[1]
            rest = parts[2] if len(parts) >= 3 else ""
            # DATA satırı ise "DATA <ip> <payload>"
            ip = None
            data = None
            if typ == "DATA":
                # rest like: "<ip> <payload>"
                spl = rest.split(" ", 1)
                ip = spl[0]
                data = spl[1] if len(spl) > 1 else ""
            else:
                # CONNECT/DISCONNECT: rest might be "ip:port"
                ip = rest.split(":", 1)[0]
                data = ""
            # insert to Supabase
            try:
                supabase.table("connections").insert({
                    "timestamp": timestamp,
                    "type": typ,
                    "ip": ip,
                    "data": data
                }).execute()
            except Exception as e:
                print("Supabase insert hata:", e)
    print("Tüm log satırları Supabase'e yüklendi.")
