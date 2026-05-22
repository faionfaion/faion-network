---
slug: security-review-new-dependency
tier: geek
group: team-ops
persona: P6
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Proposed new lib/SDK → lightweight ADR + SBOM diff + supply-chain scan + license check before merge.
content_id: 151d40fef8f3c6a9
methodology_refs:
  - sec-trivy-pinned-supply-chain-scan
  - gov-license-compliance-scan
  - mr-renovate-ai-handoff
  - gov-approval-token-signed-jwt
  - security-supply-chain
  - security-container-scanning
  - architecture-decision-records
  - architecture-decision-records-sdd-planning
  - architecture-decision-records-sdd
  - security-architecture
---

# Security review for new dependency

**Playbook slug:** `security-review-new-dependency`
**Tier:** geek
**Complexity:** medium
**Persona:** P6 — Product-Dev Team

## Intent

Proposed new lib/SDK → lightweight ADR + SBOM diff + supply-chain scan + license check before merge.

## Scope

An engineer wants to add a new library or SDK to a service. Before merge, an AI agent runs SBOM diff, supply-chain scan, license-compliance check. A security-conscious engineer reviews the diff plus considered alternatives. The decision is recorded as a lightweight ADR. Ultra-trivial bumps are auto-applied via Renovate handoff with a signed JWT approval; non-trivial additions go through the full review.

### What this playbook covers

Two stages: AI auto-screen, then human review-with-ADR. The chain refuses two common failure modes: load-bearing dependencies adopted without an ADR, and auto-merging supply-chain risks because "Renovate said so." Renovate handoff is enabled only for ultra-trivial bumps and only with a signed approval token.

The threshold question is *load-bearing or replaceable*. A load-bearing dep (one that shapes the codebase architecturally, owns a workflow, or has no safe replacement) deserves an ADR even when the scan is green — because removing it later is the expensive operation. A replaceable dep gets a lighter ADR or none, depending on team policy. The criteria need to be written down (gap) so each engineer doesn't litigate them per PR.

License compatibility is the silent killer. A new MIT lib added under an MPL dep tree can quietly relicense parts of the product. The license scan is non-skippable, and amber results stop the merge until Legal weighs in.

### Non-goals

- Annual audit prep — see `soc2-gdpr-audit-prep`
- Architectural review of in-house code — see `weekly-architectural-review`
- Removing dependencies — separate cleanup playbook

### Prerequisites

- Trivy / supply-chain scan wired into CI
- CodeQL + container scanning on PRs
- Renovate (or equivalent) handoff configured
- ADR convention adopted by team

## Success criteria

The playbook is done when:
- SBOM diff produced and reviewed
- License check pass
- Supply-chain scan green
- ADR written for non-trivial additions
- Alternatives considered + documented
- Renovate-eligible bumps auto-handled with signed JWT

## Stages

### Stage 1: Auto-screen

**Intent:** AI screens the diff; trivial bumps move through Renovate handoff.

**Methodologies in chain:**
- `sec-trivy-pinned-supply-chain-scan` → `geek/sdlc-ai/sec-trivy-pinned-supply-chain-scan`
- `gov-license-compliance-scan` → `geek/sdlc-ai/gov-license-compliance-scan`
- `mr-renovate-ai-handoff` → `geek/sdlc-ai/mr-renovate-ai-handoff`
- `gov-approval-token-signed-jwt` → `geek/sdlc-ai/gov-approval-token-signed-jwt`
- `security-supply-chain` → `pro/infra/cicd-engineer/security-supply-chain`
- `security-container-scanning` → `pro/infra/cicd-engineer/security-container-scanning`

**Decision gate:**
> If auto-merge eligible AND scans green AND license clear → merge. Otherwise advance to human review.

### Stage 2: Human review + ADR

**Intent:** Security-conscious engineer reads the diff; considers alternatives; writes an ADR.

**Methodologies in chain:**
- `architecture-decision-records` → `solo/dev/software-architect/architecture-decision-records`
- `architecture-decision-records-sdd-planning` → `solo/sdd/sdd-planning/architecture-decision-records`
- `architecture-decision-records-sdd` → `solo/sdd/sdd/architecture-decision-records`
- `security-architecture` → `solo/dev/software-architect/security-architecture`

**Decision gate:**
> Required: ADR with at least one alternative considered. ADR-less merges = future surprise.

## Common pitfalls

- Skipping ADR for a "trivial" lib — turns load-bearing six months later
- License scan amber → ignored → legal surprise
- Auto-merge without signed-JWT — supply chain liability
- Adopting a dep with no maintainer pulse

## Quality checklist (self-review)

- Is the new dependency load-bearing or replaceable?
- Did the ADR list alternatives, or is it "we picked X"?
- Does the license stack with our existing ones?

## Related playbooks

- `soc2-gdpr-audit-prep`
- `weekly-architectural-review`
- `rfc-to-production-feature-delivery`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **new-dependency-risk-checklist** (tier `geek`, blocks stage 2) — Human review stage needs a written risk checklist (maintainer pulse, transitive deps, etc.)
- **load-bearing-dep-criteria** (tier `geek`, blocks stage 2) — ADR stage needs explicit criteria to identify load-bearing dependencies

## CLI usage

```
faion get-content security-review-new-dependency --format md       # human-readable rendering
faion get-content security-review-new-dependency --format context  # agent-optimised context bundle
faion get-content security-review-new-dependency --format json     # raw structured form
```
