import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.config import settings
from db.database import get_db
from models.user import User
from schemas.token import TokenData

security_scheme = HTTPBearer()

def get_password_hash(password: str) -> str:
    """Fungsi helper modern untuk melakukan hash password menggunakan bcrypt murni"""
    # 1. Ubah string password menjadi bytes (utf-8)
    password_bytes = password.encode('utf-8')
    
    # 2. Generate salt otomatis
    salt = bcrypt.gensalt()
    
    # 3. Lakukan hashing (hasilnya berupa bytes)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # 4. Ubah kembali ke format string agar bisa masuk kolom VARCHAR database
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Memvalidasi apakah password yang diketik saat login cocok dengan hash di DB.
    Mengembalikan nilai True jika cocok, dan False jika salah.
    """
    try:
        # Ubah string dari user dan string dari DB menjadi format bytes
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Bcrypt secara otomatis mengecek kecocokan menggunakan salt internalnya
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user