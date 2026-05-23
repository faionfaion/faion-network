---
slug: fork-vs-fix-decision-rule
tier: pro
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 5-axis decision rule (urgency/blast/patch-size/upstream-responsiveness/strategic-dep) routing an upstream-library bug to workaround/monkey-patch/upstream-PR/fork-pin/replace.
content_id: "49cb81203cf71d85"
complexity: medium
produces: decision-record
est_tokens: 4400
tags: [forking, upstream, dependency, monkey-patch, decision-framework]
---
# Fork vs Fix Decision Rule

## Summary

**One-sentence:** 5-axis decision rule (urgency/blast/patch-size/upstream-responsiveness/strategic-dep) routing an upstream-library bug to workaround/monkey-patch/upstream-PR/fork-pin/replace.

**One-paragraph:** Engineers default to whichever fix path matches their mood: confident devs over-fork, cautious devs wait months for upstream, junior devs monkey-patch in `node_modules`. This methodology pins a 5-axis score: URGENCY (3=hours, 0=weeks), BLAST (3=build broken, 0=one route), PATCH-SIZE (3=>100 LOC, 0=<10), UPSTREAM-RESPONSIVENESS (3=dead repo, 0=days), STRATEGIC-DEPENDENCY (3=core forever, 0=replacing it next quarter). Total 0-15 maps to 5 actions. Strategic override forces UPSTREAM-PR-or-higher for core-forever libraries; ban list forbids monkey-patch on security-critical / framework-core libraries. Output: `FixDecision` JSON + ADR conforming to `02-output-contract.xml`.

**Ефективно для:**

- A confirmed upstream OSS library bug that blocks the project.
- Quarterly fork audit: re-evaluate whether existing forks still earn their keep.
- Reviewer asked to gate a fork PR — apply the 5-axis score before approving.
- AI agents proposing "let's just fork it" — challenge with the score.
- Cross-team standardisation of dependency-fix decisions.

## Applies If (ALL must hold)

- A confirmed bug / missing feature in an upstream OSS library blocks the project.
- The project has access to fork / patch the dependency.
- The bug has measurable impact (errored requests, blocked release, security finding).
- ≥ 30 minutes available — this is a decision exercise, not a hotfix.

## Skip If (ANY kills it)

- The bug is in your own code, not upstream — fix it.
- The dependency is proprietary / no source access — open ticket.
- 2-line config change resolves it — apply config; skip the framework.
- Bug is in a transitive dep — fix in your direct dep first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repro | minimal test case (link or commit) | engineer |
| Upstream issue link or "none yet" | URL or note | engineer |
| Library health snapshot | GitHub stats (last release age, issue cadence, maintainers) | engineer |
| Patch size estimate | LOC + files touched | engineer |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer/supply-chain-risk-checklist-spike` | Sister methodology — score the library; fork decision is the downstream action. |
| `pro/dev/software-developer/dependency-audit` | Periodic dep audit which surfaces these decision points. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 5-axis score, action map, strategic-dep override, fork hygiene, monkey-patch ban-list | ~1000 |
| `content/02-output-contract.xml` | essential | `FixDecision` JSON schema + valid/invalid examples + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: ego-fork, perma-workaround, hidden-monkey-patch, fork-orphaning, stalled-PR, replace-thrash | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: score axes → compute action → apply override → write decision → schedule sunset | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping the score to one of the 5 actions, with overrides | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `upstream_responsiveness_check` | haiku | GitHub API: median merge time |
| `axis_scoring` | sonnet | Bounded judgment per axis |
| `action_selection` | sonnet | Threshold + rule combination |
| `fork_setup_playbook` | sonnet | Step-by-step for chosen action |

## Templates

| File | Purpose |
|------|---------|
| `templates/fix-decision.json` | FixDecision artefact seed |
| `templates/fork-pin-playbook.md` | Step-by-step fork procedure |
| `templates/upstream-pr-template.md` | PR description template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-fork-vs-fix-decision-rule.py` | Validate FixDecision JSON against schema | Per fork-vs-fix decision; quarterly audit |

## Related

- [[supply-chain-risk-checklist-spike]]
- [[dependency-audit]]
- parent skill: `pro/dev/software-developer/`
- external: [Tim Bray — Bug-Filing Best Practices](https://www.tbray.org/ongoing/) · [n8n forking patterns (NERO ADR-2024-007)](https://github.com/n8n-io/n8n/) · [patch-package npm tool](https://github.com/ds300/patch-package) · [Renovate config docs](https://docs.renovatebot.com/) · [Tom Critchlow — Forking decisions](https://tomcritchlow.com/)

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the 5-axis score and routes to one of WORKAROUND / MONKEY-PATCH / UPSTREAM-PR / FORK-PIN / REPLACE, then layers the strategic-dependency override and monkey-patch ban list. Use it whenever proposing a dependency fix or reviewing one.

## Procedure

See `content/04-procedure.xml`. The procedure operationalises the tree: score → compute → override → write decision record → schedule sunset (for FORK-PIN). The procedure is the link between this AGENTS envelope and the FixDecision artefact produced.
