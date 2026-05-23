---
slug: qa-prioritization-rubric
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: A 4-tier severity rubric (S0..S3) with concrete blast-radius, frequency, and workaround thresholds for triaging bugs deterministically.
content_id: "97815e81e011c90b"
complexity: light
produces: rubric
est_tokens: 3400
tags: [qa, prioritization, severity, rubric, triage]
---
# QA Prioritization Rubric

## Summary

**One-sentence:** A 4-tier severity rubric (S0..S3) with concrete blast-radius, frequency, and workaround thresholds for triaging bugs deterministically.

**One-paragraph:** A 4-tier severity rubric (S0..S3) with concrete blast-radius, frequency, and workaround thresholds for triaging bugs deterministically. S0/S1/S2/S3 mapped to blast-radius, occurrence rate, and workaround availability. Each tier names the SLO for first response and resolution. Decision tree, output contract, failure modes, and the decision tree live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Bug backlog has > 30 open issues with inconsistent severities.
- Multiple triagers assign different severities to similar bugs.
- Need a defensible rubric for SLA reporting.
- Output produces `rubric` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Bug backlog has > 30 open issues with inconsistent severities.
- Multiple triagers assign different severities to similar bugs.
- Need a defensible rubric for SLA reporting.

## Skip If (ANY kills it)

- Single-developer project — informal triage works fine.
- Org already enforces a rubric (Atlassian, Jira default, FedRAMP) — adopt theirs.
- Backlog < 30 — rubric overhead > benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current bug backlog | tracker export | Jira/Linear |
| Workaround inventory | list | support team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[qa-bug-bash-runbook]] | Bug bash output is triaged against this rubric. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `apply-rubric` | sonnet | Map bug attributes to S0..S3. |
| `flag-disagreement` | haiku | Detect cases where reporter and triager picked different tiers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | JSON template scaffolding the artefact contract. |
| `templates/triage_form.md` | Markdown skeleton for the artefact. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-prioritization-rubric.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-bug-bash-runbook]]
- [[qa-rollback-trigger-canon]]
- [[release-qa-cycle-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are bugs being triaged with consistent severities across triagers?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
