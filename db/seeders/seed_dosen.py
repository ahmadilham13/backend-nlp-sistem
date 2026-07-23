from sqlalchemy.orm import Session
from models.dosen import Dosen
from .constants import DOSEN_ID_1

def seed_dosen(db: Session):
    print("Seeding data Dosen...")
    dosen_list = [
        Dosen(
            id=DOSEN_ID_1,
            nidn="0011223344",
            nama="Dr. Ahmad Ilham, S.Kom., M.Kom.",
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