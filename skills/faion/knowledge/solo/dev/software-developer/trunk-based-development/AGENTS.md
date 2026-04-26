# Trunk-Based Development

## Summary

Source-control branching model where all developers commit to a single trunk (main/master) via
short-lived branches (≤1-2 days) or directly. Trunk must always be releasable; incomplete work
hides behind feature flags. Core rules: branch lifetime ≤48h, PR diff ≤200 lines, CI must pass
in <10 min, no `--no-verify`, never push directly to main.

## Why

Long-lived branches accumulate merge debt and delay integration feedback. Trunk-Based
Development (TBD) forces small, reviewable increments, enabling CI/CD and correlating with
elite DORA metrics (deploy on demand, lead time <1 h). Feature flags decouple deploy from
release, allowing dark-launching and kill-switching without a rollback.

## When To Use

- Solo or small teams shipping multiple times per day where merge friction is the bottleneck
- Codebases with strong CI (<10 min) and ≥70% meaningful test coverage
- Products with feature flag infrastructure (LaunchDarkly, Flagsmith, Unleash, OpenFeature)
- LLM-driven dev loops — short branches keep agent context windows shallow
- Migrations to CD: TBD is the prerequisite branching model for elite DORA metrics

## When NOT To Use

- Pre-CI projects: "trunk is always broken" without automated gates
- Regulated industries mandating per-feature branch isolation and signed reviews
- OSS with external contributors — fork-and-PR is structurally a long-lived branch
- Mobile apps with infrequent store releases — release branches still fit better
- Junior-heavy teams without code review SLA — fast-merge amplifies bad commits

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Branch lifetime, PR size, CI speed, feature flag rules, TBD vs GitFlow |
| `content/02-patterns.xml` | Short-lived branch flow, Branch by Abstraction, keystone interface, dark launch |
| `content/03-ci-tooling.xml` | Pre-commit hooks, GitHub Actions CI pipeline, DORA metrics |

## Templates

| File | Purpose |
|------|---------|
| `templates/stale-branches.sh` | List branches older than N days for branch-watchdog agent |
| `templates/trunk-ci.yml` | GitHub Actions workflow with test, lint, type-check, staging deploy |
