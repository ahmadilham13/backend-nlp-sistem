import uuid
from sqlalchemy import Column, Integer, String, DateTime, Uuid
from sqlalchemy.sql import func
from db.database import Base

class MataKuliah(Base):
    __tablename__ = "mata_kuliah"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    kode_mk = Column(String, unique=True, index=True, nullable=False)
    nama_mk = Column(String, nullable=False)
    sks = Column(Integer, nullable=False)
    semester_tawaran = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
