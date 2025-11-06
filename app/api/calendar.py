from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.calendar import CalendarEventCreate, CalendarEventRead
from app.services.calendar import create_calendar_event, list_calendar_events
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.post("/events", response_model=CalendarEventRead, status_code=201)
def create_event(
    payload: CalendarEventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> CalendarEventRead:
    try:
        event = create_calendar_event(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return event


@router.get("/events", response_model=list[CalendarEventRead])
def list_events(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_calendar_events(db, current_user)
