import firebase_admin
from firebase_admin import credentials, auth, firestore 
from datetime import datetime,timezone   # Şikayet zamanını kaydetmek için gerekli

import os # İşletim sistemi işlemleri için os modülü ekleniyor

# Firebase kimlik doğrulama dosyasının yolu
firebase_config_path = os.path.join("backend", "aivatandastalepanalizoru-firebase-adminsdk-fbsvc-a033db91e9.json")

# Eğer Firebase daha önce başlatılmamışsa başlat
if not firebase_admin._apps:
    if os.path.exists(firebase_config_path):
        cred = credentials.Certificate(firebase_config_path)
        firebase_admin.initialize_app(cred)
        print(" Firebase bağlantısı başarıyla başlatıldı!")
    else:
        print(" Firebase kimlik doğrulama dosyası bulunamadı!")


# Firestore veritabanını başlat
db = firestore.client()

print(" Firebase Authentication başarıyla başlatıldı!")


# Kullanıcı kaydı ve rol ekleme fonksiyonu
def kullanici_kayit(email, sifre, rol="kullanici"):
    try:
        print(" Kullanıcı kaydediliyor...")

        #  Eğer kullanıcı zaten kayıtlıysa hataya düşmeden UID'yi alalım
        try:
            kullanici = auth.get_user_by_email(email)
            print(f" Kullanıcı zaten mevcut! UID: {kullanici.uid}")
            return kullanici.uid  # Mevcut kullanıcının UID'sini döndür
        except:
            pass  # Kullanıcı bulunamazsa devam et

        #  Yeni kullanıcı oluştur
        kullanici = auth.create_user(
            email=email,
            password=sifre
        )
        print(f" Kullanıcı başarıyla oluşturuldu! UID: {kullanici.uid}")

        #  Kullanıcıyı Firestore'a ekleyelim
        kullanici_ref = db.collection("kullanicilar").document(kullanici.uid)

        #  Eğer doküman zaten varsa üzerine yazma, sadece eksik alanları tamamla
        kullanici_verisi = {
            "email": email,
            "rol": rol  # Varsayılan olarak "kullanici" atanıyor
        }
        kullanici_ref.set(kullanici_verisi, merge=True)  #  merge=True sayesinde var olan verilere zarar vermez

        print(" Kullanıcı Firestore'a eklendi veya güncellendi!")

        return kullanici.uid  # Kullanıcının UID'sini döndür
    except Exception as e:
        print(f" Kullanıcı kaydı başarısız: {e}")
        return None

    
    # Kullanıcının admin olup olmadığını kontrol eden fonksiyon 
def kullanici_admin_mi(uid):
    try:
        doc = db.collection("kullanicilar").document(uid).get()
        
        if doc.exists:
            rol = doc.to_dict().get("rol", "kullanici")  # Varsayılan olarak "kullanici"
            return rol == "admin"
        else:
            print(f" Kullanıcı bulunamadı! UID: {uid}")
            return False  # Kullanıcı yoksa admin değilmiş gibi döndür

    except Exception as e:
        print(f" Kullanıcı admin kontrolü sırasında hata oluştu: {e}")
        return False


# Kullanıcının rolünü Firestore’dan getiren fonksiyon
def kullanici_rolu_getir(uid):
    try:
        doc = db.collection("kullanicilar").document(uid).get()
        if doc.exists:
            return doc.to_dict().get("rol", "kullanici")  # Eğer rol yoksa varsayılan "kullanici"
        else:
            return "kullanici"
    except Exception as e:
        print(f" Kullanıcı rolü alınamadı: {e}")
        return "kullanici"


# Test amaçlı kullanıcı oluşturma (şimdilik burada, sonra kaldırabiliriz)
if __name__ == "__main__":
    test_email = "test@example.com"
    test_sifre = "Sifre123!"
    kullanici_kayit(test_email, test_sifre)
 
 
