from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import EmailLog, User
from app.schemas.email import EmailSendRequest
from app.services.integrations import IntegrationFactory


def send_email(db: Session, user: User, payload: EmailSendRequest) -> EmailLog:
    factory = IntegrationFactory(user)
    client = factory.get_email_client()
    message_id = client.send_email(recipient=payload.recipient, subject=payload.subject, body=payload.body)
    log = EmailLog(
        user_id=user.id,
        provider=user.provider,
        subject=payload.subject,
        recipient=str(payload.recipient),
        body_preview=payload.body[:200],
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def list_email_logs(db: Session, user: User) -> list[EmailLog]:
    return sorted(user.email_logs, key=lambda entry: entry.created_at, reverse=True)
