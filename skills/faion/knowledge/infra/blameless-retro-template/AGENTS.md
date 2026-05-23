# Blameless Retro Template (Human Facilitation)

## Summary

**One-sentence:** Produces a blameless retro record: 4-block agenda (timeline → contributing factors → generative discussion → action items + meta), language-rule enforcement, owner+date per action item, published within 48h.

**One-paragraph:** Auto-drafted postmortems produce solid factual reconstruction but cannot facilitate human conversation. Blameless retros convert incidents into systemic learning — and they fail predictably when facilitation is improvised. This methodology ships a 4-block 60-90-minute template with explicit time-boxes, in-meeting language reframing (person-as-subject → system-as-subject), a forcing function that requires ≥3 contributing factors (not single root-cause), and a non-skippable META round that surfaces 'what we ALMOST learned but didn't'. Output is a retro record with contributing factors categorised, action items with named owner + date ≤90d, meta-notes, and a published URL within 48h.

**Ефективно для:**

- Incident declared + resolved (or stable workaround) — потрібен formal retro.
- Team ≥ 3 людей: responders, sub-system owners, downstream consumers.
- Auto-draft postmortem існує (або готується паралельно).
- Facilitator named + NOT a direct responder — для blameless framing.
- Cross-incident learning ціль — кодифікація патернів у culture.

## Applies If (ALL must hold)

- Incident has been declared AND resolved (or stable workaround exists).
- Team includes ≥3 people involved (responders / sub-system owners / consumers).
- Facilitator is named AND is NOT a direct responder of this incident.
- Auto-draft postmortem exists OR will be drafted in parallel.

## Skip If (ANY kills it)

- Solo founder with no team to retro — write a personal incident journal instead.
- Known recurring issue with an existing action item still in flight — re-open the existing AI; don't double-retro.
- Multi-party incident where root cause is external (cloud-provider outage, no internal mitigation gap) — run a short detection / comms retro instead.
- Team in crisis-burnout mode — postpone 1-2 weeks, run an async-async retro instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident timeline data | alert times, comms timestamps, deploy events | auto-draft postmortem / incident chat |
| Auto-draft pre-read | PDF / wiki link | incident response toolchain |
| Participant list | named individuals + roles | responder rotation |
| Psychological-safety norms | Norvig's prime directive agreed | team contract |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[aws-well-architected-checklists]] | Some action items map to WA-pillar items |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology — language enforcement, ≥3 factors, owner+date, meta round, publish 48h | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for retro-record + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: root-cause-fixation, name-leak, action-item-overflow, meta-round-skipped | 1000 |
| `content/04-procedure.xml` | essential | 6 steps: pre-read → 4 agenda blocks (timeline/factors/generative/AI+meta) → publish | 800 |
| `content/05-examples.xml` | reference | Worked example: deploy-pipeline retro (Friday 4pm deploy incident) | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on incident shape → retro mode | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `timeline_pre_read_summary` | sonnet | Compress auto-draft into a 1-page pre-read for participants. |
| `language_flag_review` | haiku | Post-retro: scan transcript for blame-language patterns and flag for facilitator coaching. |
| `action_item_clustering` | sonnet | Group similar action items proposed in retro to avoid AI overflow. |
| `meta_learning_extraction` | opus | Extract 'what we almost learned' — cross-incident pattern synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retro-agenda.md` | 4-block agenda with time-boxes and facilitator prompts |
| `templates/retro-record.json` | JSON Schema-conforming template for the retro output |
| `templates/language-rules-card.md` | Printable card with do / do-not phrasing examples |
| `templates/action-item.json` | Schema for one action item |
| `templates/_smoke-test.json` | Minimum retro-record used by validate-blameless-retro-template.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-blameless-retro-template.py` | Validate the report artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[aws-well-architected-checklists]]
- [[devops-aws-monitoring-dr]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it after every prod incident with ≥3 involved people.
