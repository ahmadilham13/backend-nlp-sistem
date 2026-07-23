from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import math

from db.database import get_db
from models.mata_kuliah import MataKuliah
from schemas.mata_kuliah import MataKuliahCreate, MataKuliahResponse
from schemas.pagination import PageResponse
from core.security import get_current_user

router = APIRouter(prefix="/mata-kuliah", tags=["Mata Kuliah"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=MataKuliahResponse, status_code=status.HTTP_201_CREATED)
def create_mata_kuliah(data: MataKuliahCreate, db: Session = Depends(get_db)):
    existing_mk = db.query(MataKuliah).filter(MataKuliah.kode_mk == data.kode_mk).first()
    if existing_mk:
        raise HTTPException(status_code=400, detail="Kode Mata Kuliah sudah terdaftar!")

    new_mk = MataKuliah(**data.model_dump())
    db.add(new_mk)
    db.commit()
    db.refresh(new_mk)
    return new_mk

@router.get("/", response_model=PageResponse[MataKuliahResponse])
def get_all_mata_kuliah(
    page: int = Query(1, ge=1, description="Halaman ke-n"),
    page_size: int = Query(10, ge=1, le=100, description="Jumlah data per halaman"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    total_items = db.query(MataKuliah).count()
    items = db.query(MataKuliah).offset(skip).limit(page_size).all()
    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1

    return PageResponse(
        items=items,
        total_items=total_items,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/{id}", response_model=MataKuliahResponse)
def get_mata_kuliah_by_id(id: UUID, db: Session = Depends(get_db)):
    mk = db.query(MataKuliah).filter(MataKuliah.id == id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Mata Kuliah tidak ditemukan!")
    return mk
