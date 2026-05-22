# purpose: Postgres + rollback conftest emitted from integration-testing decision-record
# consumes: testcontainers + sqlalchemy installed; Base.metadata defined
# produces: session-scoped engine, function-scoped Session with rollback teardown
# depends-on: r1-rollback-default, r2-container-scoping
# token-budget-impact: ~300 tokens
"""
conftest.py — PostgreSQL integration test setup.
Session-scoped Testcontainers container + function-scoped transaction rollback.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.models import Base


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container once per test session."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    """Create SQLAlchemy engine and all tables."""
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Fresh session per test with automatic transaction rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    db = Session()

    yield db

    db.close()
    transaction.rollback()
    connection.close()
