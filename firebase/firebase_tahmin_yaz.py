import csv
import firebase_admin
from firebase_admin import credentials, firestore

#  Firebase Admin başlat
cred = credentials.Certificate("backend/aivatandastalepanalizoru-firebase-adminsdk-fbsvc-a033db91e9.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

#  CSV dosyasından veriyi oku ve Firestore'a yaz
def yaz_csvden_firestorea(csv_dosyasi):
    with open(csv_dosyasi, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            metin = row["metin"]
            skor = float(row["tahmin_skoru"])

            #  Firestore dokümanını oluştur
            veri = {
                "metin": metin,
                "skor": skor
            }

            db.collection("tahminler").add(veri)
            print(f" Eklendi: {metin[:30]}... (Skor: {skor})")

#  Fonksiyonu çağır
if __name__ == "__main__":
    yaz_csvden_firestorea("nova_tahminli_sonuclar.csv")
