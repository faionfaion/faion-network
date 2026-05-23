"""
purpose: reference role × endpoint permission grid using getfixturevalue().
consumes: api_client, authenticated_client, other_authenticated_client, admin_client.
produces: one parametrized test covering all role / status-code combinations.
depends-on: pytest, pytest-django.
token-budget-impact: ~200 tokens.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "client_fixture, expected_status",
    [
        pytest.param("api_client",                    401, id="anonymous-401"),
        pytest.param("authenticated_client",          200, id="user-owns-200"),
        pytest.param("other_authenticated_client",    403, id="user-cross-403"),
        pytest.param("admin_client",                  200, id="admin-200"),
    ],
)
def test_invoice_detail_by_role(request, invoice, client_fixture: str, expected_status: int) -> None:
    # getfixturevalue selects the API client per parametrized row.
    client = request.getfixturevalue(client_fixture)
    response = client.get(f"/api/v1/invoices/{invoice.uid}/", format="json")
    assert response.status_code == expected_status
