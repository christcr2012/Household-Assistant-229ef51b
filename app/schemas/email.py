from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models import AuthProvider
from app.schemas.base import ORMBase


class EmailSendRequest(BaseModel):
    recipient: EmailStr
    subject: str
    body: str


class EmailLogRead(ORMBase):
    id: int
    provider: AuthProvider
    subject: str
    recipient: EmailStr
    body_preview: str
    created_at: datetime
