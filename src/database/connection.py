import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_URL = f"postgresql://admin:Pass123@{DB_HOST}:5432/legislacion_db"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Crea las tablas si no existen"""
    Base.metadata.create_all(engine)

def get_db():
    """Retorna una sesión"""
    return SessionLocal()