# Partner Swap Deal Template

## Summary

**One-sentence:** Drafts a peer-to-peer referral swap deal spec between specialists (scope, fee-split, conflict-of-interest, audit cadence) for the freelance reputation flywheel.

**One-paragraph:** Peer-to-peer referral swap deals between specialists (e.g., 'I send overflow API design work to X; X sends overflow Stripe-integration work to me') are the highest-trust source of leads for solo freelancers, but generic partnership-strategy methodologies assume B2B SaaS dynamics. This methodology specs a specialist-to-specialist swap deal: scope of referrals (vertical + stack), fee-split policy (referral fee, finders fee, none), conflict-of-interest rules (when both want the same client), audit cadence.

**Ефективно для:**

- Solo freelancer з overflow і trust-based partner в adjacent specialty.
- Заміна generic 'referral fee' rule на explicit swap deal spec.
- Conflict-of-interest framework: 'хто веде клієнта, якщо обоє хочуть'.
- Yearly audit з renew/exit decision на основі реальних swap-events.

## Applies If (ALL must hold)

- Solo freelancer or specialist with >=1 partner candidate in adjacent specialty.
- Both parties have client overflow (>=1 turn-down/month each).
- Adjacent specialties with low direct competition (e.g., 'API design' + 'Stripe integration').
- Both parties have >=12 months in business (trust takes time to verify).

## Skip If (ANY kills it)

- Same specialty (direct competition) — swap deals collapse under conflict-of-interest.
- Partner < 6 months in business — reputation not verified.
- No overflow on either side — swap value is zero.

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
| `draft-partner-swap-deal-template` | opus | Synthesis under output contract; final write-up. |
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
| `scripts/validate-partner-swap-deal-template.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
