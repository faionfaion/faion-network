# pytest-django Examples

Real-world testing patterns for Django applications with pytest.

---

## 1. Factory Boy Factories

### Basic Model Factory

```python
# tests/factories/users.py
import factory
from factory import fuzzy
from apps.users.models import User, Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Django 4.2+ optimization

    email = factory.Faker("email")
    name = factory.Faker("name")
    user_type = "regular"
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        # Use simple password for tests
        self.set_password(extracted or "testpass123")
        if create:
            self.save(update_fields=["password"])


class AdminUserFactory(UserFactory):
    user_type = "admin"
    is_staff = True
    is_superuser = True


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("text", max_nb_chars=200)
    avatar = factory.django.ImageField(width=100, height=100)
```

### Factory with Related Objects

```python
# tests/factories/orders.py
import factory
from decimal import Decimal
from apps.orders.models import Order, OrderItem
from apps.products.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.fuzzy.FuzzyDecimal(10.00, 100.00, precision=2)
    stock = factory.fuzzy.FuzzyInteger(1, 100)
    is_active = True


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    status = "pending"
    shipping_address = factory.Faker("address")

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                OrderItemFactory(order=self, **item)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 5)
    unit_price = factory.LazyAttribute(lambda o: o.product.price)
```

### Registering Factories as Fixtures

```python
# tests/conftest.py
from pytest_factoryboy import register
from tests.factories.users import UserFactory, AdminUserFactory, ProfileFactory
from tests.factories.orders import ProductFactory, OrderFactory, OrderItemFactory

# Register creates 'user', 'user_factory' fixtures automatically
register(UserFactory)
register(AdminUserFactory, _name="admin_user")
register(ProfileFactory)
register(ProductFactory)
register(OrderFactory)
register(OrderItemFactory)
```

---

## 2. Fixture Patterns

### API Client Fixtures

```python
# tests/conftest.py
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated DRF API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user) -> APIClient:
    """API client authenticated as regular user."""
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def admin_client(api_client, admin_user) -> APIClient:
    """API client authenticated as admin."""
    api_client.force_authenticate(user=admin_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def token_client(api_client, user):
    """API client with JWT token authentication."""
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    yield api_client
    api_client.credentials()
```

### Session-Scoped Data Fixtures

```python
# tests/conftest.py
import pytest


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Load initial data once per test session."""
    with django_db_blocker.unblock():
        # Load fixtures or create static data
        from django.core.management import call_command
        call_command("loaddata", "categories.json")


@pytest.fixture(scope="module")
def sample_products(db, product_factory):
    """Create sample products for a test module."""
    return [
        product_factory(name="Laptop", price=999.99),
        product_factory(name="Mouse", price=29.99),
        product_factory(name="Keyboard", price=79.99),
    ]
```

### Composed Fixtures

```python
# tests/fixtures/orders.py
import pytest


@pytest.fixture
def order_with_items(order_factory, product_factory):
    """Order with 3 items ready for checkout."""
    products = [product_factory() for _ in range(3)]
    order = order_factory(items=[
        {"product": p, "quantity": 2} for p in products
    ])
    return order


@pytest.fixture
def paid_order(order_with_items, payment_factory):
    """Order with completed payment."""
    payment_factory(
        order=order_with_items,
        status="completed",
        amount=order_with_items.total
    )
    order_with_items.status = "paid"
    order_with_items.save()
    return order_with_items


@pytest.fixture
def shipped_order(paid_order, shipment_factory):
    """Order that has been shipped."""
    shipment_factory(
        order=paid_order,
        tracking_number="TRACK123",
        carrier="FedEx"
    )
    paid_order.status = "shipped"
    paid_order.save()
    return paid_order
```

---

## 3. Unit Tests

### Testing Services

