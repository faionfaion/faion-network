"""
factory_boy DjangoModelFactory scaffolds.
Location: apps/<domain>/tests/factories.py
"""
import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "users.User"  # Replace with actual model path

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker("name")
    is_active = True


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = "orders.Order"  # Replace with actual model path

    user = factory.SubFactory(UserFactory)
    status = "pending"
    # Use factory.LazyAttribute for computed fields:
    # total = factory.LazyAttribute(lambda o: Decimal("9.99"))
