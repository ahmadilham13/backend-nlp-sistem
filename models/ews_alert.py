import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, JSON, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
from models.enum.tingkatRisiko import TingkatRisiko
from models.enum.statusPenanganan import StatusPenanganan


class EwsAlert(Base):
    __tablename__ = "ews_alerts"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    mahasiswa_id = Column(Uuid, ForeignKey("mahasiswa.id"), nullable=False)
    
    tingkat_risiko = Column(Enum(TingkatRisiko), nullable=False)
    skor_risiko = Column(Integer, nullable=False)
    
    # Menyimpan list pemicu & rekomendasi dalam format JSON Array
    pemicu_risiko = Column(JSON, nullable=False)
    analisis_xai = Column(Text, nullable=False)
    rekomendasi_intervensi = Column(JSON, nullable=False)
    
    # Status Tindak Lanjut Dosen PA
    status_penanganan = Column(Enum(StatusPenanganan), default=StatusPenanganan.PENDING, nullable=False)
    catatan_penanganan = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    mahasiswa = relationship("Mahasiswa", backref="ews_alerts")