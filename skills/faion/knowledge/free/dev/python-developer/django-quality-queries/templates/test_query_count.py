# purpose: pytest skeleton locking query count for a hot endpoint
# consumes: factory_boy factory + Django test client
# produces: regression test that fails when N+1 is reintroduced
# depends-on: pytest-django, factory_boy
# token-budget-impact: ~120 tokens

import pytest


@pytest.mark.django_db
def test_<endpoint>_query_count(client, django_assert_num_queries, <factory_fixture>):
    """Lock the exact query count to prevent N+1 regression."""
    for _ in range(20):
        <factory_fixture>()

    with django_assert_num_queries(3):  # adjust to selector's measured count
        response = client.get("/api/<endpoint>/")

    assert response.status_code == 200
