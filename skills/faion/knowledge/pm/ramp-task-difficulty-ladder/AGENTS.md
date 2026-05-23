# Ramp Task Difficulty Ladder

## Summary

**One-sentence:** Pins the ramp-task difficulty ladder for a product-dev team to a fixed shape (named trigger, bounded output, evidence anchors, named owner, outcome review) so onboarding stops being folklore and becomes a reviewable, owned, version-controlled operating tool.

**One-paragraph:** In project / programme management, the product-dev team runs "hire + onboard a new dev in 2 weeks" on a recurring cadence — but the corpus only covers the upstream concepts, not the artefact that closes the loop. Generic backlog selection produces inconsistent ramp quality, so onboarding buddies fall back to gut feel. `ramp-task-difficulty-ladder` pins the artefact: a fixed shape, named owner, evidence anchors, and a published review cadence. It is loaded when the product-dev team starts a hiring sprint and produces a committed artefact reviewed against onboarding outcomes at the next iteration. Mechanism: rule-bound output contract + per-application evidence + outcome review. Primary output: a versioned, owned, evidence-anchored ladder spec committed to the team's knowledge space.

**Ефективно для:** product-dev team lead, що хоче зробити 2-тижневий ramp нового розробника передбачуваним замість фольклорного.

## Applies If (ALL must hold)

- The product-dev team runs onboarding (or a similar named ramp block) on a recurring cadence (≥3 hires/year).
- The team owns the artefact or escalates ownership to a named role.
- The team uses a version-controlled or wiki-style space where the artefact lives.
- The trigger event is observable (hire signed, start date set, ticket calendar slot).
- A buddy / mentor role exists to hand new hires graded tasks against the ladder.

## Skip If (ANY kills it)

- One-shot work with no recurrence — write a single onboarding doc, not a versioned artefact.
- Team has < 3 hires per year — the review cadence costs more than it returns.
- Regulated context that mandates a different shape (use the regulator's template instead).
- No named owner is available — defer until ownership is resolved; an anonymous artefact rots.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Hiring trigger event | calendar / ATS | HR or hiring manager |
| Backlog of candidate ramp tickets | issue list | team backlog (Jira / Linear / GitHub Issues) |
| Named owner | role + person | team roster |
| Knowledge space | git repo / wiki | team SDD or docs space |
| Outcome review cadence | schedule | team operating calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |
| `pro/pm/project-manager` | Upstream PM operating cadence the artefact slots into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — fixed shape, evidence anchors, named owner, version + last_reviewed, outcome review | ~1000 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, self-check checklist | ~700 |
| `content/03-failure-modes.xml` | essential | 6 known failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Decides whether the team is ready to commit to a versioned ladder vs ad-hoc onboarding | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change onboarding behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Canonical section list with `not_applicable: <reason>` markers per section. |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root, trigger. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ramp-task-difficulty-ladder.py` | Validate that filled artefact matches the canonical schema, carries evidence links, owner, and not-stale `last_reviewed`. | Pre-merge and quarterly staleness scan. |

## Related

- [[stakeholder-sentiment-tracker]] — sibling operating artefact for the same PM space.
- [[team-charter-working-agreement]] — peer methodology shaping how the team operates around the ladder.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first asks whether the team has named-owner + evidence + ≥3 hires/year. If yes → fill the ladder spec; if no → skip the methodology and write a one-off onboarding doc instead. Run the tree the moment the product-dev team lead starts a hiring sprint — before they pull tickets from the backlog by hand.
