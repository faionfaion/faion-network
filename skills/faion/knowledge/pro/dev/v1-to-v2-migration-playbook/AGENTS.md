---
slug: v1-to-v2-migration-playbook
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Solo-SaaS pivot playbook: data + auth + billing migration when the schema and business model shift between v1 and v2 without breaking paying users.
content_id: "54d5008643123502"
complexity: deep
produces: playbook-step
est_tokens: 4100
tags: [migration, v1-v2, saas-pivot, data-migration, auth, billing]
---
# V1 to V2 Migration Playbook

## Summary

**One-sentence:** Solo-SaaS pivot playbook: data + auth + billing migration when the schema and business model shift between v1 and v2 without breaking paying users.

**One-paragraph:** Solo-SaaS pivot playbook: data + auth + billing migration when the schema and business model shift between v1 and v2 without breaking paying users. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-v1-to-v2-migration-playbook.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- P1 solo SaaS builder pivots від failed v1 to v2 із paying users to keep.
- Schema-shift (relational → multi-tenant, billing model change) — потрібен migration plan.
- Auth provider або session model змінюється (e.g. Magic Link → Clerk).
- Multi-week cutover з reversible checkpoints (можна rollback на v1).

## Applies If (ALL must hold)

- Paying users on v1 that must keep working through cutover
- Schema or business-model shift between v1 and v2 (not a refactor)
- Reversible cutover plan possible (rollback v1, replay events)
- Solo / small team — methodology aimed at low-ceremony execution

## Skip If (ANY kills it)

- No paying users — just deploy v2 and email any beta testers
- v2 is a pure refactor (same schema, same model) — use strangler-fig instead
- Large team / enterprise context — methodology too lite
- No rollback authority (one-way data migration) — methodology insufficient

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-v1-to-v2-migration-playbook` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON instance matching the output contract |
| `templates/skeleton.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-v1-to-v2-migration-playbook.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[strangler-fig-migration-pattern]]
- [[team-rfc-process-for-devs]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
