from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from db.database import get_db
from models.mahasiswa import Mahasiswa
from models.catatanKonseling import CatatanKonseling
from services.ews_engine import ews_engine
from services.xai_service import xai_service
from core.security import get_current_user

router = APIRouter(prefix="/ews", tags=["EWS Engine & XAI"], dependencies=[Depends(get_current_user)])

@router.get("/assess/{mahasiswa_id}", response_model=Dict[str, Any])
def assess_mahasiswa_risk(mahasiswa_id: int, db: Session = Depends(get_db)):
    """
    Menganalisis tingkat risiko mahasiswa berdasarkan ID (EWS Engine)
    dan menghasilkan narasi Explainable AI otomatis (Ollama / Gemini).
    """
    # 1. Ambil data mahasiswa
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan!")

    # 2. Ambil seluruh riwayat catatan konseling mahasiswa tersebut
    catatan_list = db.query(CatatanKonseling).filter(CatatanKonseling.mahasiswa_id == mahasiswa_id).all()

    # 3. Hitung status risiko lewat EWS Engine
    hasil_penilaian = ews_engine.calculate_risk(mhs, catatan_list)
    
    # 4. Hasilkan analisis & rekomendasi XAI (Ollama Local / Gemini)
    xai_output = xai_service.generate_explanation(hasil_penilaian)

    # 5. Gabungkan narasi XAI ke dalam response JSON
    hasil_penilaian["xai"] = xai_output

    return hasil_penilaian