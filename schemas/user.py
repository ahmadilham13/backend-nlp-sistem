from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    dosen_id: Optional[UUID] = None
    role: str = "dosen"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str
