# Extreme Programming

## Summary

**One-sentence:** XP adoption playbook: TDD red-green-refactor, pair programming or AI-pair, trunk-based development with green CI, continuous refactoring, on-site customer (or proxy), 40-hour week.

**One-paragraph:** Extreme Programming (XP) prescribes a tight feedback loop: write a failing test first, code minimally to green, refactor with tests green, integrate via trunk multiple times a day. The methodology fails when teams pick TDD without CI, when refactor is skipped 'until later', when pair-rotation never happens, when the customer is absent, and when overtime makes the discipline collapse. This playbook step produces an adoption plan: per-practice introduction order, success metrics per practice, and a 4-week cadence to measure adherence and lasso back drift.

**Ефективно для:**

- Команда переходить з ad-hoc на disciplined dev - XP як baseline.
- Test coverage низький - TDD як основа.
- Refactoring odkładаний - вмонтувати в red-green-refactor цикл.
- Інтеграція раз на тиждень - впровадити trunk-based.
- Solo founder з AI - AI-pair замість human-pair.

## Applies If (ALL must hold)

- Team can adopt TDD discipline (write test first).
- Build runs in <10 minutes (TDD cycle requires fast feedback).
- Codebase under version control with trunk-based discipline feasible.
- Customer or proxy is available for daily question turn-around.

## Skip If (ANY kills it)

- Pre-MVP discovery work - code is throwaway; TDD cost not justified.
- Hard real-time embedded firmware with no test harness - different methodology.
- Compliance forbids trunk-based (regulated rollback windows).
- Build time > 30 minutes - TDD becomes impractical without infra fix first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Test framework | pytest / jest / cargo test / etc. | engineering |
| CI green baseline | main branch builds green with <10min CI | platform |
| Customer access | named person + response SLA | product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[performance-testing]] | shared CI infrastructure on which XP relies. |
| [[solo-self-code-review-protocol]] | review discipline for the solo case. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: TDD cycle, trunk-based + green CI, paired + rotated, refactor while green, on-site customer, 40h week, small releases | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step adoption plan: CI < 10min, TDD, trunk-based, pairing, releases | ~900 |
| `content/05-examples.xml` | essential | Worked example for a 5-engineer team XP rollout | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ci-optimisation` | sonnet | Per-pipeline judgement on parallelisation. |
| `tdd-coaching` | haiku | Boilerplate pair-programming session protocol. |
| `branch-policy` | sonnet | Trade-off feature flags vs branch isolation. |
| `metrics-review` | opus | Stakes high; misread metrics undermine the rollout. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adoption-plan.md` | Markdown 4-week XP adoption plan with metrics gates. |
| `templates/ci-config-snippet.yaml` | Example GitHub Actions snippet sharding tests to keep CI <10min. |
| `templates/pre-commit-xp.yaml` | Pre-commit hooks enforcing TDD-friendly gates. |
| `templates/_smoke-test.json` | Minimum viable XP adoption plan for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-xp-extreme-programming.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[solo-self-code-review-protocol]]
- [[spec-driven-debugging]]
- [[performance-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - CI speed, branch age, customer SLA, release cadence - onto a rule from `content/01-core-rules.xml`. Use it before adopting XP: it catches tdd-without-fast-ci and long-branches upstream.
