# Python Code Quality Examples

Real-world examples demonstrating code quality principles, patterns, and anti-patterns.

---

## SOLID Principles Examples

### Single Responsibility Principle (SRP)

**Bad: Class with multiple responsibilities**

```python
class UserService:
    def __init__(self, db_connection):
        self.db = db_connection
        self.smtp_server = "mail.example.com"

    def create_user(self, email: str, name: str) -> User:
        user = User(email=email, name=name)
        self.db.execute("INSERT INTO users ...")

        # Violation: Also handles email sending
        self._send_welcome_email(user)

        # Violation: Also handles logging
        self._log_user_creation(user)

        return user

    def _send_welcome_email(self, user: User) -> None:
        # SMTP logic here...
        pass

    def _log_user_creation(self, user: User) -> None:
        # Logging logic here...
        pass
```

**Good: Separated responsibilities**

```python
from typing import Protocol

class EmailService(Protocol):
    def send_welcome_email(self, user: User) -> None: ...

class UserEventPublisher(Protocol):
    def publish(self, event: UserEvent) -> None: ...

class UserService:
    """Handles user-related business logic only."""

    def __init__(
        self,
        repository: UserRepository,
        email_service: EmailService,
        event_publisher: UserEventPublisher,
    ) -> None:
        self.repository = repository
        self.email_service = email_service
        self.event_publisher = event_publisher

    def create_user(self, email: str, name: str) -> User:
        user = User(email=email, name=name)
        self.repository.save(user)

        # Delegate to specialized services
        self.email_service.send_welcome_email(user)
        self.event_publisher.publish(UserCreatedEvent(user_id=user.id))

        return user
```

---

### Open/Closed Principle (OCP)

**Bad: Modifying existing code for new payment methods**

```python
class PaymentProcessor:
    def process_payment(self, payment_type: str, amount: float) -> bool:
        if payment_type == "credit_card":
            return self._process_credit_card(amount)
        elif payment_type == "paypal":
            return self._process_paypal(amount)
        elif payment_type == "stripe":  # Added for new requirement
            return self._process_stripe(amount)
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")
```

**Good: Open for extension via Strategy pattern**

```python
from abc import ABC, abstractmethod
from typing import Protocol

class PaymentStrategy(Protocol):
    """Protocol for payment processing strategies."""

    def process(self, amount: float) -> bool: ...

class CreditCardPayment:
    def process(self, amount: float) -> bool:
        # Credit card logic
        return True

class PayPalPayment:
    def process(self, amount: float) -> bool:
        # PayPal logic
        return True

class StripePayment:
    def process(self, amount: float) -> bool:
        # Stripe logic - added without modifying existing code
        return True

class PaymentProcessor:
    """Processes payments using pluggable strategies."""

    def __init__(self, strategy: PaymentStrategy) -> None:
        self.strategy = strategy

    def process_payment(self, amount: float) -> bool:
        return self.strategy.process(amount)

# Usage
processor = PaymentProcessor(StripePayment())
processor.process_payment(100.00)
```

---

### Liskov Substitution Principle (LSP)

**Bad: Subclass changes expected behavior**

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value

    def area(self) -> float:
        return self._width * self._height

class Square(Rectangle):
    """Violates LSP: changing width also changes height."""

    @Rectangle.width.setter
    def width(self, value: float) -> None:
        self._width = value
        self._height = value  # Unexpected side effect!

    @Rectangle.height.setter
    def height(self, value: float) -> None:
        self._width = value
        self._height = value

# This test fails with Square but passes with Rectangle
def test_rectangle_area(rect: Rectangle) -> None:
    rect.width = 5
    rect.height = 4
    assert rect.area() == 20  # Fails for Square!
```

**Good: Use composition or separate hierarchies**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side ** 2

# Both can be used interchangeably where Shape is expected
def print_area(shape: Shape) -> None:
    print(f"Area: {shape.area()}")
```

---

### Interface Segregation Principle (ISP)

**Bad: Fat interface forces unused implementations**

