# Agency Kickoff Deck Template

## Summary

**One-sentence:** 8-12 slide kickoff deck — Why → Scope → Metrics → Owners → Milestones → Risks → Comms → Decision asks — used for agency project kickoff with the client.

**One-paragraph:** Agency kickoff usually devolves into 40 slides of agency credentials. This methodology pins a 8-12 slide kickoff deck whose centre of gravity is decisions for the client: numbered asks slide at the end, named-owner workstreams, top-5 risks, and explicit comms cadence. Brief is 1 page, deck is short, decisions taken at kickoff are logged. Designed for agencies running ≥4 kickoffs/year that want kickoff hygiene without rebuilding the deck each time.

**Ефективно для:**

- Agency PMs running ≥4 kickoffs per year.
- Client-side sponsors who need decisions, not credentials.
- Programmes where workstream-owner clarity is the leading hygiene risk.
- Distressed-rescue kickoffs where comms cadence must be set fast.

## Applies If (ALL must hold)

- Engagement has signed SOW or LOI.
- Kickoff meeting scheduled with sponsor + delivery team.
- Comms cadence will be agreed at kickoff.
- Workstreams already mapped to named humans on agency side.

## Skip If (ANY kills it)

- Re-engagement where deck would be 'check we're still aligned' — use note instead.
- Discovery sprint where scope is hypothesis-driven — use proposal-as-question instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prior-period output | MD / CSV | agency |
| Current pipeline / roadmap | list | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | Engagement of partners / sponsors anchors the artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — max-12 slides, decision asks mandatory, named owners both sides, top-5 risks, comms cadence explicit | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agency-kickoff-deck-template artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping artefact state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from prior-period output. |
| `fill-evidence` | sonnet | Select correct evidence per row. |
| `synthesise-decisions` | opus | Cross-period synthesis for corrective decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/kickoff-deck.md` | 8-12 slide deck outline. |
| `templates/kickoff-brief.md` | 1-page brief feeding the deck. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-kickoff-deck-template.py` | Schema-validate artefact JSON. | Pre-commit + before review. |

## Related

- [[agency-annual-plan-template]]
- [[stakeholder-engagement]]
- [[risk-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the agency-kickoff-deck-template input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
