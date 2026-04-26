# TDD Examples for Different Languages

Practical TDD examples showing the Red-Green-Refactor cycle in Python, TypeScript, and Go.

## Python (pytest)

### Example: Email Validator

**Step 1: RED - Write Failing Test**

```python
# tests/test_email_validator.py
import pytest
from email_validator import EmailValidator, ValidationError


class TestEmailValidator:
    """TDD Example: Building an email validator step by step."""

    def test_valid_email_returns_true(self):
        """Given a valid email, when validated, then return True."""
        validator = EmailValidator()

        result = validator.is_valid("user@example.com")

        assert result is True

    def test_email_without_at_symbol_raises_error(self):
        """Given email without @, when validated, then raise ValidationError."""
        validator = EmailValidator()

        with pytest.raises(ValidationError) as exc_info:
            validator.is_valid("userexample.com")

        assert "must contain @" in str(exc_info.value)

    def test_email_without_domain_raises_error(self):
        """Given email without domain, when validated, then raise ValidationError."""
        validator = EmailValidator()

        with pytest.raises(ValidationError) as exc_info:
            validator.is_valid("user@")

        assert "must have domain" in str(exc_info.value)
```

Run: `pytest tests/test_email_validator.py` → FAIL (module not found)

**Step 2: GREEN - Minimal Implementation**

```python
# email_validator.py
class ValidationError(Exception):
    """Raised when email validation fails."""
    pass


class EmailValidator:
    """Validates email addresses."""

    def is_valid(self, email: str) -> bool:
        """Validate email address format.

        Args:
            email: Email address to validate

        Returns:
            True if email is valid

        Raises:
            ValidationError: If email format is invalid
        """
        if "@" not in email:
            raise ValidationError("Email must contain @ symbol")

        _, domain = email.split("@", 1)
        if not domain:
            raise ValidationError("Email must have domain")

        return True
```

Run: `pytest tests/test_email_validator.py` → PASS

**Step 3: RED - Add More Tests**

```python
    def test_email_with_multiple_at_symbols_raises_error(self):
        """Given email with multiple @, when validated, then raise error."""
        validator = EmailValidator()

        with pytest.raises(ValidationError) as exc_info:
            validator.is_valid("user@domain@example.com")

        assert "single @" in str(exc_info.value)

    def test_normalize_email_lowercases(self):
        """Given email with uppercase, when normalized, then lowercase."""
        validator = EmailValidator()

        result = validator.normalize("User@Example.COM")

        assert result == "user@example.com"
```

**Step 4: GREEN - Extend Implementation**

```python
class EmailValidator:
    def is_valid(self, email: str) -> bool:
        if "@" not in email:
            raise ValidationError("Email must contain @ symbol")

        if email.count("@") > 1:
            raise ValidationError("Email must have single @ symbol")

        _, domain = email.split("@", 1)
        if not domain:
            raise ValidationError("Email must have domain")

        return True

    def normalize(self, email: str) -> str:
        """Normalize email to lowercase."""
        return email.strip().lower()
```

**Step 5: REFACTOR - Improve Structure**

```python
class EmailValidator:
    """Validates and normalizes email addresses."""

    def is_valid(self, email: str) -> bool:
        """Validate email address format."""
        self._assert_has_at_symbol(email)
        self._assert_single_at_symbol(email)
        self._assert_has_domain(email)
        return True

    def normalize(self, email: str) -> str:
        """Normalize email to lowercase, trimmed."""
        return email.strip().lower()

    def _assert_has_at_symbol(self, email: str) -> None:
        if "@" not in email:
            raise ValidationError("Email must contain @ symbol")

    def _assert_single_at_symbol(self, email: str) -> None:
        if email.count("@") > 1:
            raise ValidationError("Email must have single @ symbol")

    def _assert_has_domain(self, email: str) -> None:
        _, domain = email.split("@", 1)
        if not domain:
            raise ValidationError("Email must have domain")
```

---

## TypeScript (Jest)

### Example: Shopping Cart

**Step 1: RED - Write Failing Test**

