from __future__ import annotations

from app.integrations.apple import AppleCredentials, AppleEcosystemClient
from app.integrations.google import GoogleCredentials, GoogleWorkspaceClient
from app.models import AuthProvider, User


class IntegrationFactory:
    """Return provider specific clients for a user."""

    def __init__(self, user: User):
        if user.credentials is None:
            raise ValueError("User has no stored credentials")
        self.user = user

    def get_calendar_client(self):
        if self.user.provider == AuthProvider.GOOGLE:
            return GoogleWorkspaceClient(
                GoogleCredentials(
                    access_token=self.user.credentials.access_token,
                    refresh_token=self.user.credentials.refresh_token,
                )
            )
        if self.user.provider == AuthProvider.APPLE:
            return AppleEcosystemClient(
                AppleCredentials(
                    username=self.user.email,
                    app_password=self.user.credentials.access_token,
                )
            )
        raise ValueError("Unsupported provider")

    def get_email_client(self):
        return self.get_calendar_client()

    def get_storage_client(self):
        return self.get_calendar_client()
