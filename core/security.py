import bcrypt

def get_password_hash(password: str) -> str:
    """Fungsi helper modern untuk melakukan hash password menggunakan bcrypt murni"""
    # 1. Ubah string password menjadi bytes (utf-8)
    password_bytes = password.encode('utf-8')
    
    # 2. Generate salt otomatis
    salt = bcrypt.gensalt()
    
    # 3. Lakukan hashing (hasilnya berupa bytes)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # 4. Ubah kembali ke format string agar bisa masuk kolom VARCHAR database
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Memvalidasi apakah password yang diketik saat login cocok dengan hash di DB.
    Mengembalikan nilai True jika cocok, dan False jika salah.
    """
    try:
        # Ubah string dari user dan string dari DB menjadi format bytes
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        # Bcrypt secara otomatis mengecek kecocokan menggunakan salt internalnya
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False