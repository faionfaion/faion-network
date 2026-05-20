---
slug: sec-secrets-defense-in-depth
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Run two complementary secret scanners in two different lifecycle stages.
content_id: "8fe3a66a9b2dcb82"
tags: [secrets, security, gitleaks, trufflehog, pre-commit]
---
# Two-Layer Secret Scanning: Gitleaks + Verified TruffleHog

## Summary

**One-sentence:** Run two complementary secret scanners in two different lifecycle stages.

**One-paragraph:** Run two complementary secret scanners in two different lifecycle stages. Layer one is `gitleaks` as a pre-commit hook on the developer or agent machine: sub-second, regex-based, blocks the commit before any secret enters local git history. Layer two is `trufflehog --results=verified` in CI on every PR: it actively calls the issuing provider (AWS STS, GitHub, Stripe, Slack, OpenAI, Anthropic) to confirm the candidate token is live, and treats verified findings as P0 incidents that trigger immediate rotation before revert.

## Applies If (ALL must hold)

- Every repository, no exception — even single-developer prototypes, because a leaked AWS or OpenAI key costs more than the project earns.
- Repos where AI agents commit on behalf of humans — verified scanning is the only check that distinguishes a real `sk-ant-` token from a docstring example.
- Monorepos with mixed languages and config formats where naive pattern matchers miss provider-specific encodings (JWT, .pem, dotenv, terraform tfvars).
- Migrations of historical secrets — pair with `detect-secrets` baseline so that historical findings can be ratcheted out without blocking every PR.

## Skip If (ANY kills it)

- There is no NOT case for the two layers themselves; only the depth (1 layer vs 2) varies. A throwaway gist might run only gitleaks pre-commit and skip the CI verifier.
- Air-gapped repos with no network egress in CI — TruffleHog verification calls providers, which is impossible without egress; substitute provider-specific offline format checks.
- Generated code drops where every blob is regenerated from a private template store — scan the template store instead of the generated tree.

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
