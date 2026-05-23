# On-Call Rotation Bootstrap

## Summary

**One-sentence:** Bootstrap kit for designing a humane on-call rotation: shift length, escalation tree, comp-time policy, follow-the-sun handoff, on-call-load metrics, and a dual-track for new joiners.

**One-paragraph:** Faion has incident runbooks but no methodology for the rotation itself. Most teams reverse-engineer their on-call rotation from a stressed Friday afternoon and end up with single-engineer 24/7 shifts, no comp, no shadow period for new joiners, no acknowledgement SLA. This methodology defines the explicit choices: shift length, primary+secondary tiers, follow-the-sun vs single-timezone, escalation paths, comp-time policy, shadow period, on-call-load metrics with red-line thresholds. Primary output: a one-page on-call charter + paging-tool schedule + comp-time policy in HR handbook.

**Ефективно для:**

- Команди 5-30 інженерів, що піднімають продакшен-rotation з нуля.
- Перепроєктування rotation, що випалює інженерів (1 page/night).
- Узгодження comp-time policy між engineering лідером і HR.
- Onboarding новачка через shadow-period замість стресового solo.

## Applies If (ALL must hold)

- team is responsible for a production system with paying customers OR an internal SLA
- team has 5-30 engineers eligible to participate in the rotation
- no formal on-call rotation exists yet, OR existing rotation is informal and breaking
- engineering leader has budget authority for comp-time (hours-off-in-lieu OR cash) for on-call work

## Skip If (ANY kills it)

- team smaller than 5 — rotation math does not work; use a shared-pager + paid retainer
- system has no real users / no SLA — on-call is theatre; defer until you have a customer who paid you to be reachable
- pre-existing rotation works and team is happy — do not redesign without a signal of dysfunction
- regulated environment (banking, healthcare) where rotation design is governed by external compliance

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| monitoring + alerting stack | list of alerts + SLOs | platform team |
| HR / legal sign-off | comp-policy document | HR + legal |
| business-hours coverage expectations | SLA + customer commitments | customer success |
| paging tool account | PagerDuty / Opsgenie / Better Stack credentials | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[alert-noise-budget]] | Alert-quality threshold must be acceptable before rotation design adds value |
| [[dora-metrics]] | MTTR is one of the rotation-health metrics |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shift_length_proposal` | sonnet | Cross-input judgment (team size, geographic spread, alert volume) |
| `escalation_tree_design` | sonnet | Bounded judgment per alert severity |
| `comp_time_policy_drafting` | opus | Cross-function synthesis with HR + finance constraints |
| `paging_tool_config_generation` | haiku | Template fill into the chosen tool config |

## Templates

| File | Purpose |
|------|---------|
| `templates/on-call-charter.md` | One-page charter posted to team wiki |
| `templates/pagerduty-schedule.yaml` | PagerDuty schedule config skeleton |
| `templates/comp-time-policy.md` | HR-handbook-ready comp-time policy document |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-on-call-rotation-bootstrap.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[alert-noise-budget]]
- [[fast-vs-slow-burn-rule]]
- [[error-budget-policy-and-freeze-rules]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
