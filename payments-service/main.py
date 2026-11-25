import os
from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="Payments Service")

PAYMENTS_API_KEY = os.getenv("PAYMENTS_API_KEY", "static-secret-123")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "payments-service"}


@app.get("/payments/{order_id}")
def get_payment(order_id: str, x_api_key: str | None = Header(default=None)):
    if not x_api_key or x_api_key != PAYMENTS_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
        )

    return {
        "order_id": order_id,
        "payment_status": "PAID",
        "amount_usd": 49.99,
        "auth_method": "static-api-key",
    }