```python
# tests/unit/test_services.py
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from apps.orders.services import OrderService
from apps.orders.exceptions import InsufficientStockError


@pytest.mark.django_db
class TestOrderService:
    """Tests for OrderService.create_order()."""

    def test_creates_order_with_valid_items(self, user, product_factory):
        """Order is created with correct user and items."""
        product = product_factory(price=Decimal("50.00"), stock=10)

        order = OrderService.create_order(
            user=user,
            items=[{"product_id": product.id, "quantity": 2}]
        )

        assert order.user == user
        assert order.status == "pending"
        assert order.items.count() == 1

    def test_calculates_total_correctly(self, user, product_factory):
        """Order total equals sum of item prices."""
        product = product_factory(price=Decimal("25.00"))

        order = OrderService.create_order(
            user=user,
            items=[{"product_id": product.id, "quantity": 4}]
        )

        assert order.total == Decimal("100.00")

    def test_reduces_product_stock(self, user, product_factory):
        """Stock is reduced after order creation."""
        product = product_factory(stock=10)

        OrderService.create_order(
            user=user,
            items=[{"product_id": product.id, "quantity": 3}]
        )

        product.refresh_from_db()
        assert product.stock == 7

    def test_raises_error_for_insufficient_stock(self, user, product_factory):
        """InsufficientStockError for oversized orders."""
        product = product_factory(stock=5)

        with pytest.raises(InsufficientStockError) as exc_info:
            OrderService.create_order(
                user=user,
                items=[{"product_id": product.id, "quantity": 10}]
            )

        assert exc_info.value.product_id == product.id
        assert exc_info.value.available == 5

    @patch("apps.orders.services.send_order_confirmation")
    def test_sends_confirmation_email(self, mock_send, user, product_factory):
        """Confirmation email task is triggered."""
        product = product_factory()

        order = OrderService.create_order(
            user=user,
            items=[{"product_id": product.id, "quantity": 1}]
        )

        mock_send.delay.assert_called_once_with(order_id=order.id)
```

### Testing Models

```python
# tests/unit/test_models.py
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.orders.models import Order


@pytest.mark.django_db
class TestOrderModel:
    """Tests for Order model."""

    def test_str_representation(self, order_factory):
        """String representation includes order number."""
        order = order_factory()
        assert str(order) == f"Order #{order.order_number}"

    def test_auto_generates_order_number(self, order_factory):
        """Order number is auto-generated on save."""
        order = order_factory()
        assert order.order_number is not None
        assert len(order.order_number) == 12

    def test_total_is_sum_of_items(self, order_factory, order_item_factory):
        """Total property returns sum of item totals."""
        order = order_factory()
        order_item_factory(order=order, unit_price=Decimal("10"), quantity=2)
        order_item_factory(order=order, unit_price=Decimal("25"), quantity=1)

        assert order.total == Decimal("45.00")

    def test_cannot_cancel_shipped_order(self, order_factory):
        """Shipped orders cannot be cancelled."""
        order = order_factory(status="shipped")

        with pytest.raises(ValidationError, match="Cannot cancel"):
            order.cancel()

    def test_cancel_restores_stock(self, order_with_items):
        """Cancelling order restores product stock."""
        product = order_with_items.items.first().product
        original_stock = product.stock

        order_with_items.cancel()

        product.refresh_from_db()
        assert product.stock > original_stock
```

### Testing Validators

```python
# tests/unit/test_validators.py
import pytest
from apps.users.validators import validate_password, PasswordValidationResult


class TestPasswordValidator:
    """Tests for password validation."""

    @pytest.mark.parametrize("password,is_valid", [
        ("ValidPass123!", True),
        ("Another$ecure1", True),
        ("short1!", False),           # Too short
        ("nouppercase123!", False),   # No uppercase
        ("NOLOWERCASE123!", False),   # No lowercase
        ("NoDigitsHere!!", False),    # No digits
        ("NoSpecial123abc", False),   # No special char
    ])
    def test_password_validation(self, password, is_valid):
        """Password validation with various inputs."""
        result = validate_password(password)
        assert result.is_valid == is_valid

    @pytest.mark.parametrize("password,expected_errors", [
        ("short", ["too_short", "no_uppercase", "no_digit", "no_special"]),
        ("NoDigits!!", ["no_digit"]),
        ("nouppercaseorspecial1", ["no_uppercase", "no_special"]),
    ])
    def test_error_codes(self, password, expected_errors):
        """Validation returns correct error codes."""
        result = validate_password(password)
        assert set(result.error_codes) == set(expected_errors)
```

---

## 4. Integration Tests

### Testing API Endpoints

