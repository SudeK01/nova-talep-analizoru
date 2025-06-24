//  Firebase modüllerini ekliyoruz
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

//  Firebase Yapılandırması
const firebaseConfig = {
    apiKey: "AIzaSyDbK46_HgV4QvWZgX4A82or66Y1Y2oJoOk",
    authDomain: "aivatandastalepanalizoru.firebaseapp.com",
    projectId: "aivatandastalepanalizoru",
    storageBucket: "aivatandastalepanalizoru.appspot.com",
    messagingSenderId: "328882761052",
    appId: "1:328882761052:web:8a66d9696e46b82caca599"
};

//  Firebase Başlat
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

//  Admin e-mail adresi ve şifresi 
const ADMIN_EMAIL = "sudekucukbekir@hotmail.com";
const ADMIN_PASSWORD = "admin1234"; 

//  Admin Login Formu
const adminLoginForm = document.getElementById("admin-login-form");

adminLoginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("admin-email").value.trim();
    const password = document.getElementById("admin-password").value;

    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        if (user.email === ADMIN_EMAIL) {
            console.log("✅ Admin girişi başarılı!");
            window.location.href = "../pages/admin_panel.html"; // Admin paneline yönlendir
        } else {
            alert(" Hatalı admin bilgileri!");
            auth.signOut();
        }
    } catch (error) {
        console.error(" Admin giriş hatası:", error);
        alert("Bir hata oluştu. Lütfen bilgilerinizi kontrol edin.");
    }
});
