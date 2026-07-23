from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from db.database import get_db
from models.dosen import Dosen
from schemas.dosen import DosenCreate, DosenResponse
from core.security import get_current_user

router = APIRouter(prefix="/dosen", tags=["Dosen"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=DosenResponse, status_code=status.HTTP_201_CREATED)
def create_dosen(data: DosenCreate, db: Session = Depends(get_db)):
    existing_dosen = db.query(Dosen).filter((Dosen.nidn == data.nidn) | (Dosen.email == data.email)).first()
    if existing_dosen:
        raise HTTPException(status_code=400, detail="NIDN atau Email sudah terdaftar!")

    new_dosen = Dosen(**data.model_dump())
    db.add(new_dosen)
    db.commit()
    db.refresh(new_dosen)
    return new_dosen

@router.get("/", response_model=List[DosenResponse])
def get_all_dosen(db: Session = Depends(get_db)):
    items = db.query(Dosen).all()
    return items

@router.get("/{id}", response_model=DosenResponse)
def get_dosen_by_id(id: UUID, db: Session = Depends(get_db)):
    dosen = db.query(Dosen).filter(Dosen.id == id).first()
    if not dosen:
        raise HTTPException(status_code=404, detail="Dosen tidak ditemukan!")
    return dosen