#Kullanıcı Giriş Yapma Fonksiyonu
def kullanici_giris(email, sifre):
    try:
        print(" Kullanıcı giriş yapıyor...")
        kullanici = auth.get_user_by_email(email)  # Kullanıcıyı e-posta ile getir
        
        # Eğer kullanıcı varsa UID bilgisini döndür
        print(f" Kullanıcı bulundu: UID: {kullanici.uid}")

        return kullanici.uid  # Kullanıcının UID'sini döndür
    except Exception as e:
        print(f" Kullanıcı girişi başarısız: {e}")  # Hata mesajını ekrana yazdır
        return None  # Giriş başarısızsa None döndür
    

#sonradan silinecek galiba
if __name__ == "__main__":
    test_email = "test@example.com"  # Kayıtlı kullanıcı
    test_sifre = "Sifre123!"  # Kullanıcının şifresi
    kullanici_giris(test_email, test_sifre)  # Kullanıcı giriş fonksiyonunu çağır


# Kullanıcı Çıkış Yapma Fonksiyonu
def kullanici_cikis():
    """
    Kullanıcı çıkış yapar ama  Firebase Admin SDK doğrudan çıkış işlemi yapmaz.
    Çıkış işlemi istemci tarafında yönetilir.
    Bu fonksiyon sadece terminalde bilgilendirme mesajı gösterir.
    """
    try:
        print(" Kullanıcı çıkış yapıyor...")
        # Firebase Admin SDK çıkış işlemi yapmaz, sadece bilgilendirme ekliyoruz.
        print(" Kullanıcı çıkış yaptı! (İstemci tarafında uygulanmalı)")
    except Exception as e:
        print(f" Kullanıcı çıkış yaparken hata oluştu: {e}")


# TEST: Kullanıcı Kaydı, Giriş ve Çıkış

if __name__ == "__main__":
    test_email = "test@example.com"  # Daha önce kaydettiğimiz kullanıcı
    test_sifre = "Sifre123!"  # Kullanıcının şifresi
    
    kullanici_giris(test_email, test_sifre)  #  Kullanıcı giriş yapıyor
    kullanici_cikis()  #  Kullanıcı çıkış yapıyor
       

# Kullanıcı şifre sıfırlama fonksiyonu
def sifre_sifirla(email):
    try:
        print(" Şifre sıfırlama bağlantısı gönderiliyor...")
        auth.generate_password_reset_link(email)
        print(f" Şifre sıfırlama bağlantısı gönderildi: {email}")
    except Exception as e:
        print(f" Şifre sıfırlama başarısız: {e}")


# Test için şifre sıfırlama işlemi
if __name__ == "__main__":
    test_email = "test@example.com"
    
    sifre_sifirla(test_email)  # Şifre sıfırla


# 🔍 Şikayet metnini analiz eden basit fonksiyon 
def sikayet_analizi_yap(sikayet_metni):
    """
    Şikayet metnini analiz eder ve negatif kelimelere göre
    sadece eksi sayısı döndürür (artılar sistem dışı bırakıldı).
    """
    negatif_kelimeler = ["gecikti", "bekledim", "yavaş", "kötü", "çözülmedi", "hala", "şikayetçiyim", "kesildi", "arıza", "çözüm yok", "üretilemedi", "3 gündür", "giderilmedi", "yetersiz"]

    kelimeler = sikayet_metni.lower().split()
    eksiler = sum(1 for kelime in kelimeler if kelime in negatif_kelimeler)

    return None, eksiler


# Şikayet ekleyen fonksiyon
def sikayet_ekle(uid, sikayet_metni):
    """
    Bu fonksiyon, bir kullanıcının şikayetini Firestore veritabanına ekler.
    Şikayet analiz edilerek sadece eksiler ve kategori alanı otomatik eklenir.
    """
    try:
        #  Şikayet metnini analiz et
        eksiler = sikayet_analizi_yap(sikayet_metni)
        kategori = sikayet_kategorisini_tahmin_et(sikayet_metni)

        #  Yeni şikayet belgesi oluştur
        sikayet_ref = db.collection("sikayetler").document()
        sikayet_verisi = {
            "kullanici_uid": uid,
            "sikayet": sikayet_metni,
            "tarih": datetime.now(timezone.utc),
            "eksiler": eksiler,
            "kategori": kategori,
            "durum": "Beklemede"  # Varsayılan durum
        }

        sikayet_ref.set(sikayet_verisi)
        print(f" Şikayet başarıyla eklendi! (UID: {uid})")
        print(f" Eksiler: {eksiler} |  Kategori: {kategori}")
        return sikayet_ref.id

    except Exception as e:
        print(f" Şikayet eklenirken hata oluştu: {e}")
        return None


