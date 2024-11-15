from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .models.database import get_db, engine
from .models import models
from .auth.oauth import get_current_user
from .api.audit import log_request
from .core import recuperar_documentos, consultar_llm
from .utils.init_setup import setup_directories, init_database
import os

# Inicialización del sistema
setup_directories()
init_database()

app = FastAPI(title="ChatBot API", version="1.0.0")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recuperar_documentos")
async def recuperar_docs(
    request: Request,
    question: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para recuperar documentos relevantes.
    Requiere autenticación y registra el uso en la auditoría.
    """
    try:
        documentos = recuperar_documentos(question)
        
        # Registra la solicitud en la auditoría
        await log_request(request, current_user.id, db, status.HTTP_200_OK)
        
        return {"documentos": documentos}
    except Exception as e:
        # Registra el error en la auditoría
        await log_request(request, current_user.id, db, status.HTTP_500_INTERNAL_SERVER_ERROR)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/consultar")
async def consultar(
    request: Request,
    question: str,
    history: list = [],
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Endpoint para consultar al LLM.
    Requiere autenticación y registra el uso en la auditoría.
    """
    try:
        # Recupera documentos y consulta al LLM
        contexto = recuperar_documentos(question)
        respuesta = consultar_llm(contexto, question, history)
        
        # Registra la solicitud en la auditoría
        await log_request(request, current_user.id, db, status.HTTP_200_OK)
        
        return {"reply": respuesta}
    except Exception as e:
        # Registra el error en la auditoría
        await log_request(request, current_user.id, db, status.HTTP_500_INTERNAL_SERVER_ERROR)
        raise HTTPException(status_code=500, detail=str(e))