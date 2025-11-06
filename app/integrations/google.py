from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class GoogleCredentials:
    access_token: str
    refresh_token: str | None


class GoogleWorkspaceClient:
    """Simplified Google API adapter used by the assistant."""

    def __init__(self, credentials: GoogleCredentials):
        self.credentials = credentials

    def create_calendar_event(self, *, title: str, start_time: datetime, end_time: datetime, metadata: dict[str, Any] | None) -> str:
        """Pretend to create an event and return an identifier."""

        return f"gcal-{abs(hash((title, start_time, end_time))) % 10_000_000}"

    def send_email(self, *, recipient: str, subject: str, body: str) -> str:
        """Pretend to send an email and return a message id."""

        preview = body[:50].replace("\n", " ")
        return f"gmail-{abs(hash((recipient, subject, preview))) % 10_000_000}"

    def store_file(self, *, name: str, mime_type: str, data: bytes) -> str:
        return f"gdrive-{abs(hash((name, mime_type, len(data)))) % 10_000_000}"
