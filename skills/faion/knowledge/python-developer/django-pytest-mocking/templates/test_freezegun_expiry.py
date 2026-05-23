"""
purpose: reference clock-frozen test using freezegun (or time-machine equivalent).
consumes: a service that compares to datetime.now() / timezone.now().
produces: pytest tests for before-expiry and after-expiry cases.
depends-on: pytest, freezegun.
token-budget-impact: ~200 tokens.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from freezegun import freeze_time

from apps.billing.services import coupon_is_valid

pytestmark = pytest.mark.django_db


class TestCouponExpiry:
    @freeze_time("2026-05-22T00:00:00Z")
    def test_coupon_valid_inside_window(self, coupon) -> None:
        # Coupon issued today, valid for 7 days.
        assert coupon_is_valid(coupon) is True

    def test_coupon_invalid_after_expiry(self, coupon) -> None:
        with freeze_time("2026-06-30T00:00:00Z"):
            assert coupon_is_valid(coupon) is False

    @freeze_time("2026-05-22T00:00:00Z")
    def test_now_is_frozen(self) -> None:
        # Reference: confirm the clock is actually frozen.
        assert datetime.now(timezone.utc).isoformat() == "2026-05-22T00:00:00+00:00"
