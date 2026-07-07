import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/nlp_sistem")
engine = create_engine(DATABASE_URL)

# Session untuk melakukan query (Insert, Select, Update, Delete) ke database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk mendefinisikan skema table nanti
Base = declarative_base()

# Fungsi helper untuk mendapatkan session database di endpoint FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()