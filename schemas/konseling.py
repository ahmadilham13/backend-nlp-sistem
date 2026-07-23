from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from models import KategoriMasalah


class CatatanKonselingCreate(BaseModel):
    mahasiswa_id: UUID
    kategori: KategoriMasalah
    catatan_teks: str


class CatatanKonselingResponse(BaseModel):
    id: UUID
    mahasiswa_id: UUID
    dosen_id: UUID
    tanggal: datetime
    kategori: KategoriMasalah
    catatan_teks: str
    catatan_cleansed: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True