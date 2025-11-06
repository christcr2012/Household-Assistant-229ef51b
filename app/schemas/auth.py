from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models import AuthProvider


class OAuthLoginRequest(BaseModel):
    email: EmailStr
    full_name: str | None = None
    access_token: str
    refresh_token: str | None = None
    scopes: list[str] | None = None
    expires_at: datetime | None = None


class AuthResponse(BaseModel):
    user_id: int
    tenant_id: str
    provider: AuthProvider
