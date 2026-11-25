from unittest.mock import AsyncMock, patch
import httpx
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "orders-service"}


@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_get_order_success(mock_get):
    mock_get.return_value = httpx.Response(
        200,
        json={
            "order_id": "101",
            "payment_status": "PAID",
            "amount_usd": 49.99,
            "auth_method": "static-api-key",
        },
    )

    response = client.get("/orders/101")
    assert response.status_code == 200
    assert response.json() == {
        "order_id": "101",
        "item": "Cloud Lab Pro Subscription",
        "status": "CONFIRMED",
        "payment_details": {
            "order_id": "101",
            "payment_status": "PAID",
            "amount_usd": 49.99,
            "auth_method": "static-api-key",
        },
    }


@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_get_order_unauthorized(mock_get):
    mock_get.return_value = httpx.Response(
        401, json={"detail": "Invalid or missing API key"}
    )

    response = client.get("/orders/101")
    assert response.status_code == 401


@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_get_order_service_unreachable(mock_get):
    mock_get.side_effect = httpx.ConnectError("Connection refused")

    response = client.get("/orders/101")
    assert response.status_code == 502
