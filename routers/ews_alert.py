import math
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from db.database import get_db
from models.mahasiswa import Mahasiswa
from models.catatanKonseling import CatatanKonseling
from models.ews_alert import EwsAlert, StatusPenanganan
from models.enum.tingkatRisiko import TingkatRisiko
from schemas.ews_alert import EwsAlertResponse, EwsAlertUpdate
from schemas.pagination import PageResponse
from services.ews_engine import ews_engine
from services.xai_service import xai_service

router = APIRouter(prefix="/ews/alerts", tags=["EWS Alerts & Intervensi"])

@router.post("/generate/{mahasiswa_id}", response_model=EwsAlertResponse, status_code=status.HTTP_201_CREATED)
def generate_and_save_alert(mahasiswa_id: int, db: Session = Depends(get_db)):
    """
    Menjalankan kalkulasi EWS + XAI lalu menyimpan hasil alert-nya ke database.
    """
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan!")

    catatan_list = db.query(CatatanKonseling).filter(CatatanKonseling.mahasiswa_id == mahasiswa_id).all()

    # 1. Jalankan Engine & XAI
    hasil_penilaian = ews_engine.calculate_risk(mhs, catatan_list)
    xai_output = xai_service.generate_explanation(hasil_penilaian)

    # 2. Simpan Alert ke DB
    new_alert = EwsAlert(
        mahasiswa_id=mahasiswa_id,
        tingkat_risiko=hasil_penilaian["tingkat_risiko"],
        skor_risiko=hasil_penilaian["skor_risiko"],
        pemicu_risiko=hasil_penilaian["pemicu_risiko"],
        analisis_xai=xai_output.get("analisis_xai", ""),
        rekomendasi_intervensi=xai_output.get("rekomendasi_intervensi", []),
        status_penanganan=StatusPenanganan.PENDING
    )

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

@router.get("/", response_model=PageResponse[EwsAlertResponse])
def get_all_alerts(
    tingkat_risiko: Optional[TingkatRisiko] = Query(None, description="Filter berdasarkan level risiko"),
    status_penanganan: Optional[StatusPenanganan] = Query(None, description="Filter berdasarkan status penanganan"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Dashboard daftar alert peringatan dini (dengan filter & pagination).
    """
    skip = (page - 1) * page_size
    query = db.query(EwsAlert)

    if tingkat_risiko:
        query = query.filter(EwsAlert.tingkat_risiko == tingkat_risiko)
    if status_penanganan:
        query = query.filter(EwsAlert.status_penanganan == status_penanganan)

    total_items = query.count()
    items = query.order_by(EwsAlert.created_at.desc()).offset(skip).limit(page_size).all()
    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

    return {
        "items": items,
        "total_items": total_items,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@router.patch("/{alert_id}", response_model=EwsAlertResponse)
def update_alert_status(alert_id: int, data: EwsAlertUpdate, db: Session = Depends(get_db)):
    """
    Memperbarui status tindakan intervensi Dosen PA (misal merubah ke IN_PROGRESS / RESOLVED).
    """
    alert = db.query(EwsAlert).filter(EwsAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="EWS Alert tidak ditemukan!")

    alert.status_penanganan = data.status_penanganan
    if data.catatan_penanganan is not None:
        alert.catatan_penanganan = data.catatan_penanganan

    db.commit()
    db.refresh(alert)
    return alert