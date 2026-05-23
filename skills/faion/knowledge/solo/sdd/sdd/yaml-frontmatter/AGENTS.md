---
slug: yaml-frontmatter
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Standardise the YAML frontmatter block at the top of every SDD markdown file: a fixed key set, typed values, semver version, ISO last_reviewed date, and inline-list fields the line-based parser can consume.
content_id: "a49818c57b9c3831"
complexity: light
produces: config
est_tokens: 2800
tags: [metadata, yaml, frontmatter, schema]
---
# YAML Frontmatter Standards

## Summary

**One-sentence:** Standardise the YAML frontmatter block at the top of every SDD markdown file: a fixed key set, typed values, semver version, ISO last_reviewed date, and inline-list fields the line-based parser can consume.

**One-paragraph:** Standardise the YAML frontmatter block at the top of every SDD markdown file: a fixed key set, typed values, semver version, ISO last_reviewed date, and inline-list fields the line-based parser can consume. The methodology pins the artefact: a closed key list, per-key type, allowed-enum values, and a validator that runs in pre-commit so drift is caught before merge.

**Ефективно для:**

- All SDD markdown documents (spec/design/impl-plan/task) sharing a metadata block.
- Pipelines that read frontmatter to route artefacts and check phase.
- Reviewers scanning metadata for last_reviewed / version drift.
- Audit surface: every doc has a parseable header.

## Applies If (ALL must hold)

- Markdown / MDX documents in the repo need machine-readable metadata.
- Multiple tools (validators, search, dashboards) consume that metadata.
- A line-based frontmatter parser is in the toolchain.

## Skip If (ANY kills it)

- Documents are free-form prose with no automated consumers.
- Single-tool setup that already enforces its own metadata format.
- Binary or non-text artefacts — frontmatter does not apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Document folder | directory | Repo |
| Frontmatter schema | yaml | Spec doc |
| Pre-commit hook config | yaml | Repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `none` | This methodology has no upstream dependency. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-yaml-frontmatter` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-yaml-frontmatter` | haiku | Schema check + threshold checks; deterministic. |
| `review-yaml-frontmatter` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/yaml-frontmatter.json` | JSON skeleton conforming to the output contract schema. |
| `templates/yaml-frontmatter.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-yaml-frontmatter.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[sdd-workflow-overview]]
- [[writing-specifications]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
