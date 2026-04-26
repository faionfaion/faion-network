# Subagent BRIEF: faion-network catalog batch

You are filling description fields for the faion-network catalog. One paragraph per methodology, plain practical English.

## Working directory

All paths are relative to `/home/nero/workspace/projects/faion-net/faion-network/`.

## Inputs

- Batch file: `/tmp/cb-<SLOT>.json` (provided by parent dispatcher; SLOT is one of A/B/C/D/E or any unique tag).
- Each batch file has: `phase`, `instructions`, `rows[]`. Each row has `key`, `tier`, `group`, `domain`, `path`, optionally `methodology`.
- The `path` field points to README.md (for methodologies) or SKILL.md (for domains).

## Output

- Write a single JSON object to `/tmp/cr-<SLOT>.json` with the SAME number of entries as `rows`.
- Keys MUST match `row.key` exactly.
- Values are description strings (no nesting).

## Description format

For each row:

| phase | length | content |
|-------|--------|---------|
| `methodologies` | 1 paragraph, 3-5 sentences | Problem the methodology solves, when to apply, the practical value delivered |
| `domains` | 1-2 paragraphs | What the domain covers, when to use, what core skills/methodology areas it includes |

Rules:
- Plain practical English. No marketing fluff. No code blocks. No headers. No bullet lists. Just prose.
- Stay close to the README — do not invent capabilities.
- 3-5 sentences for methodologies, 2-4 for domains.

## Hard rules

- Read EVERY row before writing. Do not stop early.
- Verify your output JSON has exactly N keys (N = `len(rows)`) before writing.
- Use the Write tool, not Bash echo.
- Final line of your reply: `SLOT <X>: OK N/N` (e.g. `SLOT A: OK 25/25`).
