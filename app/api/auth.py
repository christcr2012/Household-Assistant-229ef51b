from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import AuthProvider
from app.schemas.auth import AuthResponse, OAuthLoginRequest
from app.schemas.user import CredentialRead, UserRead
from app.services.user import upsert_user
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=AuthResponse)
def login_google(payload: OAuthLoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    user = upsert_user(
        db,
        email=payload.email,
        full_name=payload.full_name,
        provider=AuthProvider.GOOGLE,
        access_token=payload.access_token,
        refresh_token=payload.refresh_token,
        scopes=payload.scopes,
        expires_at=payload.expires_at,
    )
    return AuthResponse(user_id=user.id, tenant_id=user.tenant_id, provider=user.provider)


@router.post("/apple", response_model=AuthResponse)
def login_apple(payload: OAuthLoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    user = upsert_user(
        db,
        email=payload.email,
        full_name=payload.full_name,
        provider=AuthProvider.APPLE,
        access_token=payload.access_token,
        refresh_token=payload.refresh_token,
        scopes=payload.scopes,
        expires_at=payload.expires_at,
    )
    return AuthResponse(user_id=user.id, tenant_id=user.tenant_id, provider=user.provider)


@router.get("/me", response_model=UserRead)
def read_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/me/credentials", response_model=CredentialRead)
def read_credentials(current_user=Depends(get_current_user)):
    return current_user.credentials
