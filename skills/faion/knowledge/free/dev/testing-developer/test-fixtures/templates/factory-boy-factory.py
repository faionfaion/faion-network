"""
Factory Boy factories template.
Adapt models, fields, and subfactories to your domain.
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker

# from myapp.models import User, Profile, Product, Order

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Base user factory with sensible defaults."""

    class Meta:
        model = "auth.User"  # replace with your User model path
        django_get_or_create = ("email",)

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.LazyAttribute(lambda obj: obj.email.split("@")[0])
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False

    # Traits — opt in with UserFactory(admin=True)
    class Params:
        admin = factory.Trait(is_staff=True, is_superuser=True)
        inactive = factory.Trait(is_active=False)


# class ProfileFactory(DjangoModelFactory):
#     class Meta:
#         model = Profile
#
#     user = factory.SubFactory(UserFactory)
#     bio = factory.Faker("paragraph", nb_sentences=2)
#     avatar = factory.django.ImageField(color="blue", width=100, height=100)


# class ProductFactory(DjangoModelFactory):
#     class Meta:
#         model = Product
#
#     name = factory.Faker("catch_phrase")
#     description = factory.Faker("text", max_nb_chars=200)
#     price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
#     owner = factory.SubFactory(UserFactory)
#     sku = factory.Sequence(lambda n: f"SKU-{n:06d}")


# class OrderFactory(DjangoModelFactory):
#     class Meta:
#         model = Order
#
#     user = factory.SubFactory(UserFactory)
#     status = "pending"
#     total = factory.LazyAttribute(lambda obj: sum(i.price for i in obj.items.all()))
#
#     @factory.post_generation
#     def items(self, create, extracted, **kwargs):
#         if not create:
#             return
#         if extracted:
#             for item in extracted:
#                 self.items.add(item)
#         else:
#             ProductFactory.create_batch(2)
