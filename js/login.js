//  Firebase modüllerini import et
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {
  getFirestore, collection, getDocs
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import {
  getAuth, signOut
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// 🔧 Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyDbK46_HgV4QvWZgX4A82or66Y1Y2oJoOk",
  authDomain: "aivatandastalepanalizoru.firebaseapp.com",
  projectId: "aivatandastalepanalizoru",
  storageBucket: "aivatandastalepanalizoru.appspot.com",
  messagingSenderId: "328882761052",
  appId: "1:328882761052:web:8a66d9696e46b82caca599"
};

//  Firebase'i başlat
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

let tumVeriler = [];

//  Skor değerine göre rozet oluştur
function rozetOlustur(skor) {
  let className = "";
  let text = "";

  if (skor < 3) {
    className = "badge-low";
    text = "Düşük Önem";
  } else if (skor < 6) {
    className = "badge-mid";
    text = "Orta Önem";
  } else {
    className = "badge-high";
    text = "Yüksek Önem";
  }

  return `<span class="badge ${className}">${text}</span>`;
}

//  Tabloya verileri yaz
function verileriGoster(veriler) {
  const govde = document.getElementById("tahmin-tablosu-govde");
  govde.innerHTML = "";

  veriler.forEach((veri, index) => {
    const satir = document.createElement("tr");
    satir.innerHTML = `
      <td>${index + 1}</td>
      <td>${veri.metin}</td>
      <td>${rozetOlustur(veri.skor)}</td>
      <td>${veri.skor.toFixed(2)}</td>
    `;
    govde.appendChild(satir);
  });
}

//  Firebase'den tahmin verilerini al
async function tahminleriYukle() {
  const tahminRef = collection(db, "tahminler");
  const snapshot = await getDocs(tahminRef);

  tumVeriler = [];

  snapshot.forEach(doc => {
    const data = doc.data();
    tumVeriler.push({
      metin: data.metin,
      skor: Number(data.skor)
    });
  });

  verileriGoster(tumVeriler);
}

//  Filtreleme işlemi
document.querySelectorAll(".filtre-btn").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".filtre-btn").forEach(btn => btn.classList.remove("aktif"));
    button.classList.add("aktif");

    const filtre = button.dataset.filtre;
    let filtreliVeri = [];

    switch (filtre) {
      case "low":
        filtreliVeri = tumVeriler.filter(v => v.skor < 3);
        break;
      case "mid":
        filtreliVeri = tumVeriler.filter(v => v.skor >= 3 && v.skor < 6);
        break;
      case "high":
        filtreliVeri = tumVeriler.filter(v => v.skor >= 6);
        break;
      default:
        filtreliVeri = [...tumVeriler];
    }

    verileriGoster(filtreliVeri);
  });
});

//  Sıralama işlemi
document.getElementById("sirala-select").addEventListener("change", (e) => {
  const secim = e.target.value;
  let sirali = [...tumVeriler];

  if (secim === "artan") {
    sirali.sort((a, b) => a.skor - b.skor);
  } else if (secim === "azalan") {
    sirali.sort((a, b) => b.skor - a.skor);
  }

  verileriGoster(sirali);
});

//  Çıkış işlemi
const logoutBtn = document.querySelector(".logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    try {
      await signOut(auth);
      window.location.href = "../index.html";
    } catch (error) {
      console.error("Çıkış hatası:", error);
      alert("Çıkış yapılamadı!");
    }
  });
}

//  Sayfa yüklenince verileri getir
tahminleriYukle();
