---
id: continuous-delivery
name: "Continuous Delivery"
domain: DEV
skill: faion-software-developer
category: "development-practices"
---

# Continuous Delivery (CD)

**Status:** Index file - content split into focused modules.

## Contents

| File | Purpose | Lines |
|------|---------|-------|
| [cd-basics.md](cd-basics.md) | Principles, practices, challenges, roadmap | ~350 |
| [cd-pipelines.md](cd-pipelines.md) | Pipeline implementation, deployment strategies | ~400 |

## Quick Reference

### What is CD?

Continuous Delivery is a software development practice where code changes are automatically prepared for release to production. Every change that passes automated tests can be released with a button push.

### Key Concepts

- **Every commit is releasable** - automated testing, feature flags, backward compatibility
- **Deployment pipeline** - automated path from commit to production
- **Automation everything** - build, test, deploy, rollback
- **Feature flags** - deploy code, release features separately
- **Backward-compatible migrations** - safe database changes

### CD vs CI vs Continuous Deployment

| Aspect | CI | CD (Delivery) | CD (Deployment) |
|--------|----|--------------|-----------------|
| Build automation | ✅ | ✅ | ✅ |
| Automated tests | ✅ | ✅ | ✅ |
| Deploy to staging | ❌ | ✅ | ✅ |
| Production-ready | ❌ | ✅ | ✅ |
| Auto-deploy prod | ❌ | ❌ (manual) | ✅ (auto) |

### Deployment Strategies

- **Blue-Green** - Two identical environments, instant switch
- **Canary** - Gradual traffic shift (10% → 50% → 100%)
- **Rolling** - Gradual pod replacement (default Kubernetes)

### DORA Metrics (Elite Performance)

- Deployment frequency: Multiple per day
- Lead time for changes: < 1 hour
- Change failure rate: 0-15%
- Time to restore: < 1 hour

## When to Read What

| Task | Read |
|------|------|
| Understanding CD principles | [cd-basics.md](cd-basics.md) |
| Setting up CD pipeline | [cd-pipelines.md](cd-pipelines.md) |
| Database migrations for CD | [cd-basics.md](cd-basics.md) - Database Migrations |
| Feature flags | [cd-basics.md](cd-basics.md) - Feature Flags |
| Deployment strategies | [cd-pipelines.md](cd-pipelines.md) - Deployment Strategies |
| Health checks & monitoring | [cd-pipelines.md](cd-pipelines.md) - Monitoring and Rollback |
| Common challenges | [cd-basics.md](cd-basics.md) - Common Challenges |
| Implementation roadmap | [cd-basics.md](cd-basics.md) - Implementation Roadmap |

## References

- [Continuous Delivery - Jez Humble](https://continuousdelivery.com/)
- [Accelerate - Nicole Forsgren et al.](https://itrevolution.com/accelerate-book/)
- [The DevOps Handbook](https://itrevolution.com/the-devops-handbook/)
- [DORA Metrics](https://www.devops-research.com/research.html)
- [Martin Fowler - Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html)

## Related

- [feature-flags.md](feature-flags.md) - Feature flag patterns
- [tdd-workflow.md](tdd-workflow.md) - Test-driven development
- [trunk-based-dev-principles.md](trunk-based-dev-principles.md) - Core TBD principles
- [trunk-based-dev-patterns.md](trunk-based-dev-patterns.md) - TBD patterns and practices
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement continuous-delivery pattern | haiku | Straightforward implementation |
| Review continuous-delivery implementation | sonnet | Requires code analysis |
| Optimize continuous-delivery design | opus | Complex trade-offs |

