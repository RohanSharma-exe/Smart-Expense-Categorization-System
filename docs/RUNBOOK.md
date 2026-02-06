# Runbook — Smart Expense Categorization System

This guide explains how to install dependencies, run the API locally, and verify the core endpoints.

## Prerequisites
- Python 3.11+
- pip (or uv/pipx if preferred)

## Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run the API
```bash
uvicorn app.main:app --reload
```

## Verify the API
### Healthcheck
```bash
curl -s http://localhost:8000/health | jq
```

### Ingest a Transaction
```bash
curl -s -X POST http://localhost:8000/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "txn-001",
    "amount": 12.50,
    "currency": "USD",
    "timestamp": "2024-01-01T00:00:00Z",
    "merchant_raw": "Uber Trip"
  }' | jq
```

### Categorize a Transaction
```bash
curl -s -X POST http://localhost:8000/v1/transactions/<transaction_id>/categorize | jq
```

### List Transactions
```bash
curl -s http://localhost:8000/v1/transactions | jq
```

## Run Tests
```bash
pytest
```

## Dependencies
Core runtime dependencies are declared in `pyproject.toml`:
- FastAPI
- Uvicorn
- Pydantic

Developer dependencies include:
- Pytest
- HTTPX
