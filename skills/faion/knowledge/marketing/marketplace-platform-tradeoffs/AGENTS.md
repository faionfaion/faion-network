# Freelance Marketplace Platform Tradeoffs

## Summary

**One-sentence:** Compares Upwork / Toptal / Contra / Arc / Braintrust / Malt on fee / lead-quality / exclusivity / ranking and emits a platform decision matrix for a given positioning + rate band.

**One-paragraph:** Freelancers waste 4-8 months on the wrong marketplace before realizing the platform's economics misfit their positioning + rate band. This methodology scores six major platforms (Upwork, Toptal, Contra, Arc, Braintrust, Malt) on five axes: fee structure, lead quality, exclusivity clause, ranking algorithm, and audience density. Output: decision record naming the primary platform + secondary platform + entry plan + churn-out triggers (when to leave).

**Ефективно для:**

- Freelancer переходить з Upwork (low rates) на Toptal / Arc (premium).
- Solo consultant дивиться чи варто інвестувати в Contra brand-page.
- Multi-marketplace strategy: primary + secondary platform з different audiences.
- Exit-planning: коли пора покинути marketplace і йти на direct outreach.

## Applies If (ALL must hold)

- Freelancer or solo consultant evaluating new platform presence.
- Rate band $30-$400/hour or equivalent project-fee.
- Operator can invest 4-8 weeks ramp time on the chosen platform.
- Positioning lane defined (vertical x stack x outcome).

## Skip If (ANY kills it)

- Rate band < $30/hour — Upwork is the only viable platform; no comparison needed.
- Rate band > $400/hour — direct outreach + referral pipeline outperform any marketplace.
- No positioning lane — run niche-positioning-for-solo-dev first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-marketplace-platform-tradeoffs` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Markdown decision record skeleton |
| `templates/_smoke-test.md` | Minimum viable filled decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-marketplace-platform-tradeoffs.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
