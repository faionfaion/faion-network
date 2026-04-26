"""
conftest.py — Session-scoped Testcontainers Postgres + per-test transaction-rollback fixture.

Usage: place at tests/conftest.py or tests/integration/conftest.py.
Requires: testcontainers[postgres], sqlalchemy, pytest
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from app.db import Base  # Replace with your app's Base


@pytest.fixture(scope="session")
def _engine():
    """Start one Postgres container for the whole test session."""
    with PostgresContainer("postgres:16.2") as pg:
        eng = create_engine(pg.get_connection_url())
        Base.metadata.create_all(eng)
        yield eng


@pytest.fixture
def db_session(_engine):
    """Per-test session that rolls back on teardown — fastest viable isolation."""
    conn = _engine.connect()
    tx = conn.begin()
    Session = sessionmaker(bind=conn)
    s = Session()
    try:
        yield s
    finally:
        s.close()
        tx.rollback()
        conn.close()
