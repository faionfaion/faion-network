"""
purpose: Tests composing the fixtures.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import pytest


@pytest.fixture
def make_user():
    """Factory fixture: returns a callable that creates a user dict."""

    def _make(name: str = "demo", **extra):
        return {"name": name, **extra}

    return _make


def test_factory_fixture_creates_user(make_user):
    user = make_user(name="alice", role="admin")
    assert user == {"name": "alice", "role": "admin"}
