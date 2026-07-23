from sqlalchemy.orm import Session
from models.mata_kuliah import MataKuliah
from .constants import MATA_KULIAH_ID_1, MATA_KULIAH_ID_2

def seed_mata_kuliah(db: Session):
    print("Seeding data Mata Kuliah...")
    
    mk_list = [
        MataKuliah(
            id=MATA_KULIAH_ID_1,
            kode_mk="IF102",
            nama_mk="Algoritma dan Pemrograman",
            sks=3,
            semester_tawaran=1
        ),
        MataKuliah(
            id=MATA_KULIAH_ID_2,
            kode_mk="SI301",
            nama_mk="Sistem Basis Data",
            sks=3,
            semester_tawaran=3
        )
    ]
    db.add_all(mk_list)
    db.flush()
    print("-> Data 'mata_kuliah' berhasil ditambahkan.")
