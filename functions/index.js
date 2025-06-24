const { onDocumentDeleted, onDocumentCreated } = require("firebase-functions/v2/firestore");
const { setGlobalOptions } = require("firebase-functions/v2");
const admin = require("firebase-admin");
const axios = require("axios");

// Firebase Admin başlat
admin.initializeApp();
const db = admin.firestore();

// Global ayarları set et (timeout, bellek vs.)
setGlobalOptions({ region: "us-central1" });


const HF_API_URL = "https://us-central1-aivatandastalepanalizoru.cloudfunctions.net/sikayetEklendigindeTahminYap";




//  Şikayet silinince tahmini de sil
exports.sikayetSilindigindeTahminiSil = onDocumentDeleted(
  "sikayetler/{sikayetId}",
  async (event) => {
    const sikayetId = event.params.sikayetId;
    try {
      const snapshot = await db
        .collection("tahminler")
        .where("uid", "==", sikayetId)
        .get();

      const silmeIslemleri = [];
      snapshot.forEach((doc) => silmeIslemleri.push(doc.ref.delete()));
      await Promise.all(silmeIslemleri);

      console.log(`Tahmin(ler) silindi: ${sikayetId}`);
    } catch (error) {
      console.error("Tahmin silme hatası:", error);
    }
  }
);

//  Şikayet eklenince otomatik tahmin yap
exports.sikayetEklendigindeTahminYap = onDocumentCreated(
  "sikayetler/{sikayetId}",
  async (event) => {
    const sikayetId = event.params.sikayetId;
    const snapshot = event.data;
    const veriler = snapshot.data();
    const metin = veriler ? (veriler.metin || veriler.aciklama || "") : "";


      console.log(" Snapshot data:", veriler); //debug için
      console.log(" Gönderilen metin:", metin); //debug için

    try {
      const cevap = await axios.post("https://d188-176-88-39-33.ngrok-free.app/api/tahmin-yap", { metin });  // ngrok güncellenmeli her seferinde !!

      const skor = cevap.data.tahmin;

      await db.collection("tahminler").add({
        uid: sikayetId,
        metin: metin,
        skor: skor,
        tarih: new Date().toISOString()
      });

      console.log(`✅ Tahmin başarıyla kaydedildi: ${skor}`);
    } catch (error) {
      console.error(" Tahmin oluşturma hatası:", error.message);
    }
  }
);

