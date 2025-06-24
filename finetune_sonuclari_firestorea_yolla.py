import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from firebase.firebase_tahmin_kaydet import tahmin_kaydet


# CSV dosyasını yükle
df = pd.read_csv("backend/nova_finetune_sonuclar.csv")

# Gerekli sütunları kontrol et
if "metin" not in df.columns or "tahmin_skoru" not in df.columns:
    raise ValueError("CSV dosyasında 'metin' veya 'tahmin_skoru' sütunu eksik!")

# Her satırı Firestore'a gönder
for index, row in df.iterrows():
    uid = f"finetune_{index}"
    metin = row["metin"]
    skor = float(row["tahmin_skoru"])
    tahmin_kaydet(uid, metin, skor, source="finetune")

print(" Tüm fine-tune tahminleri Firestore'a aktarıldı.")
