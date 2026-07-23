import math
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from models.mahasiswa import Mahasiswa
from schemas.mahasiswa import MahasiswaCreate, MahasiswaResponse, MahasiswaUpdate
from schemas.pagination import PageResponse
from core.security import get_current_user

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=MahasiswaResponse, status_code=status.HTTP_201_CREATED)
def create_mahasiswa(data: MahasiswaCreate, db: Session = Depends(get_db)):
    # Cek apakah NIM sudah terdaftar
    existing_mhs = db.query(Mahasiswa).filter(Mahasiswa.nim == data.nim).first()
    if existing_mhs:
        raise HTTPException(status_code=400, detail="NIM sudah terdaftar!")

    new_mhs = Mahasiswa(**data.model_dump())
    db.add(new_mhs)
    db.commit()
    db.refresh(new_mhs)
    return new_mhs

@router.get("/", response_model=PageResponse[MahasiswaResponse])
def get_all_mahasiswa(
    page: int = Query(1, ge=1, description="Halaman ke-n"),
    page_size: int = Query(10, ge=1, le=100, description="Jumlah data per halaman"),
    db: Session = Depends(get_db)
):
    # 1. Hitung skip (offset) berdasarkan page & page_size
    skip = (page - 1) * page_size

    # 2. Hitung total seluruh data di database
    total_items = db.query(Mahasiswa).count()

    # 3. Ambil potongan data sesuai limit & offset
    items = db.query(Mahasiswa).offset(skip).limit(page_size).all()

    # 4. Hitung total halaman
    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

    return PageResponse(
        items=items,
        total_items=total_items,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/{id}", response_model=MahasiswaResponse)
def get_mahasiswa_by_id(id: int, db: Session = Depends(get_db)):
    mhs = db.query(Mahasiswa).filter(Mahasiswa.id == id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan!")
    return mhs