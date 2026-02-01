---
id: code-review-process
name: "Code Review Process"
domain: DEV
skill: faion-software-developer
category: "development"
parent: code-review
---

# Code Review Process

## PR Description Template

```markdown
## Description
Brief description of what this PR does and why.

## Related Issues
Closes #123
Related to #456

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran to verify your changes.

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] Any dependent changes have been merged

## Screenshots (if applicable)
Add screenshots for UI changes.

## Additional Notes
Any additional information reviewers should know.
```

## Automated Review Assistance

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run linters
        run: make lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test

  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check coverage
        run: |
          pytest --cov=src --cov-fail-under=80

  pr-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Check PR size
        run: |
          CHANGES=$(git diff --stat origin/main | tail -1 | awk '{print $4}')
          if [ "$CHANGES" -gt 500 ]; then
            echo "::warning::PR has $CHANGES changed lines. Consider splitting."
          fi
```

## Review Scenarios

```python
# Scenario 1: Bug

# Original code
def calculate_discount(price, discount_percent):
    return price - (price * discount_percent)

# Review comment:
"""
Bug: discount_percent should be divided by 100 if passed as a whole number (e.g., 20 for 20%).

Current behavior:
  calculate_discount(100, 20) returns -1900 (wrong)

Expected:
  calculate_discount(100, 20) returns 80

Suggested fix:
  return price - (price * discount_percent / 100)

Or clarify in docstring that discount_percent should be 0-1 range.
"""


# Scenario 2: Design Issue

# Original code
class OrderProcessor:
    def process(self, order):
        # Validate
        if not order.items:
            raise ValueError("Empty order")

        # Calculate total
        total = sum(item.price * item.quantity for item in order.items)

        # Apply discount
        if order.user.is_premium:
            total *= 0.9

        # Charge payment
        payment_result = PaymentGateway().charge(order.user.card, total)

        # Send email
        EmailService().send_order_confirmation(order.user.email, order)

        # Update inventory
        for item in order.items:
            InventoryService().decrease(item.product_id, item.quantity)

        return payment_result

# Review comment:
"""
Design concern: This method has too many responsibilities (validation,
calculation, payment, email, inventory). Consider:

1. Extract validation to separate method
2. Inject dependencies (PaymentGateway, EmailService) instead of creating
3. Use events/queue for email and inventory updates (shouldn't block response)

Suggested structure:
```python
class OrderProcessor:
    def __init__(self, payment: PaymentGateway, events: EventBus):
        self.payment = payment
        self.events = events

    def process(self, order: Order) -> PaymentResult:
        self._validate(order)
        total = self._calculate_total(order)
        result = self.payment.charge(order.user.card, total)
        self.events.publish(OrderCompleted(order))  # Async handling
        return result
```
"""


# Scenario 3: Security Issue

# Original code
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

# Review comment:
"""
Security: This endpoint exposes user data without authentication.
Anyone can access any user's data by guessing IDs.

Required fixes:
1. Add authentication
2. Add authorization (users can only access their own data, or admin)
3. Consider using UUIDs instead of sequential IDs

```python
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(User).filter(User.id == user_id).first()
```
"""


# Scenario 4: Performance Issue

# Original code
def get_user_orders(user_id: int) -> list[dict]:
    user = db.query(User).filter(User.id == user_id).first()
    orders = []
    for order in user.orders:
        orders.append({
            "id": order.id,
            "items": [item.name for item in order.items],  # N+1!
            "total": order.total
        })
    return orders

# Review comment:
"""
Performance: This code has an N+1 query problem. For each order,
it makes a separate query for items.

For 100 orders: 1 (user) + 1 (orders) + 100 (items) = 102 queries

Fix with eager loading:
```python
def get_user_orders(user_id: int) -> list[dict]:
    user = db.query(User)\
        .options(
            joinedload(User.orders).joinedload(Order.items)
        )\
        .filter(User.id == user_id)\
        .first()
    # Now only 1 query with JOINs
```

Or use selectinload for better performance with many items:
```python
.options(selectinload(User.orders).selectinload(Order.items))
```
"""
```

## Review Metrics

```markdown
## Healthy Review Metrics

### Time Metrics
- **Time to first review**: < 4 hours
- **Review cycle time**: < 24 hours total
- **Rework rate**: < 20% of PRs need multiple iterations

### Quality Metrics
- **Defect escape rate**: Bugs found in production vs. review
- **Review coverage**: % of code changes reviewed
- **Comment ratio**: Comments per 100 lines changed

### Team Health
- **Review distribution**: Everyone reviews, not just seniors
- **Review load balance**: No one person bottlenecked
- **Tone**: Constructive, educational comments
```

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Review code for architectural violations | sonnet | Code review with pattern matching |
| Refactor legacy code to clean architecture | opus | Complex refactoring with trade-offs |
| Calculate code coverage for module | haiku | Metric collection and reporting |
| Design domain-driven architecture | opus | Strategic design decision |
| Write test cases for edge cases | sonnet | Testing with reasoning about coverage |
| Apply decomposition pattern to class | sonnet | Refactoring with patterns |

