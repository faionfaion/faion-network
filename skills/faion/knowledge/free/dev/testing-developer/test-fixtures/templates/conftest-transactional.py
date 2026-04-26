"""
Transactional rollback fixture for pytest-django.
Each test wraps DB changes in a transaction that is rolled back at the end.
This is faster than recreating the database or using truncation.

Usage: Place in tests/conftest.py and enable with the `transactional_db` fixture
or set `django_db_reset_sequences = True` if needed.
"""
import pytest


# ---- Standard pytest-django DB fixture (non-transactional, recommended default) ----

@pytest.fixture(autouse=True)
def db_access(db):
    """
    Allow DB access in all tests without @pytest.mark.django_db.
    Remove autouse=True if you prefer explicit opt-in per test.
    """
    pass


# ---- Transactional rollback fixture (SQLAlchemy) ----
# Wraps each test in a SAVEPOINT so the main transaction is never committed.

@pytest.fixture(scope="session")
def db_engine():
    """Session-scoped engine — created once for the entire test run."""
    from sqlalchemy import create_engine
    from myapp.db import Base, DATABASE_URL  # adapt to your project

    engine = create_engine(DATABASE_URL.replace("://", "+psycopg2://"))
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine):
    """
    Function-scoped DB session with rollback.
    Each test gets a clean slate via SAVEPOINT.
    """
    from sqlalchemy.orm import sessionmaker

    connection = db_engine.connect()
    outer_transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    # Nested transaction (SAVEPOINT)
    nested = connection.begin_nested()
    session.begin_nested()

    yield session

    session.close()
    nested.rollback()
    outer_transaction.rollback()
    connection.close()


# ---- Django: separate DB per xdist worker ----

# @pytest.fixture(scope="session")
# def django_db_setup(worker_id, django_test_environment, django_db_blocker):
#     from django.conf import settings
#     db_name = f"test_{settings.DATABASES['default']['NAME']}"
#     if worker_id != "master":
#         db_name = f"{db_name}_{worker_id}"
#     settings.DATABASES["default"]["TEST"] = {"NAME": db_name}
#     with django_db_blocker.unblock():
#         from django.test.utils import setup_databases
#         setup_databases(verbosity=0, interactive=False)
