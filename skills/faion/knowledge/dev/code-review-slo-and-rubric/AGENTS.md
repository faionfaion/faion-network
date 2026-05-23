# Code Review SLO and Rubric

## Summary

**One-sentence:** Produces a code-review SLO (24h business response, reviewer-rotation algorithm, load cap) plus a rubric naming blockers vs nit-picks plus an AI-pre-review + human-final pattern.

**One-paragraph:** Generic code-review playbooks don't address what teams actually struggle with: review-time SLO (24h business), reviewer rotation that prevents single-reviewer bottlenecks, a reviewer-load cap (e.g., 5 open PRs/reviewer), a rubric that distinguishes blocking issues (correctness, security, contract) from nits (naming, formatting), and an AI-pre-review pattern where an LLM does the mechanical first pass and a human does the judgment pass.

**Ефективно для:**

- PR-floor у команді — 24h SLO замість "коли побачу".
- Rotation algorithm + load cap (≤5 open PRs / reviewer).
- Blockers vs nit-picks rubric — пишемо чесні коментарі.
- AI-pre-review (mechanical) → human-final (judgment) — два проходи.

## Applies If (ALL must hold)

- Task is an instance of p6-product-dev-team/Cross-role handoff OR adjacent.
- Operator has Prerequisites available before starting.
- Output consumed by downstream PR workflow.
- Tier == pro or higher.

## Skip If (ANY kills it)

- Solo developer — no review handoff to plan for.
- Team already maintains a documented review SLO + rubric that meets these requirements.
- Regulatory context overrides any in-methodology guidance.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current PR throughput stats | metrics | git platform |
| Reviewer roster + load metric | list | platform |
| AI pre-review tool decision | ADR | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ci-prod-readiness-gates]] | Review SLO + prod-readiness gates compose the PR-level concern surface |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure | ~800 |
| `content/05-examples.xml` | medium | One fully-worked example matching the output schema | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-throughput` | haiku | Capture median PR cycle time + reviewer load. |
| `draft-slo-and-rubric` | sonnet | Per-team judgment on SLO + rubric values. |
| `review-for-compliance` | opus | Cross-team synthesis when reviewer roster changes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/code-review-slo.md` | Markdown skeleton naming SLO + rubric + AI-pre-review pattern. |
| `templates/code-review-slo.schema.json` | JSON skeleton matching the output contract. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review-slo-and-rubric.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-code-review-slo-and-rubric.py` | Validator script. | after subagent returns, before downstream consumer reads |

## Related

- [[ci-prod-readiness-gates]]
- [[client-conventions-reverse-engineering]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates AI pre-review on tool availability and ramps SLO on baseline data, not on aspirational targets.
