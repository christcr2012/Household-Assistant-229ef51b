from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Conversation, Message, MessageRole, User

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - openai optional for tests
    OpenAI = None  # type: ignore[assignment]


class AssistantService:
    """Coordinate conversational interactions and tool suggestions."""

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user
        self.settings = get_settings()
        self._client: Any | None = None

    def run_query(self, *, conversation_id: int | None, message: str, confirm: bool) -> tuple[Conversation, str]:
        conversation = self._get_or_create_conversation(conversation_id)
        self._append_message(conversation, MessageRole.USER, message)

        reply = self._generate_reply(conversation, message, confirm=confirm)
        self._append_message(conversation, MessageRole.ASSISTANT, reply)

        self.db.commit()
        self.db.refresh(conversation)
        return conversation, reply

    def _get_or_create_conversation(self, conversation_id: int | None) -> Conversation:
        if conversation_id is not None:
            conversation = self.db.get(Conversation, conversation_id)
            if conversation is None or conversation.user_id != self.user.id:
                raise ValueError("Conversation not found")
            return conversation

        conversation = Conversation(user_id=self.user.id)
        self.db.add(conversation)
        self.db.flush()
        return conversation

    def _append_message(self, conversation: Conversation, role: MessageRole, content: str) -> None:
        message = Message(conversation_id=conversation.id, role=role, content=content)
        self.db.add(message)
        conversation.updated_at = datetime.utcnow()

    def _generate_reply(self, conversation: Conversation, message: str, *, confirm: bool) -> str:
        if self.settings.openai_api_key and OpenAI is not None:
            return self._llm_reply(conversation)
        return self._rule_based_reply(message, confirm=confirm)

    def _llm_reply(self, conversation: Conversation) -> str:
        messages = [
            {"role": m.role.value, "content": m.content}
            for m in self._get_recent_messages(conversation, limit=15)
        ]
        if OpenAI is None:
            raise RuntimeError("OpenAI library not available")
        if self._client is None:
            self._client = OpenAI(api_key=self.settings.openai_api_key)
        response = self._client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return response.choices[0].message.content or "I'm here to help."

    def _get_recent_messages(self, conversation: Conversation, limit: int) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        rows = self.db.execute(statement).scalars().all()
        return list(reversed(rows))

    def _rule_based_reply(self, message: str, *, confirm: bool) -> str:
        lowered = message.lower()
        if "calendar" in lowered or "schedule" in lowered:
            return (
                "I can help manage your calendar. Use the /calendar/events endpoint to create events, "
                "and let me know if you'd like me to draft the event details for you."
            )
        if "email" in lowered or "send" in lowered:
            return (
                "To send an email, provide the recipient, subject, and body. I'll log the message once the /email/send "
                "endpoint is called."
            )
        if "inventory" in lowered or "grocer" in lowered:
            return (
                "Inventory updates are available via /inventory items. Tell me what changed and I'll update the record for you."
            )
        if "drive" in lowered or "file" in lowered:
            return "Files can be stored securely per tenant. Upload metadata via the storage service as needed."
        if confirm:
            return "Action confirmed. I'll proceed with the requested operation using your saved integrations."
        return (
            "I'm ready to assist with scheduling, email, and household planning. Ask about calendars, inventory, or messages "
            "to get started."
        )
