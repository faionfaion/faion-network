# MVP Instrumentation Checklist

## Summary

**One-sentence:** Produces a checklist proving an MVP ships with ≥1 acquisition event + ≥1 activation event + ≥1 retention event + ≥1 revenue event wired BEFORE first user touches it.

**Ефективно для:** Solopreneurs launching an MVP and only realising after launch that they have no signal on which step in the funnel users die at.

**One-paragraph:** MVPs launch without instrumentation and the operator finds out a month later that signups exist in Stripe but no event traces the funnel — and the operator now has to retro-instrument with hypotheses instead of data. This methodology produces a binary checklist (each step instrumented yes/no) that gates the launch event: ≥1 acquisition event, ≥1 activation event, ≥1 retention event, ≥1 revenue event, plus the dashboard URL. Output is consumed by the launch-tier-decision-frame as a readiness signal.

## Applies If (ALL must hold)

- Operator is shipping an MVP to first users in the next 14 days.
- Operator has an analytics tool (Plausible / GA4 / PostHog / Mixpanel) wired or installable in <2h.
- Operator can name the four funnel steps (acquire / activate / retain / revenue) for this product.
- Operator has a dashboard surface where the events can be displayed.

## Skip If (ANY kills it)

- Product is a research prototype with no funnel intent.
- Operator refuses to install an analytics tool (privacy posture extreme) — alternate metrics-via-server-logs is a separate methodology.
- MVP is internal-only — funnel events are not meaningful.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| analytics tool URL | URL | operator |
| named funnel steps | array of 4 strings | founder |
| dashboard surface URL | URL | operator |
| launch date | ISO date | calendar |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/launch-tier-decision-frame` | Downstream — readiness gate consumes this checklist. |
| `solo/product/metric-deviation-hypothesis-framework` | Downstream — hypothesis framework requires instrumented events. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `verify_events_wired` | haiku | Per-event yes/no check via dashboard query. |
| `name_funnel_steps` | sonnet | Bounded judgement: pick the 4 steps appropriate to this product shape. |
| `readiness_synthesis` | opus | Synthesis when chained with launch-tier-decision-frame. |

## Templates

| File | Purpose |
|---|---|
| `templates/mvp-instrumentation-checklist.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/mvp-instrumentation-checklist.md` | Markdown skeleton with the required fields. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-mvp-instrumentation-checklist.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[launch-tier-decision-frame]] — related methodology.
- [[metric-deviation-hypothesis-framework]] — related methodology.
- [[solo-kpi-dashboard-template]] — related methodology.
- [[vanity-metrics-audit]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
