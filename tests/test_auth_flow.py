from datetime import datetime, timedelta

from fastapi.testclient import TestClient


def test_google_login_and_me_endpoint(app_client: TestClient):
    payload = {
        "email": "user@example.com",
        "full_name": "Test User",
        "access_token": "token123",
        "refresh_token": "refresh123",
        "scopes": ["calendar", "gmail"],
        "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
    }
    response = app_client.post("/auth/google", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tenant_id"].startswith("google-user-example-com")

    headers = {"X-User-Id": str(data["user_id"])}
    me = app_client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    me_data = me.json()
    assert me_data["email"] == "user@example.com"
    assert me_data["provider"] == "google"

    creds = app_client.get("/auth/me/credentials", headers=headers)
    assert creds.status_code == 200
    assert set(creds.json()["scopes"]) == {"calendar", "gmail"}
