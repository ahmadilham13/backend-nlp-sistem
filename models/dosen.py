import uuid
from sqlalchemy import Column, String, DateTime, Uuid
from sqlalchemy.sql import func
from db.database import Base

class Dosen(Base):
    __tablename__ = "dosen"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    nidn = Column(String, unique=True, index=True, nullable=False)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())