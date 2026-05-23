# Code Review Process

## Summary

**One-sentence:** Standardises a team's review workflow with PR template + branch protection + four scenario templates + tracked health metrics.

**One-paragraph:** Beyond the per-PR review, the process layer pins how reviews are requested, blocked, and measured. This methodology emits the PR template, the GitHub branch-protection JSON, four scenario templates (bug fix / new design / security / performance), and a metrics spec for time-to-first-review, cycle time, and rework rate. Output is a versioned process bundle a team can land in one PR. Updates quarterly.

**Ефективно для:**

- Команди, що хочуть встановити review-process з нуля без 6-місячного консалтингу.
- Аудит існуючого процесу: 'що в нас зламано', 'де дрейфує time-to-first-review'.
- Multi-repo organisation: один bundle переноситься на 10+ репо.
- Звітність по review-health: metrics dashboard spec — готова до Grafana / Looker.

## Applies If (ALL must hold)

- GitHub / GitLab / Bitbucket platform with branch protection support.
- Team is ≥4 engineers (process overhead pays off above this).
- An owner can land the bundle PR.

## Skip If (ANY kills it)

- Solo or 2-person team — overhead exceeds payoff.
- Platform without branch protection (self-hosted bare git).
- Process locked by parent org's policy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo platform | string | platform inspection |
| Current PR template | Markdown | .github/PULL_REQUEST_TEMPLATE.md |
| Branch protection state | JSON | GitHub Repository Settings API |
| Metrics source | string | CI logs / GitHub API / DORA-collector |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: template-required, branch-protection-required, scenario-templates, metrics-tracked, refresh-quarterly | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the process-bundle artefact | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: template-without-enforcement, protection-bypass, metrics-without-action | 700 |
| `content/04-procedure.xml` | essential | 5-step bundle assembly procedure | 800 |
| `content/06-decision-tree.xml` | essential | Platform + size tree | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit_current` | haiku | Reads platform settings; deterministic. |
| `draft_bundle` | sonnet | Per-team customisation of templates. |
| `publish` | haiku | Deterministic file writes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pr-checks.yml` | GitHub Actions workflow that enforces PR checks |
| `templates/pr-description.md` | PR description template |
| `templates/pr-size-guard.sh` | Shell guard that fails CI on oversize PRs |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review-process.py` | Validate the process-bundle artefact | After bundle assembly, before opening the landing PR |

## Related

- - [[code-review]] — the per-PR review this process bundle enforces.
- - [[documentation]] — AGENTS.md / CONTRIBUTING.md updates that ride along.

## Decision tree

See `content/06-decision-tree.xml`. Branches on platform (GitHub / GitLab / Bitbucket) → emits the right protection format; then on team size (4-10 vs 10+) — larger teams get stricter required-reviewers count.
