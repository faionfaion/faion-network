# PM Tools Comparison

## Summary

**One-sentence:** Comparison report scoring 2-5 PM tools on a weighted matrix (Core Features 30%, Usability 25%, Integrations 20%, Enterprise 15%, Cost 10%) plus 2-week PoC + TCO + ADR.

**One-paragraph:** PM Tools Comparison defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Teams replacing a PM tool (migration off Jira / Asana / Trello).
- New programs choosing their first PM tool with multi-stakeholder buy-in.
- PMOs needing a defensible record of why tool X was chosen over Y.
- Budget owners requiring TCO over 3 years before approving a tool purchase.

## Applies If (ALL must hold)

- >=2 candidate tools that can be trialled in a 2-week PoC.
- Budget exists for a paid tier of each candidate during PoC.
- Team can dedicate 5-10h/person across 2 weeks for the PoC.
- Named decision owner has authority to ratify the ADR.

## Skip If (ANY kills it)

- Only one tool is feasible (compliance / vendor lock-in) — write a single-choice ADR, skip comparison.
- Team size <5 — overhead exceeds value, pick the cheapest viable.
- PoC budget cannot be secured — comparison without PoC is theoretical and untrustworthy.

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
| `pm-tools-comparison_template_fill` | haiku | Bounded template fill, no judgement. |
| `pm-tools-comparison_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `pm-tools-comparison_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the PM tools comparison report artefact. |
| `templates/evaluation-scorecard.md` | Markdown skeleton for the per-tool scorecard with criteria + evidence. |
| `templates/tco.yaml` | YAML template for 3-year TCO per tool. |
| `templates/weighted_score.py` | Reference script computing weighted totals from the scorecard. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-tools-comparison.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

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
