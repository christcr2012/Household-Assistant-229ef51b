from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuthProvider, Credential, User


def generate_tenant_id(email: str, provider: AuthProvider) -> str:
    """Create a deterministic tenant identifier."""

    sanitized = email.replace("@", "-").replace(".", "-")
    return f"{provider.value}-{sanitized}"[:60]


def upsert_user(
    db: Session,
    *,
    email: str,
    full_name: str | None,
    provider: AuthProvider,
    access_token: str,
    refresh_token: str | None,
    scopes: list[str] | None,
    expires_at: datetime | None,
) -> User:
    """Create or update a user with credential information."""

    statement = select(User).where(User.email == email)
    user = db.execute(statement).scalar_one_or_none()
    if user is None:
        tenant_id = generate_tenant_id(email, provider)
        user = User(email=email, full_name=full_name, provider=provider, tenant_id=tenant_id)
        db.add(user)
        db.flush()
    else:
        if full_name and user.full_name != full_name:
            user.full_name = full_name
        if user.provider != provider:
            user.provider = provider

    credential = user.credentials
    if credential is None:
        credential = Credential(
            user_id=user.id,
            provider=provider,
            access_token=access_token,
            refresh_token=refresh_token,
            scopes=scopes or [],
            expires_at=expires_at,
        )
        db.add(credential)
    else:
        credential.access_token = access_token
        credential.refresh_token = refresh_token
        credential.provider = provider
        credential.scopes = scopes or []
        credential.expires_at = expires_at

    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)
