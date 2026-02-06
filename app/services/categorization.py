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
        merchant = txn.merchant_raw.lower()
        if "uber" in merchant or "lyft" in merchant:
            category_id = "transportation"
            confidence = 0.6
            explanation = "Matched rideshare merchant keyword."
        elif "starbucks" in merchant or "cafe" in merchant:
            category_id = "meals"
            confidence = 0.55
            explanation = "Matched coffee/meal merchant keyword."
        elif txn.amount > 500:
            category_id = "high_value"
            confidence = 0.45
            explanation = "Amount exceeds high-value threshold."
        return CategorizationResult(
            category_id=category_id,
            confidence=confidence,
            explanation=explanation,
        )
