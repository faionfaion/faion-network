# Renovate Auto-Merge + AI Handoff for Breaking Updates

## Summary

**One-sentence:** Renovate auto-merges semver-safe patch/minor bumps once CI is green and Merge-Confidence is high; major bumps and security alerts are labelled `agent-fixable` and handed to an LLM coding agent.

**One-paragraph:** LLM agents are wasted on patch-version bumps that Renovate already merges deterministically; conversely, Renovate alone cannot handle major-version bumps that require call-site rewrites and test updates. Splitting the work along the semver boundary (and Merge-Confidence threshold) keeps cost, latency, and risk all within budget. This methodology produces a Renovate config artefact that pins two `packageRules` (patch/minor auto-merge + major→agent-fixable) plus a GitHub Actions workflow that picks up the label and assigns the PR to Copilot Coding Agent, Claude, Codex, or Devin.

**Ефективно для:**

- Repos з `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `composer.json` — Renovate покриває все.
- Security-alert remediation де патч торкає call-sites.
- Multi-language monorepo з єдиним Renovate config.
- Repos, де бюджет агентських токенів обмежений — patch-bumps мають коштувати нуль.

## Applies If (ALL must hold)

- Repo uses a package manager Renovate supports.
- Team accepts auto-merge for patch + minor on stable (>=1.0.0) packages.
- CI is green and reliable enough that auto-merge on green is safe.
- An LLM coding agent (Copilot, Claude, Codex, Devin) is wired to the GitHub `agent-fixable` label.

## Skip If (ANY kills it)

- Manual release-train governance reviews every dep bump in a meeting.
- Repo pins all versions exactly and never auto-updates.
- No CI or CI is so flaky that "green" means nothing.
- Repo is a vendored mirror — upstream owns dependency policy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Renovate config | renovate.json | lead |
| Agent handoff workflow | .github/workflows/dependabot-agent-handoff.yml | platform |
| Branch protection | required checks include Renovate's CI | security |
| Coding-agent install | Copilot Coding Agent / Claude / Codex / Devin | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | Local hooks complement remote merge gating. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `config_draft` | sonnet | Renovate packageRules need light judgement on which rangeStrategy. |
| `handoff_workflow` | haiku | Boilerplate GitHub Actions YAML. |
| `agent_pick` | sonnet | Pick Copilot vs Claude vs Codex vs Devin for the org. |

## Templates

| File | Purpose |
|------|---------|
| `templates/renovate.json` | Renovate config: semver split + agent label + vulnerability route. |
| `templates/dependabot-handoff.yml` | GitHub Actions workflow assigning labelled PRs to the agent. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-renovate-ai-handoff.py` | Validate the produced config artefact against the JSON Schema. | pre-merge of renovate.json |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[mr-codemod-refactor-agent]]
- [[mr-error-tracker-draft-pr]]
- [[lint-precommit-floor]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (repo has package manager? CI green on patch? bump is major or security alert?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether to auto-merge or hand off to the agent — the tree terminates either on the active rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/renovate.json`

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "schedule:weekly",
    ":semanticCommits"
  ],
  "labels": [
    "dependencies"
  ],
  "rangeStrategy": "bump",
  "packageRules": [
    {
      "_comment": "Patch + minor on stable (>=1.0.0) auto-merge via Renovate.",
      "matchUpdateTypes": [
        "patch",
        "minor"
      ],
      "matchCurrentVersion": "!/^0/",
      "automerge": true,
      "automergeType": "branch",
      "platformAutomerge": true,
      "automergeStrategy": "rebase"
    },
    {
      "_comment": "0.x packages: minor is breaking; treat like major.",
      "matchUpdateTypes": [
        "minor"
      ],
      "matchCurrentVersion": "/^0/",
      "labels": [
        "agent-fixable",
        "dependencies"
      ],
      "automerge": false
    },
    {
      "_comment": "Major bumps always go to the AI coding agent.",
      "matchUpdateTypes": [
        "major"
      ],
      "labels": [
        "agent-fixable",
        "dependencies"
      ],
      "automerge": false
    }
  ],
  "vulnerabilityAlerts": {
    "labels": [
      "agent-fixable",
      "security"
    ],
    "automerge": false
  }
}
```

### `templates/dependabot-handoff.yml`

```yaml
# .github/workflows/dependabot-agent-handoff.yml
# When a PR (Dependabot or Renovate) carries the `agent-fixable` label,
# assign it to a coding agent so the agent rewrites breaking call-sites
# and pushes new commits to the same branch.
# Reference: https://github.blog/changelog/2026-04-07-dependabot-alerts-are-now-assignable-to-ai-agents-for-remediation/

name: dependabot-agent-handoff
on:
  pull_request:
    types: [labeled, opened, reopened]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  assign:
    if: contains(github.event.pull_request.labels.*.name, 'agent-fixable')
    runs-on: ubuntu-latest
    steps:
      - name: Pick the agent
        id: pick
        run: |
          echo "agent=copilot" >> "$GITHUB_OUTPUT"  # or claude | codex | devin

      - name: Assign PR to coding agent
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh pr edit ${{ github.event.pull_request.number }} \
            --add-assignee "${{ steps.pick.outputs.agent }}-swe-agent" \
            --add-label "assigned:${{ steps.pick.outputs.agent }}"
```
