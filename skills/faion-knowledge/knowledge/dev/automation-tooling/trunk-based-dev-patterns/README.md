---
id: trunk-based-dev-patterns
name: "Trunk-Based Development: Patterns"
domain: DEV
skill: faion-software-developer
category: "development-practices"
---

# Trunk-Based Development: Patterns

## Best Practices

### Feature Flags

```python
# Hide incomplete features behind flags
# Deploy to production without exposing

from feature_flags import is_enabled

def get_user_profile(user_id: str):
    profile = fetch_profile(user_id)

    # New feature behind flag
    if is_enabled("show_activity_feed", user_id):
        profile["activity"] = fetch_activity(user_id)

    return profile

# Feature flag service
class FeatureFlags:
    def __init__(self, provider: FlagProvider):
        self.provider = provider

    def is_enabled(self, flag: str, user_id: str = None) -> bool:
        """
        Check if feature is enabled.
        Supports:
        - Global on/off
        - Percentage rollout
        - User-specific targeting
        """
        return self.provider.evaluate(flag, {"user_id": user_id})
```

### Branch by Abstraction

```python
# Large refactoring without feature branches
# Create abstraction layer, swap implementation

# Step 1: Create abstraction
class PaymentProcessor(Protocol):
    def process(self, amount: Decimal) -> PaymentResult: ...

# Step 2: Old implementation
class LegacyPaymentProcessor:
    def process(self, amount: Decimal) -> PaymentResult:
        return self.old_gateway.charge(amount)

# Step 3: New implementation (behind flag)
class NewPaymentProcessor:
    def process(self, amount: Decimal) -> PaymentResult:
        return self.stripe.create_charge(amount)

# Step 4: Router (use flag to switch)
def get_payment_processor() -> PaymentProcessor:
    if feature_flags.is_enabled("new_payment"):
        return NewPaymentProcessor()
    return LegacyPaymentProcessor()

# Step 5: After validation, remove old code
# Delete LegacyPaymentProcessor
# Remove feature flag
# Direct instantiation of NewPaymentProcessor
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
# Ensure quality before pushing to trunk

repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: pytest --tb=short -q
        language: system
        pass_filenames: false

      - id: lint
        name: Lint code
        entry: ruff check .
        language: system
        pass_filenames: false

      - id: type-check
        name: Type check
        entry: mypy src/
        language: system
        pass_filenames: false
```

### CI Pipeline for TBD

```yaml
# .github/workflows/trunk.yml
name: Trunk CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=src --cov-fail-under=80

      - name: Lint
        run: ruff check .

      - name: Type check
        run: mypy src/

      # Fast feedback is crucial
      # Total time should be < 10 minutes

  deploy-to-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: ./deploy.sh staging

  # Optional: auto-deploy to production
  # deploy-to-production:
  #   needs: deploy-to-staging
  #   ...
```

## Common Patterns

### Keystone Interface Pattern

```python
# Build complete feature in parts
# Only enable when all parts ready

# Part 1: Add endpoint (returns 404)
@app.get("/api/v2/users/{user_id}/activity")
async def get_activity(user_id: str):
    raise HTTPException(status_code=404, detail="Coming soon")

# Part 2: Add backend logic (not called yet)
class ActivityService:
    def get_recent_activity(self, user_id: str):
        return self.repo.get_activity(user_id, limit=50)

# Part 3: Connect (behind flag)
@app.get("/api/v2/users/{user_id}/activity")
async def get_activity(user_id: str):
    if not feature_flags.is_enabled("activity_api"):
        raise HTTPException(status_code=404)
    return activity_service.get_recent_activity(user_id)

# Part 4: Enable flag, monitor, remove flag
```

### Dark Launching

```python
# Deploy to production, but don't expose
# Test with production traffic

async def process_order(order: Order):
    # Current implementation
    result = await current_processor.process(order)

    # Dark launch: run new implementation in parallel
    if feature_flags.is_enabled("dark_launch_new_processor"):
        try:
            new_result = await new_processor.process(order)
            # Compare results, log differences
            if result != new_result:
                logger.warning(f"Result mismatch: {result} vs {new_result}")
        except Exception as e:
            logger.error(f"Dark launch error: {e}")

    # Always return current result
    return result
```

## Challenges and Solutions

### "Trunk is Always Broken"

```markdown
## Cause
- Insufficient automated tests
- No pre-commit checks
- Slow CI feedback

## Solutions
1. Gate merges on passing tests
2. Add pre-commit hooks
3. Speed up CI (< 10 min)
4. Use feature flags for incomplete work
5. Smaller commits
```

### "Need Long-Lived Branches"

```markdown
## Cause
- Large features taking weeks
- No feature flag infrastructure
- Compliance requirements

## Solutions
1. Break feature into smaller parts
2. Implement feature flags
3. Use Branch by Abstraction
4. For compliance: release branches only
```

### "Code Review Bottleneck"

```markdown
## Cause
- Large PRs
- Few reviewers
- Async-only review

## Solutions
1. Smaller PRs (< 200 lines)
2. Pair programming (instant review)
3. Fast review SLA (< 4 hours)
4. Rotate reviewers
```

## Integration with SDD

### Task Execution

```markdown
## TBD + SDD Workflow
1. Create task in .aidocs/backlog/
2. Move to .aidocs/todo/
3. Create short-lived branch (< 1 day)
4. Implement with feature flags
5. Open PR, fast review
6. Merge to trunk
7. Move task to .aidocs/done/

## Feature Flags for SDD
- Flag name matches task ID
- Enable after thorough testing
- Remove after stability confirmed
```

### Continuous Delivery

```markdown
## Auto-deploy from Trunk
- trunk push → CI → staging deploy
- Manual production deploy (or auto with approval)
- Feature flags control visibility

## Task Completion
- Task done = merged to trunk
- Task deployed = feature flag enabled
- Task complete = flag removed
```

## References

- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [Feature Flags - Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
- [Branch by Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html)
- [Dark Launching](https://martinfowler.com/bliki/DarkLaunching.html)
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement trunk-based-dev-patterns pattern | haiku | Straightforward implementation |
| Review trunk-based-dev-patterns implementation | sonnet | Requires code analysis |
| Optimize trunk-based-dev-patterns design | opus | Complex trade-offs |

