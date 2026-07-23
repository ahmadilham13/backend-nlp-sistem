from sqlalchemy.orm import Session
from core.security import get_password_hash
from models.user import User

def seed_users(db: Session):
    print("Seeding data Users...")
    users_list = [
        User(
            username="admin", 
            email="admin@univ.ac.id", 
            password=get_password_hash("password123"), 
            role="admin"
        ),
        User(
            username="dosen1", 
            email="ahmad.ilham@univ.ac.id", 
            password=get_password_hash("password123"), 
            role="dosen"
        )
    ]
    db.add_all(users_list)
    db.flush()
    print("-> Data 'users' berhasil ditambahkan.")