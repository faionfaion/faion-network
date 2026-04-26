"""
Facade pattern — Python implementation.
Provides a simplified entry point to a multi-class subsystem.
The subsystem classes remain accessible for callers that need more control.
"""
from __future__ import annotations
import dataclasses


# ===================================================================
# The Subsystem: multiple classes with complex interactions
# ===================================================================

class PaymentValidator:
    def validate_card(self, card_token: str) -> bool:
        print(f"[Validator] Validating card token: {card_token[:6]}...")
        return True  # simplified

    def validate_amount(self, amount_cents: int) -> bool:
        return 50 <= amount_cents <= 99_900_00  # $0.50 to $99,900


class FraudDetector:
    def check(self, user_id: str, amount_cents: int, ip: str) -> bool:
        print(f"[FraudDetector] Checking user={user_id} amount={amount_cents} ip={ip}")
        return True  # simplified: not fraudulent


class PaymentGatewayClient:
    def charge(self, card_token: str, amount_cents: int, idempotency_key: str) -> str:
        print(f"[Gateway] Charging {amount_cents} cents with key={idempotency_key}")
        return f"txn_{idempotency_key[:8]}"


class Ledger:
    def record_charge(self, user_id: str, amount_cents: int, tx_id: str) -> None:
        print(f"[Ledger] Recording charge: user={user_id} tx={tx_id} amount={amount_cents}")

    def record_failure(self, user_id: str, amount_cents: int, reason: str) -> None:
        print(f"[Ledger] Recording failure: user={user_id} reason={reason}")


class EmailNotifier:
    def send_receipt(self, user_id: str, amount_cents: int, tx_id: str) -> None:
        print(f"[Email] Sending receipt to user={user_id} for tx={tx_id}")


# ===================================================================
# Facade: common payment workflow hidden behind a single interface
# ===================================================================

@dataclasses.dataclass
class ChargeResult:
    success: bool
    transaction_id: str | None = None
    error: str | None = None


class PaymentFacade:
    """
    Simplifies the most common payment workflow.
    Subsystem classes (Validator, FraudDetector, etc.) remain accessible
    for callers that need to customize behavior.
    """

    def __init__(
        self,
        validator: PaymentValidator | None = None,
        fraud_detector: FraudDetector | None = None,
        gateway: PaymentGatewayClient | None = None,
        ledger: Ledger | None = None,
        notifier: EmailNotifier | None = None,
    ) -> None:
        self._validator = validator or PaymentValidator()
        self._fraud = fraud_detector or FraudDetector()
        self._gateway = gateway or PaymentGatewayClient()
        self._ledger = ledger or Ledger()
        self._notifier = notifier or EmailNotifier()

    def charge(
        self,
        user_id: str,
        card_token: str,
        amount_cents: int,
        idempotency_key: str,
        ip: str = "0.0.0.0",
    ) -> ChargeResult:
        """Complete payment: validate → fraud check → charge → ledger → notify."""
        if not self._validator.validate_card(card_token):
            self._ledger.record_failure(user_id, amount_cents, "invalid_card")
            return ChargeResult(success=False, error="invalid_card")

        if not self._validator.validate_amount(amount_cents):
            return ChargeResult(success=False, error="invalid_amount")

        if not self._fraud.check(user_id, amount_cents, ip):
            self._ledger.record_failure(user_id, amount_cents, "fraud_detected")
            return ChargeResult(success=False, error="fraud_detected")

        tx_id = self._gateway.charge(card_token, amount_cents, idempotency_key)
        self._ledger.record_charge(user_id, amount_cents, tx_id)
        self._notifier.send_receipt(user_id, amount_cents, tx_id)

        return ChargeResult(success=True, transaction_id=tx_id)


# --- Client code: uses the Facade, not the subsystem ---
if __name__ == "__main__":
    payment = PaymentFacade()
    result = payment.charge(
        user_id="u-123",
        card_token="tok_visa_4242",
        amount_cents=4999,
        idempotency_key="order-8821",
        ip="203.0.113.1",
    )
    print(f"\nResult: success={result.success} tx={result.transaction_id}")
