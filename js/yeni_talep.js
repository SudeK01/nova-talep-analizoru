//  Firebase modüllerini içe aktar
import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";

//  Firebase config ayarı
const firebaseConfig = {
  apiKey: "AIzaSyDbK46_HgV4QvWZgX4A82or66Y1Y2oJoOk",
  authDomain: "aivatandastalepanalizoru.firebaseapp.com",
  projectId: "aivatandastalepanalizoru",
  storageBucket: "aivatandastalepanalizoru.appspot.com", 
  messagingSenderId: "328882761052",
  appId: "1:328882761052:web:8a66d9696e46b82caca599",
};

//  Firebase başlat
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

//  Formu gönderme işlemi
const form = document.getElementById("talep-form");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const kategori = document.getElementById("kategori").value;
  const aciklama = document.getElementById("aciklama").value.trim();
  const user = auth.currentUser;

  if (!user) {
    alert("Lütfen tekrar giriş yapınız.");
    window.location.href = "../pages/index.html"; //  Giriş yoksa ana sayfaya yönlendir
    return;
  }

  if (!aciklama) {
    alert("Açıklama kısmı boş bırakılamaz.");
    return;
  }

  try {
    await addDoc(collection(db, "sikayetler"), {
      uid: user.uid,
      ad: user.displayName || user.email,
      kategori: kategori,
      aciklama: aciklama,
      tarih: serverTimestamp(),
      durum: "Sıraya Alındı"
    });

    // Toast gösterimi için küçük geliştirme ekliyorum
    const toast = document.getElementById("toast");
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
      window.location.href = "../pages/dashboard.html"; //  Talep sonrası dashboard'a dön
    }, 2000);
    
    form.reset(); //  Formu sıfırla
  } catch (e) {
    console.error(" Hata oluştu:", e);
    alert("Bir hata oluştu, lütfen tekrar deneyin.");
  }
});
