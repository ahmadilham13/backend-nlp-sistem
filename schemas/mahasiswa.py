from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from models.enum.statusMahasiswa import StatusMahasiswa

class MahasiswaBase(BaseModel):
    nim: str
    nama: str
    email: EmailStr
    angkatan: int
    prodi: Optional[str] = None
    status: StatusMahasiswa = StatusMahasiswa.AKTIF
    ipk: float = 0.0
    ips: float = 0.0
    presensi_persen: float = 100.0
    total_sks: int = 0
    dosen_pa_id: Optional[UUID] = None

class MahasiswaCreate(MahasiswaBase):
    pass




class MahasiswaUpdate(BaseModel):
    nama: Optional[str] = None
    email: Optional[EmailStr] = None
    prodi: Optional[str] = None
    status: Optional[StatusMahasiswa] = None
    ipk: Optional[float] = None
    ips: Optional[float] = None
    presensi_persen: Optional[float] = None
    total_sks: Optional[int] = None
    dosen_pa_id: Optional[UUID] = None

class MahasiswaResponse(MahasiswaBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True