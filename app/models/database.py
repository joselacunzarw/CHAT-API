from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

# Configura la URL de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

# Crea el engine de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Solo necesario para SQLite
)

# Crea la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()