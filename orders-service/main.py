import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Orders Service")

PAYMENTS_SERVICE_URL = os.getenv("PAYMENTS_SERVICE_URL", "http://localhost:8001")
PAYMENTS_API_KEY = os.getenv("PAYMENTS_API_KEY", "static-secret-123")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "orders-service"}


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    url = f"{PAYMENTS_SERVICE_URL}/payments/{order_id}"
    headers = {"X-API-Key": PAYMENTS_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Payments service unreachable: {exc}",
        )

    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized when communicating with payments-service",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Unexpected error from payments-service: {response.status_code}",
        )

    return {
        "order_id": order_id,
        "item": "Cloud Lab Pro Subscription",
        "status": "CONFIRMED",
        "payment_details": response.json(),
    }
