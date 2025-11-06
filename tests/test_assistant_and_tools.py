from datetime import datetime, timedelta

from fastapi.testclient import TestClient


def authenticate_google(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/auth/google",
        json={
            "email": "planner@example.com",
            "full_name": "Household Planner",
            "access_token": "token456",
            "refresh_token": "refresh456",
            "scopes": ["calendar", "gmail", "drive"],
            "expires_at": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        },
    )
    response.raise_for_status()
    data = response.json()
    return {"X-User-Id": str(data["user_id"])}


def test_inventory_calendar_email_flow(app_client: TestClient):
    headers = authenticate_google(app_client)

    # Inventory creation
    create_resp = app_client.post(
        "/inventory/items",
        json={"name": "Apples", "quantity": 5, "unit": "pcs"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    item_id = create_resp.json()["id"]

    update_resp = app_client.patch(
        f"/inventory/items/{item_id}",
        json={"quantity": 8},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["quantity"] == 8

    list_resp = app_client.get("/inventory/items", headers=headers)
    assert list_resp.status_code == 200
    assert list_resp.json()[0]["name"] == "Apples"

    # Calendar event creation
    event_resp = app_client.post(
        "/calendar/events",
        json={
            "title": "Lunch with John",
            "start_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "end_time": (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
        },
        headers=headers,
    )
    assert event_resp.status_code == 201
    assert event_resp.json()["external_id"].startswith("gcal-")

    # Email sending
    email_resp = app_client.post(
        "/email/send",
        json={
            "recipient": "john@example.com",
            "subject": "Lunch Plans",
            "body": "Looking forward to lunch tomorrow!",
        },
        headers=headers,
    )
    assert email_resp.status_code == 201
    assert email_resp.json()["recipient"] == "john@example.com"

    # Assistant query
    assistant_resp = app_client.post(
        "/assistant/query",
        json={"message": "Help me update the inventory"},
        headers=headers,
    )
    assert assistant_resp.status_code == 200
    assert "inventory" in assistant_resp.json()["reply"].lower()
