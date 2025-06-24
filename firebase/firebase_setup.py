print(" Kod çalıştırılıyor...")  # Debug mesajı

import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime


# JSON dosyasının yolu
json_path = "aivatandastalepanalizoru-firebase-adminsdk-fbsvc-a033db91e9.json"


print(" JSON dosya yolu:", os.path.abspath(json_path))
print(" JSON tam yolu gerçekten var mı?", os.path.exists(json_path))

cred = credentials.Certificate(os.path.abspath(json_path))

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()



print(" Firebase modülleri içe aktarılıyor...")

try:
    # Firebase için kimlik doğrulama dosyanı yükle

    print(" Firebase başarıyla başlatıldı!")  # Debug mesajı

    # Firestore veritabanını başlat
    db = firestore.client()

except Exception as e:
    print(" Firebase başlatılırken hata oluştu:", e)



# Firestore’a veri ekleme fonksiyonu
def veri_ekle():
    try:
        print("📡 Firestore’a veri ekleniyor...")  # Debug mesajı
        doc_ref = db.collection("sikayetler").document()
        doc_ref.set({
            "konu": "Elektrik Kesintisi, elektrik yok.",
            "öncelik": "Acil",
            "açıklama": "Mahallede 5 saattir elektrik yok.",
            "tarih": firestore.SERVER_TIMESTAMP,
            "durum": "Beklemede"  # Yeni eklenen alan
        })
        print("✅ Veri Firestore’a eklendi!")  # Başarı mesajı

    except Exception as e:
        print(" Veri eklenirken hata oluştu:", e)  # Hata mesajını ekrana yazdır

# Fonksiyonu çalıştır
veri_ekle()



# Firestore'daki verileri okuma fonksiyonu
def verileri_oku():
    print(" Firestore’dan veriler okunuyor...")  # Debug mesajı
    docs = db.collection("sikayetler").stream()
    
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")  # Veriyi ekrana yazdır

def veriyi_guncelle():
    print(" Firestore’daki veri güncelleniyor...")  # Debug mesajı
    docs = db.collection("sikayetler").stream()
    
    for doc in docs:  # Koleksiyondaki ilk belgeyi güncelle
        db.collection("sikayetler").document(doc.id).update({
            "açıklama": "Elektrik kesintisi giderildi!",
            "öncelik": "Normal"
        })
        print(f" {doc.id} başarıyla güncellendi!")
        break  # İlk belgeyi güncelleyip çıkıyoruz

veriyi_guncelle()  # Fonksiyonu çalıştır

def veriyi_sil():
    print("🗑 Firestore’daki veri siliniyor...")  # Debug mesajı
    docs = db.collection("sikayetler").stream()
    
    for doc in docs:  # Koleksiyondaki ilk belgeyi sil
        db.collection("sikayetler").document(doc.id).delete()
        print(f" {doc.id} başarıyla silindi!")
        break  # İlk belgeyi silip çıkıyoruz

veriyi_sil()  # Fonksiyonu çalıştır




# 🛠 Firestore'daki tüm belgeleri siliyoruz...
print("🗑 Firestore'daki TÜM belgeler siliniyor...")

def tum_verileri_sil():
    docs = db.collection("sikayetler").list_documents()
    for doc in docs:
        print(f" {doc.id} siliniyor...")
        doc.delete()
    print(" Firestore tamamen temizlendi!")

tum_verileri_sil()


def tahmin_kaydet(uid, metin, skor):
    try:
        veri = {
            "uid": uid,
            "metin": metin,
            "skor": skor,
            "tarih": datetime.now().isoformat()
        }
        db.collection("tahminler").add(veri)
        print(f" Tahmin kaydedildi: {metin[:30]}... (Skor: {skor})")
    except Exception as e:
        print(f" Tahmin kaydı başarısız: {e}")
