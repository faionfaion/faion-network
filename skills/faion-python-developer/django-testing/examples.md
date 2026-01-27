# Django Testing Examples

Real-world test examples for Django applications using pytest-django, Factory Boy, and model_bakery.

## Table of Contents

1. [Model Tests](#model-tests)
2. [Service Tests](#service-tests)
3. [View Tests](#view-tests)
4. [API Tests (DRF)](#api-tests-drf)
5. [Factory Patterns](#factory-patterns)
6. [Fixture Patterns](#fixture-patterns)
7. [Parametrized Tests](#parametrized-tests)
8. [Transaction Tests](#transaction-tests)
9. [Signal Tests](#signal-tests)
10. [Async Tests](#async-tests)

---

## Model Tests

### Basic Model Test with model_bakery

```python
import pytest
from model_bakery import baker

from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:
    """Tests for User model."""

    def test_create_user(self):
        """Test basic user creation."""
        user = baker.make(User, email='test@example.com')

        assert user.pk is not None
        assert user.email == 'test@example.com'

    def test_user_str(self):
        """Test User.__str__ method."""
        user = baker.make(User, email='john@example.com', first_name='John')

        assert str(user) == 'john@example.com'

    def test_user_full_name(self):
        """Test User.full_name property."""
        user = baker.make(User, first_name='John', last_name='Doe')

        assert user.full_name == 'John Doe'

    def test_user_full_name_empty_last(self):
        """Test full_name when last_name is empty."""
        user = baker.make(User, first_name='John', last_name='')

        assert user.full_name == 'John'
```

### Model with Relationships

```python
import pytest
from model_bakery import baker

from apps.blog.models import Post, Comment


@pytest.mark.django_db
class TestPostModel:
    """Tests for Post model."""

    def test_post_with_author(self):
        """Test post creation with author."""
        post = baker.make('blog.Post', title='Test Post')

        assert post.author is not None
        assert post.title == 'Test Post'

    def test_post_comment_count(self):
        """Test Post.comment_count property."""
        post = baker.make('blog.Post')
        baker.make('blog.Comment', post=post, _quantity=3)

        assert post.comment_count == 3

    def test_post_is_published(self):
        """Test Post.is_published for draft."""
        post = baker.make('blog.Post', status='draft')

        assert post.is_published is False

    def test_post_is_published_true(self):
        """Test Post.is_published for published."""
        post = baker.make('blog.Post', status='published')

        assert post.is_published is True
```

### Testing Model Managers

```python
import pytest
from model_bakery import baker
from django.utils import timezone

from apps.blog.models import Post


@pytest.mark.django_db
class TestPostManager:
    """Tests for Post.objects manager methods."""

    def test_published_returns_only_published(self):
        """Test published() queryset method."""
        published = baker.make('blog.Post', status='published', _quantity=2)
        baker.make('blog.Post', status='draft')

        result = Post.objects.published()

        assert result.count() == 2
        assert all(p.status == 'published' for p in result)

    def test_by_author(self):
        """Test by_author() queryset method."""
        author = baker.make('users.User')
        baker.make('blog.Post', author=author, _quantity=3)
        baker.make('blog.Post')  # Different author

        result = Post.objects.by_author(author)

        assert result.count() == 3

    def test_recent_posts(self):
        """Test recent() returns ordered by date."""
        old = baker.make('blog.Post', published_at=timezone.now() - timezone.timedelta(days=7))
        new = baker.make('blog.Post', published_at=timezone.now())

        result = list(Post.objects.recent())

        assert result[0] == new
        assert result[1] == old
```

---

## Service Tests

### Basic Service Test

```python
import pytest
from model_bakery import baker
from decimal import Decimal

from apps.orders.models import Order, OrderItem
from apps.orders.services import OrderService


@pytest.mark.django_db
class TestOrderService:
    """Tests for OrderService."""

    def test_create_order_success(self):
        """Test successful order creation."""
        user = baker.make('users.User')
        product = baker.make('products.Product', price=Decimal('99.99'))

        order = OrderService.create_order(
            user=user,
            items=[{'product_id': product.id, 'quantity': 2}]
        )

        assert order.pk is not None
        assert order.user == user
        assert order.total == Decimal('199.98')
        assert order.items.count() == 1

    def test_create_order_empty_items_raises(self):
        """Test that empty items raises ValueError."""
        user = baker.make('users.User')

        with pytest.raises(ValueError, match='Order must have at least one item'):
            OrderService.create_order(user=user, items=[])

    def test_create_order_invalid_product_raises(self):
        """Test that invalid product_id raises."""
        user = baker.make('users.User')

        with pytest.raises(Product.DoesNotExist):
            OrderService.create_order(
                user=user,
                items=[{'product_id': 99999, 'quantity': 1}]
            )

    def test_cancel_order_success(self):
        """Test successful order cancellation."""
        order = baker.make('orders.Order', status='pending')

        result = OrderService.cancel_order(order)

        assert result.status == 'cancelled'

    def test_cancel_order_already_shipped_raises(self):
        """Test that cancelling shipped order raises."""
        order = baker.make('orders.Order', status='shipped')

        with pytest.raises(ValueError, match='Cannot cancel shipped order'):
            OrderService.cancel_order(order)
```

### Service with External Dependencies

```python
import pytest
from unittest.mock import Mock, patch
from model_bakery import baker

from apps.payments.services import PaymentService


@pytest.mark.django_db
class TestPaymentService:
    """Tests for PaymentService with external API."""

    def test_process_payment_success(self):
        """Test successful payment processing."""
        order = baker.make('orders.Order', total=Decimal('100.00'))

        with patch('apps.payments.services.stripe') as mock_stripe:
            mock_stripe.PaymentIntent.create.return_value = Mock(
                id='pi_123',
                status='succeeded'
            )

            result = PaymentService.process_payment(order)

            assert result.stripe_payment_id == 'pi_123'
            assert result.status == 'completed'
            mock_stripe.PaymentIntent.create.assert_called_once()

    def test_process_payment_failure(self):
        """Test payment processing failure."""
        order = baker.make('orders.Order', total=Decimal('100.00'))

        with patch('apps.payments.services.stripe') as mock_stripe:
            mock_stripe.PaymentIntent.create.side_effect = stripe.error.CardError(
                message='Card declined',
                param='card',
                code='card_declined'
            )

            with pytest.raises(PaymentError, match='Card declined'):
                PaymentService.process_payment(order)
```

---

## View Tests

### Function-Based View Tests

```python
import pytest
from django.urls import reverse
from model_bakery import baker


@pytest.mark.django_db
class TestPostListView:
    """Tests for post list view."""

    def test_list_view_returns_200(self, client):
        """Test list view renders successfully."""
        response = client.get(reverse('posts:list'))

        assert response.status_code == 200

    def test_list_view_shows_published_posts(self, client):
        """Test list view shows only published posts."""
        published = baker.make('blog.Post', status='published', title='Published')
        draft = baker.make('blog.Post', status='draft', title='Draft')

        response = client.get(reverse('posts:list'))

        assert 'Published' in response.content.decode()
        assert 'Draft' not in response.content.decode()

    def test_list_view_pagination(self, client):
        """Test list view pagination."""
        baker.make('blog.Post', status='published', _quantity=25)

        response = client.get(reverse('posts:list'))

        assert response.context['is_paginated'] is True
        assert len(response.context['posts']) == 10


@pytest.mark.django_db
class TestPostDetailView:
    """Tests for post detail view."""

    def test_detail_view_returns_200(self, client):
        """Test detail view for existing post."""
        post = baker.make('blog.Post', status='published')

        response = client.get(reverse('posts:detail', kwargs={'pk': post.pk}))

        assert response.status_code == 200

    def test_detail_view_draft_returns_404(self, client):
        """Test detail view returns 404 for draft."""
        post = baker.make('blog.Post', status='draft')

        response = client.get(reverse('posts:detail', kwargs={'pk': post.pk}))

        assert response.status_code == 404

    def test_detail_view_not_found(self, client):
        """Test detail view returns 404 for missing post."""
        response = client.get(reverse('posts:detail', kwargs={'pk': 99999}))

        assert response.status_code == 404
```

### Class-Based View Tests with Authentication

```python
import pytest
from django.urls import reverse
from model_bakery import baker


@pytest.fixture
def logged_in_client(client, db):
    """Client with authenticated user."""
    user = baker.make('users.User')
    client.force_login(user)
    client.user = user
    return client


@pytest.mark.django_db
class TestPostCreateView:
    """Tests for post creation view."""

    def test_create_requires_login(self, client):
        """Test create view requires authentication."""
        response = client.get(reverse('posts:create'))

        assert response.status_code == 302
        assert '/login/' in response.url

    def test_create_get_renders_form(self, logged_in_client):
        """Test create view renders form."""
        response = logged_in_client.get(reverse('posts:create'))

        assert response.status_code == 200
        assert 'form' in response.context

    def test_create_post_success(self, logged_in_client):
        """Test successful post creation."""
        response = logged_in_client.post(
            reverse('posts:create'),
            data={
                'title': 'New Post',
                'content': 'Post content here',
                'status': 'draft',
            }
        )

        assert response.status_code == 302
        assert Post.objects.filter(title='New Post').exists()

    def test_create_post_invalid_data(self, logged_in_client):
        """Test create with invalid data shows errors."""
        response = logged_in_client.post(
            reverse('posts:create'),
            data={'title': '', 'content': ''}
        )

        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors
```

---

## API Tests (DRF)

### Basic API Tests

```python
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def api_client():
    """DRF API client."""
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, db):
    """API client with authenticated user."""
    user = baker.make('users.User')
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client


@pytest.mark.django_db
class TestPostAPI:
    """Tests for Post API endpoints."""

    def test_list_posts(self, api_client):
        """Test GET /api/posts/ returns posts."""
        baker.make('blog.Post', status='published', _quantity=3)

        response = api_client.get('/api/posts/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_list_posts_pagination(self, api_client):
        """Test pagination works correctly."""
        baker.make('blog.Post', status='published', _quantity=25)

        response = api_client.get('/api/posts/')

        assert response.status_code == status.HTTP_200_OK
        assert 'next' in response.data
        assert response.data['count'] == 25

    def test_retrieve_post(self, api_client):
        """Test GET /api/posts/{id}/ returns post."""
        post = baker.make('blog.Post', status='published')

        response = api_client.get(f'/api/posts/{post.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.pk
        assert response.data['title'] == post.title

    def test_create_post_authenticated(self, authenticated_api_client):
        """Test POST /api/posts/ creates post."""
        response = authenticated_api_client.post('/api/posts/', data={
            'title': 'API Created Post',
            'content': 'Content here',
            'status': 'draft',
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'API Created Post'
        assert response.data['author'] == authenticated_api_client.user.id

    def test_create_post_unauthenticated(self, api_client):
        """Test POST /api/posts/ requires auth."""
        response = api_client.post('/api/posts/', data={
            'title': 'Test',
            'content': 'Content',
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_own_post(self, authenticated_api_client):
        """Test PATCH /api/posts/{id}/ updates own post."""
        post = baker.make('blog.Post', author=authenticated_api_client.user)

        response = authenticated_api_client.patch(
            f'/api/posts/{post.pk}/',
            data={'title': 'Updated Title'}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'

    def test_update_others_post_forbidden(self, authenticated_api_client):
        """Test cannot update other user's post."""
        other_user = baker.make('users.User')
        post = baker.make('blog.Post', author=other_user)

        response = authenticated_api_client.patch(
            f'/api/posts/{post.pk}/',
            data={'title': 'Hacked Title'}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_own_post(self, authenticated_api_client):
        """Test DELETE /api/posts/{id}/ deletes own post."""
        post = baker.make('blog.Post', author=authenticated_api_client.user)

        response = authenticated_api_client.delete(f'/api/posts/{post.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(pk=post.pk).exists()
```

### Testing Serializers

```python
import pytest
from model_bakery import baker

from apps.blog.serializers import PostSerializer, PostCreateSerializer


@pytest.mark.django_db
class TestPostSerializer:
    """Tests for PostSerializer."""

    def test_serializer_output(self):
        """Test serializer produces expected output."""
        post = baker.make('blog.Post', title='Test')
        serializer = PostSerializer(post)

        assert serializer.data['id'] == post.pk
        assert serializer.data['title'] == 'Test'
        assert 'author_name' in serializer.data
        assert 'content' in serializer.data

    def test_serializer_hides_sensitive_fields(self):
        """Test sensitive fields are not exposed."""
        post = baker.make('blog.Post')
        serializer = PostSerializer(post)

        assert 'internal_notes' not in serializer.data


@pytest.mark.django_db
class TestPostCreateSerializer:
    """Tests for PostCreateSerializer validation."""

    def test_valid_data(self):
        """Test serializer accepts valid data."""
        user = baker.make('users.User')
        data = {
            'title': 'Valid Title',
            'content': 'Valid content here',
            'status': 'draft',
        }
        serializer = PostCreateSerializer(data=data, context={'user': user})

        assert serializer.is_valid(), serializer.errors

    def test_title_too_long(self):
        """Test title length validation."""
        data = {
            'title': 'A' * 300,  # Exceeds max_length
            'content': 'Content',
        }
        serializer = PostCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert 'title' in serializer.errors

    def test_content_required(self):
        """Test content is required."""
        data = {'title': 'Title'}
        serializer = PostCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert 'content' in serializer.errors
```

---

## Factory Patterns

### Basic Factory Boy Factory

```python
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.users.models import User
from apps.blog.models import Post, Comment

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True

    # Password handling
    password = factory.django.Password('testpass123')

    class Params:
        """Traits for different user types."""
        admin = factory.Trait(
            is_staff=True,
            is_superuser=True,
            email=factory.Sequence(lambda n: f'admin{n}@example.com')
        )
        inactive = factory.Trait(is_active=False)


class PostFactory(DjangoModelFactory):
    """Factory for Post model."""

    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=6)
    content = factory.Faker('paragraphs', nb=3)
    author = factory.SubFactory(UserFactory)
    status = 'draft'

    class Params:
        published = factory.Trait(
            status='published',
            published_at=factory.LazyFunction(timezone.now)
        )


class CommentFactory(DjangoModelFactory):
    """Factory for Comment model."""

    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker('paragraph')
```

### Using Factories in Tests

```python
import pytest
from tests.factories import UserFactory, PostFactory


@pytest.mark.django_db
class TestWithFactories:
    """Tests using Factory Boy."""

    def test_create_user(self):
        """Test basic factory usage."""
        user = UserFactory()

        assert user.pk is not None
        assert '@example.com' in user.email

    def test_create_admin(self):
        """Test factory with trait."""
        admin = UserFactory(admin=True)

        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_override_fields(self):
        """Test overriding factory fields."""
        user = UserFactory(
            email='custom@example.com',
            first_name='Custom'
        )

        assert user.email == 'custom@example.com'
        assert user.first_name == 'Custom'

    def test_create_batch(self):
        """Test creating multiple objects."""
        users = UserFactory.create_batch(5)

        assert len(users) == 5
        assert len(set(u.email for u in users)) == 5  # All unique

    def test_build_without_save(self):
        """Test build() doesn't save to DB."""
        user = UserFactory.build()

        assert user.pk is None

    def test_post_with_author(self):
        """Test SubFactory creates related object."""
        post = PostFactory()

        assert post.author is not None
        assert post.author.pk is not None

    def test_post_with_specific_author(self):
        """Test passing related object to factory."""
        author = UserFactory()
        post = PostFactory(author=author)

        assert post.author == author
```

### pytest-factoryboy Integration

```python
# conftest.py
import pytest
from pytest_factoryboy import register
from tests.factories import UserFactory, PostFactory

# Register factories as fixtures
register(UserFactory)  # Creates 'user' fixture
register(PostFactory)  # Creates 'post' fixture
register(UserFactory, 'admin_user', admin=True)  # Named fixture with trait


# Usage in tests
@pytest.mark.django_db
def test_with_registered_factory(user):
    """Factory is injected as fixture."""
    assert user.is_active is True


@pytest.mark.django_db
def test_with_admin(admin_user):
    """Named fixture with trait."""
    assert admin_user.is_staff is True
```

---

## Fixture Patterns

### Shared Fixtures in conftest.py

```python
# conftest.py
import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def api_client():
    """DRF API client instance."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return baker.make('users.User', is_active=True)


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return baker.make('users.User', is_staff=True, is_superuser=True)


@pytest.fixture
def authenticated_client(client, user):
    """Django test client logged in as user."""
    client.force_login(user)
    client.user = user
    return client


@pytest.fixture
def authenticated_api_client(api_client, user):
    """DRF client authenticated as user."""
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client


@pytest.fixture
def sample_post(db, user):
    """Create a sample published post."""
    return baker.make(
        'blog.Post',
        author=user,
        status='published',
        title='Sample Post'
    )
```

### Fixture with Cleanup

```python
import pytest
import tempfile
import shutil


@pytest.fixture
def temp_media_root(settings):
    """Temporary media root for file upload tests."""
    temp_dir = tempfile.mkdtemp()
    settings.MEDIA_ROOT = temp_dir
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.mark.django_db
def test_file_upload(authenticated_api_client, temp_media_root):
    """Test file upload with cleanup."""
    with open('test.txt', 'w') as f:
        f.write('test content')

    with open('test.txt', 'rb') as f:
        response = authenticated_api_client.post(
            '/api/files/',
            {'file': f},
            format='multipart'
        )

    assert response.status_code == 201
    # temp_media_root is cleaned up automatically
```

---

## Parametrized Tests

### Basic Parametrization

```python
import pytest
from decimal import Decimal


@pytest.mark.django_db
@pytest.mark.parametrize('amount,expected_fee', [
    (Decimal('10.00'), Decimal('0.30')),
    (Decimal('100.00'), Decimal('3.00')),
    (Decimal('1000.00'), Decimal('30.00')),
])
def test_calculate_fee(amount, expected_fee):
    """Test fee calculation for different amounts."""
    result = calculate_fee(amount)
    assert result == expected_fee


@pytest.mark.parametrize('status,is_active', [
    ('active', True),
    ('inactive', False),
    ('pending', False),
    ('suspended', False),
])
def test_user_is_active(status, is_active):
    """Test is_active for different statuses."""
    user = baker.make('users.User', status=status)
    assert user.is_active == is_active
```

### Parametrized with IDs

```python
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('input_data,expected_error', [
    pytest.param(
        {'email': ''},
        'email',
        id='empty_email'
    ),
    pytest.param(
        {'email': 'invalid'},
        'email',
        id='invalid_email_format'
    ),
    pytest.param(
        {'email': 'test@example.com', 'password': ''},
        'password',
        id='empty_password'
    ),
    pytest.param(
        {'email': 'test@example.com', 'password': '123'},
        'password',
        id='password_too_short'
    ),
], ids=str)
def test_registration_validation(api_client, input_data, expected_error):
    """Test registration validation errors."""
    response = api_client.post('/api/register/', data=input_data)

    assert response.status_code == 400
    assert expected_error in response.data
```

### Parametrized API Status Codes

```python
import pytest
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize('method,expected_status', [
    ('get', status.HTTP_200_OK),
    ('post', status.HTTP_405_METHOD_NOT_ALLOWED),
    ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
    ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
])
def test_read_only_endpoint(api_client, method, expected_status):
    """Test endpoint only allows GET."""
    response = getattr(api_client, method)('/api/readonly/')
    assert response.status_code == expected_status
```

---

## Transaction Tests

### Testing Atomic Operations

```python
import pytest
from django.db import transaction
from model_bakery import baker


@pytest.mark.django_db(transaction=True)
def test_atomic_transfer():
    """Test atomic money transfer."""
    account_a = baker.make('accounts.Account', balance=Decimal('100.00'))
    account_b = baker.make('accounts.Account', balance=Decimal('0.00'))

    with transaction.atomic():
        transfer(from_account=account_a, to_account=account_b, amount=Decimal('50.00'))

    account_a.refresh_from_db()
    account_b.refresh_from_db()

    assert account_a.balance == Decimal('50.00')
    assert account_b.balance == Decimal('50.00')


@pytest.mark.django_db(transaction=True)
def test_transaction_rollback_on_error():
    """Test transaction rolls back on error."""
    account_a = baker.make('accounts.Account', balance=Decimal('100.00'))
    account_b = baker.make('accounts.Account', balance=Decimal('0.00'))

    with pytest.raises(InsufficientFunds):
        transfer(
            from_account=account_a,
            to_account=account_b,
            amount=Decimal('500.00')  # More than balance
        )

    account_a.refresh_from_db()
    account_b.refresh_from_db()

    # Balances unchanged due to rollback
    assert account_a.balance == Decimal('100.00')
    assert account_b.balance == Decimal('0.00')
```

### Testing select_for_update

```python
import pytest
from django.db import connection
from concurrent.futures import ThreadPoolExecutor


@pytest.mark.django_db(transaction=True)
def test_concurrent_updates():
    """Test that select_for_update prevents race conditions."""
    account = baker.make('accounts.Account', balance=Decimal('100.00'))

    def withdraw():
        with transaction.atomic():
            acc = Account.objects.select_for_update().get(pk=account.pk)
            if acc.balance >= Decimal('60.00'):
                acc.balance -= Decimal('60.00')
                acc.save()
                return True
            return False

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: withdraw(), range(2)))

    account.refresh_from_db()

    # Only one withdrawal should succeed
    assert results.count(True) == 1
    assert account.balance == Decimal('40.00')
```

---

## Signal Tests

### Testing Post-Save Signals

```python
import pytest
from unittest.mock import patch
from model_bakery import baker


@pytest.mark.django_db
class TestUserSignals:
    """Tests for User model signals."""

    @patch('apps.users.signals.send_welcome_email')
    def test_welcome_email_sent_on_create(self, mock_send):
        """Test welcome email is sent when user is created."""
        user = baker.make('users.User')

        mock_send.assert_called_once_with(user.email)

    @patch('apps.users.signals.send_welcome_email')
    def test_welcome_email_not_sent_on_update(self, mock_send):
        """Test welcome email is not sent on update."""
        user = baker.make('users.User')
        mock_send.reset_mock()

        user.first_name = 'Updated'
        user.save()

        mock_send.assert_not_called()


@pytest.mark.django_db
def test_mute_signals():
    """Test using mute_signals context manager."""
    from factory.django import mute_signals
    from django.db.models.signals import post_save

    with mute_signals(post_save):
        # Create user without triggering signals
        user = baker.make('users.User')

    # Verify signal side effects didn't happen
    assert not WelcomeEmail.objects.filter(user=user).exists()
```

---

## Async Tests

### Testing Async Views

```python
import pytest
from django.test import AsyncClient
from model_bakery import baker


@pytest.fixture
def async_client():
    """Async test client."""
    return AsyncClient()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_async_view(async_client):
    """Test async view returns correct response."""
    response = await async_client.get('/api/async-endpoint/')

    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_async_api(async_client):
    """Test async API endpoint."""
    post = await sync_to_async(baker.make)('blog.Post', status='published')

    response = await async_client.get(f'/api/posts/{post.pk}/')

    assert response.status_code == 200
    assert response.json()['id'] == post.pk
```

---

*See also: [templates.md](templates.md) for copy-paste configurations, [llm-prompts.md](llm-prompts.md) for LLM-assisted testing*
