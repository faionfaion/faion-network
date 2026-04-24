# LLM Prompts for pytest-django

Effective prompts for LLM-assisted Django testing with pytest.

---

## 1. Test Generation Prompts

### Generate Unit Tests for Service

```
Generate pytest tests for this Django service:

```python
# apps/orders/services.py
class OrderService:
    @staticmethod
    def create_order(user: User, items: list[dict], coupon_code: str | None = None) -> Order:
        """
        Create order with items, apply coupon if provided.
        - Validates stock availability
        - Reduces product stock
        - Applies coupon discount
        - Sends confirmation email via Celery
        Raises: InsufficientStockError, InvalidCouponError
        """
```

Requirements:
- Use pytest-django markers (@pytest.mark.django_db)
- Use Factory Boy fixtures (user_factory, product_factory, coupon_factory)
- Test happy path, error cases, and edge cases
- Mock the Celery email task
- Use AAA pattern (Arrange-Act-Assert)
- Add descriptive test names and docstrings
```

### Generate API Tests

```
Generate pytest integration tests for this DRF viewset:

```python
# apps/orders/views.py
class OrderViewSet(ModelViewSet):
    """
    Orders API:
    - list: GET /orders/ (own orders only, admin sees all)
    - create: POST /orders/ (authenticated)
    - retrieve: GET /orders/{uid}/ (own or admin)
    - update: PATCH /orders/{uid}/ (own, pending only)
    - cancel: POST /orders/{uid}/cancel/ (own, not shipped)
    """
```

Requirements:
- Test authentication (401 for anonymous)
- Test authorization (403 for other users' orders)
- Test permission levels (regular vs admin)
- Test validation errors (400)
- Test not found (404)
- Use authenticated_client, admin_client fixtures
- Use pytest.mark.parametrize for validation tests
```

### Generate Factory Boy Factories

```
Create Factory Boy factories for these Django models:

```python
# apps/orders/models.py
class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default="pending")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
```

Requirements:
- Use factory.django.DjangoModelFactory
- Use factory.SubFactory for relationships
- Use factory.Faker for realistic data
- Use factory.LazyAttribute where appropriate
- Add post_generation hook for items list
- Include docstrings
```

---

## 2. Fixture Creation Prompts

### Create API Client Fixtures

```
Create pytest fixtures for DRF API testing:

Requirements:
1. api_client - Unauthenticated APIClient
2. authenticated_client - Client with regular user (force_authenticate)
3. admin_client - Client with admin user
4. token_client - Client with JWT Bearer token

Additional requirements:
- Use yield to cleanup after tests
- Clear authentication after each test
- Support custom User model with uid field
- Compatible with pytest-factoryboy (user, admin_user fixtures)
```

### Create Database Fixtures

```
Create pytest fixtures for test data setup:

Scenario: E-commerce testing needs:
1. Product catalog with categories
2. User with shopping cart
3. Order with items and payment

Requirements:
- Use session scope for immutable data (categories)
- Use function scope for mutable data (orders)
- Compose fixtures (order_with_items depends on user, products)
- Use Factory Boy for creation
- Document each fixture with docstrings
```

### Create Mock Fixtures

```
Create pytest fixtures for mocking external services:

Services to mock:
1. Stripe payment processing
2. SendGrid email sending
3. AWS S3 file uploads
4. External REST API (partner webhook)

Requirements:
- Use unittest.mock.patch as context manager
- Use responses library for HTTP mocking
- Return realistic mock responses
- Allow customization via fixture parameters
- Auto-apply to all tests in class (autouse option)
```

---

## 3. Refactoring Prompts

### Convert unittest to pytest

```
Convert this Django TestCase to pytest style:

```python
from django.test import TestCase
from apps.orders.services import OrderService