# Firestore'daki tüm şikayetleri listeleme fonksiyonu
def sikayetleri_listele():
    try:
        sikayetler = db.collection("sikayetler").stream()
        print(" Tüm şikayetler:")
        for doc in sikayetler:
            veri = doc.to_dict()
            print(f"- UID: {veri.get('kullanici_uid', 'Bilinmiyor')}")
            print(f"  Şikayet: {veri['sikayet']}")
            print(f"  Tarih: {veri['tarih']}\n")
    except Exception as e:
        print(f" Şikayetler listelenirken hata oluştu: {e}")


# Belirli bir kullanıcıya ait şikayetleri listeleme fonksiyonu
def sikayetleri_filtrele(uid):
    try:
        print(f" {uid} kullanıcısına ait şikayetler:")
        docs = db.collection("sikayetler").where("kullanici_uid", "==", uid).stream()

        bulundu = False
        for doc in docs:
            veri = doc.to_dict()
            print(f"-  Şikayet: {veri.get('sikayet', 'Belirsiz')}")
            print(f"   Tarih: {veri.get('tarih', 'Yok')}\n")
            bulundu = True

        if not bulundu:
            print(" Bu kullanıcıya ait şikayet bulunamadı.")

    except Exception as e:
        print(f" Şikayetleri filtrelerken hata oluştu: {e}")


