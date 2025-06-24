
from firebase.firebase_auth import onem_sirasina_gore_listele

#  Önem sırasına göre sıralamayı test et
def test_onem_sirasina_gore_listele():
    print(" Test: Önem sırasına göre şikayet sıralaması")
    onem_sirasina_gore_listele()

# Testi çalıştırmak için
if __name__ == "__main__":
    test_onem_sirasina_gore_listele()




from firebase.firebase_auth import sikayet_kategorisini_tahmin_et

# 🔍 Kategori tahmini test fonksiyonu
def test_sikayet_kategorisini_tahmin_et():
    print("Test: Şikayet Kategorisi Tahmini\n")

    test_sikayetler = [
        "3 gündür elektrik kesildi, hâlâ çözüm yok.",
        "Suyumuz bugün sabahtan beri yok.",
        "Çöp kutuları günlerdir alınmadı.",
        "Yol bozuk, araçlar geçemiyor.",
        "Işıklandırma çalışmıyor, akşam çok karanlık oluyor.",
        "Parkta temizlik yapılmamış.",
        "Elektrik kesildi ama ekip çok hızlı müdahale etti, teşekkür ederiz."
    ]

    for sikayet in test_sikayetler:
        kategori = sikayet_kategorisini_tahmin_et(sikayet)
        print(f"Şikayet: {sikayet}")
        print(f"Tahmin Edilen Kategori: {kategori}\n")

# Testi çalıştırmak için
if __name__ == "__main__":
    test_sikayet_kategorisini_tahmin_et()


from firebase.firebase_auth import sikayetleri_kategoriye_gore_filtrele

def test_kategoriye_gore_filtrele():
    print("Test: Kategoriye göre filtreleme")
    sikayetleri_kategoriye_gore_filtrele("Elektrik")  # Deneme için "Elektrik" yazdık