```python
from abc import ABC, abstractmethod

class Worker(ABC):
    @abstractmethod
    def work(self) -> None:
        pass

    @abstractmethod
    def eat(self) -> None:
        pass

    @abstractmethod
    def sleep(self) -> None:
        pass

class Robot(Worker):
    def work(self) -> None:
        print("Robot working...")

    def eat(self) -> None:
        pass  # Robots don't eat - forced empty implementation

    def sleep(self) -> None:
        pass  # Robots don't sleep - forced empty implementation
```

**Good: Small, focused interfaces**

```python
from typing import Protocol

class Workable(Protocol):
    def work(self) -> None: ...

class Eatable(Protocol):
    def eat(self) -> None: ...

class Sleepable(Protocol):
    def sleep(self) -> None: ...

class Human:
    def work(self) -> None:
        print("Human working...")

    def eat(self) -> None:
        print("Human eating...")

    def sleep(self) -> None:
        print("Human sleeping...")

class Robot:
    def work(self) -> None:
        print("Robot working...")
    # No need to implement eat() or sleep()

def assign_work(worker: Workable) -> None:
    worker.work()

# Both work!
assign_work(Human())
assign_work(Robot())
```

---

### Dependency Inversion Principle (DIP)

**Bad: High-level module depends on low-level module**

```python
import sqlite3

class UserRepository:
    def __init__(self) -> None:
        # Direct dependency on SQLite - hard to test and change
        self.connection = sqlite3.connect("users.db")

    def get_user(self, user_id: int) -> dict:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

class UserService:
    def __init__(self) -> None:
        # Direct dependency on concrete implementation
        self.repository = UserRepository()

    def get_user(self, user_id: int) -> dict:
        return self.repository.get_user(user_id)
```

**Good: Both depend on abstractions**

```python
from typing import Protocol
from dataclasses import dataclass

@dataclass
class User:
    id: int
    email: str
    name: str

class UserRepository(Protocol):
    """Abstract repository - the interface."""

    def get_by_id(self, user_id: int) -> User | None: ...
    def save(self, user: User) -> None: ...

class SQLiteUserRepository:
    """Concrete implementation."""

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string

    def get_by_id(self, user_id: int) -> User | None:
        # SQLite implementation
        pass

    def save(self, user: User) -> None:
        pass

class PostgresUserRepository:
    """Another concrete implementation."""

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def get_by_id(self, user_id: int) -> User | None:
        # PostgreSQL implementation
        pass

    def save(self, user: User) -> None:
        pass

class InMemoryUserRepository:
    """Test implementation."""

    def __init__(self) -> None:
        self.users: dict[int, User] = {}

    def get_by_id(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    def save(self, user: User) -> None:
        self.users[user.id] = user

class UserService:
    """Depends on abstraction, not concrete implementation."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def get_user(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

# Production
service = UserService(PostgresUserRepository("postgresql://..."))

# Testing
test_service = UserService(InMemoryUserRepository())
```

---

## Clean Code Examples

### Meaningful Names

**Bad**

```python
def calc(d: list, t: str) -> float:
    r = 0
    for i in d:
        if i["type"] == t:
            r += i["a"]
    return r
```

**Good**

```python
def calculate_total_by_category(
    transactions: list[Transaction],
    category: str,
) -> float:
    """Calculate the sum of amounts for transactions in a category."""
    return sum(
        tx.amount
        for tx in transactions
        if tx.category == category
    )
```

---

### Small Functions with Single Responsibility

**Bad: Function doing too many things**

```python
def process_order(order_data: dict) -> dict:
    # Validate
    if not order_data.get("items"):
        raise ValueError("No items")
    if not order_data.get("customer_id"):
        raise ValueError("No customer")

    # Calculate totals
    subtotal = sum(item["price"] * item["quantity"] for item in order_data["items"])
    tax = subtotal * 0.1
    shipping = 5.99 if subtotal < 50 else 0
    total = subtotal + tax + shipping

    # Save to database
    db = get_database_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO orders ...")
    order_id = cursor.lastrowid

    # Send confirmation email
    smtp = get_smtp_connection()
    smtp.send_mail(
        to=order_data["email"],
        subject="Order Confirmed",
        body=f"Your order {order_id} is confirmed..."
    )

    # Return result
    return {
        "order_id": order_id,
        "total": total,
        "status": "confirmed"
    }
```

