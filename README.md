# nova-talep-analizoru

NOVA, vatandaşlardan gelen şikayet metinlerini analiz ederek önem derecelerini tahmin etmeyi amaçlayan bir doğal dil işleme (NLP) projesidir. Türkçe dilinde önceden eğitilmiş bir model kullanılarak, metinlerin sınıflandırılması sağlanmıştır.

## Model Eğitimi

Model, Hugging Face üzerinde yayınlanmış olan [`dbmdz/bert-base-turkish-cased`](https://huggingface.co/dbmdz/bert-base-turkish-cased) adlı Türkçe BERT tabanlı dil modeli ile eğitilmiştir. Eğitim sürecinde `transformers` kütüphanesi ve `Trainer` sınıfı kullanılmıştır.

Eğitim, **regresyon problemi** olarak yapılandırılmış ve modelin çıkışı `num_labels=1` olarak belirlenmiştir.

## Kullanılan Algoritma

Transformer tabanlı derin öğrenme mimarisi kullanılmıştır. Model, cümleleri vektöre dönüştürüp, eksiler sayısını tahmin edecek şekilde eğitilmiştir. Klasik algoritmalar yerine doğrudan fine-tuning yöntemi uygulanmıştır.

## Flask Entegrasyonu

İlk başta tahminler Hugging Face API üzerinden alınıyordu. Ancak erişim limitleri ve güvenlik kısıtları nedeniyle tahmin sistemi tamamen yerel olarak çalışacak şekilde Flask ile yeniden yazıldı.

**Flask**, Python ile yazılmış hafif bir web framework’tür. Projemizde, eğitilen model Flask üzerinden bir REST API olarak sunulmuş, şikayet geldiğinde anında tahmin yapılması sağlanmıştır.

## Ngrok Desteği

Yerel Flask sunucusunu dış dünyaya açmak için **ngrok** aracı kullanılmıştır. Böylece localhost üzerinde çalışan sistem, geçici bir genel HTTPS adresi üzerinden test edilmiştir.

## Model Performansı (F1-Score)

| Skor | Precision | Recall | F1-Score | Support |
|------|-----------|--------|----------|---------|
| 0    | 0.00      | 0.00   | 0.00     | 2       |
| 1    | 0.17      | 0.33   | 0.22     | 3       |
| 2    | 0.25      | 0.20   | 0.22     | 10      |
| 3    | 0.14      | 0.17   | 0.15     | 6       |
| 4    | 0.25      | 0.50   | 0.33     | 4       |

> Not: Veri dengesizliği, düşük performansa yol açmıştır. Bu nedenle gelecekte daha dengeli bir veri setiyle yeniden eğitim yapılması planlanmaktadır.
