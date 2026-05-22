---
slug: fork-vs-fix-decision-rule
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "9e0e4705c59ba583"
summary: Explicit decision rule for when a blocking upstream library bug should be patched via fork, upstream PR, monkey-patch, replacement, or workaround — with a 5-axis score (urgency / blast / patch size / upstream responsiveness / strategic dependency).
tags: [forking, upstream, dependency, monkey-patch, decision-framework]
---

# Fork vs Fix Decision Rule

## Summary

**One-sentence:** Explicit decision rule for when a blocking upstream library bug should be patched via fork, upstream PR, monkey-patch, replacement, or workaround — with a 5-axis score (urgency / blast / patch size / upstream responsiveness / strategic dependency).

**One-paragraph:** Engineers default to whichever fix path matches their mood: confident devs over-fork, cautious devs wait months for upstream, junior devs monkey-patch in `node_modules`. This methodology pins a 5-axis decision: URGENCY (hours/days/weeks tolerated), BLAST RADIUS (one route vs whole app vs CI), PATCH SIZE (lines changed), UPSTREAM RESPONSIVENESS (PR-merge median), STRATEGIC DEPENDENCY (is this library on our core path forever?). Each scored 0-3; total maps to one of 5 actions (workaround / monkey-patch / upstream-PR / fork-pin / replace). NERO's n8n fork is the canonical case study. Output: `FixDecision` JSON + a one-page rationale.

## Applies If (ALL must hold)

- a confirmed bug / missing feature in an upstream OSS library blocks the project
- the project has access to fork / patch the dependency
- the bug has measurable impact (errored requests, blocked release, security finding)
- ≥ 30 minutes available — this is a decision exercise, not a hotfix

## Skip If (ANY kills it)

- the bug is in your own code, not upstream — fix it
- the dependency is proprietary / no source access — open ticket
- 2-line config change resolves it — apply config; skip the framework
- bug is in a transitive dep — fix in your direct dep first

## Prerequisites

- bug reproduction in a minimal test case (link or commit)
- upstream issue OR awareness that no upstream issue exists yet
- view of the library's GitHub: last release age, issue triage cadence, maintainer count
- estimate of patch size in lines (LOC) + files touched

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-developer/supply-chain-risk-checklist-spike` | Sister methodology — score the library; fork decision is the downstream action |
| `pro/dev/software-developer/dependency-audit` | Periodic dep audit which surfaces these decision points |
| `pro/dev/software-developer/library-evaluation` | Pre-adoption framework — fork-vs-fix runs post-adoption |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 5-axis score, action map, strategic-dep override, fork hygiene, monkey-patch ban-list | ~1000 |
| `content/02-output-contract.xml` | essential | `FixDecision` schema with axis scores + action + rollback plan | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: ego-fork, perma-workaround, etc. | ~900 |

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
| `templates/fix-decision.json` | Output schema |
| `templates/fork-pin-playbook.md` | Step-by-step fork procedure |
| `templates/upstream-pr-template.md` | PR description template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-fix.py` | Take inputs, emit FixDecision | Per fork-vs-fix decision |
| `scripts/audit-forks.sh` | Quarterly: are our forks still needed? | Quarterly |

## Related

- parent skill: `pro/dev/software-developer/`
- peer methodologies: `supply-chain-risk-checklist-spike`, `dependency-audit`
- external: [Tim Bray — Bug-Filing Best Practices](https://www.tbray.org/ongoing/) · [n8n forking patterns (NERO ADR-2024-007)](https://github.com/n8n-io/n8n/) · [patch-package npm tool](https://github.com/ds300/patch-package) · [Renovate config docs](https://docs.renovatebot.com/) · [Tom Critchlow — Forking decisions](https://tomcritchlow.com/)
