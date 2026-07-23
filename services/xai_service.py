import os
import json
import urllib.request
from typing import Dict, Any
from google import genai
from google.genai import types

class XAIService:
    def __init__(self):
        # 1. Konfigurasi Ollama Local (Default untuk Dev di Lokal)
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/api/generate")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")

        # 2. Konfigurasi Gemini API (Akan aktif otomatis jika API Key diisi di .env)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            self.gemini_client = genai.Client(api_key=self.gemini_api_key)
            print("[XAI Service] Mode Aktif: Google Gemini API (Cloud)")
        else:
            self.gemini_client = None
            print(f"[XAI Service] Mode Aktif: Ollama Local Model ({self.ollama_model})")

    def _call_ollama(self, prompt: str) -> Dict[str, Any]:
        """Eksekusi permintaan ke Ollama Local via REST API."""
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "format": "json",  # Memaksa Ollama mengembalikan JSON valid
            "stream": False
        }
        
        req = urllib.request.Request(
            self.ollama_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            # Parse string response dari Ollama ke Dictionary Python
            return json.loads(result.get("response", "{}"))

    def _call_gemini(self, prompt: str) -> Dict[str, Any]:
        """Eksekusi permintaan ke Google Gemini API."""
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3
            )
        )
        return json.loads(response.text)

    def generate_explanation(self, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Kamu adalah Asisten AI Sistem Peringatan Dini (EWS) Akademik Perguruan Tinggi.
        Tugasmu adalah memberikan penjelasan Explainable AI (XAI) yang bijak, empati, dan terstruktur berdasarkan indikator risiko mahasiswa berikut:

        === DATA MAHASISWA ===
        Nama: {risk_data.get('nama')} (NIM: {risk_data.get('nim')})
        Tingkat Risiko: {risk_data.get('tingkat_risiko')} (Skor: {risk_data.get('skor_risiko')})
        Pemicu Risiko Utama:
        {json.dumps(risk_data.get('pemicu_risiko', []), indent=2, ensure_ascii=False)}

        === TUGAS KAMU ===
        Berikan respon HANYA dalam format JSON valid dengan dua key utama:
        1. "analisis_xai": Narasi ringkas 2-3 kalimat yang menjelaskan MENGAPA mahasiswa ini berisiko tinggi/sedang (gabungkan poin akademis dan catatan kualitatifnya).
        2. "rekomendasi_intervensi": Array string berisi 3 langkah konkret yang harus dilakukan oleh Dosen PA.

        Format JSON wajib:
        {{
            "analisis_xai": "string penjelasan...",
            "rekomendasi_intervensi": [
                "Langkah 1...",
                "Langkah 2...",
                "Langkah 3..."
            ]
        }}
        """

        # Jika GEMINI_API_KEY terpasang di .env, gunakan Gemini API
        if self.gemini_client:
            try:
                return self._call_gemini(prompt)
            except Exception as e:
                print(f"[XAI Service Error - Gemini]: {e}. Berpindah ke Ollama Local...")

        # Jika tidak ada GEMINI_API_KEY (atau Gemini error), jalankan Ollama Local
        try:
            return self._call_ollama(prompt)
        except Exception as e:
            print(f"[XAI Service Error - Ollama]: {e}")
            return {
                "analisis_xai": f"Gagal menghubungkan ke AI Engine (Ollama/Gemini). Pemicu utama: {', '.join(risk_data.get('pemicu_risiko', []))}",
                "rekomendasi_intervensi": [
                    "Jadwalkan sesi konsultasi bimbingan akademik individual.",
                    "Periksa kembali presensi kehadiran di kelas."
                ]
            }


# Singleton Instance
xai_service = XAIService()