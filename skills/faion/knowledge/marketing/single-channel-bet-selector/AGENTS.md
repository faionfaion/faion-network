# Single Channel Bet Selector

## Summary

**One-sentence:** A scoring rubric that intersects founder DNA (what you'll execute weekly without dropping), ICP behaviour (where they already hang out and search), and traction signal (where you've already had one real lead) to pick a single channel to bet on for 90 days.

**One-paragraph:** Solo founders fail by trying four channels poorly. Existing growth methodologies enumerate channels and tactics but do not help pick which one fits this founder + this ICP right now. This selector forces a written rubric across three axes — founder fit (1-5), ICP density (1-5), early traction (1-5) — and refuses to let the founder pick a channel that scores below 12/15. The output is a single committed 90-day plan; channels 2 and 3 go in a parking lot for review after the bet is graded.

**Ефективно для:**

- Solo founder обирає ОДИН канал на 90 днів — не чотири паралельно.
- Three-axis scoring (founder fit / ICP density / early traction).
- Pre-committed kill criterion на week 12 без emotional re-negotiation.
- Команд, які 'пробують всі канали' і не виходять з $0 traction.

## Applies If (ALL must hold)

- No channel currently yields at least one paying customer a month; the founder is spreading effort across 0 to 4 channels with none at real-revenue traction.
- At least 5 paying customers or 50 qualified conversations exist and each can be asked or checked for where they found the product.
- Inbound leads and sales can be attributed per channel well enough to count unsolicited ones.
- The founder can commit to one channel's countable weekly unit for 13 weeks and will not touch parked channels until week 12.
- The rubric can be stored in version control or a dated document the founder will re-read at the grade.

## Skip If (ANY kills it)

- One channel already produces measurable revenue: keep executing it and revisit only when it saturates.
- The founder has zero direct ICP signal (no customers, no interviews): run discovery until the 5-customer or 50-conversation sample exists.
- The product is pre-launch with no audience to observe, so neither ICP density nor early traction can be scored above 1.
- The founder wants to run two channels in parallel or reserves the right to move the kill criterion; the bet cannot be graded.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Revenue by source | paying customers per month attributed to each channel, last 3 months | billing plus CRM or attribution notes |
| ICP sample | list of paying customers and qualified conversations with where each found the product | CRM, onboarding survey, call notes |
| Inbound log | unsolicited leads and sales per channel with dates | inbox, CRM, form submissions |
| Channel taxonomy | Traction's 19 channels or an equivalent named list | Weinberg and Mares, Traction (2015) |
| Founder calendar | hours per week the founder can give one channel for 13 weeks | founder |
| `templates/single-channel-bet-selector.md.j2`, `templates/single-channel-bet-selector.json` | one-page rubric skeleton; the contract schema | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/proposal-from-discovery-template` | Upstream artefact template that anchors this methodology's recurring loop. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions; artefact lives in the team's SDD space. |

## Content (load on demand)
| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: written single-page rubric, 3 to 6 candidates from a named list, three-axis scoring, ICP density cites sample, 12 of 15 plus per-axis floor, one channel with parking lot, weekly unit and checkpoints, pre-committed kill criterion | 2350 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the channel-bet record: dated rubric and its location, ICP sample of 5 customers or 50 conversations, 3-6 tactic-level Traction candidates scored 1-5 on three unweighted axes with the density sample count, total and the 12-of-15 plus per-axis-3 gate, bet or no_bet, one 90-day bet with weekly unit, week-4 and week-8 checkpoints and a same-day kill criterion, parking lot; valid and invalid records; 8 forbidden patterns | 4650 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | 950 |
| `content/04-procedure.xml` | essential | 7 steps: confirm no working channel and the ICP sample, list tactic-level candidates, score the three axes with samples, apply the threshold and floor, commit to one channel and park the rest, write the weekly unit, checkpoints and kill criterion, store the rubric and validate | 1500 |
| `content/05-examples.xml` | recommended | Complete record for a solo founder with 11 customers (four candidates, LinkedIn founder posts at 12 with 7 of 11 observed, 90-day bet with 3 posts a week, checkpoints at weeks 4 and 8, same-day kill criterion, three parked channels) with a note per value, plus a social bet decided in Slack and what the validator prints | 2000 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule; read before drafting. | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list, low cost. |
| `populate-evidence-fields` | sonnet | Per-section judgment: select correct evidence, summarise without losing specifics. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour at the next iteration? |

## Templates

| File | Purpose |
|------|---------|
| `templates/single-channel-bet-selector.md.j2` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/single-channel-bet-selector.md` | Markdown skeleton (5-line header) for the artefact body. Generated from `templates/single-channel-bet-selector.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/single-channel-bet-selector.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-single-channel-bet-selector.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- upstream playbook: `p1-solo-saas-builder/$0 → $4K MRR bootstrap journey`
- parent skill: `pro/marketing/`

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.
