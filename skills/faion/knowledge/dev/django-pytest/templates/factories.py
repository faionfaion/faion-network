# purpose: factory_boy factories template for BaseModel inheritors.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Place at tests/factories.py.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
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
