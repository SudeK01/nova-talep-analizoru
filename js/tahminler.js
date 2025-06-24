import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {
  getFirestore, collection, getDocs
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyDbK46_HgV4QvWZgX4A82or66Y1Y2oJoOk",
  authDomain: "aivatandastalepanalizoru.firebaseapp.com",
  projectId: "aivatandastalepanalizoru",
  storageBucket: "aivatandastalepanalizoru.appspot.com",
  messagingSenderId: "328882761052",
  appId: "1:328882761052:web:8a66d9696e46b82caca599"
};

// Başlat
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

let tumVeriler = [];

// Badge oluştur
function rozetOlustur(skor) {
  let className = skor < 2 ? "badge-low" : skor < 3.2 ? "badge-mid" : "badge-high";
  let text = skor < 2 ? "Düşük Önem" : skor < 3.2 ? "Orta Önem" : "Yüksek Önem";
  return `<span class="badge ${className}">${text}</span>`;
}

// Verileri tabloya yaz
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

// Tahminleri çek
async function tahminleriYukle() {
  try {
    const snapshot = await getDocs(collection(db, "tahminler"));
    tumVeriler = [];
    snapshot.forEach(doc => {
      const data = doc.data();
       // Train ve finetune almaz
       if (data.source === "train" || data.source === "finetune") return;
       tumVeriler.push({
        metin: data.metin,
        skor: Number(data.skor)
      });
    });
    verileriGoster(tumVeriler);
  } catch (err) {
    console.error("Veri yüklenirken hata:", err);
  }
}

// Filtreleme
document.querySelectorAll(".filtre-btn").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".filtre-btn").forEach(btn => btn.classList.remove("aktif"));
    button.classList.add("aktif");

    const filtre = button.dataset.filtre;
    let filtreliVeri = [...tumVeriler];

    if (filtre === "low") filtreliVeri = tumVeriler.filter(v => v.skor < 2);
    else if (filtre === "mid") filtreliVeri = tumVeriler.filter(v => v.skor >= 2 && v.skor < 3.2);
    else if (filtre === "high") filtreliVeri = tumVeriler.filter(v => v.skor >= 3.2);

    verileriGoster(filtreliVeri);
  });
});

// Sıralama
document.getElementById("sirala-select").addEventListener("change", (e) => {
  const secim = e.target.value;
  let sirali = [...tumVeriler];

  if (secim === "artan") sirali.sort((a, b) => a.skor - b.skor);
  else if (secim === "azalan") sirali.sort((a, b) => b.skor - a.skor);

  verileriGoster(sirali);
});

// Çıkış
document.querySelector(".logout-btn")?.addEventListener("click", async () => {
  try {
    await signOut(auth);
    window.location.href = "../pages/index.html";
  } catch (err) {
    console.error("Çıkış hatası:", err);
  }
});

// İlk yükleme
tahminleriYukle();
