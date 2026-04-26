# Feature Flags

## Summary

Use feature flags to gate incomplete or experimental code behind a runtime toggle, enabling trunk-based development, progressive rollouts (percentage-based or group-based), and instant rollback without deployment. Flags must be short-lived (except ops/kill-switch types) and removed once fully rolled out.

## Why

Flags decouple deployment from release: code ships to production but stays inactive until deliberately enabled. This eliminates long-running feature branches, makes canary rollouts trivial, and provides a kill switch for production incidents. Flag debt (flags never removed) is the main failure mode — track creation date and expected cleanup date in a registry.

## When To Use

- Hiding incomplete features in trunk-based development
- Gradual rollouts to 1% → 10% → 50% → 100% of users
- A/B testing with deterministic user bucketing
- Kill switches for risky payment or external-service integrations
- Customer-specific features or beta access

## When NOT To Use

- Configuration values (timeouts, limits) — use environment variables or config files
- Access control / authorization — use RBAC/permissions, not flags
- Permanent business logic branches — model as explicit product variants instead
- Flags that are on 100% for more than 2 weeks — clean up or convert to config

## Content

| File | What's inside |
|------|---------------|
| `content/01-flag-types.xml` | Release / experiment / ops / permission / kill-switch categories with lifespan guidance |
| `content/02-implementation.xml` | FeatureFlagManager with env override + percentage rollout; decorator pattern; context manager |
| `content/03-lifecycle.xml` | Planning → development → rollout → cleanup phases; flag registry schema; stale-flag audit |

## Templates

| File | Purpose |
|------|---------|
| `templates/flag-manager.py` | FeatureFlagManager with env overrides and percentage bucketing via MD5 hash |
| `templates/flag-registry.json` | Registry schema for tracking flag owner, type, created date, cleanup date |