class TestOrderService(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.product = Product.objects.create(name="Test", price=10, stock=5)

    def test_create_order_success(self):
        order = OrderService.create_order(
            user=self.user,
            items=[{"product_id": self.product.id, "quantity": 2}]
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, "pending")

    def test_create_order_insufficient_stock(self):
        with self.assertRaises(ValueError):
            OrderService.create_order(
                user=self.user,
                items=[{"product_id": self.product.id, "quantity": 100}]
            )
```

Requirements:
- Replace setUp with fixtures
- Use Factory Boy for data creation
- Use simple assert statements
- Use pytest.raises for exceptions
- Add @pytest.mark.django_db
- Improve test names and add docstrings
```

### Optimize Slow Tests

```
Optimize these slow pytest tests:

```python
@pytest.mark.django_db
class TestReportGeneration:
    def test_monthly_report(self, user_factory, order_factory):
        # Creates 1000 orders - very slow!
        for i in range(1000):
            order_factory(user=user_factory())

        report = ReportService.generate_monthly()
        assert report.total_orders == 1000

    def test_user_statistics(self, user_factory, order_factory):
        # Same setup repeated!
        for i in range(1000):
            order_factory(user=user_factory())

        stats = UserService.get_statistics()
        assert stats.active_users > 0
```

Requirements:
- Use module-scoped fixtures for shared data
- Use bulk_create instead of loops
- Consider setUpTestData pattern
- Profile with --durations flag
- Target: < 1 second per test
```

### Add Parametrization

```
Refactor these repetitive tests using pytest.mark.parametrize:

```python
def test_validate_email_valid(self):
    assert validate_email("user@example.com") == True

def test_validate_email_valid_subdomain(self):
    assert validate_email("user@mail.example.com") == True

def test_validate_email_invalid_no_at(self):
    assert validate_email("userexample.com") == False

def test_validate_email_invalid_no_domain(self):
    assert validate_email("user@") == False

def test_validate_email_invalid_empty(self):
    assert validate_email("") == False
```

Requirements:
- Combine into parametrized tests
- Group by valid/invalid cases
- Use descriptive test IDs
- Keep tests readable
```

---

## 4. Debugging Prompts

### Diagnose Test Failure

```
This pytest test is failing. Help me debug:

```python
@pytest.mark.django_db
def test_order_creation(user, product_factory):
    product = product_factory(stock=10)

    order = OrderService.create_order(
        user=user,
        items=[{"product_id": product.id, "quantity": 2}]
    )

    product.refresh_from_db()
    assert product.stock == 8  # Fails: stock is still 10
```

Error:
```
AssertionError: assert 10 == 8
```

Questions to answer:
1. Is the stock reduction happening in a separate transaction?
2. Should I use transactional_db?
3. Is there a signal/post_save issue?
4. How do I debug the service code?
```

### Fix Flaky Tests

```
This test passes sometimes and fails randomly:

```python
@pytest.mark.django_db
def test_order_number_unique(order_factory):
    orders = [order_factory() for _ in range(10)]
    order_numbers = [o.order_number for o in orders]

    assert len(set(order_numbers)) == 10  # Sometimes fails!
```

Possible causes to investigate:
1. Race condition in order number generation?
2. Timestamp-based generation with insufficient precision?
3. Test isolation issue?
4. Random seed issue?

Provide:
- Diagnosis approach
- Potential fixes
- How to make test deterministic
```

### Transaction Error

```
Getting TransactionManagementError in tests:

```python
@pytest.mark.django_db
def test_payment_rollback(user, order_factory):
    order = order_factory(user=user)

    with pytest.raises(PaymentError):
        PaymentService.process_with_rollback(order, token="failing")

    # Error: TransactionManagementError: An error occurred in the current transaction.
    order.refresh_from_db()
    assert order.status == "pending"
```

Questions:
1. Should I use transaction=True marker?
2. Is the service using atomic() correctly?
3. How to test transaction rollback behavior?
```

---

## 5. Configuration Prompts

### Setup pytest-django Project

```
Help me set up pytest-django for a new Django project:

Project structure:
- Django 5.0 with DRF
- PostgreSQL database
- Celery for async tasks
- Custom User model with uid field

Requirements:
1. pyproject.toml configuration
2. Test settings file (test.py)
3. Root conftest.py with:
   - API client fixtures
   - Database fixtures
   - Factory registration
4. Directory structure for tests
5. GitHub Actions CI workflow

Optimization goals:
- Tests run in parallel
- Coverage reporting
- Reuse database between runs
- Fast password hashing
```

### Configure Coverage

```
Set up pytest-cov for Django project:

Requirements:
1. Coverage configuration in pyproject.toml
2. Exclude migrations, tests, admin.py
3. Set minimum coverage threshold (80%)
4. Generate HTML report locally
5. Generate XML for CI upload
6. Show missing lines in terminal

Also provide:
- GitHub Actions step for coverage upload
- Pre-commit hook for coverage check
- VS Code settings for coverage display
```

### Setup Parallel Testing

```
Configure pytest-xdist for parallel Django tests:

Current issues:
- 500 tests take 10 minutes
- Some tests share database state
- File-based tests conflict

Requirements:
1. pytest-xdist configuration
2. Fix test isolation issues
3. Handle database per worker
4. Handle file system conflicts
5. Optimize for CI (4 cores)

Expected outcome:
- Tests run in < 3 minutes
- No flaky tests from parallelization
```

---

## 6. Advanced Patterns

### Test Async Django

```
Help me test async Django views and services:

```python
# apps/orders/services.py
class AsyncOrderService:
    @staticmethod
    async def get_order_with_items(order_id: int) -> Order:
        order = await Order.objects.select_related("user").aget(id=order_id)
        items = [item async for item in order.items.all()]
        return order

# apps/orders/views.py
class AsyncOrderView(View):
    async def get(self, request, uid):
        order = await AsyncOrderService.get_order_by_uid(uid)
        return JsonResponse({"order": order.to_dict()})
```

Requirements:
- Use pytest-asyncio
- Handle database access in async context
- Use async fixtures
- Test async view with async client
```

### Test WebSockets

```
Help me test Django Channels WebSocket consumers:

```python
# apps/chat/consumers.py
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_name,
            {"type": "chat_message", "message": data["message"]}
        )
