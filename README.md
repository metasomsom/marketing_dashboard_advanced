# 📊 Meta Ads Dashboard

Meta Ads Dashboard adalah aplikasi berbasis Streamlit untuk menampilkan performa iklan dari Facebook Ads dan membantu membuat copywriting iklan dengan OpenAI.

---

## 🚀 Fitur Utama

* Menampilkan metrik per kampanye iklan:

  * Total Spend
  * Average CTR
  * Average ROAS
* Visualisasi CTR dan ROAS per iklan
* Download laporan Excel
* Generator teks iklan otomatis menggunakan GPT-4

---

## 🛠 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/meta-ads-dashboard.git
cd meta-ads-dashboard
```

### 2. Buat dan isi file `.env`

```
FB_APP_ID=your_facebook_app_id
FB_APP_SECRET=your_facebook_app_secret
FB_ACCESS_TOKEN=your_facebook_access_token
AD_ACCOUNT_ID=act_1234567890
OPENAI_API_KEY=your_openai_api_key
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi

```bash
streamlit run dashboard.py
```

---

## 📦 Deployment

### a. **Streamlit Cloud**

1. Upload semua file ke GitHub repo.
2. Login ke [https://share.streamlit.io](https://share.streamlit.io)
3. Deploy dengan repo tersebut.
4. Tambahkan secrets di dashboard:

   * `FB_APP_ID`, `FB_APP_SECRET`, `FB_ACCESS_TOKEN`, `AD_ACCOUNT_ID`, `OPENAI_API_KEY`

### b. **Docker**

#### 1. Buat image

```bash
docker build -t meta-ads-dashboard .
```

#### 2. Jalankan container

```bash
docker run -p 8501:8501 --env-file .env meta-ads-dashboard
```

---

## 📁 Struktur Proyek

```
├── dashboard.py
├── meta_api.py
├── utils.py
├── .env
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚠️ Catatan Keamanan

* Jangan commit file `.env`
* Pastikan token dan API key disimpan di environment variable saat produksi

---

## 📧 Kontak

Untuk pertanyaan dan bantuan, hubungi: [you@example.com](mailto:you@example.com)
