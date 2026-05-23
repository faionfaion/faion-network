# Proposal Red Team Checklist

## Summary

**One-sentence:** A pause-point structured red-team checklist (5–9 killer items per pause-point, READ-DO or DO-CONFIRM mode) that an architect + delivery manager run in an hour on a fixed-price proposal before it ships to the client.

**One-paragraph:** Vendors lose margin to proposals that pass an internal sniff test but blow up in delivery. The outsource delivery specialist runs fixed-price bid discovery + estimation weekly, but the artefact that closes the loop — a reviewable, owned, evidence-anchored red-team checklist — is folklore in most teams. This methodology pins the artefact's shape: READ-DO/DO-CONFIRM mode per pause-point, 5–9 items per pause-point (Miller 7±2), every item carries an executor role + artefact (link/screenshot/sign-off) + killer-anchor (incident_id / policy / postmortem), a named owner, and `last_reviewed` ≤ 90 days. Outputs are validated by `scripts/validate-proposal-red-team-checklist.py` and reviewed quarterly; stale or anchor-less items are removed.

**Ефективно для:**

- Fixed-price bid discovery + estimation (1-week cadence).
- Pre-send red-team review by architect + delivery manager (hour-long).
- Operational discipline: every killer-anchor cites an incident, postmortem, or regulator finding.
- Cross-engagement continuous improvement: quarterly review removes decorative items.

## Applies If (ALL must hold)

- Fixed-price bid discovery + estimation is a recurring weekly block.
- Outsource delivery specialist owns the artefact (or escalates ownership to a named role).
- Team uses a version-controlled or wiki-style space where the artefact lives.
- Trigger event fires at published cadence (event, threshold, or schedule).

## Skip If (ANY kills it)

- One-shot proposal with no recurrence — write a single review doc, not a versioned artefact.
- Team has < 3 proposals per year — review cadence costs more than it returns.
- Regulated context mandating a specific template (use the regulator's template instead).
- No named owner available — defer until ownership resolved.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repository / wiki space | git / Notion / Confluence | platform |
| Named owner (role + person) | YAML row in stakeholder register | HR / PM |
| Incident / postmortem corpus | Markdown / Linear / Jira | engineering |
| Last quarter's red-team logs | Markdown | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[vendor-margin-defense-checklist]] | The sibling weekly margin scan whose alerts feed this proposal review. |
| [[wbs-creation]] | Proposals decompose into WBS leaves; killer-items reference WBS IDs. |
| [[solo-change-order-mini-contract]] | CR template used when red-team finds scope holes mid-engagement. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: read-do/do-confirm mode, bounded length 5-9, killer-items only, named execution + artefact, review cadence | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `RedTeamChecklist` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, example-text leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step scaffold → populate → run → record outcome → quarterly review | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: trigger fired? owner named? anchor present? size ok? → run / suppress / repair | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from header + section list. |
| `populate-evidence-fields` | sonnet | Per-section judgment selecting correct evidence. |
| `outcome-review-synthesis` | opus | Cross-cycle synthesis: does the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Canonical section list with `not_applicable: <reason>` markers per section |
| `templates/header.yaml` | Frontmatter schema: owner, version, last_reviewed, evidence_root, mode |
| `templates/_smoke-test.json` | Minimum-viable filled `RedTeamChecklist` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-proposal-red-team-checklist.py` | Validate filled artefact: mode, pause-point sizing, evidence anchors, owner, last_reviewed | Pre-merge |
| `scripts/staleness-check.py` | Flag artefacts whose `last_reviewed` exceeds the published window | Weekly cron |

## Related

- [[vendor-margin-defense-checklist]]
- [[wbs-creation]]
- [[solo-change-order-mini-contract]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (trigger present, owner named, killer-anchor populated, pause-point size, staleness) to a concrete action — run-the-checklist, suppress, repair-anchors, or refresh-cadence. Every leaf references a rule from `01-core-rules.xml`.