```

Requirements:
- Use channels testing utilities
- Test connect/disconnect
- Test message sending/receiving
- Test authentication
- Mock channel layer for unit tests
```

### Test File Uploads

```
Help me test DRF file upload endpoints:

```python
# apps/documents/views.py
class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES["file"]
        # Validate file type, size
        # Save to S3
        # Create Document record
        return Response({"id": doc.id})
```

Requirements:
- Create test files (SimpleUploadedFile)
- Test file validation (type, size limits)
- Mock S3 upload
- Test multipart form data
- Cleanup uploaded files after tests
```

---

## 7. Review Prompts

### Review Test Quality

```
Review these tests for quality and suggest improvements:

```python
@pytest.mark.django_db
class TestOrderAPI:
    def test_order(self, client, user):
        client.force_authenticate(user)
        r = client.post("/api/orders/", {"items": [1, 2]})
        assert r.status_code == 201
        assert r.data["id"]

    def test_order2(self, client, user):
        client.force_authenticate(user)
        r = client.post("/api/orders/", {})
        assert r.status_code == 400
```

Review for:
1. Test naming clarity
2. Assertion completeness
3. Test isolation
4. Fixture usage
5. Edge case coverage
6. Documentation
```

### Suggest Missing Tests

```
Given this service, suggest tests that are missing:

```python
class PaymentService:
    @staticmethod
    def process_payment(order: Order, payment_method: str, token: str) -> Payment:
        if order.status != "pending":
            raise InvalidOrderStateError()

        if payment_method == "stripe":
            charge = stripe.Charge.create(...)
        elif payment_method == "paypal":
            charge = paypal.capture_order(...)
        else:
            raise UnsupportedPaymentMethodError()

        payment = Payment.objects.create(
            order=order,
            method=payment_method,
            external_id=charge.id,
            amount=order.total,
            status="completed"
        )

        order.status = "paid"
        order.save()

        send_payment_confirmation.delay(payment.id)

        return payment
```

Consider:
- Happy paths for each payment method
- Error handling (invalid state, API failures)
- Idempotency (duplicate payments)
- Partial failures (payment succeeds, email fails)
- Race conditions
```

---

## 8. Quick Reference Prompts

### Explain Fixture Scope

```
Explain pytest fixture scopes for Django testing:

1. When to use function scope (default)?
2. When to use class scope?
3. When to use module scope?
4. When to use session scope?

For each, provide:
- Use case example
- Potential pitfalls
- Performance implications
- Code example
```

### Compare Testing Approaches

```
Compare these Django testing approaches:

1. pytest-django with fixtures
2. Django TestCase with setUp
3. pytest with Factory Boy
4. pytest with model_bakery

For each, show:
- Code example for same test
- Pros and cons
- When to use
- Performance characteristics
```

### Best Practices Summary

```
Summarize pytest-django best practices for:

1. Test organization (directory structure)
2. Fixture management (conftest.py)
3. Database access (markers, fixtures)
4. Factory usage (Factory Boy patterns)
5. Mocking (when and how)
6. Performance (parallel, reuse-db)
7. CI integration (GitHub Actions)

Format as a quick reference cheat sheet.
```
