from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = Flask(__name__)

# MODEL YOLU
MODEL_PATH = "model"


# Cihaz kontrolü
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model ve tokenizer'ı yükle
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

@app.route("/api/tahmin-yap", methods=["POST"])
def tahmin_yap():
    try:
        data = request.json
        text = data.get("metin", "")
        if not text:
            return jsonify({"hata": "Metin eksik!"}), 400

        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            skor = outputs.logits.squeeze().item()

        return jsonify({"tahmin": round(skor, 2)})
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
