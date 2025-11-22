# src/analyzer.py

import os
import pandas as pd
from datetime import datetime
from ml_model import load_model, predict_anomaly
from supabase_client import supabase  

def fetch_connections():
    """
    Supabase connections tablosundan verileri çeker
    """
    response = supabase.table("connections").select("*").execute()
    data = response.data
    if not data:
        print("Veri yok")
        return pd.DataFrame()
    df = pd.DataFrame(data)
    return df

def analyze_connections():
    """
    Her connection için ML modeli ile anomali tahmini yapar
    """
    df = fetch_connections()
    if df.empty:
        print("İşlenecek veri yok.")
        return

    results = []
    for index, row in df.iterrows():
        ip = row.get("ip", "")
        is_anomaly = predict_anomaly(ip)
        feature_count = row.get("ip_feature", 1) 
        results.append({
            "ip": ip,
            "feature_count": feature_count,
            "anomaly": is_anomaly,
            "created_at": datetime.utcnow().isoformat()
        })


    for res in results:
        supabase.table("analysis").insert(res).execute()

    print(f"{len(results)} kayıt analiz edildi ve Supabase'e yazıldı.")



if __name__ == "__main__":
    analyze_connections()
