from datetime import datetime

from pydantic import EmailStr

from app.models import AuthProvider
from app.schemas.base import ORMBase


class UserBase(ORMBase):
    email: EmailStr
    full_name: str | None = None
    provider: AuthProvider


class UserCreate(UserBase):
    tenant_id: str
    access_token: str
    refresh_token: str | None = None
    scopes: list[str] | None = None
    expires_at: datetime | None = None


class UserRead(UserBase):
    id: int
    tenant_id: str
    created_at: datetime


class CredentialRead(ORMBase):
    provider: AuthProvider
    scopes: list[str]
    expires_at: datetime | None
    updated_at: datetime
