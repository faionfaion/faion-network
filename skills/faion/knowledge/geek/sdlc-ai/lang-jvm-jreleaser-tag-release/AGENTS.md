# JVM One-Tag Release via JReleaser

## Summary

Replace ad-hoc `mvn deploy` / `gradle publish` plus hand-edited `CHANGELOG.md` with a single `jreleaser.yml` checked into the repo. A pushed git tag (e.g. `v1.4.0`) triggers one CI workflow that signs artifacts (GPG / Sigstore), uploads to Maven Central via the new Sonatype Central Portal, publishes a GitHub Release with notes generated from conventional commits, and optionally distributes binaries to Homebrew / Scoop / SDKMAN. AI agents never touch deploy YAML — they only land the change behind the tag.

## Why

JVM release pipelines historically sprawl across `pom.xml`/`build.gradle`, signing keys, Sonatype OSSRH credentials, GitHub release notes, and homebrew taps; an LLM agent editing any one of those silently breaks the others (forgotten `gpg.passphrase`, wrong `nexus-staging` URL, stale `CHANGELOG.md`). JReleaser (Apache 2.0, JVM-native) consolidates the whole flow into one declarative config; failures surface in one workflow log; the canonical input is `git tag` and `jreleaser.yml`. With Sonatype OSSRH retired (June 30 2025) and Central Portal mandatory in 2026, releases that hand-roll `nexus-staging-maven-plugin` are already broken — JReleaser tracks the new endpoint and is the path of least resistance.

## When To Use

- Libraries published to Maven Central or another public Maven repo (Central Portal, Gradle Plugin Portal, GitHub Packages).
- CLIs distributed via Homebrew, Scoop, SDKMAN, Snap, or Chocolatey alongside JARs.
- Polyglot repos with JVM + Go / Rust / Native binaries needing one release flow (JReleaser supports non-JVM artifacts too).
- Any team where the release process has at least one "tribal knowledge" step that an agent would skip.

## When NOT To Use

- Single-artifact internal libraries published to a private corporate Nexus where `mvn deploy` already works — the migration cost exceeds the value.
- Snapshot-only flows (continuous main → SNAPSHOT pushes) — JReleaser is for tagged releases.
- Air-gapped environments without outbound HTTPS to GitHub / Maven Central / signing services.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tag-as-release-trigger.xml` | Tag-driven release contract, `jreleaser.yml` skeleton, agent boundary. |
| `content/02-central-portal-signing.xml` | Sonatype Central Portal endpoint, GPG/Sigstore signing, conventional-commit notes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/jreleaser.yml` | Minimum-viable config: Maven Central + GitHub Release + GPG signing. |
| `templates/release.yml` | GitHub Actions workflow triggered by `v*` tags, invoking JReleaser. |
