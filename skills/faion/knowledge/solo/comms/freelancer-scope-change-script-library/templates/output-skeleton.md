<!-- purpose: minimal Freelancer Scope-Change Script Library artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-freelancer-scope-change-script-library.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# Freelancer Scope-Change Script Library — Artefact

| Field | Value |
|-------|-------|
| artefact_id | freelancer-scope-change-script-library-YYYY-MM-DD |
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
| situation_type | small-ask|big-ask|mission-creep|emergency |
| empathy_line | one-sentence acknowledgement of the client's pressure |
| impact_line | one-sentence statement of cost (time, money, sequence) |
| options | ≥2 named options each with price + timeline tradeoff |
| next_step | single concrete proposal (call slot, written agreement, escalation) |
| trigger_quote | verbatim 1-2 sentence quote of the client's ask |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-freelancer-scope-change-script-library.py --file artefact.json` exits 0
