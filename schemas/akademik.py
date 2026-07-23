from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class AkademikSemesterBase(BaseModel):
    mahasiswa_id: UUID
    semester: int
    ipk: float
    ips: float
    persentase_kehadiran: float

class AkademikSemesterCreate(AkademikSemesterBase):
    pass

class AkademikSemesterResponse(AkademikSemesterBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class NilaiMataKuliahBase(BaseModel):
    mahasiswa_id: UUID
    mata_kuliah_id: UUID
    dosen_pengajar_id: UUID
    semester_diambil: int
    nilai_angka: float
    nilai_huruf: str

class NilaiMataKuliahCreate(NilaiMataKuliahBase):
    pass

class NilaiMataKuliahResponse(NilaiMataKuliahBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
