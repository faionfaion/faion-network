# Code Review Basics

## Summary

**One-sentence:** Five-item PR review checklist with Conventional Comments labels; 400-line cap; agent never sole approver.

**One-paragraph:** The simplest workable review: five questions, five comment labels, hard caps on PR size and comment volume. Output is a checklist artefact a junior reviewer can use without prior training. Intended as the floor for `code-review` and the input to `code-review-process`. Conventional Comments give the label vocabulary; the cap stops mega-PRs from polluting the inbox.

**Ефективно для:**

- Junior-QA / junior-eng review training: чек-лист дає 'що поставити в комент'.
- Solo / 2-person team: процес-overhead мінімальний, але якість фіксована.
- AI-агенти: draft a structured 5-item PR review без надмірних reasoning steps.
- Hot-fix flow: легка форма дозволяє швидкий, але not-zero review.

## Applies If (ALL must hold)

- PR workflow exists.
- Reviewer needs a deterministic starting point.
- Team accepts Conventional Comments vocabulary.

## Skip If (ANY kills it)

- Repo already runs the full code-review methodology — basics is the floor, full is the ceiling.
- Solo project with no second reviewer.
- Vendored / generated code PRs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff | unified diff | git / PR API |
| PR description | Markdown | PR body |
| CI status | string | GitHub check API |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: conventional-labels, 400-cap, 20-cap, ask-not-assert, human-approver | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema for checklist artefact | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: nit-bombing, opinion-as-issue, agent-merging-own-PR | 600 |
| `content/06-decision-tree.xml` | essential | Size + label decision tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `size_gate` | haiku | Deterministic; line count check. |
| `checklist_walk` | sonnet | Per-question structured pass over the diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-context.sh` | Shell that gathers PR context (diff, CI status, description) for the reviewer |
| `templates/review-prompt.txt` | LLM prompt that drives the checklist walk |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review-basics.py` | Validate the checklist artefact against schema | After checklist walk, before posting |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- - [[code-review]] — the full 6-category methodology.
- - [[code-review-process]] — workflow templates this checklist plugs into.

## Decision tree

See `content/06-decision-tree.xml`. Branches: PR &gt; 400 lines? → block. Else walk the 5-item checklist; emit issue-labels if any gap; recommend approve if all 5 pass and CI is green.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/pr-context.sh`

```bash
#!/usr/bin/env bash
# pr-context.sh — emit review-ready context for an agent.
# Usage: pr-context.sh <owner/repo> <pr-number>
# Requires: gh CLI authenticated
set -euo pipefail

REPO="${1:?owner/repo required}"
PR="${2:?PR number required}"

echo "## PR metadata"
gh pr view "$PR" --repo "$REPO" \
  --json title,body,author,additions,deletions,changedFiles \
  | jq '{ title, author: .author.login, additions, deletions, changedFiles }'

echo ""
echo "## Files changed"
gh pr diff "$PR" --repo "$REPO" --name-only

echo ""
echo "## Failing CI checks (agent must not review if any)"
gh pr checks "$PR" --repo "$REPO" --json name,state,conclusion \
  | jq '[.[] | select(.conclusion == "failure" or .state == "FAILURE")]'

LINES=$(gh pr diff "$PR" --repo "$REPO" | wc -l)
if [ "$LINES" -gt 3000 ]; then
  echo ""
  echo "## WARNING: PR exceeds 400 changed lines ($LINES diff lines)."
  echo "## Instruct author to split before proceeding with agent review."
  exit 0
fi

echo ""
echo "## Diff"
gh pr diff "$PR" --repo "$REPO" | head -2000
```

### `templates/review-prompt.txt`

```text
Review the diff below. Output a JSON array of review comments.

Each comment object:
{
  "path": "<file path>",
  "line": <line number in new file>,
  "label": "blocking | suggestion | nit | question | praise",
  "body": "<comment text>"
}

Rules:
- Review ONLY changed lines (+ up to 3 lines context each side).
- Skip style issues already enforced by the linter config in the repo.
- Use Conventional Comments labels for every comment.
- Prioritize: correctness > security > maintainability > nits.
- Max 20 comments total.
- Every blocking comment must quote the offending line and either provide a fix or describe the exact failing input.
- List every file you reviewed at the end; if you had to skip any file due to context limits, say so and do NOT output an approval.
- You are NOT the approver; output comments only.

<diff>
{{DIFF}}
</diff>
```
