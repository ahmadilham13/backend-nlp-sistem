# Adaptive Early Warning System (EWS) - Backend Engine

Repository ini merupakan *backend engine* untuk sistem *Adaptive Early Warning System* (EWS) mahasiswa berbasis **Explainable Machine Learning (XAI)** dan **Natural Language Processing (NLP)**. Sistem ini berfungsi untuk memprediksi risiko akademik mahasiswa serta memberikan penalaran intervensi secara otomatis.

## 🚀 Tech Stack

- **Core Framework:** Python 3.12+ (FastAPI)
- **Database:** PostgreSQL
- **ORM & Migrations:** SQLAlchemy & Alembic
- **AI & NLP Ecosystem:** Google AI Studio (Gemini Pro API), Ollama (Local LLM: Llama 3 / Gemma), Sastrawi (NLP Stemmer)

## 📁 Struktur Proyek

```text
server/
├── alembic/            # Folder konfigurasi & riwayat migrasi database
├── venv/               # Virtual environment Python (diabaikan oleh git)
├── database.py         # Konfigurasi koneksi PostgreSQL & Session SQLAlchemy
├── main.py             # Entry point utama aplikasi & registrasi endpoint API
├── models.py           # Definisi skema tabel database (SQLAlchemy Models)
├── alembic.ini         # Berkas konfigurasi internal Alembic
├── .gitignore          # Daftar file/folder yang diabaikan oleh Git
└── requirements.txt    # Daftar library Python yang dibutuhkan
```

## 🛠️ Panduan Instalasi Lokal (Local Setup)
Ikuti langkah-langkah berikut untuk menjalankan proyek ini di komputer lokal Anda:

## 1. Kloning Repositori
```bash
git clone [https://github.com/username_kamu/nama_repo_kamu.git](https://github.com/username_kamu/nama_repo_kamu.git)
cd ews-backend
```

## 2. Setup Virtual Environment

Untuk Windows (PowerShell/CMD):
```bash
python -m venv venv
.\venv\Scripts\activate
```

Untuk Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

## 3. Instal Dependencies
Pastikan virtual environment telah aktif (ditandai dengan teks (venv) di terminal), lalu jalankan:

```bash
pip install -r requirements.txt
```

## 4. Konfigurasi Database
1. Buat database kosong bernama nlp_db di PostgreSQL lokal Anda.
2. jalankan command 
```bash
cp .envexample .env
 ```
2. Sesuaikan kredensial pada file .env

## 5. Jalankan Migrasi Database
Tembakkan skema tabel yang ada ke PostgreSQL lokal menggunakan Alembic:

```bash
alembic upgrade head
```

# 🏃 Menjalankan Aplikasi
Untuk menyalakan server lokal FastAPI, jalankan perintah berikut:

```basb
uvicorn main:app --reload
```

Server akan berjalan secara default di alamat: **http://127.0.0.1:8000**

# 📄 Dokumentasi API (Swagger UI)
FastAPI secara otomatis menyediakan dokumentasi interaktif yang dapat diakses melalui browser di:
**🔗 http://127.0.0.1:8000/docs**