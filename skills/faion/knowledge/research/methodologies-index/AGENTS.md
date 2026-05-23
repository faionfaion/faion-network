# Methodologies Index

## Summary

**One-sentence:** Authors the L2 INDEX.xml for the research domain: groups methodologies into 3-8 sub-clusters, attaches complexity + produces + summary, keeps the list sorted and count-correct.

**One-paragraph:** Authoring methodology for the per-domain L2 INDEX.xml. Partitions research methodologies into 3-8 sub-clusters (e.g., market-sizing, competitor-intel, user-research, discovery-ops, framework-routing), attaches `complexity` + `produces` attributes to every row, keeps each `<group>` alphabetically sorted by slug, and validates the index against the F-066 A2 checklist.

**Ефективно для:**

- Додано нову методологію - треба її вмонтувати в INDEX.xml правильної групи.
- Перейменування / переміщення методології - оновити slug у L2.
- Поява нової sub-cluster (наприклад, 'forecasting' як окремий cluster).
- Аудит: чи всі methodologies мають complexity + produces attrs.
- Перегляд count attr після додавання нових methodologies.

## Applies If (ALL must hold)

- Adding a new methodology to the research domain L2 index.
- Renaming or moving an existing methodology (slug update).
- Introducing a new sub-cluster (group) inside the domain.
- Audit: do all methodologies carry complexity + produces attrs?
- Updating the count attr after methodology additions/removals.

## Skip If (ANY kills it)

- Editing a methodology's body (this is INDEX-only; edit AGENTS.md or content/ directly).
- Authoring the L1 domains.xml (use domains-index methodology).
- One-off methodology audit (use validate-domain-index.py + a manual diff).
- Tier promotion (free -> solo) - separate workflow.
- Renaming the whole domain - run a domain-rename migration first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Updated AGENTS.md for new/renamed methodology | markdown | authoring step |
| Existing INDEX.xml | XML | knowledge/<domain>/INDEX.xml |
| Decision on sub-cluster | label | domain editor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[methodologies-detail]] | ensures every linked methodology has its detail page authored |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 4-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `slot-into-group` | sonnet | Decide which group the new methodology belongs to. |
| `alphabetize` | haiku | Mechanical alpha-sort within group. |
| `count-and-attrs` | haiku | Update count attr; assert complexity + produces present on every row. |
| `validate` | haiku | Run validate-domain-index.py and report violations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/INDEX.xml` | Skeleton L2 INDEX with <groups> partition |
| `templates/index-checklist.md` | Author / audit checklist for INDEX.xml against F-066 A2 |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodologies-index.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[methodologies-detail]]
- [[frameworks]]
- [[workflows]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
