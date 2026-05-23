# Scope Management

## Summary

**One-sentence:** Define, document, and control project scope with a written statement, explicit exclusions, signed baseline, change-control gate, and RTM from source to acceptance.

**One-paragraph:** Scope management produces a signed scope baseline with an explicit out-of-scope list and a Requirements Traceability Matrix from source (charter, stakeholder elicitation) to acceptance test. A formal change-control gate evaluates every new request for cost and schedule impact before it enters the project. Acceptance criteria are testable, not business-prose. Scope creep is the leading cause of overrun; baseline + change-control discipline turns it from drift into a decision.

**Ефективно для:**

- Fixed-price / fixed-scope contracts where creep damages margin.
- Regulated programmes where scope is part of compliance evidence.
- Multi-vendor programmes where vendor scope must compose.
- Strategic transformations (ERP, CRM, cloud migration) needing scope-WBS-validation chain.

## Applies If (ALL must hold)

- Fixed-price or fixed-scope contract anchors the work.
- Regulated compliance evidence requires written scope.
- Multi-vendor scope must compose into one deliverable.
- Project shows scope creep symptoms (repeated re-baselining, ambiguous acceptance).

## Skip If (ANY kills it)

- Pre-PMF startup iterating on hypotheses — strict scope kills learning.
- Internal R&D / discovery sprints.
- Pure-agile team with continuous discovery + backlog refinement.
- One-person side project — scope statement is overhead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Charter | Markdown / signed PDF | sponsor |
| Stakeholder requirements | elicitation notes | BA |
| Change-control board membership | RACI | governance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-register` | Names sponsors authorised to sign baseline. |
| `wbs-creation` | Decomposes the signed scope into deliverable packages. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — explicit exclusions, testable AC, signed baseline, RTM, change-control gate | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for scope-statement artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns — vague AC, missing exclusions, no signed baseline, abandoned RTM | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: elicit → write → sign → baseline → control | 800 |
| `content/05-examples.xml` | optional | Worked scope statement snippet | 600 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping scope state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `write-exclusions` | sonnet | Needs domain judgment; haiku generates generic exclusions. |
| `rtm-build` | haiku | Mechanical mapping source → acceptance test. |
| `change-impact-analysis` | opus | Cross-cutting impact across cost, schedule, quality. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scope-statement.md` | Scope statement skeleton with exclusions + AC + RTM. |
| `templates/requirements-doc.md` | Numbered requirements with source + acceptance tests. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scope-management.py` | Schema-validate scope-statement JSON. | Pre-commit + pre-baseline. |
| `scripts/rtm_coverage.py` | Check every requirement has an acceptance test and every AC has a requirement. | Weekly + pre-release. |

## Related

- [[wbs-creation]]
- [[stakeholder-register]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the scope-management input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
