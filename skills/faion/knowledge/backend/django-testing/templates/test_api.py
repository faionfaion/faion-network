"""
purpose: Skeleton for DRF API integration test with auth + status + body asserts.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import pytest


@pytest.mark.django_db
def test_endpoint_unauth_returns_401(api_client):
    response = api_client.get("/api/v1/example/")
    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client_fixture,expected_status",
    [
        ("api_client", 401),
        ("authed_client", 200),
        ("staff_client", 200),
    ],
    ids=["unauth", "user", "staff"],
)
def test_endpoint_permission_matrix(request, client_fixture, expected_status):
    client = request.getfixturevalue(client_fixture)
    response = client.get("/api/v1/example/")
    assert response.status_code == expected_status
