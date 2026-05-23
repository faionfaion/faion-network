<!-- purpose: minimal Freelancer Weekly Report Template artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: report artefact validated by scripts/validate-freelancer-weekly-report-template.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# Freelancer Weekly Report Template — Artefact

| Field | Value |
|-------|-------|
| artefact_id | freelancer-weekly-report-template-YYYY-MM-DD |
| owner | named human (no group terms) |
| last_touched | ISO-8601 timestamp |
| template_version | 1.1.0 |
| status | draft \| ready_for_review \| approved \| archived |

## Inputs

- Triggering activity: [from AGENTS.md Applies If list]
- Source-of-truth refs: [list URLs / design-file ids / dashboard snapshots]

## Methodology fields

| Field | Purpose |
|-------|---------|
| report_week | ISO week (YYYY-Www) the report covers |
| shipped | list of {item, evidence} pairs — each evidence is a PR URL, ticket id, or commit hash |
| next | list of {item, owner, deadline} for the next cycle |
| risks | list of {risk, mitigation, owner} entries |
| asks | list of {ask, recipient} pairs — empty array means no blockers |
| client | named client (organisation + primary contact) |
| cadence_anchor | fixed day-of-week + time the report ships every week |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-freelancer-weekly-report-template.py --file artefact.json` exits 0
