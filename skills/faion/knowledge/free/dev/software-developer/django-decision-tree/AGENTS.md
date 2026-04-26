# Django Code Decision Tree

## Summary

A decision framework for placing code in Django applications: views handle HTTP, services handle business logic and DB writes, utils hold pure functions, integrations wrap third-party APIs, tasks run async jobs. The dependency direction is strict: views depend on services, not vice versa.

## Why

Without an explicit placement rule, developers put business logic in views, DB queries in utils, and external API calls anywhere. This makes the codebase unpredictable, breaks testability (pure functions mixed with side effects), and creates circular imports. The tree gives every team member — including agents — a deterministic answer for where any piece of code belongs.

## When To Use

- Deciding where to implement new functionality in a Django project.
- Refactoring existing code into proper architectural layers.
- Code review to verify correct module placement.
- Onboarding agents or new developers to the project's architecture.

## When NOT To Use

- Non-Django backends — the layer names (views, serializers, tasks) are Django-specific.
- Microservices with no shared codebase — each service has its own architecture.
- Trivial scripts or management commands with no reuse requirement.

## Content

| File | What's inside |
|------|---------------|
| `content/01-decision-rules.xml` | The placement tree, layer responsibility table, dependency direction rules. |
| `content/02-examples-and-antipatterns.xml` | Correct service/utils/integration patterns; antipatterns for services-in-utils, logic-in-views, circular deps. |

## Templates

none
