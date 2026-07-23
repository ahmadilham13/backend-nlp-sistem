from sqlalchemy.orm import Session
from models.dosen import Dosen

def seed_dosen(db: Session):
    print("Seeding data Dosen...")
    dosen_list = [
        Dosen(
            nidn="0412089001",
            nama="Dr. Ahmad Ilham, M.T.",
            email="ahmad.ilham@univ.ac.id"
        ),
        Dosen(
            nidn="0415028802",
            nama="Siti Rahma, M.Kom.",
            email="siti.rahma@univ.ac.id"
        )
    ]
    db.add_all(dosen_list)
    db.flush()  # Mengisi ID tanpa commit langsung agar relasi bisa dibaca
    print("-> Data 'dosen' berhasil ditambahkan.")