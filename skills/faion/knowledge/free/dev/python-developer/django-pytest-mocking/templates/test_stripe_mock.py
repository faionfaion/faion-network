"""
purpose: reference pattern for mocking an SDK call at the import site + verifying the call.
consumes: a service that imports stripe.
produces: pytest test that asserts on assert_called_once_with.
depends-on: pytest, unittest.mock.
token-budget-impact: ~200 tokens.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from apps.billing import services

pytestmark = pytest.mark.django_db


class TestChargeCustomer:
    # Patch at the CONSUMER's import path: apps.billing.services.stripe.
    @patch("apps.billing.services.stripe.Charge.create")
    def test_creates_charge_with_correct_args(self, mock_create, customer) -> None:
        mock_create.return_value = {"id": "ch_123", "status": "succeeded"}

        services.charge_customer(customer=customer, amount_cents=1000)

        # Verifies BOTH that the call happened and that the arguments are right.
        mock_create.assert_called_once_with(
            amount=1000,
            currency="usd",
            customer=customer.stripe_id,
        )
