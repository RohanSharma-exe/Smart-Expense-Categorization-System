from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException

from app.models.transactions import CategorizationResponse, TransactionIn, TransactionOut
from app.services.categorization import CategorizationService
from app.store.memory import InMemoryStore, StoredTransaction

router = APIRouter()
store = InMemoryStore()
service = CategorizationService()


@router.post("/transactions", response_model=TransactionOut)
def create_transaction(payload: TransactionIn) -> TransactionOut:
    existing = store.get_by_external_id(payload.external_id)
    if existing:
        return TransactionOut(transaction_id=existing.transaction_id, status="duplicate")

    transaction_id = str(uuid.uuid4())
    store.add_transaction(
        StoredTransaction(
            transaction_id=transaction_id,
            external_id=payload.external_id,
            amount=payload.amount,
            currency=payload.currency,
            timestamp=payload.timestamp,
            merchant_raw=payload.merchant_raw,
            metadata=payload.metadata,
        )
    )
    return TransactionOut(transaction_id=transaction_id, status="ingested")


@router.post("/transactions/{transaction_id}/categorize", response_model=CategorizationResponse)
def categorize_transaction(transaction_id: str) -> CategorizationResponse:
    txn = store.get_by_id(transaction_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    result = service.categorize(txn)
    return CategorizationResponse(
        category_id=result.category_id,
        confidence=result.confidence,
        explanation=result.explanation,
    )
