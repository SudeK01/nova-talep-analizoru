import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
import numpy as np

#  1. Veriyi oku
df = pd.read_csv("../nova_finetune_final.csv")

#  2. Gerekli sütunları al
df = df[["metin", "onem_skoru"]].dropna()
df["labels"] = df["onem_skoru"].astype(float)  # Regresyon = float

#  3. Train-test böl
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

#  4. HuggingFace Dataset formatına çevir
train_dataset = Dataset.from_pandas(train_df[["metin", "labels"]])
val_dataset = Dataset.from_pandas(val_df[["metin", "labels"]])

#  5. Tokenizer yükle (lokal!)
model_path = "./model"
tokenizer = AutoTokenizer.from_pretrained(model_path)

#  6. Tokenize et
def tokenize_function(example):
    return tokenizer(example["metin"], truncation=True, padding="max_length", max_length=128)

train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

#  7. Modeli yükle (regresyon için!)
model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=1)

#  8. Eğitim ayarları
training_args = TrainingArguments(
    output_dir="./finetuned_model",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=10,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=1
)

#  9. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

#  10. Eğit
trainer.train()

#  11. Tahmin al
predictions = trainer.predict(val_dataset)
val_preds = [round(float(p[0]), 2) for p in predictions.predictions]

#  12. Tahminleri CSV olarak kaydet
val_df = val_df.copy()
val_df["tahmin_skoru"] = val_preds
val_df.to_csv("nova_finetune_sonuclar.csv", index=False)

print(" Fine-tuning ve tahmin tamamlandı. CSV kaydedildi.")
