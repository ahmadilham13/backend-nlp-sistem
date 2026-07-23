from sqlalchemy.orm import Session
from models.akademik import AkademikSemester, NilaiMataKuliah
from .constants import MAHASISWA_ID_1, MAHASISWA_ID_2, MATA_KULIAH_ID_1, DOSEN_ID_1

def seed_akademik(db: Session):
    print("Seeding data Akademik (Semester & Nilai MK)...")
    
    semester_list = [
        AkademikSemester(
            mahasiswa_id=MAHASISWA_ID_1,
            semester=1,
            ipk=2.15,
            ips=1.80,
            persentase_kehadiran=68.5
        ),
        AkademikSemester(
            mahasiswa_id=MAHASISWA_ID_2,
            semester=1,
            ipk=3.75,
            ips=3.85,
            persentase_kehadiran=95.0
        )
    ]
    db.add_all(semester_list)
    
    nilai_list = [
        NilaiMataKuliah(
            mahasiswa_id=MAHASISWA_ID_1,
            mata_kuliah_id=MATA_KULIAH_ID_1,
            dosen_pengajar_id=DOSEN_ID_1,
            semester_diambil=1,
            nilai_angka=55.0,
            nilai_huruf="D"
        ),
        NilaiMataKuliah(
            mahasiswa_id=MAHASISWA_ID_2,
            mata_kuliah_id=MATA_KULIAH_ID_1,
            dosen_pengajar_id=DOSEN_ID_1,
            semester_diambil=1,
            nilai_angka=90.0,
            nilai_huruf="A"
        )
    ]
    db.add_all(nilai_list)
    db.flush()
    print("-> Data 'akademik_semester' & 'nilai_mata_kuliah' berhasil ditambahkan.")
