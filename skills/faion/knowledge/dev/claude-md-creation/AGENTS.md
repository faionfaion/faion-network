# CLAUDE.md Creation (Software Developer)

## Summary

**One-sentence:** Produces a CLAUDE.md project brief — tech stack, commands, file conventions, owners, anti-patterns — tuned for a software developer opening a new repo in Claude Code, with bounded token budget and zero secrets.

**One-paragraph:** Produces a CLAUDE.md project brief — tech stack, commands, file conventions, owners, anti-patterns — tuned for a software developer opening a new repo in Claude Code, with bounded token budget and zero secrets. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** software developers opening a new repo in Claude Code who need a fast, token-efficient project brief their team can amend in PRs without rewriting it every Monday.

## Applies If (ALL must hold)

- A named trigger has fired (release, incident, schedule, scope change) that warrants producing the artefact.
- The owner is a named person (role:handle), not a team alias or channel.
- The required input artefacts in `## Prerequisites` are available and machine-readable.
- The downstream consumer for the produced artefact is known (review board, CI gate, customer, regulator).

## Skip If (ANY kills it)

- Trigger is vague ("when needed", "soon"); rewrite the trigger first.
- No named owner — refuse to produce; assign first.
- Inputs are missing or non-deterministic; fix the upstream observability before applying.
- A different, already-pinned methodology handles this exact decision (avoid duplicate artefacts).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Trigger record | text / ticket link | upstream alerting / planning queue |
| Owner identity | `role:handle` string | RACI / org directory |
| Input artefacts | as listed in `02-output-contract.xml` `required` | upstream methodology output |
| Prior artefact (if exists) | JSON matching the output contract | repo `.product/claude-md-creation/` |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | recommended | Step-by-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | recommended | One full worked example end-to-end | ~600 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |
| `templates/claude-md-minimal.md.j2` | Minimal CLAUDE.md skeleton for single-language repos. |
| `templates/claude-md-minimal.md` | Minimal CLAUDE.md skeleton for single-language repos. Generated from `templates/claude-md-minimal.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/claude-md-standard.md.j2` | Standard CLAUDE.md skeleton for product repos. |
| `templates/claude-md-standard.md` | Standard CLAUDE.md skeleton for product repos. Generated from `templates/claude-md-standard.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/claude-md-monorepo.md.j2` | Monorepo CLAUDE.md skeleton — root brief + per-app addenda. |
| `templates/claude-md-monorepo.md` | Monorepo CLAUDE.md skeleton — root brief + per-app addenda. Generated from `templates/claude-md-monorepo.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/extract-commands.sh` | Shell helper dumping repo commands into CLAUDE.md-ready format. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-claude-md-creation.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "trigger": {
    "kind": "weekly-review",
    "url": "https://example.com/trigger/1"
  },
  "owner": "swe:alice",
  "inputs": [
    {
      "name": "scope",
      "value": "billing"
    }
  ],
  "decision": "Adopt variant A behind feature flag.",
  "evidence": [
    "https://example.com/pr/1"
  ],
  "review": {
    "cadence": "quarterly",
    "next_review_at": "2026-08-22"
  }
}
```

### `templates/extract-commands.sh`

````bash
# extract-commands.sh — Dump project commands into CLAUDE.md-ready format.
# Usage: bash extract-commands.sh
# Output: Commands section for CLAUDE.md based on package.json, Makefile, pyproject.toml

echo "## Commands"
echo ""

if [ -f package.json ]; then
  echo "### npm / Node"
  echo '```bash'
  jq -r '.scripts | to_entries[] | "\(.key)  # \(.value)"' package.json 2>/dev/null \
    | head -20
  echo '```'
fi

if [ -f Makefile ]; then
  echo ""
  echo "### Make"
  echo '```bash'
  grep -E "^[a-zA-Z_-]+:" Makefile \
    | sed 's/:.*//' \
    | head -20 \
    | while read -r t; do echo "make $t"; done
  echo '```'
fi

if [ -f pyproject.toml ]; then
  echo ""
  echo "### Python (ruff)"
  echo '```bash'
  echo "ruff check . --fix  # Lint + auto-fix"
  echo "ruff format .        # Format"
  echo "pytest --cov=src     # Tests with coverage"
  echo '```'
fi
````
