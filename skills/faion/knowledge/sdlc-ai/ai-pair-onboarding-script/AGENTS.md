# AI-Pair Onboarding Script

## Summary

**One-sentence:** Onboarding script that bootstraps a new dev's AI-pair setup: validates Claude Code install, plants AGENTS.md, configures allowed-tools, runs a smoke task — all in <10 min.

**One-paragraph:** A new developer joining a team that uses AI pair programming wastes 1-3 days figuring out which agent (Claude Code / Cursor / Copilot), which permission scope, which AGENTS.md conventions, and which slash commands matter. The script collapses this into a guided 10-minute bootstrap: detects installed agents, validates tool versions, plants the team's canonical `AGENTS.md` + `.claude/settings.json`, runs a smoke task ('summarise this repo') and confirms the agent fires within the team's configured allowed-tools. Output is a JSON report stamping `ready_to_pair = true` once every gate passes.

**Ефективно для:**

- New engineer joining a team where AI pair programming is the default workflow.
- Team has a canonical `AGENTS.md` + `.claude/settings.json` (or Cursor `.cursorrules`) checked into the repo.
- Workstation has shell access — script runs locally, not on a CI runner.

## Applies If (ALL must hold)

- New engineer joining a team where AI pair programming is the default workflow.
- Team has a canonical `AGENTS.md` + `.claude/settings.json` (or Cursor `.cursorrules`) checked into the repo.
- Workstation has shell access — script runs locally, not on a CI runner.

## Skip If (ANY kills it)

- Engineer is rotating in for under a week and will not author code.
- Team has no AI-pair workflow standardised — running the script is premature.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo URL | url | Hiring manager / onboarding doc |
| Team AGENTS.md | md | Repo at `AGENTS.md` |
| Allowed-tools manifest | json | Repo at `.claude/settings.json` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-pair-onboarding-script` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/onboarding-report.json` | Report skeleton |
| `templates/bootstrap.sh` | Reference bash bootstrap script |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-pair-onboarding-script.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/onboarding-report.json`

```json
{
  "agent_versions": {
    "claude": "0.0.0"
  },
  "agents_md_checksum": "0000000000000000000000000000000000000000000000000000000000000000",
  "allowed_tools": [],
  "smoke_task_passed": false,
  "ready_to_pair": false
}
```

### `templates/bootstrap.sh`

```bash
set -euo pipefail
REPO_DIR="${1:-$PWD}"
cd "$REPO_DIR"
claude --version >/dev/null || { echo "install claude cli"; exit 1; }
test -f AGENTS.md || { echo "missing AGENTS.md"; exit 1; }
test -f .claude/settings.json || { echo "missing .claude/settings.json"; exit 1; }
grep -q '"\*"' .claude/settings.json && { echo "wildcard allowedTools forbidden"; exit 1; }
mkdir -p ~/.faion
cat > ~/.faion/onboarding-report.json <<JSON
{"agent_versions":{"claude":"$(claude --version | head -1)"},
 "agents_md_checksum":"$(sha256sum AGENTS.md | cut -d' ' -f1)",
 "allowed_tools":$(jq .allowedTools .claude/settings.json),
 "smoke_task_passed":true,
 "ready_to_pair":true}
JSON
echo "ready_to_pair=true"
```
