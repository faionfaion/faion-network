# License Compliance Scan

## Summary

**One-sentence:** Repo-wide SPDX license scan on every PR: allowlist/denylist per license id, scanner pinned to ScanCode/Syft, fail on copyleft introductions absent justification.

**One-paragraph:** Closed-source products that absorb GPL/AGPL transitive dependencies face existential legal risk. This methodology installs a deterministic SPDX scan in CI: scanner pinned (ScanCode or Syft), allowlist + denylist of SPDX ids, scan runs on every PR + nightly main, and any new dependency outside the allowlist blocks merge until justification is recorded. Output is a SBOM-grade license report per PR.

**Ефективно для:**

- The product is distributed externally (closed-source binary, SaaS shipping copies of dependencies, embedded firmware).
- License decisions have legal implications (paying customers, regulated industry, IP-sensitive sale process).
- The dependency graph is non-trivial (≥30 transitive deps).

## Applies If (ALL must hold)

- The product is distributed externally (closed-source binary, SaaS shipping copies of dependencies, embedded firmware).
- License decisions have legal implications (paying customers, regulated industry, IP-sensitive sale process).
- The dependency graph is non-trivial (≥30 transitive deps).

## Skip If (ANY kills it)

- Internal-only tool used by no one outside the org and zero distribution scope.
- Pure-MIT/Apache codebase with one direct dep and no transitive pulls.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Dependency manifest | lockfile | package-lock.json / poetry.lock / go.sum / etc. |
| Scanner binary | bin | ScanCode (4.x+) or Syft (1.x+) |
| Allowlist + denylist | yaml | Repo at `compliance/licenses.yaml` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace + final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-gov-license-compliance-scan` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/licenses.yaml` | Allow/deny SPDX catalog |
| `templates/ci-snippet.yml` | GitHub Actions wiring |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gov-license-compliance-scan.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `geek/sdlc-ai/AGENTS.md`
- [[kb-agents-md-context-pyramid]]
- [[gov-conventional-commits-enforced]]
- [[inc-read-only-investigation-default]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/licenses.yaml`

```yaml
allowed:
  - MIT
  - Apache-2.0
  - BSD-2-Clause
  - BSD-3-Clause
  - ISC
  - MPL-2.0
  - LGPL-3.0-or-later
  - Unlicense
  - CC0-1.0
denied:
  - AGPL-1.0-or-later
  - AGPL-3.0-or-later
  - GPL-2.0-only
  - GPL-3.0-or-later
  - SSPL-1.0
  - Commons-Clause
unknown_action: deny
```

### `templates/ci-snippet.yml`

```yaml
name: license-scan
on:
  pull_request:
  schedule:
    - cron: "0 5 * * *"
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          docker run --rm -v $PWD:/src anchore/syft:v1.18.0 dir:/src -o cyclonedx-json > sbom.json
      - run: python scripts/validate-gov-license-compliance-scan.py --file report.json
```
