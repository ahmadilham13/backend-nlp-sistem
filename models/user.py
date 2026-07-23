import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Uuid
from sqlalchemy.sql import func
from db.database import Base

# --- Models  ---

class User(Base):
    __tablename__ = "users"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    dosen_id = Column(Uuid, ForeignKey("dosen.id"), nullable=True)
    role = Column(String, default="dosen")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())