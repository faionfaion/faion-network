# New Dependency Risk Checklist

## Summary

**One-sentence:** Produces a new-dependency risk record — licence, maintainer count, last release, CVE history, alternative-considered, owner — so adding a transitive dependency stops being a one-click decision.

**One-paragraph:** Produces a new-dependency risk record — licence, maintainer count, last release, CVE history, alternative-considered, owner — so adding a transitive dependency stops being a one-click decision. The methodology pins shape + owner + evidence + outcome review so the artefact becomes a reviewable operating tool rather than folklore. Inputs are validated against a JSON schema; outputs are gated by the `## Decision tree` so the agent skips the methodology when preconditions don't hold.

**Ефективно для:** tech leads and security reviewers approving net-new npm/pypi/cargo dependencies who need a written risk record before a 'tiny utility' becomes a CVE / licence / supply-chain liability.

## Applies If (ALL must hold)

- A net-new npm, PyPI, crates.io, Go, Maven, RubyGems or NuGet package (not already in the committed lockfile at the same major version) is about to be added.
- The repository has a committed lockfile (package-lock.json, yarn.lock, pnpm-lock.yaml, poetry.lock, uv.lock, Cargo.lock, go.sum) and CI installs from it.
- The registry exposes licence, maintainers, last release, install scripts and repository metadata for the package.
- OSV.dev, the GitHub Advisory Database or NVD can be queried for the exact name and version on the day of the record.
- One person will own the package's upgrade alerts (Dependabot, Renovate, audit tooling) as `role:handle`.

## Skip If (ANY kills it)

- The package is already in the lockfile, directly or transitively, at the same major version; import from the existing version instead.
- The change is a patch or minor bump of an already recorded dependency; the named upgrade owner handles it without a new record.
- The repository has no committed lockfile; no dependency is approved until one exists, so write the lockfile first.
- The code is being vendored into the repo with attribution and a test rather than installed from a registry; record it as `in-house`.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Package metadata | `npm view <pkg>` / PyPI JSON / `cargo info` output: licence, maintainers, latest release, scripts, repository | package registry |
| LICENSE file | text at the source repository root | upstream repository |
| Dry-run install diff | `npm install --package-lock-only` diff, `pip install --dry-run --report`, `cargo tree --prefix none` | local checkout |
| Advisory lookup | URL on OSV.dev / GitHub Advisory Database / NVD for the exact name and version, dated | advisory database |
| Lockfile PR | commit or PR URL updating the lockfile with the exact version | the dependency PR |
| Alert routing | Dependabot / Renovate / audit configuration naming the recipient | repo CI configuration |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[code-review]]` | Peer methodology that reviews the artefact before merge. |
| `[[incident-decision-template]]` | Peer methodology for incident-time decisions referenced by this artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: SPDX licence, transitive count, maintainer/release recency, advisory lookup, alternative incl. in-house, exact pin + lockfile, install hooks/provenance, upgrade owner + patch window | ~2300 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the risk record: exact package and provenance (install hooks, repository match, near-name), SPDX licence, transitive count, maintainers, last release, alternatives with in-house, patch window, dated advisory lookup, lockfile commit, structured verdict with fallback and mitigation, alert recipient equal to owner; valid and invalid records; 8 forbidden patterns | ~4800 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~1450 |
| `content/04-procedure.xml` | recommended | 9 steps: check already-in-tree, read SPDX licence, count the subtree, maintainers and recency, dated advisory lookup, install hooks and provenance, alternatives including in-house, pin version with lockfile commit, decide and route alerts | ~1700 |
| `content/05-examples.xml` | recommended | Complete accepted record for dayjs@1.11.10 (MIT, zero transitive, clean OSV, three alternatives, pnpm lockfile, Renovate to owner) with a note per value, plus the crossenv typosquat record and what the validator prints | ~1800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Parse inputs + check preconditions | haiku | Mechanical schema parse. |
| Author the artefact body | sonnet | Bounded synthesis from typed inputs. |
| Review for compliance + cross-cutting impact | opus | Cross-input judgement when stakes are high. |
| Outcome-review synthesis at cadence | opus | Did the artefact change behaviour? |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | Markdown skeleton of the artefact with all required sections. |
| `templates/skeleton.md` | Markdown skeleton of the artefact with all required sections. Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum-viable filled JSON instance, parseable by the validator. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-new-dependency-risk-checklist.py` | Validate an artefact JSON against the output-contract schema + cross-field rules. | Pre-merge of the artefact PR + weekly staleness scan. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[code-review]] — gates the artefact before merge.
- [[incident-decision-template]] — sibling 2-minute decision record.
- [[regression-test-first-bugfix-workflow]] — sibling workflow that pins red-test-first discipline.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether preconditions hold (named trigger + named owner + typed inputs). If yes, it routes between the full artefact form and a minimal-record fallback when the trigger is below the materiality threshold. If preconditions don't hold, the conclusion is to skip this methodology and route the work upstream.
