from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    """Modelo para almacenar usuarios"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    google_id = Column(String, unique=True)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # admin, user, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con la tabla de auditoría
    audit_logs = relationship("AuditLog", back_populates="user")

class AuditLog(Base):
    """Modelo para registrar el uso de las APIs"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String)  # Ruta de la API llamada
    method = Column(String)    # Método HTTP
    request_data = Column(JSON)  # Datos de la solicitud
    response_status = Column(Integer)  # Código de estado HTTP
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relación con la tabla de usuarios
    user = relationship("User", back_populates="audit_logs")