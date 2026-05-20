---
slug: ai-generated-code-compliance-validation
tier: pro
group: dev
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d5e4ce9c3273e68d"
summary: A fast validation pass that the senior dev runs on AI-generated diffs before they enter a client PR — catches violations of client coding standards, audit / compliance posture, license drift, and forbidden APIs.
tags: [compliance, outsource, ai-codegen, audit, senior-dev]
---
# AI-Generated Code Compliance Validation

## Summary

**One-sentence:** A fast, repeatable validation pass that a senior dev runs on AI-shipped code before opening a client PR, catching client-coding-standard violations, compliance-posture drift (SOC 2 / HIPAA / PCI / GDPR), license drift, and forbidden APIs.

**One-paragraph:** AI coding assistants generate code at high velocity but with high client-side variance — naming conventions, log shapes, error wrappers, retry policies, AGPL imports, regulated-data handling — that consistently violates the *specific* contract a client repo requires. This methodology gives the senior dev a 7-step validation pass: (1) ingest the client's coding-standard charter; (2) run a delta-scope filter (only AI-touched files); (3) lint against the client's profile, not the project default; (4) license / SBOM diff; (5) forbidden-API scan tied to the client's compliance posture; (6) secret + PII regex; (7) PR-comment composition with rationale and a recommendation per finding. Output: a per-PR validation report; the senior dev accepts findings, the AI output ships only after.

## Applies If (ALL must hold)

- Senior dev is doing outsourced work for a client (P4 outsource-specialist persona or peer).
- Client has a written coding-standard / compliance posture (SOC 2, HIPAA, PCI, GDPR, internal style guide).
- AI assistant (Claude Code, Cursor, Copilot, aider) authored or substantially modified the diff in question.
- A client PR will be opened against a client-controlled repo (not the dev's sandbox).

## Skip If (ANY kills it)

- Client has no documented coding standard — load `client-conventions-reverse-engineering` first to infer one.
- Internal sandbox project with no client review — overhead exceeds the win.
- Diff is a documentation / typo fix with no executable change — skip license + forbidden-API checks.
- Client repo already enforces all the relevant rules in CI (lint, license, secret scan all green) AND the senior dev has reviewed the CI matrix — minimal pass.

## Prerequisites

- The client's coding-standard charter as a checked-in file (or a faithful summary).
- A `forbidden-apis.yaml` per client capturing compliance-posture restrictions (e.g. no console.log to STDOUT in HIPAA; no `eval`; no unbounded `requests.get` without timeout).
- The client's allowed-license list as an SPDX expression.
- A diff of AI-generated changes scoped to the current branch.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/client-conventions-reverse-engineering` | If a charter is missing, this methodology produces one to validate against. |
| `geek/sdlc-ai/gov-license-compliance-scan` | License scan engine that validates SBOM diff. |
| `geek/sdlc-ai/sec-secrets-defense-in-depth` | Secret-scan rules consumed by step 6. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: charter immutability, delta-scope filter, client-profile lint, forbidden-API per posture, PR-comment rationale | ~1100 |
| `content/02-output-contract.xml` | essential | Validation-report schema, finding severity, recommendation rule | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: charter drift, false-positive rate, forbidden-API drift, license-list rot | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `charter-ingest-and-summarise` | sonnet | Bounded summarisation of the client charter |
| `delta-scope-and-lint` | haiku | Mechanical: filter, run lint, parse output |
| `compliance-posture-scan` | sonnet | Per-API judgement; bounded by `forbidden-apis.yaml` |
| `pr-comment-compose` | sonnet | Structured comment composition with rationale per finding |
| `escalation-decision` | opus | Cross-finding synthesis: should the senior dev pause and call the client lead |

## Templates

| File | Purpose |
|------|---------|
| `templates/validation-report.json` | JSON schema for the per-PR validation report |
| `templates/forbidden-apis.yaml` | Per-client list of forbidden APIs tied to compliance posture |
| `templates/pr-comment.md` | Reviewer-facing markdown template with findings and rationale |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scope-diff.sh` | Compute the AI-touched file set from branch diff | First step of the pass |
| `scripts/run-client-lint.sh` | Run the client-profile lint config across the scoped diff | After scope step |
| `scripts/sbom-diff.py` | Compare current SBOM to baseline; flag new dependencies | Before PR open |
| `scripts/forbidden-api-scan.py` | Match diff hunks against forbidden-apis.yaml | After lint |

## Related

- parent skill: `pro/dev/software-architect/`
- peer methodologies: `client-conventions-reverse-engineering`, `dependency-adoption-checklist`, `adr-staleness-audit`
- external: [SOC 2 Trust Services Criteria](https://www.aicpa-cima.com/) · [HIPAA Security Rule §164.312](https://www.hhs.gov/) · [SPDX license list](https://spdx.org/licenses/)
