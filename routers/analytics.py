from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from db.database import get_db
from models.mahasiswa import Mahasiswa
from models.ews_alert import EwsAlert
from models.catatanKonseling import CatatanKonseling
from core.security import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics & Dashboard"], dependencies=[Depends(get_current_user)])

@router.get("/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    # 1. Total Mahasiswa
    total_mahasiswa = db.query(Mahasiswa).count()
    
    # 2. Sebaran Status Mahasiswa
    status_mhs = db.query(Mahasiswa.status, func.count(Mahasiswa.id)).group_by(Mahasiswa.status).all()
    sebaran_status = {status.name: count for status, count in status_mhs}

    # 3. Count alert berdasarkan tingkat risiko
    risiko_alerts = db.query(EwsAlert.tingkat_risiko, func.count(EwsAlert.id)).group_by(EwsAlert.tingkat_risiko).all()
    alert_risiko = {risiko.name: count for risiko, count in risiko_alerts}

    # 4. Count alert berdasarkan status penanganan
    status_alerts = db.query(EwsAlert.status_penanganan, func.count(EwsAlert.id)).group_by(EwsAlert.status_penanganan).all()
    alert_status = {status.name: count for status, count in status_alerts}

    # 5. Persentase kategori masalah terbanyak
    total_konseling = db.query(CatatanKonseling).count()
    kategori_konseling = db.query(CatatanKonseling.kategori, func.count(CatatanKonseling.id)).group_by(CatatanKonseling.kategori).all()
    
    sebaran_kategori = {}
    for kategori, count in kategori_konseling:
        persentase = round((count / total_konseling) * 100, 2) if total_konseling > 0 else 0
        sebaran_kategori[kategori.name] = {
            "count": count,
            "persentase": persentase
        }

    return {
        "total_mahasiswa": total_mahasiswa,
        "sebaran_status_mahasiswa": sebaran_status,
        "alert_berdasarkan_risiko": alert_risiko,
        "alert_berdasarkan_status": alert_status,
        "sebaran_kategori_masalah": sebaran_kategori
    }
