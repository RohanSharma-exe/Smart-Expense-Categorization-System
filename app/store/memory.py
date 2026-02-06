from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class StoredTransaction:
    transaction_id: str
    external_id: str
    amount: float
    currency: str
    timestamp: datetime
    merchant_raw: str
    metadata: dict[str, object] | None = None


@dataclass(slots=True)
class InMemoryStore:
    transactions_by_id: dict[str, StoredTransaction] = field(default_factory=dict)
    transactions_by_external: dict[str, StoredTransaction] = field(default_factory=dict)

    def add_transaction(self, txn: StoredTransaction) -> None:
        self.transactions_by_id[txn.transaction_id] = txn
        self.transactions_by_external[txn.external_id] = txn

    def get_by_external_id(self, external_id: str) -> StoredTransaction | None:
        return self.transactions_by_external.get(external_id)

    def get_by_id(self, transaction_id: str) -> StoredTransaction | None:
        return self.transactions_by_id.get(transaction_id)

    def list_transactions(self) -> list[StoredTransaction]:
        return list(self.transactions_by_id.values())
