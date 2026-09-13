# Activation Tactics

## Summary

**One-sentence:** Playbook step: applies friction-reduction + motivation tactics (checklists, email sequences, in-app guides) to top activation drop-offs.

**One-paragraph:** Playbook step: applies friction-reduction + motivation tactics (checklists, email sequences, in-app guides) to top activation drop-offs. Use it when top drop-off ідентифікований — потрібна конкретна tactical intervention. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Top drop-off ідентифікований — потрібна конкретна tactical intervention.
- Налаштування activation checklist + tooltips в onboarding flow.
- Lifecycle email sequence для re-engage signups, що не дійшли до aha moment.
- Сегментована onboarding (по use case) для multi-persona продуктів.

## Applies If (ALL must hold)

- An activation event and window are defined and a drop-off ranking gives each step's current conversion and screen (from activation-metrics or activation-framework).
- The list of tactics currently live per step is known, so a second tactic on the same step can be deferred.
- The product can bind checklist items to tracked events, deep-link emails to the action screen, and evaluate `not activated` at send time.
- A rollout can run for at least two closed signup weeks so the exit criterion can be measured against the step's baseline.

## Skip If (ANY kills it)

- No measured drop-off with a conversion rate exists: run activation-metrics first; a tactic without a target step is not accepted.
- The target step already carries a live tactic this period and the new one is not an arm of the same experiment: defer, do not stack.
- The stall is on a screen with no measured drop-off (a feature tour request): no guide or checklist is placed there.
- The email platform can only evaluate suppression at enrolment: fix the platform before running a sequence, or the Day 1-7 sends go to activated users.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Drop-off ranking | step, screen path, current conversion (ratio), users lost | activation-metrics report or activation-framework spec |
| Activation definition | event name (snake_case) + window in days | activation-framework spec |
| Live tactics per step | list of step -> tactic running this period | growth team experiment log |
| Tracked events between the step and activation | event names from the event table | product analytics warehouse |
| Deep links for the targeted actions | authenticated URLs to the action screens | product / web team |
| `templates/activation-checklist.yaml`, `templates/email-sequence.md.j2` | checklist config and 4-email sequence skeleton | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: tactic targets a measured step, 3-5 item checklist with one activation item, one direct CTA per email, send-time suppression, segment key at signup, guides only at drop-off, exit criterion with threshold, one tactic per step | 1750 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the playbook step: activation event and window, measured drop-offs with conversion and live-tactic flag, tactics typed as checklist (3-5 items, one activation item) / email sequence (max 4, one deep-linked CTA, send-time suppression) / in-app guide (drop-off screen only) / segmented onboarding (key at signup), rollout steps with metric, baseline and minimum lift, decision branches with the deferral; valid and invalid steps; 8 forbidden patterns | ~4950 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7 steps: take the measured drop-offs, pick one tactic per step by where the user drops, build the checklist, build the email sequence, place the guide or split segments, write the rollout step with a numeric exit criterion, add branches and validate | ~1550 |
| `content/05-examples.xml` | recommended | Complete playbook step (3-item checklist on /projects/new at 0.326 baseline, 3-send verification sequence with send-time suppression, deferral of the step with a live tooltip, two rollout steps with lift thresholds) with a note per value, plus the usual playbook step and what the validator prints | ~2600 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-activation-tactics.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/activation-tactics.playbook-step.md.j2` | Markdown playbook-step skeleton: drop-offs, one tactic per step with checklist / email / guide / segmentation blocks, rollout steps with exit criteria, decision branches |
| `templates/activation-tactics.playbook-step.md` | Markdown playbook-step skeleton: drop-offs, one tactic per step with checklist / email / guide / segmentation blocks, rollout steps with exit criteria, decision branches. Generated from `templates/activation-tactics.playbook-step.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/activation-tactics.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |
| `templates/email-sequence.md.j2` | 4-email activation lifecycle sequence for not-yet-activated signups. |
| `templates/email-sequence.md` | 4-email activation lifecycle sequence for not-yet-activated signups. Generated from `templates/email-sequence.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-activation-tactics.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
