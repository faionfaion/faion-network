"""
pytest fixtures for Celery task testing.

Strategy:
- Unit tests: use celery_config fixture with ALWAYS_EAGER=True for fast feedback.
- Integration tests: use celery_worker fixture against a real Redis broker.
  Mark these @pytest.mark.integration and run in CI with a Redis service.

CAUTION: ALWAYS_EAGER hides broker bugs (visibility timeout, serializer mismatch).
At least one integration test per task should run against a real worker.
"""
import pytest
from celery import Celery
from celery.contrib.pytest import celery_config  # noqa: F401 — imported for fixture registration


@pytest.fixture(scope="session")
def celery_app():
    """Return the project Celery app for test sessions."""
    from config.celery import app
    return app


@pytest.fixture
def celery_eager(settings):
    """
    Run tasks synchronously in-process (no broker needed).
    Use for unit tests only. Hides broker-level bugs.
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    yield
    settings.CELERY_TASK_ALWAYS_EAGER = False


@pytest.fixture(scope="session")
def celery_worker_parameters():
    """
    Worker parameters for integration tests.
    Requires CELERY_BROKER_URL pointing at a real Redis.
    """
    return {
        "queues": ("default", "heavy"),
        "concurrency": 1,
        "loglevel": "warning",
    }


# Integration test example:
# @pytest.mark.integration
# def test_process_order_integration(celery_worker, order_factory):
#     order = order_factory(status=Order.Status.PENDING)
#     result = process_order.delay(order.id)
#     result.get(timeout=10)
#     order.refresh_from_db()
#     assert order.status == Order.Status.PROCESSED
