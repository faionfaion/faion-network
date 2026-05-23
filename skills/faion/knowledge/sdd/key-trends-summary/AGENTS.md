# Key Trends Summary 2025-2026

## Summary

**One-sentence:** Produces an orientation report on 6 SDD shifts (SDD-as-paradigm + docs-as-code + ADRs + LLM-first + platform engineering + OpenTelemetry) so planning sessions start with shared 2025-2026 context.

**Ефективно для:** Solo PMs and architects whose planning sessions stall on outdated assumptions because nobody re-read the trend map this year.

**One-paragraph:** Architectural planning starts from stale context when the trend map isn't refreshed. This methodology pins the 2025-2026 orientation: SDD as the dominant paradigm, docs-as-code, ADRs as standard at AWS/GCP/Azure, LLM-first workflows, platform-engineering adoption (45%→80%), OpenTelemetry as the #2 CNCF project. Load once per planning cycle, not per task. Output is consumed by design-docs-patterns and architecture-decision-records.

## Applies If (ALL must hold)

- Quarterly architectural planning session.
- Onboarding new contributor to architecture decisions.
- Pre-RFC orientation before drafting cross-org docs.
- Annual roadmap review.

## Skip If (ANY kills it)

- Per-task work — load is per-planning-cycle, not per-task.
- Operations / incident response — different context.
- Operator already loaded the report within 90 days.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| planning session scheduled | calendar slot | operator |
| trend report source | doc/url | repo |
| audience role list | array | operator |
| last_loaded_at timestamp | datetime | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/design-docs-big-tech` | Sibling — surveys company practices. |
| `solo/sdd/sdd/design-docs-patterns` | Downstream — uses trend context for format selection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/key-trends-summary.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/key-trends-summary.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-key-trends-summary.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[design-docs-patterns]] — related methodology.
- [[design-docs-big-tech]] — related methodology.
- [[architecture-decision-records]] — related methodology.
- [[living-documentation]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
