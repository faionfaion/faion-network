# Code Review

## Summary

**One-sentence:** Reviews a PR against six categories with five-kind comment labels, capping comment volume and PR size and never auto-approving.

**One-paragraph:** A PR review without comment-kind labels turns into a Slack thread; a 1500-line PR makes meaningful review impossible. This methodology enforces Conventional Comments labels (praise, nitpick, suggestion, issue, question), six review categories (correctness, design, security, performance, tests, docs), a 400-line PR cap, and a 20-comment-per-PR ceiling. Output is a structured review report — comments grouped by category, severity flagged, recommended action explicit. Agents may draft the report; humans approve. Agent is never the sole approver.

**Ефективно для:**

- Команди з ≥3 інженерів, де review-якість тривіально дрейфує до 'looks good'.
- AI-asisted review-loop: агент драфтить, людина approve — clear roles.
- Стандартизація мови review: junior+senior коментують однаковим лексиконом.
- PR-size enforcement: 400-line cap зрізає 'mega PR' до того, як їх неможливо ревю'ити.

## Applies If (ALL must hold)

- PR workflow is in use (GitHub / GitLab / Bitbucket).
- Team is ≥3 engineers (with 1-2 review is co-located conversation).
- Quality bar matters more than throughput (early-stage prototype is exempt).

## Skip If (ANY kills it)

- Solo dev — no other reviewer exists.
- Hot-fix flow with explicit emergency bypass.
- Vendored / generated code PRs — code review provides no signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff | unified diff | git / PR API |
| PR description | Markdown | PR body |
| Repo conventions | Markdown | CONTRIBUTING.md / repo AGENTS.md |
| Test results | JSON | CI status check |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 400-line-cap, conventional-labels, six-categories, comment-ceiling, no-sole-approver | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for review-report artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: drive-by-approval, comment-flood, missing-category, agent-sole-approver | 700 |
| `content/04-procedure.xml` | essential | 5-step review procedure | 700 |
| `content/06-decision-tree.xml` | essential | Size gate → category coverage → approve / request changes | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `size_gate_check` | haiku | Diff size + file count; deterministic. |
| `category_scan` | sonnet | Per-file judgement across six categories. |
| `synthesise_report` | sonnet | Aggregates comments into the report. |

## Templates

| File | Purpose |
|------|---------|
| `templates/agent-review.yml` | GitHub workflow that runs the agent reviewer on PRs |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- - [[code-review-basics]] — Conventional Comments labels and minimal review pattern.
- - [[code-review-process]] — the workflow this review fits into (templates, metrics).

## Decision tree

See `content/06-decision-tree.xml`. Branches first on PR size — &gt;400 lines blocks review until split. Otherwise category coverage check → if any category 'critical' issue is found, request changes; else approve with human sign-off.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/agent-review.yml`

```yaml
name: agent-review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

concurrency:
  group: agent-review-${{ github.event.pull_request.number }}
  cancel-in-progress: true

jobs:
  review:
    if: github.event.pull_request.draft == false
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Pre-flight secret scan
        run: |
          curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
          trufflehog git file://. --since-commit HEAD~1 --only-verified --fail

      - name: Check PR size
        run: |
          LINES=$(git diff --shortstat origin/main...HEAD | awk '{n=$4+$6} END{print n+0}')
          echo "PR changes $LINES lines"
          if [ "$LINES" -gt 1500 ]; then
            echo "::error::PR too large ($LINES lines). Split into smaller PRs."; exit 1
          fi
          if [ "$LINES" -gt 400 ]; then
            echo "::warning::PR large ($LINES lines). Agent quality drops above 400."
          fi

      - name: Run agent review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh pr diff ${{ github.event.pull_request.number }} > diff.patch

          # Include project conventions for better precision
          CONTEXT=""
          [ -f CONTRIBUTING.md ] && CONTEXT=$(head -100 CONTRIBUTING.md)

          claude -p "You are reviewing a PR. Use comment types: BLOCKING, SUGGESTION, NITPICK, QUESTION, PRAISE.
          For each finding: file:line | type | body | optional fix (single-file, max 15 lines).
          Categories: correctness, design, maintainability, testing, performance, security.
          Rules:
          - Quote exact lines you reference.
          - If unsure, use QUESTION not BLOCKING.
          - Cap NITPICK at 5.
          - End with one PRAISE if merited.
          Project conventions: $CONTEXT
          Diff:" < diff.patch > review.md

          gh pr comment ${{ github.event.pull_request.number }} -F review.md
```
