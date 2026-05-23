# Cross Role Handoff Protocol

## Summary

**One-sentence:** Pins the canonical handoff protocol (definition-of-ready + artifact list + sign-off) for BA → Architect → Dev → QA → DevOps transitions in multi-week product-team flows.

**One-paragraph:** Pins the canonical handoff protocol (definition-of-ready + artifact list + sign-off) for BA → Architect → Dev → QA → DevOps transitions in multi-week product-team flows. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у в команді з 5+ ролей — щоб BA-Architect-Dev-QA handoff не зривався мовчки на artifact-list gap.

## Applies If (ALL must hold)

- Product team has ≥4 distinct roles (BA / Architect / Dev / QA / DevOps).
- Multi-week flows exist where work crosses ≥3 role boundaries.
- ≥1 handoff failure happened in the last quarter (silent drop, rework).
- A named PM owns the protocol.

## Skip If (ANY kills it)

- Single-role pair (Dev↔QA only) — pair-level checklist is cheaper.
- Team uses paired-flow / mob-style work — handoffs do not exist.
- Org mandates a different lifecycle template — comply.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Role roster + responsibilities | doc | delivery-org |
| Lifecycle map | diagram | SDD constitution |
| Prior handoff-failure logs | tickets | issue tracker |
| Sign-off mechanism | tool | tracker workflow OR a checklist file |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager/1on1-template-managers` | Per-role 1:1 cadence where handoff health gets surfaced. |
| `geek/pm/dependency-graph-reasoning` | Cross-team dependencies are a superset of cross-role handoffs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-handoff-doc` | haiku | Template fill per transition. |
| `artifact-list-derive` | sonnet | Bounded judgement: what is on the DoR for X→Y. |
| `failure-mode-write-up` | opus | Cross-transition synthesis for PM retro. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Handoff protocol skeleton: per-transition DoR + artifact list + sign-off block + carry-forward. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-role-handoff-protocol.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[1on1-template-managers]]
- [[engineering-ladder-and-growth-plan]]
- [[dependency-graph-reasoning]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to adopt the protocol (≥4 roles + failures + PM + sign-off), block (no sign-off mechanism), or skip (small role set). Run before the next multi-week flow kickoff.