# Belirli bir tarihten sonraki şikayetleri listeleme fonksiyonu
def sikayetleri_tarihe_gore_filtrele(tarih_str):
    """
    Bu fonksiyon, Firestore'dan sadece belirli bir tarihten sonraki şikayetleri getirir.
    tarih_str: 'YYYY-MM-DD' formatında bir tarih örneği, örnek: '2025-03-15'
    """
    try:
        print(" Tarihe göre filtrelenmiş şikayetler:")
        # Naive tarihi aware hale getiriyoruz
        filtre_tarihi = datetime.strptime(tarih_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        docs = db.collection("sikayetler").stream()
        for doc in docs:
            data = doc.to_dict()
            sikayet_tarihi = data.get("tarih")
            if sikayet_tarihi and sikayet_tarihi.tzinfo is None:
             sikayet_tarihi = sikayet_tarihi.replace(tzinfo=timezone.utc)

            if sikayet_tarihi and sikayet_tarihi > filtre_tarihi:
                print(f"- UID: {data.get('kullanici_uid')}")
                print(f"  Şikayet: {data.get('sikayet')}")
                print(f"  Tarih: {sikayet_tarihi}")
                print("")

    except Exception as e:
        print(f" Filtreleme sırasında hata oluştu: {e}")


#  Gelişmiş Kullanıcı Şikayet Listesi
def kullanici_sikayetlerini_detayli_listele(uid):
    """
    Belirli bir kullanıcıya ait tüm şikayetleri, detaylı bilgilerle birlikte listeler.
    """
    try:
        print(f" Kullanıcının detaylı şikayet listesi (UID: {uid})")

        docs = db.collection("sikayetler").where("kullanici_uid", "==", uid).stream()
        for doc in docs:
            data = doc.to_dict()
            print("──────────────────────────────")
            print(f" Şikayet: {data.get('sikayet', 'Belirsiz')}")
            print(f" Tarih: {data.get('tarih', 'Yok')}")
            print(f" Eksiler: {data.get('eksiler', 0)}")
            print(f" Kategori: {data.get('kategori', 'Tahmin edilmedi')}")
            print(f" Durum: {data.get('durum', 'Bilinmiyor')}")
        print(" Şikayetler başarıyla listelendi!")
    except Exception as e:
        print(f" Detaylı şikayet listelenemedi: {e}")


#  Eksilere göre şikayetleri sırala (önemli olan)
def sikayetleri_eksilere_gore_sirala():
    try:
        print(" Eksilere göre sıralanmış şikayetler:")
        docs = db.collection("sikayetler").order_by("eksiler", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            data = doc.to_dict()
            print(f" Eksiler: {data.get('eksiler', 0)}")
            print(f" Şikayet: {data.get('sikayet', 'Belirsiz')}")
            print("")
    except Exception as e:
        print(f" Sıralama sırasında hata oluştu: {e}")


#  Admin mi? Normal kullanıcı mı? Ona göre şikayetleri listele
def sikayetleri_listele_yetkiye_gore(uid):
    """
    Admin kullanıcı tüm şikayetleri görebilir,
    Normal kullanıcı sadece kendi şikayetlerini görebilir.
    """
    try:
        if kullanici_admin_mi(uid):
            print(" Admin tespit edildi. Tüm şikayetler listeleniyor...")
            sikayetleri_listele()  # Tüm şikayetleri listeler
        else:
            print(f" Normal kullanıcı. Sadece kendi şikayetleri listeleniyor... (UID: {uid})")
            kullanici_sikayetlerini_detayli_listele(uid)
    except Exception as e:
        print(f" Şikayet listeleme sırasında hata oluştu: {e}")


#  Sadece eksilere göre önem sıralaması yapan fonksiyon
def sikayetleri_onem_sirasina_gore_sirala():
    try:
        print(" Eksilere göre önem derecesine göre sıralanmış şikayetler:")
        docs = db.collection("sikayetler").order_by("eksiler", direction="DESCENDING").stream()

        for doc in docs:
            data = doc.to_dict()
            print(f" Eksiler: {data.get('eksiler')}")
            print(f" Şikayet: {data.get('sikayet')}")
            print("")
    except Exception as e:
        print(f" Önem sırasına göre sıralama sırasında hata oluştu: {e}")


#  Önem sırasına göre şikayetleri listele (sadece eksilere göre)
def onem_sirasina_gore_listele():
    try:
        print(" Önem derecesine göre sıralanmış şikayetler listeleniyor...")

        # Tüm şikayet belgelerini çek
        docs = db.collection("sikayetler").stream()

        # Her belge için önem skorunu hesapla (yalnızca eksilere göre)
        sikayet_listesi = []
        for doc in docs:
            data = doc.to_dict()
            eksiler = data.get("eksiler", 0)
            tarih = data.get("tarih")
            onem_skoru = eksiler * 3
            sikayet_listesi.append((onem_skoru, tarih, data))

        # Önce önem skoruna, sonra tarihe göre sırala
        sikayet_listesi.sort(key=lambda x: (-x[0], -x[1].timestamp() if x[1] else 0))

        # Listele
        for onem_skoru, tarih, data in sikayet_listesi:
            print(f"\n Önem Skoru: {onem_skoru}")
            print(f" Tarih: {tarih}")
            print(f" Şikayet: {data.get('sikayet')}")
            print(f" Eksiler: {data.get('eksiler')}")

        print("\n Sıralama tamamlandı.")

    except Exception as e:
        print(f" Önem sırasına göre listeleme hatası: {e}")

#  Belirli bir şikayet ID'sine göre Firestore'dan şikayeti sil
def sikayet_sil(sikayet_id):

    try:
        sikayet_ref = db.collection("sikayetler").document(sikayet_id)
        doc = sikayet_ref.get()

        if doc.exists:
            sikayet_ref.delete()
            print(f" Şikayet başarıyla silindi! (ID: {sikayet_id})")
        else:
            print(f" Şikayet bulunamadı. (ID: {sikayet_id})")
    except Exception as e:
        print(f" Şikayet silinirken hata oluştu: {e}")



#  Şikayet durumu güncelle
def sikayet_durumunu_guncelle(sikayet_id, yeni_durum):
    try:
        doc_ref = db.collection("sikayetler").document(sikayet_id)
        if doc_ref.get().exists:
            doc_ref.update({"durum": yeni_durum})
            print(f" Şikayet durumu güncellendi! (ID: {sikayet_id}, Yeni Durum: {yeni_durum})")
        else:
            print(f" Şikayet bulunamadı. (ID: {sikayet_id})")
    except Exception as e:
        print(f" Güncelleme hatası: {e}")


#  Belirli bir kategoriye ait tüm şikayetleri listele (sadece eksilere göre)
def kategoriye_gore_sikayetleri_listele(kategori):
    try:
        print(f" '{kategori}' kategorisine ait şikayetler listeleniyor...\n")
        docs = db.collection("sikayetler").where("kategori", "==", kategori).stream()
        
        bulundu = False
        for doc in docs:
            bulundu = True
            data = doc.to_dict()
            print(f" Şikayet: {data.get('sikayet')}")
            print(f" Kategori: {data.get('kategori')}")
            print(f" Tarih: {data.get('tarih')}")
            print(f" Eksiler: {data.get('eksiler')}")
            print("-" * 40)

        if not bulundu:
            print(f" '{kategori}' kategorisine ait hiçbir şikayet bulunamadı.")

    except Exception as e:
        print(f" Kategoriye göre listeleme sırasında hata oluştu: {e}")


# 🔍 Mevcut tüm kategorileri listele
def listele_kategoriler():
    try:
        print(" Mevcut kategoriler listeleniyor...\n")
        docs = db.collection("sikayetler").stream()
        kategoriler = set()

        for doc in docs:
            data = doc.to_dict()
            kategori = data.get("kategori")
            if kategori:
                kategoriler.add(kategori)

        if kategoriler:
            for kategori in sorted(kategoriler):
                print(f" {kategori}")
        else:
            print(" Henüz herhangi bir kategori bulunamadı.")

    except Exception as e:
        print(f" Kategori listeleme sırasında hata oluştu: {e}")


#  Şikayet metnine göre kategori tahmini yapar (NOVA'ya özel)
def sikayet_kategorisini_tahmin_et(sikayet_metni):
    """
    Şikayet metninde geçen anahtar kelimelere göre kategori tahmini yapar.
    Örn: 'salıncak kırık' → 'Park'
    """
    sikayet_metni = sikayet_metni.lower()

    kategoriler = {
        "Altyapı": ["elektrik", "su", "kesildi", "boru", "altyapı", "asfalt", "çukur", "patlak", "yol", "kanalizasyon"],
        "Aydınlatma": ["lamba", "aydınlatma", "karanlık", "sokak lambası", "ışık"],
        "Temizlik": ["çöp", "koku", "temizlik", "döküntü", "birikinti"],
        "Park": ["salıncak", "park", "oyun alanı", "kaydırak", "spor aleti"],
        "Sosyal Hizmet": ["yardım", "başvuru", "geri dönüş", "sosyal", "hizmet", "evrak"],
        "Güvenlik": ["kamera", "güvenlik", "tehdit", "kavga", "polis", "tehlike"]
    }

    for kategori, anahtarlar in kategoriler.items():
        for kelime in anahtarlar:
            if kelime in sikayet_metni:
                return kategori

    return "Diğer"


#  Kategoriye göre şikayetleri filtrele (sadece eksilerle)
def sikayetleri_kategoriye_gore_filtrele(kategori):
    """
    Belirtilen kategoriye ait şikayetleri listeler (eksiler baz alınır).
    """
    try:
        print(f" '{kategori}' kategorisindeki şikayetler listeleniyor...")
        docs = db.collection("sikayetler").where("kategori", "==", kategori).stream()
        bulundu = False

        for doc in docs:
            data = doc.to_dict()
            bulundu = True
            print("\n Şikayet:", data.get("sikayet"))
            print(" Tarih:", data.get("tarih"))
            print(" Eksiler:", data.get("eksiler"))

        if not bulundu:
            print(" Bu kategoriye ait şikayet bulunamadı.")
    except Exception as e:
        print(f" Kategoriye göre filtreleme hatası: {e}")
