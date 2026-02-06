from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TransactionIn(BaseModel):
    external_id: str = Field(..., min_length=3)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    timestamp: datetime
    merchant_raw: str = Field(..., min_length=1)
    metadata: dict[str, Any] | None = None


class TransactionOut(BaseModel):
    transaction_id: str
    status: str


class CategorizationResponse(BaseModel):
    category_id: str
    confidence: float
    explanation: str
