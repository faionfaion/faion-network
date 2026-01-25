---
id: cd-basics
name: "Continuous Delivery Basics"
domain: DEV
skill: faion-software-developer
category: "development-practices"
parent: continuous-delivery
---

# Continuous Delivery Basics

## Overview

Continuous Delivery is a software development practice where code changes are automatically prepared for release to production. It expands on Continuous Integration by ensuring that code is always in a deployable state. Every change that passes automated tests can be released to production with the push of a button.

## When to Use

- Web applications and SaaS products
- Teams aiming for frequent releases
- When manual deployments cause bottlenecks
- Projects requiring rapid iteration
- Organizations seeking to reduce deployment risk

## Prerequisites

- Continuous Integration in place
- Comprehensive automated testing
- Version control (everything in code)
- Infrastructure as Code
- Feature flags (for incomplete features)

## Key Principles

### Every Commit is Releasable

```markdown
## Requirements
- Automated testing at every stage
- No manual testing gates
- Feature flags for incomplete work
- Backward compatible changes

## Benefits
- Reduced risk (small batches)
- Faster feedback
- Lower deployment stress
- Easy rollback
```

### Deployment Pipeline

```markdown
## Pipeline Stages
Commit → Build → Test → Stage → Production
   ↓       ↓       ↓       ↓         ↓
 Trigger  Compile  Unit   Deploy   Deploy
         Package  Integ   Test    Manual/Auto
                  E2E    Verify
```

### Automation Everything

```markdown
## Automate
✅ Build process
✅ Test execution
✅ Environment provisioning
✅ Database migrations
✅ Configuration management
✅ Deployment
✅ Monitoring setup
✅ Rollback

## Manual (Approval Only)
- Production deployment trigger (CD)
- Or fully automated (Continuous Deployment)
```

## Database Migrations

```python
# Continuous Delivery requires safe migrations
# Use backward-compatible migrations only

# migrations/versions/001_add_user_email.py

"""Add email column to users table."""

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Step 1: Add nullable column (backward compatible)
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('users', 'email')

# Next deployment: make required
# migrations/versions/002_make_email_required.py
def upgrade():
    # Step 2: After data migration, add constraint
    op.alter_column('users', 'email', nullable=False)
```

## Feature Flags for CD

```python
# features/flags.py
from typing import Optional
import httpx

class FeatureFlagService:
    """
    Feature flags enable CD by hiding incomplete features.

    Deployment: Code ships to production
    Release: Feature becomes visible to users
    """

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self._cache: dict[str, bool] = {}

    def is_enabled(
        self,
        flag: str,
        user_id: Optional[str] = None,
        default: bool = False
    ) -> bool:
        """
        Check if feature flag is enabled.

        Supports:
        - Global on/off
        - Percentage rollout
        - User targeting
        - Environment targeting
        """
        cache_key = f"{flag}:{user_id or 'global'}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = httpx.post(
                f"{self.api_url}/flags/{flag}/evaluate",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"user_id": user_id}
            )
            result = response.json().get("enabled", default)
            self._cache[cache_key] = result
            return result
        except Exception:
            return default

# Usage in code
feature_flags = FeatureFlagService(
    api_url=settings.FEATURE_FLAG_URL,
    api_key=settings.FEATURE_FLAG_API_KEY
)

@app.get("/dashboard")
async def dashboard(user: User):
    data = get_dashboard_data(user)

    # New feature behind flag
    if feature_flags.is_enabled("new_analytics", user.id):
        data["analytics"] = get_new_analytics(user)

    return data
```

## CD vs CI vs Continuous Deployment

| Aspect | CI | CD (Delivery) | CD (Deployment) |
|--------|----|--------------|-----------------|
| Build automation | ✅ | ✅ | ✅ |
| Automated tests | ✅ | ✅ | ✅ |
| Deploy to staging | ❌ | ✅ | ✅ |
| Production-ready | ❌ | ✅ | ✅ |
| Auto-deploy prod | ❌ | ❌ (manual) | ✅ (auto) |
| Risk level | Low | Medium | Higher |

## Common Challenges

### "We Can't Deploy That Often"

```markdown
## Cause
- Large batch sizes
- Manual testing requirements
- Fear of production issues

## Solutions
1. Smaller changes (< 200 lines)
2. Comprehensive automated tests
3. Feature flags
4. Canary deployments
5. Fast rollback capability
```

### "Testing Takes Too Long"

```markdown
## Cause
- Serial test execution
- Slow E2E tests
- Flaky tests

## Solutions
1. Parallelize tests
2. Test pyramid (more unit, fewer E2E)
3. Fix or quarantine flaky tests
4. Run E2E only on staging
5. Use contract testing
```

### "Database Changes Break CD"

```markdown
## Cause
- Non-backward-compatible migrations
- Long-running migrations
- Data migration during deployment

## Solutions
1. Expand-contract pattern
2. Split schema and data migrations
3. Online schema change tools
4. Blue-green for database changes
```

## DORA Metrics

```markdown
## Elite Performance (Target)
- Deployment frequency: On-demand (multiple per day)
- Lead time for changes: < 1 hour
- Change failure rate: 0-15%
- Time to restore: < 1 hour

## Measuring
- Track every deployment
- Measure from commit to production
- Count rollbacks and incidents
- Time to recovery from incidents
```

## Implementation Roadmap

```markdown
## Phase 1: CI Foundation (2-4 weeks)
- [ ] Automated builds on every commit
- [ ] Unit tests in pipeline (> 70% coverage)
- [ ] Code quality gates (lint, type check)
- [ ] Build artifacts stored

## Phase 2: Automated Testing (4-6 weeks)
- [ ] Integration tests automated
- [ ] E2E tests on staging
- [ ] Test parallelization
- [ ] < 15 min total pipeline time

## Phase 3: Staging Deployment (2-4 weeks)
- [ ] Auto-deploy to staging
- [ ] Staging mirrors production
- [ ] Smoke tests automated
- [ ] Feature flags implemented

## Phase 4: Production Deployment (4-8 weeks)
- [ ] One-click production deploy
- [ ] Deployment strategies (rolling/canary)
- [ ] Automated rollback
- [ ] Monitoring and alerting

## Phase 5: Continuous Deployment (optional)
- [ ] Auto-deploy to production
- [ ] Canary analysis automated
- [ ] Progressive delivery
- [ ] Chaos engineering
```

## References

- [Continuous Delivery - Jez Humble](https://continuousdelivery.com/)
- [Accelerate - Nicole Forsgren et al.](https://itrevolution.com/accelerate-book/)
- [The DevOps Handbook](https://itrevolution.com/the-devops-handbook/)
- [DORA Metrics](https://www.devops-research.com/research.html)
- [Martin Fowler - Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html)

## Related

- [cd-pipelines.md](cd-pipelines.md) - Pipeline implementation and deployment strategies
