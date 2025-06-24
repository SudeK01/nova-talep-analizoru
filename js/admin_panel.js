//  Firebase modüllerini içe aktar
import { getFirestore, collection, getDocs, doc, updateDoc, deleteDoc, query, where, orderBy } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

//  Firebase Yapılandırması
const firebaseConfig = {
  apiKey: "AIzaSyDbK46_HgV4QvWZgX4A82or66Y1Y2oJoOk",
  authDomain: "aivatandastalepanalizoru.firebaseapp.com",
  projectId: "aivatandastalepanalizoru",
  storageBucket: "aivatandastalepanalizoru.appspot.com",
  messagingSenderId: "328882761052",
  appId: "1:328882761052:web:8a66d9696e46b82caca599",
};


const tarihSiralaAdmin = document.getElementById("tarihSiralaAdmin");
const kategoriSecAdmin = document.getElementById("kategoriSecAdmin");
const onemSiralaAdmin = document.getElementById("onemSiralaAdmin");
const durumSecAdmin = document.getElementById("durumSecAdmin");


//  Firebase Başlat
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);


tarihSiralaAdmin.addEventListener("change", adminSikayetleriListele);
kategoriSecAdmin.addEventListener("change", adminSikayetleriListele);
onemSiralaAdmin.addEventListener("change", adminSikayetleriListele);
durumSecAdmin.addEventListener("change", adminSikayetleriListele);


//  Admin Panelde Şikayetleri Filtrele ve Listele
async function adminSikayetleriListele() {
 
  const tarihSirasi = tarihSiralaAdmin.value;
  const kategori = kategoriSecAdmin.value;
  const onemSirasi = onemSiralaAdmin.value;
  const secilenDurum = durumSecAdmin.value;

  try {
    const sikayetRef = collection(db, "sikayetler");
    let filtreler = [];

    //  Filtre 1: Kategori
    if (kategori !== "hepsi") {
      filtreler.push(where("kategori", "==", kategori));
    }

    //  Filtre 2: Durum
    if (secilenDurum !== "hepsi") {
      filtreler.push(where("durum", "==", secilenDurum));
    }

    //  Tarih sıralaması
    filtreler.push(orderBy("tarih", tarihSirasi));

    //  Sorguyu birleştir
    const q = query(sikayetRef, ...filtreler);
    const snapshot = await getDocs(q);

    //  Önem sıralaması (veri geldikten sonra yapılır)
  let sikayetler = [];
  snapshot.forEach((docSnap) => {
    const veri = docSnap.data();
    veri.docId = docSnap.id;
    sikayetler.push(veri);
  });

  if (onemSirasi === "onemli") {
    sikayetler.sort((a, b) => {
      const skorA = (a.eksiler || 0) * 3;
      const skorB = (b.eksiler || 0) * 3;
      return skorB - skorA;
    });
  } else if (onemSirasi === "onemsiz") {
    sikayetler.sort((a, b) => {
      const skorA = (a.eksiler || 0) * 3;
      const skorB = (b.eksiler || 0) * 3;
      return skorA - skorB;
    });
 }

 
    //  HTML'e yaz
    const tbody = document.getElementById("admin-talep-listesi");
    tbody.innerHTML = "";

    sikayetler.forEach((veri) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${veri.uid || "-"}</td>
        <td>${veri.ad || "-"}</td>
        <td>${veri.kategori || "-"}</td>
        <td>${veri.aciklama || veri.metin || "-"}</td>
        <td>${veri.tarih ? formatTarih(veri.tarih.toDate()) : "-"}</td>
        <td>${veri.durum ? rozetOlustur(veri.durum) : "-"}</td>
        <td>
          <div class="durum-butonlari">
            <button class="durum-btn" data-id="${veri.docId}" data-durum="Sıraya Alındı">Sıraya Alındı</button>
            <button class="durum-btn" data-id="${veri.docId}" data-durum="Çalışmalara Başlandı">Çalışmalara Başlandı</button>
            <button class="durum-btn" data-id="${veri.docId}" data-durum="Çözüm Üretildi">Çözüm Üretildi</button>
            <button class="sil-btn" data-id="${veri.docId}">🗑️ Sil</button>
          </div>
        </td>
      `;
      tbody.appendChild(tr);
    });

    durumButonlariniAyarla();
    silButonlariniAyarla();

    console.log(" Tüm filtrelere göre listeleme başarılı!");
  } catch (error) {
    console.error(" Listeleme hatası:", error);
  }
}


function formatTarih(date) {
  const gun = date.getDate().toString().padStart(2, "0");
  const ay = (date.getMonth() + 1).toString().padStart(2, "0");
  const yil = date.getFullYear();
  return `${gun}.${ay}.${yil}`;
}

function durumButonlariniAyarla() {
  const butonlar = document.querySelectorAll(".durum-btn");
  butonlar.forEach((button) => {
    button.addEventListener("click", async (e) => {
      const yeniDurum = e.target.getAttribute("data-durum");
      const docId = e.target.getAttribute("data-id");

      const onay = confirm(`Durumu '${yeniDurum}' yapmak istiyor musunuz?`);
      if (!onay) return;

      try {
        const talepDoc = doc(db, "sikayetler", docId);
        await updateDoc(talepDoc, { durum: yeniDurum });
        alert(" Durum güncellendi!");
        adminSikayetleriListele();
      } catch (e) {
        console.error(" Durum güncellenemedi:", e);
        alert("Hata oluştu.");
      }
    });
  });
}

function silButonlariniAyarla() {
  const silButonlari = document.querySelectorAll(".sil-btn");

  silButonlari.forEach((button) => {
    button.addEventListener("click", async (e) => {
      const docId = e.target.getAttribute("data-id");
      const onay = confirm("Şikayeti silmek istiyor musunuz?");
      if (!onay) return;

      try {
        await deleteDoc(doc(db, "sikayetler", docId));
        alert(" Şikayet silindi!");
        adminSikayetleriListele();
      } catch (e) {
        console.error(" Silme hatası:", e);
        alert("Hata oluştu.");
      }
    });
  });
}

function rozetOlustur(durum) {
  let className = "";
  switch (durum) {
    case "Sıraya Alındı":
      className = "badge-siraya-alindi";
      break;
    case "Çalışmalara Başlandı":
      className = "badge-calisma-basladi";
      break;
    case "Çözüm Üretildi":
      className = "badge-cozum-uretildi";
      break;
    default:
      className = "";
  }
  return `<span class="badge ${className}">${durum}</span>`;
}

document.addEventListener("DOMContentLoaded", () => {
  adminSikayetleriListele();
  const auth = getAuth();
  const logoutButton = document.querySelector(".logout-btn");

  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      signOut(auth)
        .then(() => {
          window.location.href = "index.html";
        })
        .catch((error) => {
          console.error("Çıkış hatası:", error);
          alert("Çıkış sırasında hata oluştu.");
        });
    });
  } else {
    console.error("Çıkış butonu bulunamadı.");
  }
});
