from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db


app = FastAPI(
    title="Adaptive Early Warning System API",
    description="Backend Engine menggunakan FastAPI dan PostgreSQL",
    version="1.0.0"
)

# Endpoint 1: Tes apakah API hidup (Root Endpoint)
@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Selamat datang di API Adaptive Early Warning System"
    }
    
# Endpoint 2: Tes Koneksi ke PostgreSQL Lokal
@app.get("/tes-koneksi-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Mencoba melakukan query ringan ke database
        db.execute(text("SELECT 1"))
        return {
            "status": "Sukses",
            "message": "Python FastAPI berhasil terhubung ke PostgreSQL lokal!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Gagal terhubung ke database. Error: {str(e)}"
        )