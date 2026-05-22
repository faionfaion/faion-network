"""
purpose: skeleton integration test module for one DRF endpoint covering all 5 cases.
consumes: api_client, authenticated_client, admin_client fixtures + factories.
produces: pytest module that the codegen agent fills with the specific resource details.
depends-on: pytest, pytest-django, factory-boy, rest_framework.
token-budget-impact: ~340 tokens.
"""

from __future__ import annotations

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.billing.models import Invoice  # adapt to the resource under test

pytestmark = pytest.mark.django_db


class TestInvoiceCreate:
    url = "/api/v1/invoices/"

    def test_anonymous_returns_401(self, api_client: APIClient) -> None:
        response = api_client.post(self.url, data={"amount": "10.00"}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_wrong_permission_returns_403(self, api_client: APIClient, other_user) -> None:
        api_client.force_authenticate(user=other_user)
        response = api_client.post(self.url, data={"amount": "10.00"}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_happy_path_returns_201_and_body(self, authenticated_client: APIClient, customer) -> None:
        payload = {"customer_uid": str(customer.uid), "amount": "10.00", "due_date": "2026-06-01"}
        response = authenticated_client.post(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        # Always assert at least one body field — never status-code-only.
        assert response.data["amount"] == "10.00"
        assert "uid" in response.data
        assert Invoice.objects.filter(uid=response.data["uid"]).exists()

    def test_validation_failure_returns_400(self, authenticated_client: APIClient, customer) -> None:
        bad_payload = {"customer_uid": str(customer.uid), "amount": "-5.00"}
        response = authenticated_client.post(self.url, data=bad_payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data
