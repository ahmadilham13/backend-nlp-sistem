from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class DosenBase(BaseModel):
    nidn: str
    nama: str
    email: EmailStr

class DosenCreate(DosenBase):
    pass

class DosenResponse(DosenBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
