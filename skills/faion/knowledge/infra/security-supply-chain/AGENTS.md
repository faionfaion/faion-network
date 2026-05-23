# Supply Chain Security: Secrets, SCA, SBOM, SLSA

## Summary

**One-sentence:** Produces a supply-chain config bundle (pre-commit + CI hooks, SBOM gen, license policy) plus a fix-PR workflow for known-vulnerable dependencies.

**One-paragraph:** Supply-chain attacks target dependencies, build tooling, and secrets in CI rather than the application code itself. Defend with: secret scanning on every commit and full history in CI (Gitleaks / detect-secrets); SCA (Software Composition Analysis) for dependency CVEs; SBOM generation per build; lock files for all dependency manifests; SLSA provenance attestation. Automate dependency updates with Dependabot or Renovate with a capped auto-merge policy. License policy defaults to deny with an explicit allowlist.

**Ефективно для:**

- будь-який проєкт із external dependencies — SCA є minimum viable supply-chain control.
- репо, де developers випадково commit secrets — pre-commit + CI secret scanning є non-negotiable.
- проєкти, що ship artifacts externally або в regulated industries — SBOM + SLSA стають обов'язковими.
- standing up 'security PR bot' що auto-opens fix PRs для known-vulnerable dependencies.

## Applies If (ALL must hold)

- Project has external dependencies (any language: pip / npm / cargo / gomod / maven).
- CI system runs on every push (GitHub Actions, GitLab CI, Buildkite, or equivalent).
- Secrets store is configured for the runtime (Vault, AWS Secrets Manager, GCP Secret Manager).
- Team will respond to security PR bot output rather than auto-ignoring it.

## Skip If (ANY kills it)

- Replacing code review for novel dependency selection — SCA catches known CVEs, not design choices like overly broad transitive dependency trees.
- Auto-merging dependency updates that include major version bumps — require human review for breaking changes even if CI passes.
- One-off scripts with no external dependencies — overhead exceeds value.
- Team has no security incident response path — adding more findings without a triage workflow is worse than skipping.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI workflow file | YAML | platform team |
| Pre-commit config | YAML | repo root |
| Dependency manifests + lock files | committed | repo |
| Secrets store credentials | env / OIDC | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer/secrets-management` | secrets backend assumed |
| `pro/infra/cicd-engineer` | parent group context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-deps` | haiku | Read manifests + lock files |
| `compose-scan-config` | sonnet | Wire Gitleaks + SCA + SBOM + license-allowlist |
| `policy-review` | opus | Cross-tool consistency + escalation matrix |

## Templates

| File | Purpose |
|------|---------|
| `templates/pre-commit-config.yaml` | Pre-commit hooks for Gitleaks + dependency lock check |
| `templates/sbom-config.yaml` | Syft / Trivy SBOM generation config |
| `templates/skeleton.json` | JSON schema for the supply-chain config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-security-supply-chain.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[secrets-management]]
- [[cve-exception-template]]
- [[security-as-code]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Supply Chain Security: Secrets, SCA, SBOM, SLSA methodology when in doubt about scope or fit.
