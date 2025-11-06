from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models import AuthProvider, CalendarEvent, User
from app.schemas.calendar import CalendarEventCreate
from app.services.integrations import IntegrationFactory


def create_calendar_event(db: Session, user: User, payload: CalendarEventCreate) -> CalendarEvent:
    factory = IntegrationFactory(user)
    client = factory.get_calendar_client()
    external_id = client.create_calendar_event(
        title=payload.title,
        start_time=payload.start_time,
        end_time=payload.end_time,
        metadata=payload.metadata,
    )
    event = CalendarEvent(
        user_id=user.id,
        provider=user.provider,
        external_id=external_id,
        title=payload.title,
        start_time=payload.start_time,
        end_time=payload.end_time,
        metadata=payload.metadata,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_calendar_events(db: Session, user: User) -> list[CalendarEvent]:
    return [
        event
        for event in user.calendar_events
        if event.provider in {AuthProvider.GOOGLE, AuthProvider.APPLE}
    ]
