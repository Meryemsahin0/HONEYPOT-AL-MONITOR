# src/ml_model.py

import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest

# Model dosyası
MODEL_FILE = os.path.join(os.path.dirname(__file__), "..", "model", "isolation_model.pkl")
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "logs", "connections.log")


def load_data():
    """
    connections.log dosyasını okuyup sayısal feature üretir.
    Basit olarak IP adreslerinin son octetini feature olarak alır.
    """
    if not os.path.exists(LOG_FILE):
        print("Log dosyası bulunamadı.")
        return pd.DataFrame()

    df = pd.read_csv(LOG_FILE, names=["timestamp", "type", "ip", "data"], sep=" ", on_bad_lines="skip")
    df['ip_feature'] = df['ip'].apply(lambda x: int(x.split('.')[-1]) if isinstance(x, str) else 0)
    return df[['ip_feature']]


def train_model():
    """
    Isolation Forest modeli eğitir ve kaydeder
    """
    X = load_data()
    if X.empty:
        print("Veri yok, model eğitilemiyor.")
        return None

    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)

    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    print(f"Model kaydedildi: {MODEL_FILE}")

    return model


def load_model():
    """
    Eğitilmiş modeli yükler. Eğer yoksa eğitir.
    """
    if os.path.exists(MODEL_FILE):
        model = joblib.load(MODEL_FILE)
        return model
    else:
        return train_model()


def predict_anomaly(ip):
    """
    Tek bir IP için anomali tahmini yapar
    """
    model = load_model()
    feature = int(ip.split('.')[-1])
    pred = model.predict([[feature]])[0]
    return True if pred == -1 else False


if __name__ == "__main__":
    model = load_model()
    test_ip = "10.10.10.123"
    if predict_anomaly(test_ip):
        print(f"{test_ip} şüpheli!")
    else:
        print(f"{test_ip} normal.")
