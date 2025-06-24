import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

# CSV dosyasını oku
df = pd.read_csv("nova_autotrain_ready.csv")

# Gerekli sütunları filtrele ve boş değerleri çıkar
df = df[["metin", "eksiler"]].dropna()
df["eksiler"] = df["eksiler"].astype(float)

# Hugging Face Dataset'e dönüştürmeden önce labels ismini verelim
df = df.rename(columns={"eksiler": "labels"})

# Hugging Face Dataset'e dönüştür
hf_dataset = Dataset.from_pandas(df)

# Tokenizer'ı yükle
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")

# Veriyi tokenize et
def tokenize_function(example):
    return tokenizer(example["metin"], truncation=True, padding="max_length")

# Dataseti tokenize et
tokenized_dataset = hf_dataset.map(tokenize_function, batched=True)

# Kontrol için ilk örneği yazdır
print(tokenized_dataset[0])

# Veriyi eğitim ve doğrulama olarak ayır
train_test = tokenized_dataset.train_test_split(test_size=0.2, seed=42)
train_dataset = train_test["train"]
val_dataset = train_test["test"]

print("Train örneği:", train_dataset[0])
print("Validation örneği:", val_dataset[0])

from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

# Modeli yükle (regresyon için tek çıkış!)
model = AutoModelForSequenceClassification.from_pretrained(
    "dbmdz/bert-base-turkish-cased",
    num_labels=1  # regresyon = 1 etiket
)

# Eğitim ayarları
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="no",  # model kaydetmiyoruz
)

# Trainer nesnesi
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()

# YENİ EKLENEN KISIM: Trainer ile regresyon tahmini // pipeline ı çıkarttık 

# Validation set üzerinden tahminleri al
raw_pred = trainer.predict(val_dataset)

# Tahmin skorlarını yaz
df_val = df.tail(len(val_dataset)).copy()  # sadece validation verisini alıyoruz
df_val["tahmin_skoru"] = [round(float(p), 2) for p in raw_pred.predictions]

# Kaydet
df_val.to_csv("nova_tahminli_sonuclar.csv", index=False)
print("CSV dosyası başarıyla oluşturuldu!")
print("\nİlk 5 tahmin sonucu:")
print(df_val[["metin", "tahmin_skoru"]].head())
