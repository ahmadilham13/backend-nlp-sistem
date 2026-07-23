from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from db.database import get_db
from models.mata_kuliah import MataKuliah
from schemas.mata_kuliah import MataKuliahCreate, MataKuliahResponse
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

@router.get("/", response_model=List[MataKuliahResponse])
def get_all_mata_kuliah(db: Session = Depends(get_db)):
    items = db.query(MataKuliah).all()
    return items

@router.get("/{id}", response_model=MataKuliahResponse)
def get_mata_kuliah_by_id(id: UUID, db: Session = Depends(get_db)):
    mk = db.query(MataKuliah).filter(MataKuliah.id == id).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Mata Kuliah tidak ditemukan!")
    return mk
