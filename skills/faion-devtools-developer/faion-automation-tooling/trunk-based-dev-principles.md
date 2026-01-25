---
id: trunk-based-dev-principles
name: "Trunk-Based Development: Principles"
domain: DEV
skill: faion-software-developer
category: "development-practices"
---

# Trunk-Based Development: Principles

## Overview

Trunk-Based Development (TBD) is a source-control branching model where developers collaborate on code in a single branch called "trunk" (or "main/master"), resisting any pressure to create long-lived development branches. Small, frequent commits to trunk enable Continuous Integration and reduce merge conflicts.

## When to Use

- Teams practicing CI/CD
- Projects requiring fast iteration
- When merge conflicts are a problem
- High-performing DevOps teams
- Feature flag infrastructure exists
- Strong automated testing in place

## When to Avoid

- Weak test coverage
- No CI/CD pipeline
- Regulatory compliance requiring branch isolation
- Open-source projects with external contributors

## Key Principles

### Single Source of Truth

```markdown
## Rules
- One main branch ("trunk" / "main")
- All developers commit to trunk
- Trunk is always releasable
- No long-lived feature branches (> 1-2 days max)

## Benefits
- Everyone sees latest code
- No merge hell
- Faster feedback
- Simpler mental model
```

### Small, Frequent Commits

```markdown
## Commit Patterns
- At least once per day
- Smaller changes = easier review
- Each commit builds and tests pass
- Ideally < 200 lines changed

## Anti-patterns
- Commits once a week
- "WIP" commits to trunk
- Large refactoring in one commit
```

### Trunk is Always Releasable

```markdown
## Enforced By
- Automated tests (must pass to merge)
- Feature flags (hide incomplete work)
- Code review (short turnaround)
- CI pipeline (fast feedback)

## If Trunk Breaks
- Stop everything
- Fix immediately
- Root cause analysis
- Improve tests/gates
```

## Branching Strategies

### Pure Trunk (Commit Directly)

```bash
# For small teams (2-3) with high trust
# and strong local testing

# Work on trunk directly
git checkout main
git pull

# Make changes
vim src/feature.py

# Test locally
pytest

# Commit directly to trunk
git add .
git commit -m "feat: add user validation"
git push origin main
```

### Short-Lived Feature Branches

```bash
# For most teams (recommended)
# Branches live < 1-2 days

# Create short-lived branch
git checkout -b feat/user-validation
git push -u origin feat/user-validation

# Work in small increments
vim src/feature.py
git add . && git commit -m "add email validator"

# Frequently integrate from main
git fetch origin main
git rebase origin/main

# Open PR same day
gh pr create --title "Add user validation" --body "..."

# Merge same day (after review)
gh pr merge --squash

# Delete branch immediately
git checkout main
git pull
git branch -d feat/user-validation
```

### Release Branches (Optional)

```markdown
## When Needed
- Long release testing cycles
- Regulatory requirements
- Multiple versions in production

## Rules
- Branch from trunk for release
- Only hotfixes go to release branch
- Cherry-pick fixes back to trunk
- Never develop on release branch

## Flow
main → release/v2.1 → production
         ↓ hotfix
       release/v2.1 → cherry-pick to main
```

## TBD vs GitFlow

| Aspect | Trunk-Based | GitFlow |
|--------|-------------|---------|
| Main branches | 1 (trunk) | 5+ (main, develop, feature/, release/, hotfix/) |
| Branch lifetime | Hours to 1-2 days | Days to weeks |
| Merge conflicts | Rare, small | Common, large |
| Deployment | Continuous | Scheduled releases |
| Complexity | Simple | Complex |
| Best for | Web apps, SaaS | Mobile apps, packaged software |

## Code Review in TBD

```markdown
## Fast Reviews Required
- Review within 4 hours (ideally 1 hour)
- Small PRs = fast reviews
- Async review or pair on complex changes

## Review Checklist
- [ ] Tests pass
- [ ] Feature flag if needed
- [ ] Backward compatible
- [ ] No breaking changes to trunk

## Pair Programming Alternative
- Write code together = no review needed
- Pair = instant review
- Good for complex changes
```

## Metrics

```markdown
## Leading Indicators
- Branch lifetime (target: < 1 day)
- PR size (target: < 200 lines)
- CI time (target: < 10 minutes)
- Review time (target: < 4 hours)

## Lagging Indicators
- Deployment frequency
- Lead time for changes
- Change failure rate
- Time to restore service

## DORA Metrics
TBD correlates with elite DORA performers:
- Deploy on demand (multiple times per day)
- Lead time < 1 hour
- Change failure rate < 15%
- Time to restore < 1 hour
```

## Implementation Roadmap

```markdown
## Phase 1: Foundation (2-4 weeks)
- [ ] Improve test coverage (> 70%)
- [ ] Speed up CI (< 10 min)
- [ ] Add pre-commit hooks
- [ ] Define branch naming conventions

## Phase 2: Short-Lived Branches (2-4 weeks)
- [ ] Set branch lifetime limit (2 days)
- [ ] Implement feature flags
- [ ] Fast code review SLA
- [ ] Monitor branch lifetime

## Phase 3: Continuous Deployment (4-8 weeks)
- [ ] Auto-deploy to staging
- [ ] Implement dark launching
- [ ] Add production monitoring
- [ ] Optional: auto-deploy to prod

## Phase 4: Optimization (ongoing)
- [ ] Track DORA metrics
- [ ] Optimize CI further
- [ ] Reduce feature flag debt
- [ ] Continuous improvement
```

## References

- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [Accelerate - Nicole Forsgren et al.](https://itrevolution.com/accelerate-book/)
- [Continuous Delivery - Jez Humble](https://continuousdelivery.com/)
- [Feature Flags - Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
