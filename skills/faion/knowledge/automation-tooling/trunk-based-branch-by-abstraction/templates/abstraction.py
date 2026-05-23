# purpose: Python Protocol skeleton for BbA
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for trunk-based-branch-by-abstraction
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

from typing import Protocol
from decimal import Decimal


class PaymentProcessor(Protocol):
    def process(self, amount: Decimal) -> dict: ...


class LegacyProcessor:
    def process(self, amount: Decimal) -> dict:
        return self.old_gateway.charge(amount)


class StripeV2Processor:
    def process(self, amount: Decimal) -> dict:
        return self.stripe.create_charge(amount)


def get_processor(flags) -> PaymentProcessor:
    if flags.is_enabled('billing.use_stripe_v2'):
        return StripeV2Processor()
    return LegacyProcessor()
