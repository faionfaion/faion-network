---
slug: sec-secrets-defense-in-depth
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Two-layer secret scanning — gitleaks pre-commit (regex, sub-second, blocks commit) + TruffleHog --results=verified in CI (provider-verified, treats live tokens as P0 incidents).
content_id: "bb2bfe71cf6eb3f0"
complexity: medium
produces: config
est_tokens: 3400
tags: [secrets, security, gitleaks, trufflehog, pre-commit]
---
# Two-Layer Secret Scanning: Gitleaks + Verified TruffleHog

## Summary

**One-sentence:** Two-layer secret scanning — gitleaks pre-commit (regex, sub-second, blocks commit) + TruffleHog --results=verified in CI (provider-verified, treats live tokens as P0 incidents).

**One-paragraph:** Single-layer secret scanning either blocks too aggressively (developers disable it) or misses verified live tokens (regex false negatives). This methodology produces a two-layer config: gitleaks runs sub-second pre-commit on the developer or agent machine and blocks the commit before any secret enters local git history; TruffleHog runs in CI with `--results=verified` to actively call providers (AWS STS, GitHub, Stripe, Slack, OpenAI, Anthropic) confirming the token is live. Verified findings trigger immediate rotation + revert.

**Ефективно для:**

- Будь-який repo (single-dev або team) — leaked AWS/OpenAI key коштує більше за project.
- Repo, де AI agents коммітять від імені людей — verified scan відрізняє sk-ant-... від example в docstring.
- Monorepo з mixed languages (JWT/.pem/dotenv/tfvars) — pattern matchers пропускають.
- Migration з legacy git history — `detect-secrets` baseline + ratchet.

## Applies If (ALL must hold)

- Repo exists in any form (single-dev prototype counts — leaked key is the same cost).
- Repo has any code, config, or commit (not pure binary asset mirror).
- CI runner has outbound network egress (TruffleHog verification calls providers).
- Team accepts blocking commits on regex match + blocking PRs on verified findings.

## Skip If (ANY kills it)

- Air-gapped CI without network egress — substitute provider-specific offline format checks.
- Generated-code drops where every blob is regenerated from a private template store — scan the template store instead.
- Vendored read-only mirror with no commit pipeline.
- Pre-prod prototype where speed of iteration matters more than risk (rare; revisit weekly).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pre-commit framework | pre-commit / lefthook / husky | lead |
| Gitleaks binary | installed locally + in CI | platform |
| TruffleHog action | aquasecurity-style GH action | platform |
| Outbound network | egress from CI | sec |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[lint-precommit-floor]] | The pre-commit framework that gitleaks lives in. |
| [[sec-codeql-autofix-on-pr]] | Complementary SAST layer. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 500 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `precommit_wire` | haiku | Boilerplate hook config. |
| `ci_wire` | haiku | Boilerplate GitHub Actions. |
| `incident_response` | sonnet | Verified-finding triage requires judgement (rotate vs revert vs both). |

## Templates

| File | Purpose |
|------|---------|
| `templates/precommit-secrets.yaml` | pre-commit framework hooks section for gitleaks. |
| `templates/trufflehog-action.yml` | GitHub Actions workflow with --results=verified. |
| `templates/gitleaks.toml` | gitleaks config with org-specific allowlist. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sec-secrets-defense-in-depth.py` | Validate produced two-layer config artefact. | Pre-merge of pre-commit + workflow |

## Related

- [[lint-precommit-floor]]
- [[sec-codeql-autofix-on-pr]]
- [[sec-trivy-pinned-supply-chain-scan]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (CI egress available? pre-commit installed?) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure how many layers to ship — the tree terminates either on the active rule or on `skip-this-methodology`.