```python
# tests/integration/test_api_users.py
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestUserListAPI:
    """Tests for GET /api/v1/users/."""

    endpoint = "/api/v1/users/"

    def test_requires_authentication(self, api_client):
        """Returns 401 for unauthenticated requests."""
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_user_list(self, authenticated_client, user_factory):
        """Returns paginated list of users."""
        user_factory.create_batch(3)

        response = authenticated_client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) >= 3

    def test_filters_by_user_type(self, authenticated_client, user_factory, admin_user_factory):
        """Filters users by user_type query param."""
        user_factory.create_batch(2, user_type="regular")
        admin_user_factory.create_batch(2)

        response = authenticated_client.get(f"{self.endpoint}?user_type=admin")

        assert response.status_code == status.HTTP_200_OK
        assert all(u["user_type"] == "admin" for u in response.data["results"])


@pytest.mark.django_db
class TestUserCreateAPI:
    """Tests for POST /api/v1/users/."""

    endpoint = "/api/v1/users/"

    def test_admin_can_create_user(self, admin_client):
        """Admin can create new users."""
        payload = {
            "email": "newuser@example.com",
            "name": "New User",
            "user_type": "regular"
        }

        response = admin_client.post(self.endpoint, payload, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == payload["email"]

    def test_regular_user_cannot_create(self, authenticated_client):
        """Regular users get 403 Forbidden."""
        payload = {"email": "test@example.com", "name": "Test"}

        response = authenticated_client.post(self.endpoint, payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize("field,value,error", [
        ("email", "invalid", "Enter a valid email address"),
        ("email", "", "This field may not be blank"),
        ("name", "", "This field may not be blank"),
    ])
    def test_validation_errors(self, admin_client, field, value, error):
        """Returns validation errors for invalid data."""
        payload = {"email": "test@example.com", "name": "Test"}
        payload[field] = value

        response = admin_client.post(self.endpoint, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert error in str(response.data[field])


@pytest.mark.django_db
class TestUserDetailAPI:
    """Tests for GET/PATCH/DELETE /api/v1/users/{uid}/."""

    def test_get_user_by_uid(self, authenticated_client, user):
        """Retrieves user by UID."""
        response = authenticated_client.get(f"/api/v1/users/{user.uid}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["uid"] == str(user.uid)
        assert response.data["email"] == user.email

    def test_update_own_profile(self, authenticated_client, user):
        """User can update their own profile."""
        response = authenticated_client.patch(
            f"/api/v1/users/{user.uid}/",
            {"name": "Updated Name"},
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Name"

    def test_cannot_update_others(self, authenticated_client, user_factory):
        """Cannot update other user's profile."""
        other_user = user_factory()

        response = authenticated_client.patch(
            f"/api/v1/users/{other_user.uid}/",
            {"name": "Hacked"},
            format="json"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
```

### Testing with Transactions

```python
# tests/integration/test_transactions.py
import pytest
from django.db import transaction
from apps.orders.services import OrderService


@pytest.mark.django_db(transaction=True)
class TestOrderTransactions:
    """Tests requiring explicit transaction handling."""

    def test_rollback_on_payment_failure(self, user, product_factory):
        """Order is rolled back if payment fails."""
        product = product_factory(stock=10)
        original_stock = product.stock

        with pytest.raises(PaymentError):
            OrderService.create_order_with_payment(
                user=user,
                items=[{"product_id": product.id, "quantity": 2}],
                payment_token="failing_token"
            )

        # Verify rollback
        product.refresh_from_db()
        assert product.stock == original_stock

    def test_atomic_stock_update(self, user, product_factory):
        """Stock updates are atomic under concurrent access."""
        product = product_factory(stock=1)

        # Simulate concurrent order
        with pytest.raises(InsufficientStockError):
            with transaction.atomic():
                OrderService.create_order(
                    user=user,
                    items=[{"product_id": product.id, "quantity": 1}]
                )
                # Simulate another process taking the stock
                product.stock = 0
                product.save()
                # This should fail
                OrderService.create_order(
                    user=user,
                    items=[{"product_id": product.id, "quantity": 1}]
                )
```

---

## 5. Mocking External Services

### Mocking with unittest.mock

```python
# tests/unit/test_payments.py
import pytest
from unittest.mock import patch, MagicMock
from apps.payments.services import PaymentService


class TestPaymentService:
    """Tests for PaymentService with mocked Stripe."""

    @patch("apps.payments.services.stripe")
    def test_creates_stripe_charge(self, mock_stripe, order):
        """Creates Stripe charge with correct parameters."""
        mock_stripe.Charge.create.return_value = MagicMock(
            id="ch_123",
            status="succeeded"
        )

        result = PaymentService.process_payment(
            order=order,
            token="tok_visa"
        )

        mock_stripe.Charge.create.assert_called_once_with(
            amount=int(order.total * 100),  # Cents
            currency="usd",
            source="tok_visa",
            metadata={"order_id": str(order.uid)}
        )
        assert result.stripe_charge_id == "ch_123"

    @patch("apps.payments.services.stripe")
    def test_handles_stripe_error(self, mock_stripe, order):
        """Handles Stripe API errors gracefully."""
        import stripe
        mock_stripe.Charge.create.side_effect = stripe.error.CardError(
            message="Card declined",
            param="card",
            code="card_declined"
        )

        with pytest.raises(PaymentError) as exc_info:
            PaymentService.process_payment(order=order, token="tok_declined")

        assert "Card declined" in str(exc_info.value)
```

### Mocking HTTP with responses

