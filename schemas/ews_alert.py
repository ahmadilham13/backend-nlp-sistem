from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from models.enum.tingkatRisiko import TingkatRisiko
from models.enum.statusPenanganan import StatusPenanganan

class EwsAlertUpdate(BaseModel):
    status_penanganan: StatusPenanganan
    catatan_penanganan: Optional[str] = None

class EwsAlertResponse(BaseModel):
    id: UUID
    mahasiswa_id: UUID
    tingkat_risiko: TingkatRisiko
    skor_risiko: int
    pemicu_risiko: List[str]
    analisis_xai: str
    rekomendasi_intervensi: List[str]
    status_penanganan: StatusPenanganan
    catatan_penanganan: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True