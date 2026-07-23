import enum

class StatusMahasiswa(str, enum.Enum):
    AKTIF = "AKTIF"
    CUTI = "CUTI"
    DROP_OUT = "DROP_OUT"
    LULUS = "LULUS"