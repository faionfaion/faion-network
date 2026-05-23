# Research Repository Setup

## Summary

**One-sentence:** Initial setup of a research repository (Dovetail / Notion / Airtable): platform selection, taxonomy authoring, access matrix, ingestion wiring, kickoff backfill of last 90 days.

**One-paragraph:** First-time setup methodology for a research repository. Picks the platform on 5 criteria (API maturity, AI tagging, integration matrix, cost-per-user, ZDR support); authors a tag taxonomy with frozen + proposed channels; defines an access matrix (admin / researcher / read-only); wires upstream ingestion from interview + survey + analytics sources; runs a 90-day backfill kickoff so the repo is useful from day 1.

**Ефективно для:**

- Перший research repository - бо tooling зростає, треба зафіксувати структуру.
- Міграція з ad-hoc Notion / Google Docs у структурований repo.
- Multi-team org консолідовує studies в один шар.
- Compliance: треба audit trail + access matrix.
- AI tagging вмикається - потрібен фрімований tag taxonomy.

## Applies If (ALL must hold)

- First-time research repository - tooling is growing and the team needs structure.
- Migration from ad-hoc Notion / Google Docs to a structured repo.
- Multi-team org consolidating studies into one layer.
- Compliance requires audit trail + access matrix.
- AI tagging is being enabled and needs a frozen taxonomy.

## Skip If (ANY kills it)

- Repository already exists; use research-repository-ops.
- Single-researcher solo workflow with <50 studies/year.
- Throwaway research without ongoing reuse.
- Pure interview-as-Notion-page workflow that the team prefers to keep.
- Compliance forbids cloud storage of transcripts (build a self-hosted variant).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Vendor shortlist | list of 2-3 platforms | research-ops / IT |
| Tag seed list | markdown | research lead |
| Access policy draft | markdown | legal + research lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[research-repository-ops]] | consumes the artefacts this methodology produces |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `platform-pick` | sonnet | Score 2-3 platforms on 5 criteria. |
| `author-taxonomy` | sonnet | Compose 30-80 starter tags grouped by class. |
| `access-matrix` | haiku | Map roles to permissions. |
| `wire-ingestion` | sonnet | Connect upstream sources via API. |
| `backfill-90d` | haiku | Mechanical historical pull + tagging. |

## Templates

| File | Purpose |
|------|---------|
| `templates/platform-scorecard.md` | Scorecard template for repository platform selection |
| `templates/taxonomy-seed.yaml` | Starter tag taxonomy grouped by class (segment / pain / JTBD / behavior) |
| `templates/access-matrix.md` | Role-to-permission mapping |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-research-repository-setup.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[research-repository-ops]]
- [[user-research-at-scale]]
- [[continuous-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
