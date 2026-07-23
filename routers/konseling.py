import math
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models.catatanKonseling import CatatanKonseling
from schemas.konseling import CatatanKonselingCreate, CatatanKonselingResponse
from schemas.pagination import PageResponse
from services.nlp_service import nlp_service

router = APIRouter(prefix="/konseling", tags=["Catatan Konseling"])

@router.post("/", response_model=CatatanKonselingResponse, status_code=status.HTTP_201_CREATED)
def create_catatan_konseling(
    data: CatatanKonselingCreate, 
    dosen_id: int = 1, # Sementara hardcode ID Dosen PA (nanti diganti dari token JWT)
    db: Session = Depends(get_db)
):
    # 1. Jalankan pembersihan NLP Sastrawi secara otomatis pada teks mentah
    cleansed_text = nlp_service.preprocess_catatan(data.catatan_teks)

    # 2. Simpan catatan mentah DAN catatan yang sudah dibersihkan ke DB
    new_catatan = CatatanKonseling(
        mahasiswa_id=data.mahasiswa_id,
        dosen_id=dosen_id,
        kategori=data.kategori,
        catatan_teks=data.catatan_teks,
        catatan_cleansed=cleansed_text
    )

    db.add(new_catatan)
    db.commit()
    db.refresh(new_catatan)
    return new_catatan

@router.get("/mahasiswa/{mahasiswa_id}", response_model=PageResponse[CatatanKonselingResponse])
def get_catatan_by_mahasiswa(
    mahasiswa_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size

    # Query dasar khusus mahasiswa_id terkait
    query = db.query(CatatanKonseling).filter(CatatanKonseling.mahasiswa_id == mahasiswa_id)

    total_items = query.count()
    items = query.offset(skip).limit(page_size).all()
    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

    return PageResponse(
        items=items,
        total_items=total_items,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )