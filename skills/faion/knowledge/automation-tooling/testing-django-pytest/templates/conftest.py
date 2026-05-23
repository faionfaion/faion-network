# purpose: factory_boy factories + pytest fixtures
# consumes: input artefacts described in AGENTS.md ## Prerequisites
# produces: artefact conforming to content/02-output-contract.xml for testing-django-pytest
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1200 tokens when loaded as context

import pytest
import factory
from django.contrib.auth import get_user_model
from orders.models import Order


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory)
    amount = 1000
    status = 'pending'


@pytest.fixture
def order(db):
    return OrderFactory()
