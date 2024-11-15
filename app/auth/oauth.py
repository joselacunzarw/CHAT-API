from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.models import User
from datetime import datetime

# Configuración de OAuth2
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/v2/auth",
    tokenUrl="https://oauth2.googleapis.com/token"
)

async def verify_google_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Verifica el token de Google y retorna la información del usuario"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            os.getenv("GOOGLE_CLIENT_ID")
        )
        return idinfo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Obtiene el usuario actual basado en el token"""
    user_info = await verify_google_token(token)
    
    # Busca el usuario en la base de datos
    user = db.query(User).filter(User.email == user_info["email"]).first()
    
    # Si no existe, lo crea
    if not user:
        user = User(
            email=user_info["email"],
            google_id=user_info["sub"],
            full_name=user_info.get("name", ""),
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user