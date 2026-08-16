# Minimum Product Frameworks

## Summary

**One-sentence:** Selection matrix that chooses one of nine 'minimum product' frameworks (MVP, MLP, MMP, MAC, RAT, MDP, MVA, MFP, SLC) by market density × ICP × differentiator BEFORE the first spec.md exists.

**One-paragraph:** Forces the team to evaluate all 9 minimum-product frameworks across 3 signal axes (market density blue/red, buyer type, differentiator), record the choice as a decision-record with proof gates + revisit triggers, and avoid default-MVP bias. Output: framework-decision-record markdown + scorecard YAML.

**Ефективно для:**

- Новий продукт або major module — до першого spec.md.
- Команда reflexively вибирає MVP без перевірки market density чи buyer type.
- Pivot moment: поточний build програє на retention/conversion.
- Pre-board memo: justify chosen framework на тлі blue/red ocean і ICP.

## Applies If (ALL must hold)

- New product or major module — before the first spec.md exists.
- Team is reflexively saying 'let's ship an MVP' without checking market density, buyer type, or differentiator.
- Pivot moment: current build is failing on retention or conversion — re-pick the framework before re-scoping.
- Multiple stakeholders disagree on what 'minimum' means — use the matrix as a forcing function.
- Pre-investment or pre-board memo: justify the chosen framework against blue/red ocean and ICP positioning.

## Skip If (ANY kills it)

- Framework already chosen and a DR exists <=90 days old — re-pick is premature.
- Non-product engagement (consulting / services) — no minimum-product framework applies.
- Compliance-driven product where regulatory scope defines the build, not market fit.
- Iteration on a stable product where MVP/MLP boundary is moot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Market density assessment | blue/red ocean classification | research / GTM |
| Buyer type | consumer / prosumer / enterprise / dev | GTM / PM |
| Differentiator hypothesis | price / experience / capability / distribution | PM |
| Existing DR (if any) | markdown | team archive |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[portfolio-strategy]] | Portfolio horizons constrain which frameworks are admissible. |
| [[mvp-scoping]] | Downstream methodology when the matrix selects MVP. |
| [[mlp-planning]] | Downstream methodology when the matrix selects MLP. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology: DR recorded, 9-framework coverage, differentiator test, revisit triggers, framework-vs-product separation, downstream routing | 1150 |
| `content/01-frameworks.xml` | essential | Catalogue of the nine frameworks — purpose + primary use condition for each | 550 |
| `content/02-decision-matrix.xml` | essential | Market-condition to framework mapping (blue/red ocean, enterprise, consumer, technical uncertainty) + selection antipatterns | 650 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for framework-decision-record | 850 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: default-MVP bias, conflated framework/feature, missing triggers, unmeasured differentiator, frame-without-routing, acronym-soup | 1000 |
| `content/04-procedure.xml` | essential | 5-step procedure: signals -> matrix -> pick -> proof -> DR | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on existence of DR + product status | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `signal-extract` | sonnet | Read briefs/research to extract market density + buyer + differentiator. |
| `matrix-score` | haiku | Mechanical scoring across 9 frameworks. |
| `dr-author` | sonnet | Write the decision record with rationale + triggers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-choice.md.j2` | Decision-record skeleton with signals + scorecard + triggers. |
| `templates/framework-choice.md` | Decision-record skeleton with signals + scorecard + triggers. Generated from `templates/framework-choice.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-minimum-product-frameworks.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[portfolio-strategy]]
- [[product-lifecycle]]
- [[mlp-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
