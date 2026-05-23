# purpose: Django + Factory Boy conftest emitted from integration-testing
# consumes: pytest-django, factory-boy installed; User model importable
# produces: UserFactory + user + admin_user fixtures with savepoint rollback
# depends-on: r1-rollback-default, r5-factory-uniqueness
# token-budget-impact: ~250 tokens
"""
conftest.py — Django integration test setup with Factory Boy.
Requires: pytest-django, factory-boy
"""
import factory
import pytest
from factory.django import DjangoModelFactory

from myapp.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def admin_user(db):
    return UserFactory(is_staff=True, is_superuser=True)
