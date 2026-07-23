import uuid
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Enum, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
from models.enum.statusMahasiswa import StatusMahasiswa

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    nim = Column(String, unique=True, index=True, nullable=False)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    angkatan = Column(Integer, nullable=False)
    prodi = Column(String, nullable=True) # Tambahan prodi
    status = Column(Enum(StatusMahasiswa), default=StatusMahasiswa.AKTIF, nullable=False)
    
    # Indikator Akademik Dasar
    ipk = Column(Float, default=0.0)
    ips = Column(Float, default=0.0)
    presensi_persen = Column(Float, default=100.0)
    total_sks = Column(Integer, default=0)

    # Foreign Key ke Dosen PA
    dosen_pa_id = Column(Uuid, ForeignKey("dosen.id"), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    dosen_pa = relationship("Dosen", backref="mahasiswa_bimbingan")
    catatan_konseling = relationship("CatatanKonseling", back_populates="mahasiswa", cascade="all, delete-orphan")