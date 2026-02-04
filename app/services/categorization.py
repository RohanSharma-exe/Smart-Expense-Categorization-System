from __future__ import annotations

from dataclasses import dataclass

from app.store.memory import StoredTransaction


@dataclass(slots=True)
class CategorizationResult:
    category_id: str
    confidence: float
    explanation: str


class CategorizationService:
    def categorize(self, txn: StoredTransaction) -> CategorizationResult:
        category_id = "uncategorized"
        confidence = 0.1
        explanation = "Default category pending rules/ML configuration."
        if "uber" in txn.merchant_raw.lower():
            category_id = "transportation"
            confidence = 0.6
            explanation = "Matched merchant keyword: uber."
        return CategorizationResult(
            category_id=category_id,
            confidence=confidence,
            explanation=explanation,
        )
