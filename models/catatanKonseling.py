import uuid
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
from models.enum.kategoriMasalah import KategoriMasalah

class CatatanKonseling(Base):
    __tablename__ = "catatan_konseling"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    mahasiswa_id = Column(Uuid, ForeignKey("mahasiswa.id"), nullable=False)
    dosen_id = Column(Uuid, ForeignKey("dosen.id"), nullable=False)
    
    tanggal = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    kategori = Column(Enum(KategoriMasalah), default=KategoriMasalah.AKADEMIK, nullable=False)
    
    # Teks mentah hasil input Dosen PA (bahan baku NLP)
    catatan_teks = Column(Text, nullable=False)
    
    # Kolom untuk menampung hasil pembersihan NLP nantinya
    catatan_cleansed = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    mahasiswa = relationship("Mahasiswa", back_populates="catatan_konseling")
    dosen = relationship("Dosen")