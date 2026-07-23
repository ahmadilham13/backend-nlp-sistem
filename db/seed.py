from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from sqlalchemy import text
from core.security import get_password_hash
from db.seeders import seed_users, seed_dosen, seed_mahasiswa, seed_konseling

def run_seeders():
    db: Session = SessionLocal()
    
    try:
        print("==========================================")
        print("MEMULAI PROSES FRESH SEEDING DATABASE")
        print("==========================================")

        # 1. TRUNCATE semua tabel sekaligus dengan urutan yang benar (CASCADE)
        print("Membersihkan seluruh data lama...")
        db.execute(text(
            "TRUNCATE TABLE users, dosen, mahasiswa, catatan_konseling RESTART IDENTITY CASCADE;"
        ))
        db.commit()
        print("-> Database berhasil dibersihkan (Primary Keys di-reset).\n")

        # 2. Jalankan seeder berurutan sesuai relasi Foreign Key
        seed_users(db)
        seed_dosen(db)
        seed_mahasiswa(db)
        seed_konseling(db)

        # 3. Commit seluruh transaksi jika semua lancar
        db.commit()
        print("\n==========================================")
        print("PROSES SEEDING SELESAI DENGAN SUKSES!")
        print("==========================================")

    except Exception as e:
        db.rollback()
        print(f"\n[ERROR] Terjadi kesalahan saat seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seeders()