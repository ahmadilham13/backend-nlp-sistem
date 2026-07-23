from db.database import Base
from models.user import User
from models.dosen import Dosen
from models.mahasiswa import Mahasiswa, StatusMahasiswa
from models.catatanKonseling import CatatanKonseling, KategoriMasalah
from models.ews_alert import EwsAlert, StatusPenanganan
from models.mata_kuliah import MataKuliah
from models.akademik import AkademikSemester, NilaiMataKuliah

__all__ = [
    "Base",
    "User",
    "Dosen",
    "Mahasiswa",
    "StatusMahasiswa",
    "CatatanKonseling",
    "KategoriMasalah",
    "EwsAlert",
    "StatusPenanganan",
    "MataKuliah",
    "AkademikSemester",
    "NilaiMataKuliah"
]