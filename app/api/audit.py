from fastapi import Request
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.models import AuditLog

async def log_request(request: Request, user_id: int, db: Session, status_code: int):
    """Registra la solicitud en el log de auditoría"""
    # Obtiene el cuerpo de la solicitud
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
        except:
            body = {}

    # Crea el registro de auditoría
    audit_log = AuditLog(
        user_id=user_id,
        endpoint=str(request.url),
        method=request.method,
        request_data=body,
        response_status=status_code,
        timestamp=datetime.utcnow()
    )
    
    db.add(audit_log)
    db.commit()