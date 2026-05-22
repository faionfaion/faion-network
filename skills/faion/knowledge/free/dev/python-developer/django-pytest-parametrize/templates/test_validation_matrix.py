"""
purpose: reference validation matrix test using (field, value, expected_error) tuples.
consumes: a valid baseline payload + invalid (field, value, error) cases.
produces: pytest test that one row per case with descriptive ID.
depends-on: pytest, pytest-django, factories.
token-budget-impact: ~250 tokens.
"""

from __future__ import annotations

import pytest
from rest_framework import status
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def _valid_payload(customer_uid: str) -> dict[str, object]:
    return {
        "customer_uid": customer_uid,
        "amount": "10.00",
        "due_date": "2026-12-31",
    }


@pytest.mark.parametrize(
    "field, value, expected_error",
    [
        pytest.param("amount", "-5",          "must be positive",            id="amount-negative"),
        pytest.param("amount", "abc",         "must be a number",            id="amount-non-numeric"),
        pytest.param("due_date", "2020-01-01","must be in the future",       id="due-date-past"),
        pytest.param("customer_uid", None,    "this field is required",      id="missing-customer"),
    ],
)
def test_create_invoice_validation(
    authenticated_client: APIClient,
    customer,
    field: str,
    value: object,
    expected_error: str,
) -> None:
    payload = _valid_payload(str(customer.uid))
    payload[field] = value

    response = authenticated_client.post("/api/v1/invoices/", data=payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert expected_error in str(response.data.get(field, ""))
