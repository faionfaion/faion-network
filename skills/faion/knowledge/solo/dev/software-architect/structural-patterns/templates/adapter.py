"""
Adapter pattern — Python implementation.
Wraps an incompatible Adaptee to conform to the Target interface.
Prefer Object Adapter (composition) over Class Adapter (multiple inheritance).
"""
from __future__ import annotations
from typing import Protocol


# --- Target interface: what the client expects ---
class PaymentProvider(Protocol):
    """The interface the client code depends on."""

    def charge(self, amount_cents: int, token: str) -> str:
        """Charge a payment token. Returns a transaction ID."""
        ...

    def refund(self, transaction_id: str, amount_cents: int) -> bool:
        """Refund a previous transaction. Returns True on success."""
        ...


# --- Adaptee: existing class with an incompatible interface ---
class StripeClient:
    """Third-party Stripe SDK — cannot be modified."""

    def create_payment_intent(self, amount: int, currency: str, source: str) -> dict:
        # Real Stripe SDK call
        return {"id": f"pi_{source[:8]}", "status": "succeeded"}

    def create_refund(self, payment_intent_id: str, amount: int) -> dict:
        return {"id": f"re_{payment_intent_id[:8]}", "status": "succeeded"}


# --- Object Adapter: composition-based (preferred) ---
class StripeAdapter:
    """Adapts StripeClient to the PaymentProvider interface."""

    def __init__(self, stripe_client: StripeClient) -> None:
        self._client = stripe_client

    def charge(self, amount_cents: int, token: str) -> str:
        result = self._client.create_payment_intent(
            amount=amount_cents,
            currency="usd",
            source=token,
        )
        return result["id"]

    def refund(self, transaction_id: str, amount_cents: int) -> bool:
        result = self._client.create_refund(
            payment_intent_id=transaction_id,
            amount=amount_cents,
        )
        return result["status"] == "succeeded"


# --- Client code: depends only on the Target interface ---
def process_payment(provider: PaymentProvider, amount_cents: int, token: str) -> str:
    """Client depends on PaymentProvider, not on StripeClient."""
    return provider.charge(amount_cents, token)


# --- Wiring (at composition root / DI container) ---
if __name__ == "__main__":
    stripe = StripeClient()
    adapter = StripeAdapter(stripe)
    tx_id = process_payment(adapter, 9900, "tok_visa")
    print(f"Transaction: {tx_id}")
