from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models.enum.statusMahasiswa import StatusMahasiswa

class MahasiswaBase(BaseModel):
    nim: str
    nama: str
    email: EmailStr
    angkatan: int
    status: StatusMahasiswa = StatusMahasiswa.AKTIF
    ipk: float = 0.0
    ips: float = 0.0
    presensi_persen: float = 100.0
    total_sks: int = 0
    dosen_pa_id: Optional[int] = None

class MahasiswaCreate(MahasiswaBase):
    pass




class MahasiswaUpdate(BaseModel):
    nama: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[StatusMahasiswa] = None
    ipk: Optional[float] = None
    ips: Optional[float] = None
    presensi_persen: Optional[float] = None
    total_sks: Optional[int] = None
    dosen_pa_id: Optional[int] = None


class MahasiswaResponse(MahasiswaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True