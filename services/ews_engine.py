from typing import List, Dict, Any, Tuple
from enum import Enum
from models.mahasiswa import Mahasiswa
from models.catatanKonseling import CatatanKonseling, KategoriMasalah
from models.enum.tingkatRisiko import TingkatRisiko

class EWSEngine:
    # Kata kunci kualitatif dari hasil NLP Sastrawi yang mengindikasikan masalah
    KEYWORDS_HIGH_RISK = [
        "phk", "drop", "out", "biaya", "ukt", "paruh", "waktu", "kerja", 
        "sakit", "meninggal", "pindah", "depresi", "paling", "sulit", "tua"
    ]
    
    KEYWORDS_MEDIUM_RISK = [
        "pbo", "matematika", "algoritma", "bingung", "tugas", "tidur", 
        "lambat", "keluh", "kurang", "malas", "bolos"
    ]

    def calculate_risk(
        self, 
        mahasiswa: Mahasiswa, 
        catatan_list: List[CatatanKonseling]
    ) -> Dict[str, Any]:
        """
        Mengkalkulasi tingkat risiko mahasiswa berdasarkan indikator kuantitatif 
        dan indikator kualitatif (teks konseling hasil pembersihan NLP).
        """
        pemicu_risiko: List[str] = []
        skor_risiko: int = 0  # Skor kumulatif penentu tingkat risiko

        # ==========================================
        # 1. EVALUASI KUANTITATIF (IPK & Presensi)
        # ==========================================

        # Evaluasi IPK
        if mahasiswa.ipk < 2.0:
            skor_risiko += 3
            pemicu_risiko.append(f"IPK sangat rendah ({mahasiswa.ipk}) di bawah 2.00")
        elif mahasiswa.ipk < 2.5:
            skor_risiko += 2
            pemicu_risiko.append(f"IPK tergolong rendah ({mahasiswa.ipk}) di bawah 2.50")

        # Evaluasi Presensi
        if mahasiswa.presensi_persen < 70.0:
            skor_risiko += 3
            pemicu_risiko.append(f"Presensi kehadiran kritis ({mahasiswa.presensi_persen}%) di bawah 70%")
        elif mahasiswa.presensi_persen < 80.0:
            skor_risiko += 1
            pemicu_risiko.append(f"Presensi kehadiran kurang ({mahasiswa.presensi_persen}%) di bawah 80%")

        # ==========================================
        # 2. EVALUASI KUALITATIF (Catatan Konseling NLP)
        # ==========================================
        
        found_keywords: List[str] = []

        for catatan in catatan_list:
            # Pengecekan Kategori Masalah
            if catatan.kategori in [KategoriMasalah.FINANSIAL, KategoriMasalah.KESEHATAN]:
                skor_risiko += 2
                pemicu_risiko.append(f"Terdapat catatan bimbingan kategori masalah {catatan.kategori.value}")

            # Pengecekan Kata Kunci pada teks yang telah dibersihkan (catatan_cleansed)
            cleansed_text = catatan.catatan_cleansed or ""
            words = cleansed_text.split()

            for word in words:
                if word in self.KEYWORDS_HIGH_RISK and word not in found_keywords:
                    found_keywords.append(word)
                    skor_risiko += 2
                elif word in self.KEYWORDS_MEDIUM_RISK and word not in found_keywords:
                    found_keywords.append(word)
                    skor_risiko += 1

        if found_keywords:
            pemicu_risiko.append(f"Terdeteksi kata kunci masalah pada catatan konseling: {', '.join(found_keywords)}")

        # ==========================================
        # 3. PENENTUAN TINGKAT RISIKO AKHIR
        # ==========================================
        
        if skor_risiko >= 4:
            tingkat = TingkatRisiko.HIGH
        elif skor_risiko >= 2:
            tingkat = TingkatRisiko.MEDIUM
        else:
            tingkat = TingkatRisiko.LOW

        return {
            "mahasiswa_id": mahasiswa.id,
            "nim": mahasiswa.nim,
            "nama": mahasiswa.nama,
            "tingkat_risiko": tingkat,
            "skor_risiko": skor_risiko,
            "pemicu_risiko": pemicu_risiko,
            "indikator": {
                "ipk": mahasiswa.ipk,
                "presensi_persen": mahasiswa.presensi_persen,
                "total_catatan_konseling": len(catatan_list)
            }
        }

# Singleton Instance
ews_engine = EWSEngine()