```typescript
// __tests__/shoppingCart.test.ts
import { ShoppingCart, CartItem } from '../src/shoppingCart';

describe('ShoppingCart', () => {
  let cart: ShoppingCart;

  beforeEach(() => {
    cart = new ShoppingCart();
  });

  describe('addItem', () => {
    it('should add item to empty cart', () => {
      const item: CartItem = { id: '1', name: 'Widget', price: 10.00, quantity: 1 };

      cart.addItem(item);

      expect(cart.items).toHaveLength(1);
      expect(cart.items[0]).toEqual(item);
    });

    it('should increase quantity when adding existing item', () => {
      const item: CartItem = { id: '1', name: 'Widget', price: 10.00, quantity: 1 };

      cart.addItem(item);
      cart.addItem(item);

      expect(cart.items).toHaveLength(1);
      expect(cart.items[0].quantity).toBe(2);
    });
  });

  describe('getTotal', () => {
    it('should return 0 for empty cart', () => {
      expect(cart.getTotal()).toBe(0);
    });

    it('should calculate total for multiple items', () => {
      cart.addItem({ id: '1', name: 'Widget', price: 10.00, quantity: 2 });
      cart.addItem({ id: '2', name: 'Gadget', price: 25.00, quantity: 1 });

      expect(cart.getTotal()).toBe(45.00);
    });
  });
});
```

Run: `npm test` → FAIL

**Step 2: GREEN - Minimal Implementation**

```typescript
// src/shoppingCart.ts
export interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

export class ShoppingCart {
  private _items: CartItem[] = [];

  get items(): CartItem[] {
    return [...this._items];
  }

  addItem(item: CartItem): void {
    const existingItem = this._items.find(i => i.id === item.id);

    if (existingItem) {
      existingItem.quantity += item.quantity;
    } else {
      this._items.push({ ...item });
    }
  }

  getTotal(): number {
    return this._items.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
  }
}
```

Run: `npm test` → PASS

**Step 3: RED - Add Discount Feature**

```typescript
  describe('applyDiscount', () => {
    it('should apply percentage discount', () => {
      cart.addItem({ id: '1', name: 'Widget', price: 100.00, quantity: 1 });

      cart.applyDiscount(10); // 10% off

      expect(cart.getTotal()).toBe(90.00);
    });

    it('should throw error for negative discount', () => {
      expect(() => cart.applyDiscount(-5)).toThrow('Discount must be positive');
    });

    it('should throw error for discount over 100%', () => {
      expect(() => cart.applyDiscount(150)).toThrow('Discount cannot exceed 100%');
    });
  });
```

**Step 4: GREEN - Implement Discount**

```typescript
export class ShoppingCart {
  private _items: CartItem[] = [];
  private _discountPercent: number = 0;

  // ... existing methods ...

  applyDiscount(percent: number): void {
    if (percent < 0) {
      throw new Error('Discount must be positive');
    }
    if (percent > 100) {
      throw new Error('Discount cannot exceed 100%');
    }
    this._discountPercent = percent;
  }

  getTotal(): number {
    const subtotal = this._items.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
    return subtotal * (1 - this._discountPercent / 100);
  }
}
```

**Step 5: REFACTOR - Extract Calculator**

```typescript
// src/priceCalculator.ts
export class PriceCalculator {
  calculateSubtotal(items: CartItem[]): number {
    return items.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
  }

  applyDiscount(amount: number, discountPercent: number): number {
    return amount * (1 - discountPercent / 100);
  }
}

// src/shoppingCart.ts
export class ShoppingCart {
  private _items: CartItem[] = [];
  private _discountPercent: number = 0;
  private calculator = new PriceCalculator();

  // ... other methods ...

  getTotal(): number {
    const subtotal = this.calculator.calculateSubtotal(this._items);
    return this.calculator.applyDiscount(subtotal, this._discountPercent);
  }
}
```

---

## Go (go test)

### Example: User Repository

**Step 1: RED - Write Table-Driven Test**

```go
// user_repository_test.go
package repository

import (
    "testing"
)

func TestUserRepository_Create(t *testing.T) {
    tests := map[string]struct {
        user        User
        wantErr     bool
        errContains string
    }{
        "valid user": {
            user:    User{Name: "John", Email: "john@example.com"},
            wantErr: false,
        },
        "empty name": {
            user:        User{Name: "", Email: "john@example.com"},
            wantErr:     true,
            errContains: "name is required",
        },
        "invalid email": {
            user:        User{Name: "John", Email: "invalid"},
            wantErr:     true,
            errContains: "invalid email",
        },
        "duplicate email": {
            user:        User{Name: "Jane", Email: "existing@example.com"},
            wantErr:     true,
            errContains: "email already exists",
        },
    }

    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            // Arrange
            repo := NewUserRepository()
            if name == "duplicate email" {
                repo.Create(User{Name: "Existing", Email: "existing@example.com"})
            }

            // Act
            err := repo.Create(tc.user)

            // Assert
            if tc.wantErr {
                if err == nil {
                    t.Errorf("expected error containing %q, got nil", tc.errContains)
                } else if !contains(err.Error(), tc.errContains) {
                    t.Errorf("expected error containing %q, got %q", tc.errContains, err.Error())
                }
            } else {
                if err != nil {
                    t.Errorf("unexpected error: %v", err)
                }
            }
        })
    }
}

func contains(s, substr string) bool {
    return len(s) >= len(substr) && (s == substr || len(s) > 0 && containsAt(s, substr, 0))
}

func containsAt(s, substr string, start int) bool {
    if start+len(substr) > len(s) {
        return false
    }
    if s[start:start+len(substr)] == substr {
        return true
    }
    return containsAt(s, substr, start+1)
}
```

