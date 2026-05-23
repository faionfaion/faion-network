# Research Repository Operations

## Summary

**One-sentence:** Day-2 ops for a research repository: ingestion, tagging, deduplication, retention, access control, weekly health report, and a kill-switch for stale studies.

**One-paragraph:** Operational methodology for running a research repository (Dovetail / Notion / Airtable) after initial setup. Defines weekly ingestion + tagging + deduplication routines, a retention policy (older than 24 months -> archive), access control reviews, weekly health-report emission, and a kill-switch for stale or contested studies.

**Ефективно для:**

- Repository вже існує; треба запустити день-2 ops (не setup).
- Studies накопичились без тегів - треба бек-філ.
- Дублі (один інтервʼю в трьох слотах) - треба дедуп.
- Retention pass: що архівувати, що видалити, що зберегти.
- Access review (хто має admin, хто read-only).

## Applies If (ALL must hold)

- Repository exists; need day-2 ops, not initial setup.
- Studies accumulated without consistent tagging; backfill required.
- Duplicate records (same interview in multiple slots); need dedup.
- Retention pass: archive / delete / keep older studies.
- Access review (who is admin, who is read-only).

## Skip If (ANY kills it)

- Initial repository selection / setup (use research-repository-setup).
- One-off study without a repository.
- Pure analysis methodology (this is ops, not findings).
- Compliance-mandated audit (separate workflow).
- Repository being decommissioned.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repository platform credentials | API keys | research-ops admin |
| Tag taxonomy | YAML | previous setup |
| Retention policy doc | markdown | legal + research lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[research-repository-setup]] | provided the initial taxonomy + permissions baseline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ingestion-sync` | haiku | Mechanical sync of new sessions from upstream sources. |
| `tagging-backfill` | sonnet | Apply taxonomy tags to unrated studies. |
| `dedup` | haiku | Hash-based duplicate detection + merge. |
| `retention-pass` | sonnet | Archive / delete / keep decisions per study. |
| `health-report` | sonnet | Weekly metrics + escalations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/repo-health-report.md` | Weekly repository health-report skeleton |
| `templates/ops-playbook.md` | Day-2 ops playbook (weekly tasks + monthly tasks) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-research-repository-ops.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[research-repository-setup]]
- [[user-research-at-scale]]
- [[continuous-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
