# Junior Next Pr Checklist Template

## Summary

**One-sentence:** Mentor-emitted PR checklist a junior carries to their next review: bounded, traceable items.

**One-paragraph:** Mentor-emitted PR checklist a junior carries to their next review: bounded, traceable items. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness without re-deriving the rationale.

**Ефективно для:**

- Pro-tier dev workflow, де потрібен auditable artefact замість ad-hoc decision.
- Команди, де ≥2 stakeholders читають один артефакт і повинні дійти однакового висновку.
- Cases where input must be cited (no fabrication) і decision-trail зберігається для review.
- Recurring trigger, що з'являється ≥1 раз на cycle і виправдовує methodology overhead.

## Applies If (ALL must hold)

- A PR review by a named mentor of a junior author has just completed with at least one substantive comment (not only nits a formatter would catch).
- Review comments and diff lines have permalinks the checklist can point at (GitHub, GitLab or equivalent).
- The team has a written style guide, ADRs or CONTRIBUTING.md to cite, or the mentor is willing to label uncited items as preferences.
- The junior will author their next PR within the same review loop, so the checklist can be pasted and ticked there.

## Skip If (ANY kills it)

- The review left only formatting or import-order comments; those go into lint and CI config, not a checklist.
- No previous or next PR from this author is expected (one-off contributor); a checklist has no next review to be carried to.
- The mentor is not available to confirm permalinks and severity; an unconfirmed AI draft must not be handed to the junior.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| The completed review: every comment and diff-line comment with its permalink | PR review thread | GitHub / GitLab PR |
| The previous checklist and its tick state | Markdown block in the just-reviewed PR description | previous PR |
| Team standards: style guide sections, ADR ids, CONTRIBUTING.md anchors | repository docs | repository |
| Linter, formatter, type-checker and CI configuration | config files | repository |
| Mentor and junior handles | team roster | mentor |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/dev/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: item traces to review comment, 3 to 7 items, verifiable on next PR, lintable items become lint, cites team standard, one blocker, carry-forward and retire, junior self-ticks | 1550 |
| `content/02-output-contract.xml` | essential | Draft-07 schema: 3-7 items each with a review-comment permalink, yes/no phrasing (trait words rejected), blocking / should with at most one blocker, standard citation or preference label, lint rule and ticket where machine-enforceable, new / carried (max 2) / done status, retired and pairing-session lists, deferred candidates, junior-ticks-first posting, mentor confirmation before handover; valid + invalid examples, forbidden patterns | ~3700 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 1050 |
| `content/04-procedure.xml` | essential | 7 steps: reconcile the previous checklist, harvest candidates with permalinks, phrase as yes/no checks, route machine-checkable items to lint, cite the standard and set one blocker, cut to 3-7 with a deferred list, hand the draft to the mentor | ~1450 |
| `content/05-examples.xml` | recommended | Complete checklist from a nine-comment review (four items, one blocker, one deferred, one retired, one routed to mypy), the Markdown the junior pastes, a note per non-obvious value, and a bad checklist with the validator output | ~2400 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation |
| `synthesize-decision` | sonnet | Per-instance judgment; bounded inputs |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/output.md.j2` | Checklist skeleton matching the schema in 02-output-contract.xml |
| `templates/output.md` | Checklist skeleton matching the schema in 02-output-contract.xml Generated from `templates/output.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Filled-in canonical example for calibration |
| `templates/_smoke-test.md` | Filled-in canonical example for calibration Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-junior-next-pr-checklist-template.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[audit-grade-code-review-checklist]]
- [[architect-mentoring-curriculum]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
