# OKR Setting

## Summary

**One-sentence:** Produces an OKR config (≤3 objectives + 2-4 measurable KRs each + quarter boundary + check-in cadence + named owners) so quarter goals stop being a list of features.

**Ефективно для:** Solopreneur PMs whose 'quarter goals' read like a feature list and whose KRs are activity counts instead of outcome measurements.

**One-paragraph:** OKR theatre is common: objectives become feature lists, KRs become activity counts ('ship 5 features'), and quarter-end is the first time anyone checks. This methodology enforces ≤3 objectives, 2-4 KRs per objective with numeric outcome metrics (not activity counts), a hard quarter boundary, biweekly check-ins, and named owners. Output is consumed by the roadmap + weekly planning + the 30-day post-launch review.

## Applies If (ALL must hold)

- Operator runs quarter-bounded planning (≥1 quarter horizon).
- Operator can name 1-3 outcomes worth pursuing this quarter.
- KRs can be tied to instrumented metrics.
- Biweekly check-in slot can be calendared.

## Skip If (ANY kills it)

- Pure flow / no quarter boundary — OKRs degenerate to weekly todos.
- No instrumented metrics — KRs collapse to activity counts.
- Operator unwilling to cut features for OKR focus — OKRs become a feature wishlist.
- Company-wide OKR cascade already in place — adapt to that frame, don't double-set.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| quarter dates | ISO range | calendar |
| candidate outcomes | array | founder |
| metrics instrumented per outcome | object | analytics |
| biweekly slot | recurring calendar event | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/outcome-based-roadmaps` | Sibling — roadmap layers on top of OKRs. |
| `solo/product/mvp-instrumentation-checklist` | Upstream — KRs require instrumented metrics. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_okrs` | haiku | Template fill from candidate outcomes. |
| `audit_kr_outcome_vs_activity` | sonnet | Bounded judgement: are KRs outcome metrics or activity counts? |
| `check_in_synthesis` | opus | Biweekly synthesis: are OKRs trending toward targets? |

## Templates

| File | Purpose |
|---|---|
| `templates/okr-setting.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/okr-setting.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-okr-setting.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[outcome-based-roadmaps]] — related methodology.
- [[feature-prioritization-rice]] — related methodology.
- [[metric-deviation-hypothesis-framework]] — related methodology.
- [[mvp-instrumentation-checklist]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
