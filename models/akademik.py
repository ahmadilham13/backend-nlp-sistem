import uuid
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class AkademikSemester(Base):
    __tablename__ = "akademik_semester"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    mahasiswa_id = Column(Uuid, ForeignKey("mahasiswa.id"), nullable=False)
    semester = Column(Integer, nullable=False)
    ipk = Column(Float, nullable=False)
    ips = Column(Float, nullable=False)
    persentase_kehadiran = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    mahasiswa = relationship("Mahasiswa")


class NilaiMataKuliah(Base):
    __tablename__ = "nilai_mata_kuliah"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    mahasiswa_id = Column(Uuid, ForeignKey("mahasiswa.id"), nullable=False)
    mata_kuliah_id = Column(Uuid, ForeignKey("mata_kuliah.id"), nullable=False)
    dosen_pengajar_id = Column(Uuid, ForeignKey("dosen.id"), nullable=False)
    
    semester_diambil = Column(Integer, nullable=False)
    nilai_angka = Column(Float, nullable=False)
    nilai_huruf = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    mahasiswa = relationship("Mahasiswa")
    mata_kuliah = relationship("MataKuliah")
    dosen_pengajar = relationship("Dosen")
