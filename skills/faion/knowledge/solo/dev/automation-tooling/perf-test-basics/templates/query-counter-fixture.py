# tests/conftest.py — SQLAlchemy event-listener fixture for N+1 detection.
# More reliable than log scraping: fires on every cursor execution regardless of log level.
import pytest
from sqlalchemy import event


@pytest.fixture
def query_counter(db_session):
    """Count SQL queries executed during a test block.

    Usage:
        def test_orders_no_n_plus_one(client, query_counter):
            r = client.get("/orders?limit=10")
            assert r.status_code == 200
            assert query_counter["n"] <= 3, f"N+1 suspected: {query_counter['n']} queries"
    """
    counter = {"n": 0}
    bind = db_session.get_bind()

    @event.listens_for(bind, "before_cursor_execute")
    def _count(conn, cursor, statement, params, ctx, em):
        counter["n"] += 1

    yield counter

    event.remove(bind, "before_cursor_execute", _count)
