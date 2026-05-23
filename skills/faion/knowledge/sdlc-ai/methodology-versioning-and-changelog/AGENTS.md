# Methodology Versioning and CHANGELOG

## Summary

**One-sentence:** Defines semver rules + CHANGELOG entries for faion methodologies and the migration plan emitted when content shape changes.

**One-paragraph:** Without versioning, downstream agents cannot tell a no-op rewrite apart from a breaking shape change. This methodology pins semver semantics for methodologies (MAJOR = breaking schema or rule-id rename; MINOR = additive rule or new content file; PATCH = wording / non-semantic fix), the CHANGELOG entry shape, and the migration plan that ships when MAJOR triggers. Output is a versioning record per change, validated against the schema before merge.

**Ефективно для:**

- Maintainers cutting a release of a methodology and unsure which semver bump applies.
- Downstream agents that pin methodology versions via `content_id` and need accurate bump signals.
- CI gate that blocks merges with missing or malformed CHANGELOG entries.
- Migration planning: every MAJOR bump emits a migration plan with from/to mapping.

## Applies If (ALL must hold)

- Methodology body or content/*.xml changes are being merged.
- Some `content_id` or schema field will shift.
- Downstream methodologies / playbooks reference this methodology by slug.

## Skip If (ANY kills it)

- Pure typo fix that touches no code path or schema field — use PATCH inline without record.
- Brand-new methodology — initial 1.0.0 record uses a separate skeleton.
- Content marked `deprecated` and scheduled for removal — use the removal flow.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Diff | git diff between current and previous version | git |
| Schema diff | JSON Schema diff of 02-output-contract.xml | internal tool |
| Rule-id diff | list of added / removed / renamed rule ids | internal tool |
| Last published version | semver string from previous AGENTS.md | AGENTS.md |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| methodology-contribution-flow-open-authorship | External contributions feed into this versioning loop. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: semver-rules, changelog-required, migration-plan-on-major, content-id-recompute, no-silent-rules-drop | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the versioning record + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: silent-major-as-minor, missing-changelog, broken-migration-plan, content-id-stale, rule-id-renamed-without-mapping | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: diff → classify → write CHANGELOG → emit migration plan if MAJOR → tag and merge | 800 |
| `content/06-decision-tree.xml` | essential | Maps schema/rule diff signals to MAJOR / MINOR / PATCH and routes whether a migration plan is required | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-bump` | sonnet | Reads schema + rule-id diff and chooses the bump. |
| `draft-changelog` | haiku | Bounded transformation from diff to bullet list. |
| `emit-migration-plan` | opus | MAJOR bumps carry stakes — needs care. |

## Templates

| File | Purpose |
|------|---------|
| `templates/changelog-entry.md` | CHANGELOG entry skeleton (heading, summary, scope, migration link). |
| `templates/migration-plan.md` | Migration plan template for MAJOR bumps. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-methodology-versioning-and-changelog.py` | Validate the artefact against the JSON Schema in `content/02-output-contract.xml`. | After draft, before downstream consumer reads. |

## Related

- [[methodology-contribution-flow-open-authorship]]
- [[shift-log-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, choice of variant, and the verdict label.
