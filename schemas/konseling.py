from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models import KategoriMasalah


class CatatanKonselingCreate(BaseModel):
    mahasiswa_id: int
    kategori: KategoriMasalah
    catatan_teks: str


class CatatanKonselingResponse(BaseModel):
    id: int
    mahasiswa_id: int
    dosen_id: int
    tanggal: datetime
    kategori: KategoriMasalah
    catatan_teks: str
    catatan_cleansed: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True