**Good: Small, focused functions**

```python
@dataclass
class OrderTotals:
    subtotal: Decimal
    tax: Decimal
    shipping: Decimal
    total: Decimal

class OrderService:
    def __init__(
        self,
        validator: OrderValidator,
        calculator: PriceCalculator,
        repository: OrderRepository,
        notifier: OrderNotifier,
    ) -> None:
        self.validator = validator
        self.calculator = calculator
        self.repository = repository
        self.notifier = notifier

    def process_order(self, order: Order) -> ProcessedOrder:
        """Process an order: validate, calculate, save, notify."""
        self.validator.validate(order)

        totals = self.calculator.calculate_totals(order)

        saved_order = self.repository.save(order, totals)

        self.notifier.send_confirmation(saved_order)

        return saved_order

class PriceCalculator:
    TAX_RATE = Decimal("0.10")
    FREE_SHIPPING_THRESHOLD = Decimal("50.00")
    SHIPPING_COST = Decimal("5.99")

    def calculate_totals(self, order: Order) -> OrderTotals:
        subtotal = self._calculate_subtotal(order.items)
        tax = self._calculate_tax(subtotal)
        shipping = self._calculate_shipping(subtotal)

        return OrderTotals(
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=subtotal + tax + shipping,
        )

    def _calculate_subtotal(self, items: list[OrderItem]) -> Decimal:
        return sum(item.price * item.quantity for item in items)

    def _calculate_tax(self, subtotal: Decimal) -> Decimal:
        return subtotal * self.TAX_RATE

    def _calculate_shipping(self, subtotal: Decimal) -> Decimal:
        if subtotal >= self.FREE_SHIPPING_THRESHOLD:
            return Decimal("0.00")
        return self.SHIPPING_COST
```

---

### Early Returns (Guard Clauses)

**Bad: Deep nesting**

```python
def process_user_request(user: User | None, request: Request) -> Response:
    if user is not None:
        if user.is_active:
            if user.has_permission(request.resource):
                if request.is_valid():
                    # Finally do the work
                    result = perform_action(user, request)
                    return Response(status=200, data=result)
                else:
                    return Response(status=400, error="Invalid request")
            else:
                return Response(status=403, error="Permission denied")
        else:
            return Response(status=403, error="User inactive")
    else:
        return Response(status=401, error="Not authenticated")
```

**Good: Guard clauses with early returns**

```python
def process_user_request(user: User | None, request: Request) -> Response:
    if user is None:
        return Response(status=401, error="Not authenticated")

    if not user.is_active:
        return Response(status=403, error="User inactive")

    if not user.has_permission(request.resource):
        return Response(status=403, error="Permission denied")

    if not request.is_valid():
        return Response(status=400, error="Invalid request")

    # Happy path - clear and flat
    result = perform_action(user, request)
    return Response(status=200, data=result)
```

---

### Type Hints Best Practices

**Modern Python 3.10+ type hints**

```python
from collections.abc import Callable, Sequence
from typing import TypeVar, TypedDict, Protocol

# Use built-in generics (3.9+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Use union syntax (3.10+)
def find_user(user_id: int) -> User | None:
    return users.get(user_id)

# TypedDict for structured dicts
class UserData(TypedDict):
    id: int
    email: str
    name: str
    is_active: bool

def create_user(data: UserData) -> User:
    return User(**data)

# Generic functions
T = TypeVar("T")

def first_or_none(items: Sequence[T]) -> T | None:
    return items[0] if items else None

# Callable types
Handler = Callable[[Request], Response]

def register_handler(path: str, handler: Handler) -> None:
    routes[path] = handler

# Protocol for duck typing
class Serializable(Protocol):
    def to_dict(self) -> dict: ...

def serialize(obj: Serializable) -> str:
    return json.dumps(obj.to_dict())
```

---

### Error Handling

**Bad: Catching too broadly**

```python
def fetch_user_data(user_id: int) -> dict:
    try:
        response = requests.get(f"/api/users/{user_id}")
        data = response.json()
        return process_data(data)
    except Exception:  # Too broad!
        return {}  # Silent failure - hides bugs
```

**Good: Specific exceptions with context**

