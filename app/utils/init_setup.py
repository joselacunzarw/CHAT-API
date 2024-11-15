import os
from pathlib import Path
from sqlalchemy.orm import Session
from ..models.models import User
from ..models.database import engine, Base, SessionLocal
from datetime import datetime

def setup_directories():
    """Crea las estructuras de directorios necesarias"""
    # Crea el directorio data si no existe
    data_dir = Path("/data")
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
        # Asigna permisos 755 al directorio
        data_dir.chmod(0o755)
    
    return True

def create_default_user(db: Session):
    """Crea el usuario por defecto si no existe"""
    default_email = "joselacunzarw@gmail.com"
    
    # Verifica si el usuario ya existe
    user = db.query(User).filter(User.email == default_email).first()
    if not user:
        default_user = User(
            email=default_email,
            full_name="Jose Lacunza",
            google_id="default_id",  # Se actualizará cuando el usuario haga login
            is_active=True,
            role="admin",
            created_at=datetime.utcnow()
        )
        db.add(default_user)
        db.commit()
        print(f"Usuario por defecto creado: {default_email}")
    
    return True

def init_database():
    """Inicializa la base de datos y crea el usuario por defecto"""
    # Crea las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crea el usuario por defecto
    db = SessionLocal()
    try:
        create_default_user(db)
    finally:
        db.close()