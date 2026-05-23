<!-- purpose: minimal AI Prompt as Commit Artefact artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-ai-prompt-as-commit-artifact.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# AI Prompt as Commit Artefact — Artefact

| Field | Value |
|-------|-------|
| artefact_id | ai-prompt-as-commit-artifact-YYYY-MM-DD |
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
| commit_sha | git short SHA of the commit being annotated |
| prompt | verbatim prompt sent to the agent |
| model | model id (e.g. claude-opus-4-7, gpt-5) |
| context_refs | list of file paths + line ranges the agent read |
| verifier | tests/lints/manual-check that confirmed the diff before commit |
| author | named human who reviewed and committed |
| status | draft|ready_for_review|approved|archived |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-ai-prompt-as-commit-artifact.py --file artefact.json` exits 0