```python
from dataclasses import dataclass

class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

class UserServiceError(Exception):
    """Base exception for user service errors."""
    pass

def fetch_user_data(user_id: int) -> UserData:
    """Fetch user data from the API.

    Raises:
        UserNotFoundError: If user doesn't exist.
        UserServiceError: If API call fails.
    """
    try:
        response = requests.get(
            f"/api/users/{user_id}",
            timeout=5.0,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise UserNotFoundError(user_id) from e
        raise UserServiceError(f"API error: {e}") from e
    except requests.exceptions.RequestException as e:
        raise UserServiceError(f"Connection error: {e}") from e

    try:
        return UserData(**response.json())
    except (json.JSONDecodeError, TypeError) as e:
        raise UserServiceError(f"Invalid response format: {e}") from e
```

---

### Docstrings (Google Style)

```python
def calculate_discount(
    price: Decimal,
    discount_percent: Decimal,
    max_discount: Decimal | None = None,
) -> Decimal:
    """Calculate the discounted price.

    Applies a percentage discount to the original price, optionally
    capping the discount at a maximum value.

    Args:
        price: The original price before discount.
        discount_percent: The discount percentage (0-100).
        max_discount: Optional maximum discount amount. If the
            calculated discount exceeds this, the max is used instead.

    Returns:
        The final price after applying the discount.

    Raises:
        ValueError: If price is negative or discount_percent is not
            between 0 and 100.

    Examples:
        >>> calculate_discount(Decimal("100"), Decimal("20"))
        Decimal('80')

        >>> calculate_discount(Decimal("100"), Decimal("50"), Decimal("30"))
        Decimal('70')  # Discount capped at 30
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount percent must be between 0 and 100")

    discount = price * discount_percent / 100

    if max_discount is not None and discount > max_discount:
        discount = max_discount

    return price - discount
```

---

## Common Anti-Patterns

### Mutable Default Arguments

**Bad**

```python
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)  # Mutates the default!
    return items

# Surprising behavior:
add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] - unexpected!
```

**Good**

```python
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

---

### Boolean Parameters

**Bad**

```python
def create_user(email: str, name: str, send_email: bool, admin: bool) -> User:
    pass

# What do these booleans mean?
create_user("test@example.com", "Test", True, False)
```

**Good: Use explicit parameters or enums**

```python
from enum import Enum, auto

class UserRole(Enum):
    USER = auto()
    ADMIN = auto()

@dataclass
class CreateUserRequest:
    email: str
    name: str
    role: UserRole = UserRole.USER
    send_welcome_email: bool = True

def create_user(request: CreateUserRequest) -> User:
    pass

# Clear intent
create_user(CreateUserRequest(
    email="test@example.com",
    name="Test",
    role=UserRole.USER,
    send_welcome_email=True,
))
```

---

### God Classes

**Bad: Class with too many responsibilities**

```python
class UserManager:
    def create_user(self, ...): ...
    def delete_user(self, ...): ...
    def send_email(self, ...): ...
    def generate_report(self, ...): ...
    def validate_password(self, ...): ...
    def hash_password(self, ...): ...
    def check_permissions(self, ...): ...
    def log_activity(self, ...): ...
    def sync_with_ldap(self, ...): ...
    # ... 50 more methods
```

**Good: Split into focused classes**

```python
class UserRepository:
    def create(self, user: User) -> User: ...
    def delete(self, user_id: int) -> None: ...
    def find_by_id(self, user_id: int) -> User | None: ...

class PasswordService:
    def validate(self, password: str) -> ValidationResult: ...
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hash: str) -> bool: ...

class UserEmailService:
    def send_welcome(self, user: User) -> None: ...
    def send_password_reset(self, user: User) -> None: ...

class PermissionChecker:
    def check(self, user: User, permission: str) -> bool: ...

class UserService:
    """Coordinates user operations using specialized services."""

    def __init__(
        self,
        repository: UserRepository,
        password_service: PasswordService,
        email_service: UserEmailService,
        permission_checker: PermissionChecker,
    ) -> None:
        self.repository = repository
        self.password_service = password_service
        self.email_service = email_service
        self.permission_checker = permission_checker
```
