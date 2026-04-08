# 🫧 BIST Balonları

**Borsa İstanbul hisselerini cryptobubbles.net tarzında canlı balon görselleştirmesiyle takip et.**

[![Demo](https://img.shields.io/badge/Demo-GitHub%20Pages-blue)](https://YOUR_USERNAME.github.io/bist-bubbles)

---

## 🚀 Kurulum (5 Dakika)

### 1. Repoyu Fork / Clone Et

```bash
git clone https://github.com/YOUR_USERNAME/bist-bubbles.git
cd bist-bubbles
```

### 2. Vercel'e API Deploy Et

```bash
# Vercel CLI yoksa yükle
npm i -g vercel

# Deploy et (proje kökünde)
vercel deploy --prod
```

> Vercel sana bir URL verir: `https://bist-bubbles-xyz.vercel.app`

### 3. GitHub Pages'i Aktif Et

GitHub → Settings → Pages → **Source: `docs/` klasörü**

Site yayına girer: `https://YOUR_USERNAME.github.io/bist-bubbles`

### 4. API URL'ini Ayarla

Sitede sağ üstteki **⚙** butonuna tıkla →  
Vercel URL'ini gir → **Kaydet**

---

## 🗂 Proje Yapısı

```
bist-bubbles/
├── docs/              ← GitHub Pages (frontend)
│   └── index.html
├── api/               ← Vercel (Python proxy)
│   ├── main.py
│   └── requirements.txt
├── vercel.json
└── README.md
```

---

## 🧩 Özellikler

| Özellik | Detay |
|---------|-------|
| 📊 60+ Hisse | BIST100'ün büyük hisseleri |
| 🎨 Balon Boyutu | Piyasa değerine göre |
| 🟢🔴 Renk | % değişime göre (koyu yeşil → koyu kırmızı) |
| ⏱ Periyotlar | 1G · 1H · 1A · 3A · YBB |
| 🖱 Hover | Fiyat, hacim, piyasa değeri, 52H aralık |
| 🔗 Click | Yahoo Finance sayfasına git |
| 🔄 Otomatik | Her yenileme butonu ile güncel veri |

---

## ⚙️ Yerel Geliştirme

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend'de `localStorage`'a `http://localhost:8000` yaz.

---

## 📡 Veri Kaynağı

Yahoo Finance API (`query1.finance.yahoo.com`) — BIST hisseleri `.IS` suffix ile.

---

## 📄 Lisans

MIT
