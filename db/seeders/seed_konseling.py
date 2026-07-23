from sqlalchemy.orm import Session
from models.catatanKonseling import CatatanKonseling, KategoriMasalah

def seed_konseling(db: Session):
    print("Seeding data Catatan Konseling...")
    
    catatan_list = [
        CatatanKonseling(
            mahasiswa_id=1,  # Budi Santoso
            dosen_id=1,      # Dr. Ahmad Ilham
            kategori=KategoriMasalah.FINANSIAL,
            catatan_teks="Mahasiswa mengeluhkan sulit membayar UKT semester ini karena orang tua terkena PHK. Mengaku sering tidak masuk kuliah karena kerja paruh waktu malam hari."
        ),
        CatatanKonseling(
            mahasiswa_id=3,  # Rian Hidayat
            dosen_id=1,      # Dr. Ahmad Ilham
            kategori=KategoriMasalah.AKADEMIK,
            catatan_teks="Mahasiswa merasa salah jurusan dan kesulitan mengikuti mata kuliah Pemrograman Berorientasi Objek. Mengaku sering tidur di kelas dan tidak mengumpulkan tugas 3 minggu terakhir."
        )
    ]
    db.add_all(catatan_list)
    db.flush()
    print("-> Data 'catatan_konseling' berhasil ditambahkan.")