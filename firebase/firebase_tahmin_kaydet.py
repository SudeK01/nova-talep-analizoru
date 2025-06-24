import os
from datetime import datetime
from firebase_admin import credentials, firestore
import firebase_admin
import requests


#  Firebase bağlantısını sadece bir kez başlat
if not firebase_admin._apps:
    json_path = os.path.abspath("backend/aivatandastalepanalizoru-firebase-adminsdk-fbsvc-a033db91e9.json")
    cred = credentials.Certificate(json_path)
    firebase_admin.initialize_app(cred)

#  Firestore istemcisi
db = firestore.client()


#  Tahmin verisini Firestore'a kaydet
def tahmin_kaydet(uid, metin, skor, source="kullanici"):
    try:
        print("Firestore’a tahmin verisi gönderiliyor...")
        veri = {
          "uid": uid,
          "metin": metin,
          "skor": skor,
          "tarih": datetime.now().isoformat(),
          "source": source
        }     
        db.collection("tahminler").add(veri)
        print(f"Tahmin kaydedildi: {metin[:30]}... (Skor: {skor})")
    except Exception as e:
        print(f"Tahmin kaydı başarısız: {e}")
        raise  


# Yerel model API'si ile skor hesapla
def tahmin_modeli_ile_skor_hesapla(metin):
    try:
        response = requests.post("http://127.0.0.1:5000/api/tahmin-yap", json={"metin": metin})
        if response.status_code == 200:
            return response.json().get("skor", 0.0)
        else:
            print("Tahmin servisi 200 dönmedi:", response.text)
            return 0.0
    except Exception as e:
        print("Tahmin API çağrısı başarısız:", str(e))
        return 0.0


#  Yükleme kontrolü
print(" firebase_tahmin_kaydet.py yüklendi!")

# test
if __name__ == "__main__":
    print(" Manuel test başlatılıyor...")
    test_uid = "test_user"
    test_metin = "Bugün yollar çok bozuk."
    test_skor = 3.5
    tahmin_kaydet(test_uid, test_metin, test_skor)

