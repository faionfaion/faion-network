# Security review for new dependency

## Context

Engineer wants to add a new lib / SDK. Before merge: AI runs SBOM diff, supply-chain scan, license check; security-conscious engineer reviews the diff + alternatives. Decision recorded as a lightweight ADR. Auto-applied for ultra-trivial bumps via Renovate handoff.

## Outcome

By the end of this playbook, the operator has run the 4 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 4 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Justify the Dependency

Why this one, why now.

Tasks:
- Document the use case and alternatives considered
- Confirm we can't build it cheaply in-house
- Note licence implications

Outputs:
- use-case + alternatives memo
- build-or-buy note
- licence note

Decision gate: Advance only when the justification is on paper.

### 2. Inspect the Package

Look before you import.

Tasks:
- Pin the version; review release notes and CHANGELOG
- Run SCA (e.g., Snyk / Trivy) for known CVEs
- Check maintainer activity and download trend

Outputs:
- pinned version
- SCA report
- maintainer activity notes

Decision gate: Advance only when no critical CVE is open and maintainer signal is healthy.

### 3. Sandbox & Surface Risk

What does it actually touch.

Tasks:
- Enumerate what it reads, writes, and sends over the network
- Check transitive deps for risky packages
- Run it in a sandboxed environment for behaviour

Outputs:
- surface enumeration
- transitive-dep review
- sandbox log

Decision gate: Advance only when surface is acceptable and behaviour is clean.

### 4. Decide & Document

Approve / reject with a written trail.

Tasks:
- Write the security review decision: approve / reject / approve-with-controls
- Add to the approved-deps registry with the trail
- Set the review cadence (e.g., quarterly)

Outputs:
- decision doc
- registry entry
- review cadence

Decision gate: Required output: a signed-off security decision in the registry.

## Decision points

- Stage 1 (Justify the Dependency): Advance only when the justification is on paper.
- Stage 2 (Inspect the Package): Advance only when no critical CVE is open and maintainer signal is healthy.
- Stage 3 (Sandbox & Surface Risk): Advance only when surface is acceptable and behaviour is clean.
- Stage 4 (Decide & Document): Required output: a signed-off security decision in the registry.

## References

- `gov-approval-token-signed-jwt`
- `gov-license-compliance-scan`
- `mr-renovate-ai-handoff`
- `sec-trivy-pinned-supply-chain-scan`
- `security-container-scanning`
- `security-supply-chain`
- `architecture-decision-records`
- `security-architecture`
- `architecture-decision-records`
- `architecture-decision-records`

Gaps (status: draft until empty):
- `new-dependency-risk-checklist` (see `gaps[]` in `playbook.yaml`)
- `load-bearing-dep-criteria` (see `gaps[]` in `playbook.yaml`)
