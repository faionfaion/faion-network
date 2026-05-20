---
slug: dependency-adoption-checklist
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "9e9418e3c4f4ec64"
summary: Concrete adoption checklist for a new dependency or service edge — pin, named owner, SBOM entry, escape hatch — distinct from the trade-off decision phase.
tags: [supply-chain, dependency-adoption, sbom, software-architect, dependency-policy]
---
# Dependency Adoption Checklist

## Summary

**One-sentence:** A checklist applied AFTER the decision to adopt a new dependency or service edge — pinning version, naming an owner, recording in the SBOM, defining the escape hatch — distinct from the trade-off analysis that produced the decision.

**One-paragraph:** Dependency-decision methodologies (trade-off analysis, security review) ask "should we use this?" This methodology answers "now that we said yes, what must be true before merge?" — five concrete checks: exact version pin, named maintainer/owner in the team, SBOM entry, escape-hatch (an exit plan if the dependency gets abandoned/compromised/relicensed), and a renewal review date. Currently these items are scattered across security, supply-chain, and ops methodologies, leaving the adopting developer to assemble them from memory. The output is a one-page dependency-adoption.md file checked into the repo alongside the PR introducing the dependency.

## Applies If (ALL must hold)

- A new dependency (library, framework, service-edge API) is being adopted.
- The dependency is direct (declared by your team), not transitive.
- Adoption has been agreed via the trade-off methodology (security review, vendor evaluation, etc.).
- Repo has dependency-management infrastructure (lockfile, SBOM, CI pipeline).

## Skip If (ANY kills it)

- Transitive dep introduced by an existing direct dep — handle via parent.
- Dev-only tool not shipping to production (linter, local CLI) — apply only pin + owner.
- Prototype/spike not destined for production — skip; revisit on promotion.
- Vendor service with a fully managed SLA and contract — the checklist applies at the contract level, different methodology.

## Prerequisites

- Decision-to-adopt completed via the trade-off/security review.
- Repo has a lockfile (package-lock.json, poetry.lock, Pipfile.lock, Cargo.lock, go.sum, etc.).
- SBOM tooling configured (Syft, cyclonedx, or vendor-provided).
- Team roster known.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-architect/dependency-tradeoff-analysis` | Produces the decision; this methodology runs after. |
| `geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan` | Supply-chain scan results inform pinning + owner. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: pin exact, named owner, SBOM entry, escape hatch, renewal date | ~900 |
| `content/02-output-contract.xml` | essential | dependency-adoption.md shape; required per-dependency fields | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: caret-pin, ownerless deps, no escape hatch | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-pin-from-lockfile` | haiku | Mechanical: read lockfile, grab exact version |
| `find-maintainer-signal` | sonnet | Survey upstream activity, BUS-factor, last release date |
| `draft-escape-hatch` | opus | Synthesis: list replacement candidates + migration shape |

## Templates

| File | Purpose |
|------|---------|
| `templates/dependency-adoption.md` | One file per adopted dep with all required fields |
| `templates/escape-hatch-skeleton.md` | Replacement candidates + migration outline |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/adoption-coverage-check.py` | Lockfile direct deps vs dependency-adoption files: flag uncovered | Quarterly |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodology: `dependency-tradeoff-analysis`, `sec-trivy-pinned-supply-chain-scan` (geek), `vendor-evaluation`
- external: [NIST SSDF dependency management](https://csrc.nist.gov/Projects/ssdf) · [SLSA framework](https://slsa.dev/) · [Snyk Open Source Advisor](https://snyk.io/advisor/)
