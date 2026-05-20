---
slug: team-methodology-overlay-mechanism
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a2744d762913d082"
summary: Specifies the per-user and per-repo overlay layer that lets in-house teams substitute their own ADR templates, RFC formats, code-review checklists, and security policies on top of the shipped faion methodology corpus with deterministic precedence.
tags: [team, overrides, customisation, sdd, geek-tier]
---

# Team Methodology Overlay Mechanism

## Summary

**One-sentence:** Specifies the per-user and per-repo overlay layer that lets in-house teams substitute their own ADR templates, RFC formats, code-review checklists, and security policies on top of the shipped faion methodology corpus with deterministic precedence.

**One-paragraph:** Faion ships free / solo / pro / geek as a content ladder, but in-house teams need to overlay company-specific opinions (e.g. "we use OneRFC not ADR", "every PR needs SOC-2 evidence row", "rust-clippy strict mode"). Without an overlay layer, teams either fork the corpus (drift within 90 days) or never adopt org-wide (it stays single-dev). This methodology defines the directory structure (`~/.faion/overrides/` user-level + `<repo>/.faion/overrides/` repo-level), the precedence rules (repo &gt; user &gt; shipped), the merge semantics (replace, prepend, append per file kind), and the validator that detects conflicts. Output: a runtime-resolved methodology view + an audit log of overrides applied.

## Applies If (ALL must hold)

- consumer is an in-house team ≥ 3 developers OR a regulated org with its own policies
- team has at least 1 existing custom doc (ADR template, code-review checklist, RFC format) it wants to keep
- faion-cli v1.0+ installed with overlay support
- team is willing to maintain the overrides folder under source control

## Skip If (ANY kills it)

- single solo operator — overrides add complexity without payoff
- team has zero custom docs — adopt shipped corpus as-is
- team wants to fork the entire corpus — that's a fork, not an overlay; use git fork instead
- team has &lt; 30 days of faion usage — wait for actual friction before overriding

## Prerequisites

- list of team-specific docs to overlay (paths, versions, owners)
- existing `tier-manifest.json` of methodologies the team consumes
- a designated overlay maintainer (one human, not "everyone")
- git repo for the overrides folder (e.g. `acme/faion-overrides`)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdd/sdd/sdd-tier-manifest` | Defines the path-to-tier map this overlay layer rewrites |
| `pro/dev/software-developer/adr-architecture-decisions` | Canonical ADR shipped — example of what teams override |
| `geek/ai/claude-code/skills` | Skill resolution order; this methodology extends it for content |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: directory layout, precedence order, merge semantics, validator, audit log | ~1100 |
| `content/02-output-contract.xml` | essential | `OverlayResolution` schema + audit-event schema | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: silent override, version skew, partial merge, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `overrides_discovery` | haiku | Filesystem scan |
| `precedence_resolution` | sonnet | Deterministic rule application |
| `conflict_detection` | sonnet | Diff vs shipped, flag breaking overrides |
| `audit_log_compose` | sonnet | Structured event log |

## Templates

| File | Purpose |
|------|---------|
| `templates/overrides-config.yaml` | Team's overlay declaration file |
| `templates/overlay-resolution.json` | Resolved methodology view schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/resolve-overlay.py` | Compute precedence-resolved methodology set | Pre-faion-command runtime |
| `scripts/audit-overlay-diff.py` | Compare shipped vs overlay; flag breaking changes | Quarterly review |

## Related

- parent skill: `geek/sdd/sdd/`
- peer methodologies: `sdd-tier-manifest`, `tier-policy-enforcement`
- external: [GitHub CODEOWNERS docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) · [Helm chart overrides pattern](https://helm.sh/docs/chart_template_guide/values_files/) · [git config precedence](https://git-scm.com/docs/git-config#FILES)
