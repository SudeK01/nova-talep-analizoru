import pandas as pd
import sys
import os

# backend klasörünü görünür yap
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from firebase.firebase_tahmin_kaydet import tahmin_kaydet

# CSV'yi yükle
df = pd.read_csv("nova_tahminli_sonuclar.csv")

# Her satırı Firestore'a gönder
for index, row in df.iterrows():
    uid = f"train_{index}"
    metin = row["metin"]
    skor = round(float(row["tahmin_skoru"]), 2)
    tahmin_kaydet(uid, metin, skor, source="train")

print(" Train sonrası tahminler Firestore'a aktarıldı.")