Run: `go test -v` → FAIL

**Step 2: GREEN - Minimal Implementation**

```go
// user_repository.go
package repository

import (
    "errors"
    "strings"
)

type User struct {
    ID    string
    Name  string
    Email string
}

type UserRepository struct {
    users map[string]User
}

func NewUserRepository() *UserRepository {
    return &UserRepository{
        users: make(map[string]User),
    }
}

func (r *UserRepository) Create(user User) error {
    if user.Name == "" {
        return errors.New("name is required")
    }

    if !strings.Contains(user.Email, "@") {
        return errors.New("invalid email format")
    }

    if _, exists := r.users[user.Email]; exists {
        return errors.New("email already exists")
    }

    r.users[user.Email] = user
    return nil
}
```

Run: `go test -v` → PASS

**Step 3: RED - Add Find Method**

```go
func TestUserRepository_FindByEmail(t *testing.T) {
    tests := map[string]struct {
        setup   func(*UserRepository)
        email   string
        want    *User
        wantErr bool
    }{
        "found": {
            setup: func(r *UserRepository) {
                r.Create(User{Name: "John", Email: "john@example.com"})
            },
            email:   "john@example.com",
            want:    &User{Name: "John", Email: "john@example.com"},
            wantErr: false,
        },
        "not found": {
            setup:   func(r *UserRepository) {},
            email:   "missing@example.com",
            want:    nil,
            wantErr: true,
        },
    }

    for name, tc := range tests {
        t.Run(name, func(t *testing.T) {
            repo := NewUserRepository()
            tc.setup(repo)

            got, err := repo.FindByEmail(tc.email)

            if tc.wantErr && err == nil {
                t.Error("expected error, got nil")
            }
            if !tc.wantErr && err != nil {
                t.Errorf("unexpected error: %v", err)
            }
            if tc.want != nil && (got == nil || got.Email != tc.want.Email) {
                t.Errorf("got %v, want %v", got, tc.want)
            }
        })
    }
}
```

**Step 4: GREEN - Implement Find**

```go
func (r *UserRepository) FindByEmail(email string) (*User, error) {
    user, exists := r.users[email]
    if !exists {
        return nil, errors.New("user not found")
    }
    return &user, nil
}
```

**Step 5: REFACTOR - Extract Validation**

```go
// validation.go
package repository

import (
    "errors"
    "strings"
)

var (
    ErrNameRequired   = errors.New("name is required")
    ErrInvalidEmail   = errors.New("invalid email format")
    ErrEmailExists    = errors.New("email already exists")
    ErrUserNotFound   = errors.New("user not found")
)

func validateUser(user User) error {
    if user.Name == "" {
        return ErrNameRequired
    }
    if !isValidEmail(user.Email) {
        return ErrInvalidEmail
    }
    return nil
}

func isValidEmail(email string) bool {
    return strings.Contains(email, "@") && strings.Contains(email, ".")
}

// user_repository.go
func (r *UserRepository) Create(user User) error {
    if err := validateUser(user); err != nil {
        return err
    }

    if _, exists := r.users[user.Email]; exists {
        return ErrEmailExists
    }

    r.users[user.Email] = user
    return nil
}
```

---

## Key Takeaways

| Language | Test Framework | Key Pattern |
|----------|---------------|-------------|
| Python | pytest | Fixtures + parametrize |
| TypeScript | Jest | describe/it + beforeEach |
| Go | testing | Table-driven tests |

## Common Patterns Across Languages

1. **Arrange-Act-Assert**: Structure every test the same way
2. **One behavior per test**: Easy to identify what broke
3. **Descriptive names**: Test name = documentation
4. **Independent tests**: No shared mutable state
5. **Fast execution**: Unit tests < 100ms each
