# Solo Retainer Reactivation Cadence

## Summary

**One-sentence:** A 30/60/90-day post-project check-in cadence with copy-pasteable scripts that re-opens a retainer conversation without sounding like a CS chase.

**One-paragraph:** `ops-upselling-cross-selling` assumes a CS team running playbooks against a CRM. A solo freelancer who just closed a project has 60 days before the relationship goes cold — and no CS team to manage that window. This methodology supplies three timed touchpoints (30d "is it sticking", 60d "next quarter shape", 90d "want me back for X") with the actual message text, the exact trigger conditions, and a hard stop after touch 3.

**Ефективно для:**

- Post-project window 30/60/90: solo operator без CS team.
- Value-first touches з named client-specific триггером.
- Hard stop після touch 3 — не псувати relationship.
- Конвертація фіксованих проектів у retainer без CS-language.

## Applies If (ALL must hold)

- a fixed-price or milestone-based project just closed (last delivery accepted)
- the operator wants to convert one-off work into a retainer or repeat engagement
- the client gave at least neutral debrief feedback (not actively unhappy)
- there is no existing retainer or follow-on contract already signed

## Skip If (ANY kills it)

- the project ended in dispute or with payment friction
- the client explicitly said "no further work needed" in the debrief
- the operator is at capacity and cannot accept the retainer if it lands
- a retainer is already signed — switch to retainer-renewal methodology

## Prerequisites

- a clean project closure (final invoice paid, retro completed)
- decision-maker contact info (email + LinkedIn)
- a one-paragraph offer for what the retainer would look like (scope + monthly cost)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/agency-niche-positioning` | parent skill |
| `pro/pm/retainer-vs-project-rubric` | sibling — decides whether retainer is the right offer at all |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/solo-retainer-reactivation-cadence.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/solo-retainer-reactivation-cadence.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-retainer-reactivation-cadence.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/agency-niche-positioning`
- upstream playbook: `p3-technical-freelancer/Project closure debrief + retrospective`
- sibling: `pro/pm/retainer-vs-project-rubric`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

