from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class MataKuliahBase(BaseModel):
    kode_mk: str
    nama_mk: str
    sks: int
    semester_tawaran: int

class MataKuliahCreate(MataKuliahBase):
    pass

class MataKuliahResponse(MataKuliahBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
