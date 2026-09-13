# Pr Pattern Mining For Feedback

## Summary

**One-sentence:** Mines repeated PR-review comments into a feedback report: top antipatterns + suggested rule additions.

**One-paragraph:** Mines repeated PR-review comments into a feedback report: top antipatterns + suggested rule additions. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- Merged PRs and their review comments for the window can be fetched by one reproducible query (`gh api graphql`, `gh pr list --search`, or the GitLab equivalent) and the window holds at least 20 merged PRs and 100 review comments.
- Review comments carry author, URL and resolution history, so distinct reviewers and review round-trips can be counted.
- A formatter and linter exist for the language, so formatter-coverable comments can be identified and excluded.
- The scope (team or a named mentee) is agreed with the report owner before mining starts.
- A named owner will check the cited comment URLs and the scope declaration before the report is shared.

## Skip If (ANY kills it)

- The window holds fewer than 20 merged PRs or 100 review comments; record observations only, widen the window or wait a cycle.
- Review comments are not retrievable with URLs (reviews happen in chat or meetings); nothing can be cited.
- The request is for per-author rankings under a team scope; that is a leaderboard, not feedback.
- The language has no formatter or linter and reviewers are still doing formatting by hand; fix the tooling first, then mine.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Merged PRs and review comments in the window with author, URL, body and resolution | GraphQL or REST export from the stated query | GitHub / GitLab API |
| Review round-trip counts per comment thread, or the team's severity labels (issue / suggestion / nitpick) | thread metadata or label convention | PR platform |
| Formatter and linter rule catalogue for the language (ruff, eslint, prettier, gofmt, rustfmt) | rule ids | tool documentation |
| CI configuration and PR template | repository files | repository |
| Previous report for the same scope and query, with its baselines | prior report JSON | report store |
| Scope agreement: team, or mentee handle with consent and evaluation use stated | note from the owner | report owner |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: corpus + query stated, recurrence threshold, patterns as code behaviour, ranked by frequency x cost, formatter comments excluded, enforcement channel per rule, scope declared + consented, baseline + remeasure | 2050 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: team / mentee scope with no author leaderboard, corpus with window, counts, query and the 20 PR / 100 comment gate, patterns as code behaviour with before and after, 3 PRs and 2 reviewers with 3+ comment URLs, count x cost ranking with at most 5 top patterns, one automation-gap item, suggested rules with an enforcement channel and reasons, baseline and re-measure per pattern, ineffective after two cycles, owner check before sharing; valid + invalid examples, forbidden patterns | ~4850 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | 1200 |
| `content/04-procedure.xml` | essential | 8 steps: declare scope, fetch the corpus with a stated query and apply the sample gate, strip formatter-coverable comments, cluster by behaviour and apply recurrence, phrase with before and after, rank by count x cost and cut to five, attach an enforcement channel, set baselines and hand to the owner | ~1700 |
| `content/05-examples.xml` | recommended | Complete team report from 64 PRs and 412 comments (three top patterns with lint, checkbox and CI channels; 38 formatter comments as one ruff change), a note per non-obvious value, and a bad report with the validator output | ~2800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.md.j2` | Report skeleton matching the schema in 02-output-contract.xml |
| `templates/output.md` | Report skeleton matching the schema in 02-output-contract.xml Generated from `templates/output.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in canonical example for calibration |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pr-pattern-mining-for-feedback.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[junior-next-pr-checklist-template]]
- [[code-review-slo-and-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
