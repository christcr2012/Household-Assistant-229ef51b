from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class AppleCredentials:
    username: str
    app_password: str


class AppleEcosystemClient:
    """Simplified Apple ecosystem adapter using CalDAV/IMAP style semantics."""

    def __init__(self, credentials: AppleCredentials):
        self.credentials = credentials

    def create_calendar_event(self, *, title: str, start_time: datetime, end_time: datetime, metadata: dict[str, Any] | None) -> str:
        return f"icloud-{abs(hash((title, start_time, end_time))) % 10_000_000}"

    def send_email(self, *, recipient: str, subject: str, body: str) -> str:
        preview = body[:50].replace("\n", " ")
        return f"icloudmail-{abs(hash((recipient, subject, preview))) % 10_000_000}"

    def store_file(self, *, name: str, mime_type: str, data: bytes) -> str:
        return f"icloud-drive-{abs(hash((name, mime_type, len(data)))) % 10_000_000}"