```python
# tests/unit/test_webhooks.py
import pytest
import responses
from apps.integrations.services import WebhookService


class TestWebhookService:
    """Tests for external webhook calls."""

    @responses.activate
    def test_sends_webhook_notification(self, order):
        """Sends webhook with correct payload."""
        responses.add(
            responses.POST,
            "https://api.partner.com/webhooks/orders",
            json={"status": "received"},
            status=200
        )

        result = WebhookService.notify_order_created(order)

        assert result["status"] == "received"
        assert len(responses.calls) == 1

        request_body = responses.calls[0].request.body
        assert order.order_number in request_body

    @responses.activate
    def test_retries_on_failure(self, order):
        """Retries webhook on temporary failure."""
        responses.add(
            responses.POST,
            "https://api.partner.com/webhooks/orders",
            status=503
        )
        responses.add(
            responses.POST,
            "https://api.partner.com/webhooks/orders",
            json={"status": "received"},
            status=200
        )

        result = WebhookService.notify_order_created(order, max_retries=2)

        assert len(responses.calls) == 2
        assert result["status"] == "received"
```

### Mocking Time with freezegun

```python
# tests/unit/test_expiration.py
import pytest
from freezegun import freeze_time
from datetime import datetime, timedelta
from apps.coupons.models import Coupon


@pytest.mark.django_db
class TestCouponExpiration:
    """Tests for coupon expiration logic."""

    @freeze_time("2025-01-15 12:00:00")
    def test_coupon_is_valid_before_expiry(self, coupon_factory):
        """Coupon is valid before expiration date."""
        coupon = coupon_factory(
            expires_at=datetime(2025, 1, 20, 12, 0, 0)
        )

        assert coupon.is_valid() is True

    @freeze_time("2025-01-25 12:00:00")
    def test_coupon_is_expired_after_date(self, coupon_factory):
        """Coupon is invalid after expiration date."""
        coupon = coupon_factory(
            expires_at=datetime(2025, 1, 20, 12, 0, 0)
        )

        assert coupon.is_valid() is False

    def test_coupon_expires_correctly(self, coupon_factory):
        """Coupon validity changes over time."""
        coupon = coupon_factory(
            expires_at=datetime(2025, 6, 1, 0, 0, 0)
        )

        with freeze_time("2025-05-31"):
            assert coupon.is_valid() is True

        with freeze_time("2025-06-02"):
            assert coupon.is_valid() is False
```

---

## 6. Async Tests

### Testing Async Views

```python
# tests/integration/test_async_views.py
import pytest
from asgiref.sync import sync_to_async


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_async_user_lookup(async_client, user_factory):
    """Test async view with async client."""

    @sync_to_async
    def create_user():
        return user_factory()

    user = await create_user()

    response = await async_client.get(f"/api/v1/users/{user.uid}/")

    assert response.status_code == 200
```

### Testing Celery Tasks

```python
# tests/unit/test_tasks.py
import pytest
from unittest.mock import patch
from apps.orders.tasks import send_order_confirmation


@pytest.mark.django_db
class TestOrderTasks:
    """Tests for Celery tasks."""

    @patch("apps.orders.tasks.send_mail")
    def test_sends_confirmation_email(self, mock_send_mail, order):
        """send_order_confirmation sends email."""
        send_order_confirmation(order_id=order.id)

        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args.kwargs
        assert order.user.email in call_kwargs["recipient_list"]
        assert order.order_number in call_kwargs["subject"]

    def test_handles_missing_order(self):
        """Task handles non-existent order gracefully."""
        # Should not raise, just log warning
        result = send_order_confirmation(order_id=99999)
        assert result is None
```

---

## 7. Testing Permissions

```python
# tests/integration/test_permissions.py
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestOrderPermissions:
    """Permission tests for Order API."""

    def test_anonymous_cannot_list_orders(self, api_client):
        """Anonymous users get 401."""
        response = api_client.get("/api/v1/orders/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_sees_only_own_orders(self, authenticated_client, user, order_factory, user_factory):
        """Users only see their own orders."""
        # User's orders
        order_factory.create_batch(2, user=user)
        # Other user's orders
        other = user_factory()
        order_factory.create_batch(3, user=other)

        response = authenticated_client.get("/api/v1/orders/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_admin_sees_all_orders(self, admin_client, order_factory):
        """Admins see all orders."""
        order_factory.create_batch(5)

        response = admin_client.get("/api/v1/orders/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 5

    def test_cannot_access_other_users_order(self, authenticated_client, order_factory, user_factory):
        """403 when accessing another user's order."""
        other_user = user_factory()
        order = order_factory(user=other_user)

        response = authenticated_client.get(f"/api/v1/orders/{order.uid}/")

        assert response.status_code == status.HTTP_403_FORBIDDEN
```
