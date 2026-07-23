from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from db.database import get_db
from models.akademik import AkademikSemester, NilaiMataKuliah
from schemas.akademik import (
    AkademikSemesterCreate, 
    AkademikSemesterResponse, 
    NilaiMataKuliahCreate, 
    NilaiMataKuliahResponse
)
from core.security import get_current_user

router = APIRouter(prefix="/akademik", tags=["Akademik"], dependencies=[Depends(get_current_user)])

# --- KHS / Akademik Semester ---
@router.post("/semester", response_model=AkademikSemesterResponse, status_code=status.HTTP_201_CREATED)
def create_akademik_semester(data: AkademikSemesterCreate, db: Session = Depends(get_db)):
    new_sem = AkademikSemester(**data.model_dump())
    db.add(new_sem)
    db.commit()
    db.refresh(new_sem)
    return new_sem

@router.get("/semester/mahasiswa/{mahasiswa_id}", response_model=List[AkademikSemesterResponse])
def get_semester_by_mahasiswa(mahasiswa_id: UUID, db: Session = Depends(get_db)):
    items = db.query(AkademikSemester).filter(AkademikSemester.mahasiswa_id == mahasiswa_id).order_by(AkademikSemester.semester.asc()).all()
    return items

# --- Nilai Mata Kuliah ---
@router.post("/nilai", response_model=NilaiMataKuliahResponse, status_code=status.HTTP_201_CREATED)
def create_nilai_mata_kuliah(data: NilaiMataKuliahCreate, db: Session = Depends(get_db)):
    new_nilai = NilaiMataKuliah(**data.model_dump())
    db.add(new_nilai)
    db.commit()
    db.refresh(new_nilai)
    return new_nilai

@router.get("/nilai/mahasiswa/{mahasiswa_id}", response_model=List[NilaiMataKuliahResponse])
def get_nilai_by_mahasiswa(mahasiswa_id: UUID, db: Session = Depends(get_db)):
    items = db.query(NilaiMataKuliah).filter(NilaiMataKuliah.mahasiswa_id == mahasiswa_id).all()
    return items
