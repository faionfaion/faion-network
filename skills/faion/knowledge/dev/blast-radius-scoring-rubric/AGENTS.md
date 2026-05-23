# Blast Radius Scoring Rubric

## Summary

**One-sentence:** A 60-second scoring rubric that triages every PR on services × users × reversibility (3-15 scale) with category overrides, routing it to light skim, standard review, or deep read.

**One-paragraph:** A solo developer or outsource lead reviewing 3+ PRs per day cannot afford to deep-read every diff and cannot afford to skim every diff either. The rubric estimates each PR's blast radius along three axes — services touched, users affected, reversibility — produces a 3-15 score, and routes the review accordingly. Auto-bumps to 11+ kick in for auth, payments, secrets, migrations, deletions, money, PII, and cron — regardless of axis math. Outputs a per-PR rubric artefact (artefact_id, axes, total, verdict, rollback-plan-required) that is auditable post-incident.

**Ефективно для:**

- Соло-розробник або outsource-lead, який ревьюїть 3+ PR на день і втрачає час на Tailwind-tweak deep-reads.
- Командний шаблон PR — заставити автора заявити blast self-score, який ревьювер тільки верифікує.
- Триаж incident-черги (той же фреймворк: S+U+R ≥11 пейджить on-call).
- Audit-trail після prod-incident: чи рубрика дала правильний score-route, чи треба додати категорію.

## Applies If (ALL must hold)

- The reviewer (you or outsource lead) processes ≥3 PRs per day.
- The repo has more than one service / module / shared library — radius varies across PRs.
- The team can name the auth / data / infra / payments surfaces in the stack.
- The PR template (GitHub / Linear / GitLab) supports a custom field for the score.

## Skip If (ANY kills it)

- You merge your own PRs without review — there is no reviewer to triage to.
- All PRs touch the same single service and the same single DB table — score is constant.
- A dedicated SRE / release engineer runs staged rollout gates that already enforce the same routing.
- The PR is a one-line copy/CSS fix — just skim and merge, the rubric overhead exceeds the payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| PR diff + description | text + diff | tracker (GitHub, GitLab, Linear) |
| Surface inventory (auth / data / infra / payments paths) | YAML or Markdown | team handbook |
| Severity / priority matrix | Markdown | QA handbook |
| Score field in PR template | YAML (GitHub) / JSON (Linear) | repo `.github/` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/ci-quality-gate-design` | The rubric is one gate among several; CI design assumes blast scoring exists. |
| none | Otherwise standalone — runs at PR open. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules: 3-axis scoring 1/3/5, route by total, category auto-bump, rollback-plan-required, audit field, quarterly recalibration, incident-triage parity | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for rubric output: per-axis scores, total, verdict, override-fired, rollback_plan, version, last_reviewed | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: score-by-LOC, missing override, fake rollback plan, recalibration skipped | 700 |
| `content/06-decision-tree.xml` | essential | Routes by total + override; produces verdict ∈ {light-skim, standard, deep-read, block-missing-rollback} | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-axes` | haiku | Mechanical: count touched services, lookup user-impact band, classify reversibility. |
| `apply-override` | haiku | Pattern match diff paths against surface inventory. |
| `draft-rollback-plan` | sonnet | Free-form text generation grounded in the diff + override category. |

## Templates

| File | Purpose |
|------|---------|
| `templates/blast-radius-scoring-rubric.json` | JSON Schema for the rubric output artefact. |
| `templates/pr-template-blast-field.md` | Markdown snippet for the PR template's blast self-score block. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-blast-radius-scoring-rubric.py` | Validate a rubric JSON against the schema + override consistency. | On PR open, by the bot, before assigning reviewer. |

## Related

- [[ci-quality-gate-design]] — the rubric is one gate the CI design composes.
- [[changelog-automation-conventional-commits]] — categorical signal complementary to blast score.
- [[bug-pattern-to-lint-rule-conversion]] — converts repeat-offender clusters into deterministic gates.

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks whether an override category is touched (auth / payments / secrets / migrations / deletes / money / PII / cron) — if yes, force total ≥ 11 → deep-read. Otherwise it routes by raw total: 3-5 light-skim, 6-10 standard, 11-15 deep-read. A separate leaf blocks merge when verdict is deep-read AND rollback_plan is missing for irreversible (R=5) changes. Each leaf references a rule id in `01-core-rules.xml`.
