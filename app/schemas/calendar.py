from datetime import datetime

from pydantic import BaseModel

from app.models import AuthProvider
from app.schemas.base import ORMBase


class CalendarEventCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    metadata: dict[str, str] | None = None


class CalendarEventRead(ORMBase):
    id: int
    provider: AuthProvider
    external_id: str | None
    title: str
    start_time: datetime
    end_time: datetime
    metadata: dict[str, str] | None
