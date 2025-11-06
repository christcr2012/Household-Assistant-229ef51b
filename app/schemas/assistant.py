from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import ORMBase


class AssistantQuery(BaseModel):
    conversation_id: int | None = None
    message: str
    confirm: bool = False


class AssistantResponse(BaseModel):
    conversation_id: int
    reply: str


class ConversationSummary(ORMBase):
    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime
