# LLM Prompts for Test-First Development

Effective prompts for TDD workflow with Claude Code, Cursor, Copilot, and other LLM assistants.

## Test-First Prompting Philosophy

Traditional prompting asks LLM to write code. Test-first prompting asks LLM to write **specifications as tests first**, then implement against them.

```
Traditional:  "Write a function to validate passwords"
Test-first:   "Write failing tests for password validation: min 8 chars,
              uppercase, lowercase, digit. Then implement to pass."
```

The test-first approach:
- Defines success criteria explicitly
- Prevents over-engineering
- Creates automatic verification
- Keeps LLM focused on one behavior at a time

---

## RED Phase Prompts

### Basic Test Generation

```
Write a pytest test for a function called `calculate_shipping_cost` that:
- Takes order_total (float) and destination_zone (str)
- Returns free shipping for orders over $100
- Charges $10 for zone "domestic"
- Charges $25 for zone "international"

Use Given-When-Then format in docstrings.
The function does NOT exist yet - tests should fail.
```

### Edge Case Test

```
Add tests for edge cases to TestPasswordValidator:
- Empty string input
- Exactly 8 characters (boundary)
- Special characters only
- Unicode characters

Each test should have a descriptive name explaining the scenario.
```

### API Endpoint Test

```
Write integration tests for POST /api/users endpoint:
1. Valid user data returns 201 with user object
2. Missing email returns 400 with "email required" error
3. Duplicate email returns 409 with "already exists" error
4. Invalid JSON returns 400 with "invalid format" error

Use pytest with httpx for async requests.
Mock the database layer.
```

### React Component Test

```
Write React Testing Library tests for a LoginForm component:
- Renders email and password inputs
- Submit button is disabled when fields are empty
- Calls onSubmit prop with credentials when form submitted
- Shows error message when onSubmit rejects

The component does not exist yet. Tests define the interface.
```

### Error Handling Test

```
Write tests for error handling in PaymentService.process_payment():
1. Gateway timeout -> raise PaymentTimeoutError
2. Invalid card -> raise InvalidCardError with card_last_four
3. Insufficient funds -> raise InsufficientFundsError with available_balance
4. Network error -> retry 3 times, then raise PaymentNetworkError

Use pytest.raises with match parameter for message validation.
```

---

## GREEN Phase Prompts

### Minimal Implementation

```
Implement the `calculate_shipping_cost` function to make all tests pass.
Rules:
- Write ONLY the code needed to pass existing tests
- Do NOT add features not covered by tests
- Do NOT optimize prematurely
- Keep implementation simple and straightforward
```

### Implementation with Context

```
Make the following failing test pass:

```python
def test_user_can_be_created_with_email_and_name(self):
    user = User(email="john@example.com", name="John Doe")
    assert user.email == "john@example.com"
    assert user.name == "John Doe"
    assert user.id is not None  # Auto-generated UUID
```

Implementation requirements:
- Use dataclass
- ID should be auto-generated UUID4
- Do not add any methods not required by this test
```

### Bug Fix Implementation

```
This test fails due to a bug:

```python
def test_discount_with_zero_quantity_items():
    cart = Cart(items=[
        CartItem(sku="A", quantity=0, price=10.00),
        CartItem(sku="B", quantity=2, price=20.00),
    ])
    result = cart.apply_discount(10)  # 10% off
    assert result.total == 36.00  # ZeroDivisionError occurs
```

Fix the bug in Cart.apply_discount() without modifying the test.
The fix should skip zero-quantity items in calculations.
```

---

## REFACTOR Phase Prompts

### Extract Method

```
Refactor UserService.create_user() to improve readability:
- Extract email validation to _validate_email()
- Extract password hashing to _hash_password()
- Extract welcome email sending to _send_welcome_email()

Keep all existing tests passing.
Run tests after each extraction to verify.
```

### Remove Duplication

```
The following tests have duplicated setup code:

```python
def test_order_total_calculation(self):
    order = Order()
    order.add_item(Item("Widget", 10.00, 2))
    order.add_item(Item("Gadget", 25.00, 1))
    # ...

def test_order_discount_application(self):
    order = Order()
    order.add_item(Item("Widget", 10.00, 2))
    order.add_item(Item("Gadget", 25.00, 1))
    # ...
```

Refactor to use a pytest fixture for the common setup.
Tests must continue to pass.
```

### Improve Naming

```
Review and improve naming in this class:

```python
class Proc:
    def do_it(self, d):
        r = self.v(d)
        if r:
            return self.h(d)
        return None
```

Rename to be self-documenting:
- Class name should describe its purpose
- Method names should be verbs describing the action
- Variable names should describe content
- Keep all tests passing
```

### Apply Design Pattern

```
Refactor PaymentProcessor to use Strategy pattern:
- Extract each payment method (credit_card, paypal, crypto) to separate strategy classes
- PaymentProcessor should accept PaymentStrategy in constructor
- Keep existing tests passing, they should not need modification
- Add tests for each strategy class

Current implementation uses if/elif chain based on payment_type.
```

---

## Multi-Step TDD Prompts

### Feature Implementation Workflow

```
Implement user registration feature using TDD workflow:

Step 1 (RED): Write failing test for email validation
Step 2 (GREEN): Implement email validation
Step 3 (RED): Write failing test for password requirements
Step 4 (GREEN): Implement password validation
Step 5 (RED): Write failing test for user creation
Step 6 (GREEN): Implement user creation
Step 7 (REFACTOR): Extract validators to separate module

After each step, run tests and commit.
Report test results after each phase.
```

### Bug Fix Workflow

```
Fix bug #1234 using TDD:

Bug: Users can submit empty reviews

Step 1: Write failing test reproducing the bug
        (empty review body should raise ValidationError)
Step 2: Verify test fails for the right reason
Step 3: Fix the bug in ReviewService.submit_review()
Step 4: Verify test passes
Step 5: Add edge case test (whitespace-only review)
Step 6: Update implementation if needed
Step 7: Commit with reference to bug number
```

---

## Framework-Specific Prompts

### pytest

```
Write pytest tests for UserRepository using these conventions:
- Use fixtures from conftest.py for database setup
- Use @pytest.mark.parametrize for multiple inputs
- Use pytest.raises for exception testing
- Group related tests in classes (TestUserRepository)
- Use descriptive test names: test_{method}_{scenario}_{expected}
```

### Jest

```
Write Jest tests for OrderService with:
- Mocked database using jest.mock()
- Async tests with async/await
- BeforeEach for fresh instance per test
- Test coverage for all public methods
- Use describe/it structure for organization
```

### Go

```
Write table-driven tests for ParseConfig function:
- Use map[string]struct for test cases
- Include test name as map key
- Use t.Run for subtests
- Use t.Parallel() for independent tests
- Use t.Helper() for helper functions
- Follow Go testing conventions (TestFunctionName)
```

---

## Anti-Pattern Prompts (What NOT to Do)

### Vague Prompts

```
Bad:  "Write tests for the user module"
Good: "Write tests for User.validate_email() covering:
       valid email, missing @, missing domain, multiple @ symbols"
```

### Implementation Before Test

```
Bad:  "Write a login function and its tests"
Good: "Write failing tests for login function:
       successful login, invalid password, user not found.
       Then implement to make tests pass."
```

### Modifying Tests to Pass

```
Bad:  "The test is failing, fix it"
Good: "The test is failing. Fix the implementation,
       NOT the test. The test defines correct behavior."
```

### Testing Implementation Details

```
Bad:  "Test that _internal_method is called"
Good: "Test that public behavior works correctly.
       Internal methods are implementation details."
```

---

## CLAUDE.md Configuration for TDD

Add to project's CLAUDE.md to enforce TDD workflow:

```markdown
## Testing Rules

### TDD Workflow (REQUIRED)
1. Write failing test FIRST
2. Implement minimal code to pass
3. Refactor while keeping tests green
4. Commit after each phase

### Test Requirements
- Every new function needs tests before implementation
- Bug fixes require reproduction test first
- Use pytest for Python, Jest for TypeScript, go test for Go

### Forbidden Actions
- Do NOT modify tests to make them pass
- Do NOT write implementation before tests
- Do NOT skip the refactor phase
- Do NOT commit without running tests

### Test Naming Convention
- Python: test_{method}_{scenario}_{expected}
- TypeScript: should {expected} when {scenario}
- Go: Test{Function}_{Scenario}
```

---

## Prompt Templates Quick Reference

| Phase | Template |
|-------|----------|
| RED | "Write failing test for {function} covering {scenarios}. Use {framework}. Tests define the interface." |
| GREEN | "Implement {function} to make all tests pass. Only code needed for current tests. No optimization." |
| REFACTOR | "Refactor {target} to {improvement}. Keep all tests passing. Run tests after each change." |
| Bug Fix | "Write test reproducing bug: {description}. Then fix implementation. Do not modify test." |

## Command Integration

### Claude Code /test

```
/test          # Run all tests
/test --watch  # Watch mode
/test -k name  # Run specific test
```

### Suggested Workflow

```
1. Write tests → /test (should fail)
2. Commit tests
3. Implement → /test (should pass)
4. Commit implementation
5. Refactor → /test (should still pass)
6. Commit refactoring
```
