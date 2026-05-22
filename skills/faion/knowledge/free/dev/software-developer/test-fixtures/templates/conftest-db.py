# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
conftest-db.py — SQLAlchemy database fixtures with savepoint rollback.
Each test gets a clean state without DROP/CREATE overhead.
Copy to tests/conftest.py and adapt to your ORM setup.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models import Base


@pytest.fixture(scope="session")
def engine():
    """Create database engine once for the test session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine):
    """Session factory shared across all tests."""
    return sessionmaker(bind=engine)


@pytest.fixture
def db_session(session_factory):
    """
    Transactional test session: each test gets a savepoint.
    Rolls back to savepoint after test — no data leaks between tests.
    """
    session = session_factory()
    session.begin_nested()  # Create savepoint

    yield session

    session.rollback()  # Roll back to savepoint
    session.close()
