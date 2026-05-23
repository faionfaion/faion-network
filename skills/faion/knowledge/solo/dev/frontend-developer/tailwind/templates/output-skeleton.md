<!-- purpose: minimal Tailwind CSS artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: config artefact validated by scripts/validate-tailwind.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# Tailwind CSS — Artefact

| Field | Value |
|-------|-------|
| artefact_id | tailwind-YYYY-MM-DD |
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
| config_id |  |
| settings | key:value config map |
| applies_to |  |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-tailwind.py --file artefact.json` exits 0
