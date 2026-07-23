from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db.database import Base

class Dosen(Base):
    __tablename__ = "dosen"

    id = Column(Integer, primary_key=True, index=True)
    nidn = Column(String, unique=True, index=True, nullable=False)
    nama = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())