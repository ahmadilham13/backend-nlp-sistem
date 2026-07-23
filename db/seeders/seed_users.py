from sqlalchemy.orm import Session
from core.security import get_password_hash
from models.user import User
from .constants import USER_ID_ADMIN, USER_ID_DOSEN, DOSEN_ID_1

def seed_users(db: Session):
    print("Seeding data Users...")
    users_list = [
        User(
            id=USER_ID_ADMIN,
            username="admin", 
            email="admin@univ.ac.id", 
            password=get_password_hash("password123"), 
            role="admin",
            dosen_id=None
        ),
        User(
            id=USER_ID_DOSEN,
            username="dosen1", 
            email="ahmad.ilham@univ.ac.id", 
            password=get_password_hash("password123"), 
            role="dosen",
            dosen_id=DOSEN_ID_1
        )
    ]
    db.add_all(users_list)
    db.flush()
    print("-> Data 'users' berhasil ditambahkan.")