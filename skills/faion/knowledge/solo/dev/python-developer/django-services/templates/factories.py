"""
factory_boy model factories for Django services tests.

Rules:
- One factory per model, in tests/factories.py
- Use factory.SubFactory for FK relations
- Override only in test that needs the specific state
- Use factory.LazyAttribute for computed fields
- Do NOT commit generated fixture files
"""
import factory
from factory.django import DjangoModelFactory

from apps.users.models import User
from apps.products.models import Product
from apps.orders.models import Order


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    stock = 100


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
    status = Order.Status.PENDING


# Test usage example:
# def test_order_cancel():
#     order = OrderFactory(status=Order.Status.PENDING)
#     result = order_cancel(order=order, reason="Customer request")
#     assert result.status == Order.Status.CANCELLED
