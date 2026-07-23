# Agent Context & Architectural Guidelines: EWS Backend Engine

You are an expert Senior Python Backend Engineer assigned to build the **Adaptive Early Warning System (EWS)** backend engine for student academic monitoring using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**.

---

## 1. Project Overview & Tech Stack
- **Project Name:** Adaptive Early Warning System (EWS) - Backend Engine
- **Core Stack:** Python 3.12+, FastAPI, Uvicorn, Pydantic v2
- **Database Layer:** PostgreSQL, SQLAlchemy ORM (v2 style), Alembic Migrations
- **Security:** `bcrypt` for password hashing, JWT Authentication (OAuth2)
- **Environment Management:** `python-dotenv` reading from `.env`
- **Future AI Integration:** Google Gemini API (Cloud) & Ollama (Local Fallback) for Explainable AI (XAI) & NLP processing.

---

## 2. Directory Structure Conventions
Always follow this clean directory layout:

```text
ews-backend/
├── alembic/            # Alembic migration scripts and env.py
├── core/               # App-wide configurations, security, and constants
│   ├── config.py       # Pydantic Settings / Environment variables
│   └── security.py     # Bcrypt hashing & JWT token validation
├── db/                 # Database initialization and sessions
│   ├── database.py     # SQLAlchemy engine and get_db dependency
│   └── seed.py         # Seed script for initial/fresh database data
├── models/             # SQLAlchemy ORM models (Database Schemas)
│   ├── enum/           # Enum definitions (Status, TingkatRisiko, dll)
│   ├── user.py
│   ├── dosen.py
│   └── mahasiswa.py
├── schemas/            # Pydantic models (Data validation & API payloads)
│   ├── user.py
│   ├── dosen.py
│   └── mahasiswa.py
├── routers/            # FastAPI Endpoint Handlers (API Controllers)
│   ├── auth.py
│   ├── ews.py
│   ├── ews_alert.py
│   └── mahasiswa.py
├── services/           # Logika Bisnis, NLP, dan AI Engine
│   ├── ews_engine.py   # Kalkulasi skor risiko akademik EWS
│   ├── nlp_service.py  # Pembersihan & stemming catatan konseling
│   └── xai_service.py  # Eksekusi LLM (Ollama/Gemini) untuk XAI
├── main.py             # App entry point
├── alembic.ini         # Alembic configuration file
├── .env                # Local environment secrets (IGNORED BY GIT)
└── .gitignore          # Git exclusion rules
```

## 3. Strict Coding & Architectural Rules

### A. Environment & Configuration
- NEVER hardcode database URLs or API keys.
- Always load configuration dynamically using os.getenv or python-dotenv from the .env file.
- Expected .env variable for DB: DATABASE_URL=postgresql://username:password@localhost:5432/nlp_db

### B. Security & Password Handling
- DO NOT use passlib. Use the native bcrypt library directly for password hashing and verification to avoid Python 3.12+ compatibility issues.
- Never return plain or hashed passwords in API responses (always exclude hashed_password in Pydantic response schemas).

### C. Database & ORM Standard
- Every database interaction must use the get_db SQLAlchemy session dependency via FastAPI's Depends(get_db).
- Use SQLAlchemy 2.0 style queries where possible.
- Schema changes must ALWAYS be handled through Alembic migrations (alembic revision --autogenerate followed by alembic upgrade head). Do not rely on Base.metadata.create_all(bind=engine) in production code.

### D. Data Seeding Rules
- Fresh seeding must clean tables using SQL TRUNCATE TABLE ... RESTART IDENTITY CASCADE; to safely reset auto-increment primary keys.

## 4. Current Progress & Roadmap
- [x] Basic FastAPI setup with Uvicorn.
- [x] PostgreSQL connection with SQLAlchemy ORM (database.py).
- [x] Alembic migration setup connected dynamically to .env.
- [x] Native bcrypt utility functions in security.py (get_password_hash, verify_password).
- [x] Base models created: User and Dosen.
- [x] Fresh DB Seeder script created (seed.py).
- [x] Create Pydantic Schemas for Request/Response validation.
- [x] Implement JWT Authentication Endpoints (/login, /me).
- [x] Implement Data Models, Schemas, & Endpoints for Mahasiswa, Dosen & Konseling.
- [x] Implement Pembersihan Teks Catatan Konseling (NLP Sastrawi Stemming).
- [x] Implement EWS Engine (Kalkulasi Risiko) & Integrasi LLM Decision Maker (XAI).
- [x] Implement EWS Alerts Tracking & Dashboard Endpoints.

### Next Phases (Frontend Readiness)
**Fase 1: Keamanan & Autentikasi (JWT + RBAC)**
- [x] 1.1 Pasang JWT Dependency di Endpoint Konseling (routers/konseling.py).
- [x] 1.2 Pasang Proteksi Role (RBAC) pada Endpoint EWS & Alert (routers/ews_alert.py).

**Fase 2: Endpoint Analitik & Dashboard Summary**
- [x] 2.1 Buat Router Analytics (routers/analytics.py) untuk data agregat dashboard.

**Fase 3: Integrasi & Konfigurasi Server (CORS & Environment)**
- [x] 3.1 Tambahkan CORS Middleware di main.py.
- [x] 3.2 Standardisasi Environment Variables (.env.example).

**Fase 4: Pengujian Akhir & Pembersihan Data (Final Check)**
- [x] 4.1 Jalankan Reset Seeder Utuh (seed.py).
- [x] 4.2 Sanity Test via Swagger UI (/docs) untuk End-to-End flow.