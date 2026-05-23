# Partnership Co-Marketing Playbook

## Summary

**One-sentence:** Identifies co-marketing partners with overlapping ICPs, structures a joint asset (webinar / research / bundle), and wires UTM-based attribution — the highest-leverage zero-CAC channel.

**One-paragraph:** Co-marketing is the highest-leverage zero-CAC channel for solos and mid-stage teams, but existing partnership content is operations-flavored (contracts, terms). This methodology covers partner shortlist (ICP-overlap > 60%, audience-density match, brand-fit), asset structure (webinar / research report / bundle), attribution plan (shared UTM + post-event survey), and the exit criteria (when to stop or scale). Output: partnership spec + asset template + attribution plan.

**Ефективно для:**

- Solo або small team з ICP overlap >=60% з потенційним партнером.
- Zero-CAC growth move: joint webinar з partner's audience access.
- Joint research report з cross-promo для thought-leadership.
- Bundle deal для cross-promote on email + social.

## Applies If (ALL must hold)

- Marketing owner with authority to commit joint resources (asset time, audience access).
- ICP defined and overlapping (>=60% audience-ICP match) with >=1 candidate partner.
- Both parties have audiences >= 500 active subscribers / followers / community members.
- Asset format (webinar / report / bundle) achievable in <=4 weeks.

## Skip If (ANY kills it)

- No ICP overlap candidate — partnership wastes both audiences.
- Audience < 500 on one side — asymmetric value, deal collapses.
- Authority to commit joint resources missing — committee partnerships fail.

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
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-partnership-co-marketing-playbook` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-partnership-co-marketing-playbook.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
