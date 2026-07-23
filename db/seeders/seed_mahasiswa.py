from sqlalchemy.orm import Session
from models.mahasiswa import Mahasiswa, StatusMahasiswa
from .constants import DOSEN_ID_1, MAHASISWA_ID_1, MAHASISWA_ID_2, MAHASISWA_ID_3

def seed_mahasiswa(db: Session):
    print("Seeding data Mahasiswa...")
    
    dosen_pa_id = DOSEN_ID_1 

    mahasiswa_list = [
        Mahasiswa(
            id=MAHASISWA_ID_1,
            nim="220101001",
            nama="Budi Santoso",
            email="budi@student.univ.ac.id",
            angkatan=2022,
            prodi="Informatika",
            status=StatusMahasiswa.AKTIF,
            ipk=2.15,
            ips=1.80,
            presensi_persen=68.5,
            total_sks=45,
            dosen_pa_id=dosen_pa_id
        ),
        Mahasiswa(
            id=MAHASISWA_ID_2,
            nim="220101002",
            nama="Siti Aminah",
            email="siti@student.univ.ac.id",
            angkatan=2022,
            prodi="Informatika",
            status=StatusMahasiswa.AKTIF,
            ipk=3.75,
            ips=3.85,
            presensi_persen=95.0,
            total_sks=48,
            dosen_pa_id=dosen_pa_id
        ),
        Mahasiswa(
            id=MAHASISWA_ID_3,
            nim="220101003",
            nama="Rian Hidayat",
            email="rian@student.univ.ac.id",
            angkatan=2022,
            prodi="Sistem Informasi",
            status=StatusMahasiswa.AKTIF,
            ipk=1.90,
            ips=1.75,
            presensi_persen=55.0,
            total_sks=40,
            dosen_pa_id=dosen_pa_id
        )
    ]
    db.add_all(mahasiswa_list)
    db.flush()
    print("-> Data 'mahasiswa' berhasil ditambahkan.")