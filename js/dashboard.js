//  Firebase modüllerini içe aktar
import { getFirestore, collection, addDoc, serverTimestamp, getDocs, query, where, orderBy } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

//  Firebase config ayarı
const firebaseConfig = {
  apiKey: "AIzaSyDbK46_HgV4QvWZgX4A82or66Y1Y2oJoOk",
  authDomain: "aivatandastalepanalizoru.firebaseapp.com",
  projectId: "aivatandastalepanalizoru",
  storageBucket: "aivatandastalepanalizoru.appspot.com",
  messagingSenderId: "328882761052",
  appId: "1:328882761052:web:8a66d9696e46b82caca599",
  measurementId: "G-JFCGHV7SNZ"
};

//  Firebase başlat
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

//  Kullanıcı oturum kontrolü
onAuthStateChanged(auth, (user) => {
  if (user) {
    const adSoyad = user.displayName || user.email;
    document.querySelector(".dashboard-header h1").textContent = `Hoşgeldiniz, ${adSoyad.toUpperCase()}!`;

    sikayetleriListele();
  } else {
    window.location.href = "../pages/index.html";
  }
});

//  Çıkış yapma işlemi
document.querySelector(".logout-btn").addEventListener("click", () => {
  signOut(auth).then(() => {
    window.location.href = "../pages/index.html";
  });
});

const tarihSec = document.getElementById("tarihSirala");
const kategoriSec = document.getElementById("kategori-sec");

tarihSec.addEventListener("change", sikayetleriListele);
kategoriSec.addEventListener("change", sikayetleriListele);

// Talep listeleme
async function sikayetleriListele() {
  const user = auth.currentUser;
  if (!user) return;

  const kategoriSec = document.getElementById("kategori-sec");
  const tarihSirala = document.getElementById("tarihSirala");
  const kategori = kategoriSec?.value || "hepsi";
  const tarihSirasi = tarihSirala?.value || "desc";

  let q = query(collection(db, "sikayetler"), where("uid", "==", user.uid));

  if (kategori !== "hepsi") {
    q = query(q, where("kategori", "==", kategori));
  }

  if (tarihSirasi === "desc") {
    q = query(q, where("uid", "==", user.uid), orderBy("tarih", "desc"));
  } else {
    q = query(q, where("uid", "==", user.uid), orderBy("tarih", "asc"));
  }

  const snapshot = await getDocs(q);
  const container = document.getElementById("talep-container");
  container.innerHTML = "";

  snapshot.forEach((doc) => {
    const veri = doc.data();
    const li = document.createElement("li");
    li.classList.add("talep-kart");

    li.innerHTML = `
      <div class="talep-ust">
        <strong>${veri.metin || veri.aciklama || "Açıklama Yok"}</strong>
        <span class="rozet ${veri.durum === 'Sıraya Alındı' ? 'siraya-alindi' : veri.durum === 'Çalışmalara Başlandı' ? 'calisma-basladi' : veri.durum === 'Çözüm Üretildi' ? 'cozum-uretildi' : ''}">
          ${veri.durum || "Sıraya Alındı"}
        </span>
      </div>
      <div class="talep-alt">
        <span class="tarih">${veri.tarih ? formatTarih(veri.tarih) : "Tarih Yok"}</span>
      </div>
    `;

    container.appendChild(li);
  });
}

//  Tarih formatlama
function formatTarih(timestamp) {
  const tarih = timestamp.toDate();
  const aylar = [
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
  ];

  const gun = tarih.getDate();
  const ay = aylar[tarih.getMonth()];
  const yil = tarih.getFullYear();

  return `${gun} ${ay} ${yil}`;
}
