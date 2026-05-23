# RACI Matrix

## Summary

**One-sentence:** Generic cross-functional RACI matrix assigning exactly one of R / A / C / I per stakeholder per task, with one Accountable per row and explicit C-vs-I discipline.

**One-paragraph:** RACI Matrix defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Cross-functional initiative with >=3 disciplines (eng / design / marketing / ops).
- Recurring confusion about 'who owns this' or 'who should I tell'.
- PM running an audit before a milestone with multiple gates.
- Onboarding new lead who needs the accountability map for the program.

## Applies If (ALL must hold)

- Tasks / deliverables can be enumerated (rows of the matrix).
- Stakeholders can be enumerated (columns of the matrix).
- A lead exists who can ratify ambiguous assignments.
- Authority to publish + maintain the RACI is granted.

## Skip If (ANY kills it)

- Solo work — RACI is not meaningful with one person.
- Highly volatile scope where tasks rotate weekly — RACI rots within the cycle.
- Use launch-raci-template for launches specifically; this generic RACI is for ongoing work.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `raci-matrix_template_fill` | haiku | Bounded template fill, no judgement. |
| `raci-matrix_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `raci-matrix_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the RACI matrix artefact. |
| `templates/raci-template.md` | Markdown skeleton for the RACI matrix table. |
| `templates/raci-lint.py` | Reference script enforcing one-A-per-row + non-empty R. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-raci-matrix.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
