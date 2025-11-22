# src/supabase_client.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # .env dosyasından SUPABASE_URL ve SUPABASE_KEY okunur

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL veya SUPABASE_KEY bulunamadı. .env dosyasını kontrol et.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
