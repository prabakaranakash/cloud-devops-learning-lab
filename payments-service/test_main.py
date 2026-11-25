from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "payments-service"}


def test_get_payment_valid_key():
    response = client.get("/payments/101", headers={"X-API-Key": "static-secret-123"})
    assert response.status_code == 200
    assert response.json() == {
        "order_id": "101",
        "payment_status": "PAID",
        "amount_usd": 49.99,
        "auth_method": "static-api-key",
    }


def test_get_payment_invalid_key():
    response = client.get("/payments/101", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API key"}


def test_get_payment_missing_key():
    response = client.get("/payments/101")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API key"}
