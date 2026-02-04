from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ingest_and_categorize() -> None:
    payload = {
        "external_id": "txn-001",
        "amount": 12.5,
        "currency": "USD",
        "timestamp": datetime(2024, 1, 1, tzinfo=timezone.utc).isoformat(),
        "merchant_raw": "Uber Trip",
    }
    ingest = client.post("/v1/transactions", json=payload)
    assert ingest.status_code == 200
    transaction_id = ingest.json()["transaction_id"]

    categorize = client.post(f"/v1/transactions/{transaction_id}/categorize")
    assert categorize.status_code == 200
    data = categorize.json()
    assert data["category_id"] == "transportation"
    assert data["confidence"] >= 0.6
