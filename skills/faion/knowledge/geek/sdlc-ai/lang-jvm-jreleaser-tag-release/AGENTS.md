---
slug: lang-jvm-jreleaser-tag-release
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Replace ad-hoc mvn deploy / gradle publish plus hand-edited CHANGELOG.
content_id: "95f3bdf051e20282"
tags: [jvm, jreleaser, maven-central, release, java]
---
# JVM One-Tag Release via JReleaser

## Summary

**One-sentence:** Replace ad-hoc mvn deploy / gradle publish plus hand-edited CHANGELOG.

**One-paragraph:** Replace ad-hoc mvn deploy / gradle publish plus hand-edited CHANGELOG.md with a single jreleaser.yml checked into the repo. A pushed git tag (e.g. v1.4.0) triggers one CI workflow that signs artifacts (GPG / Sigstore), uploads to Maven Central via the new Sonatype Central Portal, publishes a GitHub Release with notes generated from conventional commits, and optionally distributes binaries to Homebrew / Scoop / SDKMAN. AI agents never touch deploy YAML — they only land the change behind the tag.

## Applies If (ALL must hold)

- Libraries published to Maven Central or another public Maven repo (Central Portal, Gradle Plugin Portal, GitHub Packages).
- CLIs distributed via Homebrew, Scoop, SDKMAN, Snap, or Chocolatey alongside JARs.
- Polyglot repos with JVM + Go / Rust / Native binaries needing one release flow (JReleaser supports non-JVM artifacts too).
- Any team where the release process has at least one "tribal knowledge" step that an agent would skip.

## Skip If (ANY kills it)

- Single-artifact internal libraries published to a private corporate Nexus where mvn deploy already works — the migration cost exceeds the value.
- Snapshot-only flows (continuous main → SNAPSHOT pushes) — JReleaser is for tagged releases.
- Air-gapped environments without outbound HTTPS to GitHub / Maven Central / signing services.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/sdlc-ai/sdlc-ai/`
