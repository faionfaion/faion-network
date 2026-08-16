# Changelog Automation from Conventional Commits

## Summary

**One-sentence:** Reads a commit range, groups commits by conventional-commits type, detects breaking changes via `!:` and `BREAKING CHANGE:` markers, and emits a CHANGELOG update artefact with per-release sections.

**One-paragraph:** A team that practices trunk-based development with conventional commits has the raw material for a CHANGELOG already in the commit log — the only thing missing is the automation. This methodology takes a commit range (or tag) and emits a CHANGELOG update artefact: a Markdown block per release that groups commits by type (Features, Fixes, Chores, etc.), surfaces breaking changes prominently, and lists scope where present. Output validates against a JSON Schema so the CI gate can refuse a release that lacks a changelog entry. Pre-merge Friday cleanup becomes a single command, not a 30-minute manual exercise.

**Ефективно для:**

- Solo dev / outsource lead doing pre-merge Friday cleanup; one command replaces 30 min of manual aggregation.
- Releases that customers / clients can read — turning `git log` into a curated artefact.
- Conventional-commits adoption check — the generator surfaces commits that don't follow the format.
- AI-assisted release notes — LLM enriches one-liners; the type taxonomy keeps the structure.

## Applies If (ALL must hold)

- Repo uses Conventional Commits (`feat:`, `fix:`, `chore:`, etc.) consistently OR you can fix the deviations in the same session.
- A `CHANGELOG.md` file (or equivalent) exists or is acceptable to create.
- Commit history for the range is linear or rebase-clean (no spaghetti merge graph).
- A release tag scheme (semver) is in use OR you are willing to add one.

## Skip If (ANY kills it)

- Repo does not use conventional-commits AND there is no plan to retroactively normalize.
- Monorepo with multiple independent release cadences — use a multi-package tool (changesets) instead.
- Releases are not visible to anyone (internal-only) — manual notes are fine.
- &lt;5 commits per release — handwritten is faster.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Commit range | `git log A..B` | repo |
| Previous CHANGELOG.md | Markdown | repo |
| Release tag candidate | semver | author |
| Convention spec | Markdown | conventionalcommits.org |
| Scope inventory | YAML / Markdown | repo handbook |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/automation-tooling/trunk-based-dev-principles` | Small daily commits feed the changelog. |
| `solo/dev/automation-tooling/trunk-based-feature-flags` | Flag-cleanup commits get a dedicated section. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: type-taxonomy, breaking-prominence, scope-surfacing, no-merge-commits, semver-mapping, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the changelog-update artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: silent malformed commits, missed breaking, merge-noise, version-bump-mismatch | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: pick-range → parse → group → emit-md → validate | 700 |
| `content/05-examples.xml` | reference | Worked release-notes example for v1.4.0 of a small CLI | 500 |
| `content/06-decision-tree.xml` | essential | Tree: range valid? → all conv-commits? → breaking? → version bump → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse-commits` | haiku | Mechanical regex against conventional-commits format. |
| `enrich-headlines` | sonnet | Optional human-facing rewrite of one-liners into release-notes prose. |
| `version-bump` | haiku | Deterministic: breaking → major; feat → minor; fix/chore → patch. |

## Templates

| File | Purpose |
|------|---------|
| `templates/changelog-automation-conventional-commits.json` | JSON Schema for the changelog-update artefact. |
| `templates/CHANGELOG.md` | Skeleton CHANGELOG with `## [Unreleased]` block. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-changelog-automation-conventional-commits.py` | Validate a changelog-update JSON against the schema + semver rule. | Pre-merge gate; release script. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[trunk-based-dev-principles]] — small commits feed the changelog.
- [[trunk-based-feature-flags]] — flag-cleanup commits flagged in their own section.
- [[ci-quality-gate-design]] — the gate that blocks releases lacking a changelog.

## Decision tree

See `content/06-decision-tree.xml`. The tree first verifies the commit range is bounded and clean (no merge commits with foreign histories). It then walks: are all commits conventional? are any marked breaking? what semver bump is required? Leaves emit `emit-changelog`, `block-non-conventional`, `block-missing-version-bump`, or `block-merge-noise`. Each leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/changelog-automation-conventional-commits.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/changelog-automation-conventional-commits.json",
  "type": "object",
  "required": [
    "artefact_id",
    "range_from",
    "range_to",
    "release_version",
    "release_date",
    "sections",
    "semver_bump",
    "verdict",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^chg-[a-z0-9-]{6,}$"
    },
    "range_from": {
      "type": "string",
      "minLength": 1
    },
    "range_to": {
      "type": "string",
      "minLength": 1
    },
    "release_version": {
      "type": "string",
      "pattern": "^v?\\d+\\.\\d+\\.\\d+(-[a-z0-9.-]+)?$"
    },
    "release_date": {
      "type": "string",
      "format": "date"
    },
    "semver_bump": {
      "enum": [
        "major",
        "minor",
        "patch"
      ]
    },
    "sections": {
      "type": "object",
      "required": [
        "breaking",
        "feat",
        "fix"
      ],
      "properties": {
        "breaking": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "feat": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "fix": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "chore": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "refactor": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "docs": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "perf": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "test": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "build": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "ci": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "style": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "deviations": {
          "type": "array",
          "items": {
            "type": "string"
          }
        }
      }
    },
    "verdict": {
      "enum": [
        "emit-changelog",
        "block-non-conventional",
        "block-missing-version-bump",
        "block-merge-noise"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```
