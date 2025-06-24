import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from firebase.firebase_setup import db
from firebase_admin import firestore
from firebase.firebase_auth import sikayet_analizi_yap
from firebase.firebase_tahmin_kaydet import tahmin_kaydet, tahmin_modeli_ile_skor_hesapla  

print("BU DOSYA ÇALIŞTI: backend_api.py")



app = Flask(__name__)
CORS(app)

@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"message": "API çalışıyor!"})


@app.route('/api/sikayet-ekle', methods=['POST'])
def sikayet_ekle():
    data = request.get_json()
    uid = data.get('uid')
    sikayet_metni = data.get('sikayet')

    if not uid or not sikayet_metni:
        return jsonify({"error": "Eksik veri"}), 400

    #  Şikayet analizini yap (sadece eksiler önemli)
    _, eksiler = sikayet_analizi_yap(sikayet_metni)

    #  Firestore'a kaydet
    db.collection("sikayetler").add({
        "uid": uid,
        "sikayet": sikayet_metni,
        "eksiler": eksiler,
        "tarih": firestore.SERVER_TIMESTAMP
    })

    return jsonify({
        "message": "Şikayet alındı",
        "uid": uid,
        "sikayet": sikayet_metni,
        "eksiler": eksiler
    })


@app.route('/api/sikayetleri-getir', methods=['GET'])
def sikayetleri_getir():
    sikayetler_ref = db.collection("sikayetler").order_by("tarih", direction=firestore.Query.DESCENDING)
    docs = sikayetler_ref.stream()

    sikayet_listesi = []
    for doc in docs:
        data = doc.to_dict()
        sikayet_listesi.append({
            "uid": data.get("uid"),
            "sikayet": data.get("sikayet"),
            "eksiler": data.get("eksiler", 0),
            "tarih": data.get("tarih").isoformat() if data.get("tarih") else None
        })

    return jsonify(sikayet_listesi)


@app.route('/api/sikayetleri-tarihe-gore', methods=['GET'])
def sikayetleri_tarihe_gore_getir():
    try:
        sikayetler_ref = db.collection("sikayetler").order_by("tarih", direction=firestore.Query.DESCENDING)
        docs = sikayetler_ref.stream()
        sikayet_listesi = []

        for doc in docs:
            veri = doc.to_dict()
            veri["id"] = doc.id
            if "tarih" in veri and hasattr(veri["tarih"], "isoformat"):
                veri["tarih"] = veri["tarih"].isoformat()
            sikayet_listesi.append(veri)

        return jsonify(sikayet_listesi), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/sikayetleri-eksilere-gore', methods=['GET'])
def sikayetleri_eksilere_gore():
    try:
        sikayetler_ref = db.collection('sikayetler')
        sikayetler = sikayetler_ref.order_by('eksiler', direction="DESCENDING").stream()

        sikayet_listesi = []
        for doc in sikayetler:
            veri = doc.to_dict()
            veri['id'] = doc.id
            sikayet_listesi.append(veri)

        return jsonify(sikayet_listesi)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/sikayetleri-onem-sirasina-gore', methods=['GET'])
def sikayetleri_onem_sirasina_gore():
    try:
        sikayetler_ref = db.collection('sikayetler')
        sikayetler = sikayetler_ref.stream()

        sikayet_listesi = []
        for doc in sikayetler:
            veri = doc.to_dict()
            veri['id'] = doc.id

            # Eksilere dayalı önem skoru
            eksiler = veri.get('eksiler', 0)
            onem_skoru = eksiler * 3
            veri['onem_skoru'] = onem_skoru
            sikayet_listesi.append(veri)

        # Skora göre sırala
        sikayet_listesi.sort(key=lambda x: x['onem_skoru'], reverse=True)

        return jsonify(sikayet_listesi)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/tahmin-kaydet", methods=["POST"])
def tahmin_kaydet_api():
    try:
        veri = request.get_json()
        uid = veri.get("uid")
        metin = veri.get("metin")
        skor = veri.get("skor")

        if not uid or not metin or skor is None:
            return jsonify({"hata": "Eksik veri"}), 400

        tahmin_kaydet(uid, metin, skor)
        return jsonify({"mesaj": "Tahmin başarıyla kaydedildi"}), 200

    except Exception as e:
        return jsonify({"hata": str(e)}), 500


@app.route("/api/tahminleri-getir", methods=["GET"])
def tahminleri_getir():
    try:
        tahminler_ref = db.collection("tahminler")
        docs = tahminler_ref.stream()

        liste = []
        for doc in docs:
            veri = doc.to_dict()
            veri["id"] = doc.id
            liste.append(veri)

        return jsonify(liste), 200
    except Exception as e:
        return jsonify({"hata": str(e)}), 500


@app.route("/tahminler", methods=["GET"])
def tahminler_sayfasi():
    try:
        tahminler_ref = db.collection("tahminler")
        docs = tahminler_ref.order_by("skor", direction=firestore.Query.DESCENDING).stream()


        tahmin_listesi = []
        for doc in docs:
            veri = doc.to_dict()
            veri["id"] = doc.id
            tahmin_listesi.append(veri)

        return render_template("tahminler.html", tahminler=tahmin_listesi)

    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500
    

@app.route("/api/tahmin-yap", methods=["POST"])
def tahmin_yap():
    try:
        veri = request.get_json()
        metin = veri.get("metin")
        uid = veri.get("uid")  

        if not metin:
            return jsonify({"hata": "Metin eksik"}), 400

        skor = tahmin_modeli_ile_skor_hesapla(metin)
        tahmin_kaydet(uid, metin, skor)  

        return jsonify({"tahmin": skor})
    except Exception as e:
        return jsonify({"hata": str(e)}), 500



print(app.url_map)


import threading
print("Aktif thread ismi:", threading.current_thread().name)


if __name__ == "__main__":

    print(" Flask app.run çağrılmak üzere")

    app.run(debug=False, port=5000, use_reloader=False)



