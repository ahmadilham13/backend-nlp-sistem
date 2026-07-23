import enum

class KategoriMasalah(str, enum.Enum):
    AKADEMIK = "AKADEMIK"
    FINANSIAL = "FINANSIAL"
    KESEHATAN = "KESEHATAN"
    PRIBADI = "PRIBADI"
    LAINNYA = "LAINNYA"