# Founder Time Audit Tool

## Summary

**One-sentence:** Two-week personal time-allocation audit artefact: delivery vs sales vs ops vs strategic split, founder-bottleneck flag, suggested delegations or drops, next-cycle target band.

**One-paragraph:** Founder Time Audit Tool delivers a defensible report artefact for the pro PM cohort. It binds typed inputs to a strict output contract, enumerates known failure modes, and routes between optimistic and conservative variants via a decision tree. Downstream consumers (human reviewer or agent) accept the artefact without re-deriving the rationale because every claim cites an input by name.

**Ефективно для:**

- Founder, що відчуває себе bottleneck-ом і має 2 тижні clean time-tracking data.
- Solo консультант з 2-3 паралельними engagement-ами, що шукає systematic over-commit.
- Bootstrapper після першого hiring round, що оцінює, які задачі можна делегувати.
- Co-founder pair, що калібрує розподіл technical/business навантаження.

## Applies If (ALL must hold)

- the operator is a founder or solo-PM whose own time is the limiting resource
- two consecutive weeks of time-tracking data exist or can be captured
- the founder has authority to delegate, drop, or reschedule audited activities
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- founder is in active fundraising and a fixed schedule is non-negotiable — audit insights stale
- the team already runs OKR + capacity tooling that covers personal allocation — duplication overhead
- founder lacks delegation authority (e.g. solo-operator with no team) — audit possible but suggested-delegations bullet empty

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| recent context for the triggering activity | log/doc/ticket | last 30 days |
| write-access to the artefact store | repo / wiki / decision log | team policy |
| named accountable owner downstream | handle / email / role | RACI / org chart |
| baseline conventions | CLAUDE.md / AGENTS.md / CONVENTIONS.md | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | testable rules with statement + rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the report + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | step-by-step procedure with decision-gates | ~900 |
| `content/05-examples.xml` | essential | worked example end-to-end | ~700 |
| `content/06-decision-tree.xml` | essential | root question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs` | haiku | template fill from typed inputs |
| `synthesize-founder_time_audit_tool` | sonnet | per-instance judgment with bounded inputs |
| `review-for-stakes` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/founder-time-audit-tool.md` | report skeleton with required fields + 5-line header |
| `templates/founder-time-audit-tool.schema.json` | JSON Schema for the output contract |
| `templates/_smoke-test.md` | minimum viable filled-in example |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-founder-time-audit-tool.py` | enforce output-contract against template instance | after subagent returns, before downstream consumer reads |

## Related

- [[project-manager]]
- [[pm-traditional]]
- [[founder-as-pm-survival-kit]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, stakes, recurrence) onto a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply or whether to skip the methodology entirely.
