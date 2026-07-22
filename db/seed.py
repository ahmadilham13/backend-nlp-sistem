from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from sqlalchemy import text
from core.security import get_password_hash
from models.user import User

def seed_data():
    # 1. Buka session database
    db = SessionLocal()
    
    try:
        print("Membersihkan data lama...")
        db.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        db.commit()
        print("-> Database berhasil dibersihkan.")

        print("Memulai proses seeding data...")

        user_exist = db.query(User).first()
        if not user_exist:
            # Contoh data User untuk Login (Password idealnya di-hash nanti)
            user_baru = [
                User(username="admin", email="admin@univ.ac.id", password=get_password_hash("password123"), role="admin"),
                User(username="dosen1", email="ahmad.ilham@univ.ac.id", password=get_password_hash("password123"), role="dosen")
            ]
            db.add_all(user_baru)
            print("-> Data tabel 'users' berhasil ditambahkan.")
        else:
            print("-> Tabel 'users' sudah memiliki data, skipping...")

        # 3. Commit semua perubahan ke PostgreSQL
        db.commit()
        print("Proses seeding selesai dengan sukses!")

    except Exception as e:
        db.rollback()
        print(f"Terjadi kesalahan saat seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()