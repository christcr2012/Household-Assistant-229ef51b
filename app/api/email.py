from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.email import EmailLogRead, EmailSendRequest
from app.services.email import list_email_logs, send_email
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send", response_model=EmailLogRead, status_code=201)
def send_email_route(
    payload: EmailSendRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> EmailLogRead:
    try:
        log = send_email(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return log


@router.get("/logs", response_model=list[EmailLogRead])
def list_logs(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_email_logs(db, current_user)
