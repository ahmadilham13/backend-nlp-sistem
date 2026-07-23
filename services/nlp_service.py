import re
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class NLPService:
    def __init__(self):
        # Initialize the stop word remover and stemmer
        stopword_factory = StopWordRemoverFactory()
        self.stopword_remover = stopword_factory.create_stop_word_remover()

        # Inisialisasi Stemmer Sastrawi
        stemmer_factory = StemmerFactory()
        self.stemmer = stemmer_factory.create_stemmer()
        
    def clean_text(self, text: str) -> str:
        """
        Menghapus karakter non-alphabet, angka, dan spasi berlebih.
        """
        if not text:
            return ""

        # 1. Case Folding
        text = text.lower()

        # 2. Hapus angka dan tanda baca / karakter spesial
        text = re.sub(r'[^a-z\s]', ' ', text)

        # 3. Hapus spasi ganda / berlebih
        text = re.sub(r'\s+', ' ', text).strip()

        return text
    
    def preprocess_catatan(self, text: str) -> str:
        """
        Pipeline lengkap pembersihan teks catatan bimbingan:
        Case Folding & Cleaning -> Stopword Removal -> Stemming Sastrawi
        """
        # Step 1: Cleaning dasar
        cleaned = self.clean_text(text)

        # Step 2: Stopword Removal (Hapus kata hubung)
        without_stopwords = self.stopword_remover.remove(cleaned)

        # Step 3: Stemming (Ubah ke kata dasar Bahasa Indonesia)
        stemmed_text = self.stemmer.stem(without_stopwords)

        return stemmed_text

# Singleton Instance agar tidak inisialisasi Sastrawi berulang kali (efisiensi memori)
nlp_service = NLPService()


# if __name__ == "__main__":
#     contoh_teks = "Mahasiswa mengeluhkan sulit membayar UKT semester ini karena orang tua terkena PHK."
    
#     print("--- UJI COBA NLP SERVICE ---")
#     print(f"Teks Asli      : {contoh_teks}")
    
#     hasil_cleansed = nlp_service.preprocess_catatan(contoh_teks)
#     print(f"Hasil Cleansed : {hasil_cleansed}")