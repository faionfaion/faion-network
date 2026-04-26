# Agent Integration — Security Architecture

## When to use
- Designing authentication, authorization, and identity flows for a new product or new tenant model.
- Threat modeling a new feature, integration, or third-party dependency before code freeze.
- Compliance-driven design (SOC 2, HIPAA, GDPR, PCI-DSS, ISO 27001) that requires documented controls and evidence.
- Reviewing existing architecture for Zero Trust gaps, secret-handling failures, or perimeter-only assumptions.
- Hardening an LLM-augmented system — prompt-injection surface, tool-permission scope, exfiltration paths.

## When NOT to use
- Fixing a single CVE in a dependency — use SCA tooling, not a full architecture loop.
- Pure secret rotation operational tasks — use Vault/KMS runbooks.
- UI form validation hygiene only — covered by application-developer methodologies.

## Where it fails / limitations
- LLMs hallucinate plausible-looking auth flows; OAuth/OIDC details (PKCE, audience, JWKS rotation) are frequently wrong. Pin to RFCs and provider docs.
- Threat models become checkbox theatre if no adversary persona is named — agents will list every CWE without prioritization.
- Zero Trust architectures are expensive to retrofit; agents under-cost the migration of legacy services.
- "Encrypt everything" is the LLM default; without classification it produces operational pain (key management, recovery) without a real risk reduction.
- Compliance prompts encourage copy-paste boilerplate that doesn't match the real system; require evidence anchors.

## Agentic workflow
Run a STRIDE threat-modeling agent over a system diagram (C4 L2/L3), an OWASP/CWE mapper agent that proposes controls, a code-side reviewer agent that validates the controls actually exist in the repo, and a critic that argues for the *attacker*. Always keep human approval at policy boundaries: identity, key management, network egress, third-party data sharing. Persist threat-model output in `docs/security/threats/<feature>.md` so the next iteration starts from the prior model.

### Recommended subagents
- `faion-brainstorm` — diverge over auth/authz options (RBAC vs ABAC vs ReBAC, OIDC vs custom JWT).
- `faion-sdd-execution` — turn chosen approach into spec/design/test-plan with explicit security acceptance criteria.
- `password-scrubber-agent` — sweep diffs/branches for leaked secrets pre-commit.
- `faion-improver` — quarterly Zero Trust posture audit against the latest design.

### Prompt pattern
```
ROLE: STRIDE threat modeler
INPUT: C4 L2 diagram + data classification table.
TASK: For each component and trust boundary, list threats per STRIDE category.
Score with DREAD (1-10 each). Produce a top-10 ranked list with concrete
mitigations citing OWASP/NIST controls. Reject mitigations that are not
verifiable in code or infra.
```

```
ROLE: red-team critic
TASK: Given the proposed auth design, attempt three concrete attacks:
(1) account takeover via auth flow abuse,
(2) privilege escalation via authz bypass,
(3) data exfiltration via tool/MCP abuse (if LLM agent).
For each: precondition, exploit steps, detection signal.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| trivy | Container/IaC/SBOM vulnerability scan | https://aquasecurity.github.io/trivy/ |
| grype + syft | SBOM + vulnerabilities | https://github.com/anchore/grype |
| semgrep | SAST for code-level controls | https://semgrep.dev/ |
| gitleaks / trufflehog | Secret scanning | https://github.com/gitleaks/gitleaks |
| zap-baseline | OWASP ZAP CI scan | https://www.zaproxy.org/ |
| nuclei | Templated DAST | https://github.com/projectdiscovery/nuclei |
| checkov / tfsec / kics | IaC security policy | https://www.checkov.io/ |
| openssl s_client | TLS posture inspection | bundled |
| step-cli | mTLS/PKI bootstrap | https://smallstep.com/cli/ |
| kubescape / kube-bench | K8s CIS/NSA hardening | https://kubescape.io/ |
| fido2-tools / yubikey-manager | Passkey/FIDO2 testing | per-vendor |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Auth0 / Okta / Stytch / Clerk / WorkOS | SaaS | Yes | Modern OIDC + passkeys; agent-drivable APIs |
| Keycloak / Authentik / Zitadel / Authelia | OSS | Yes | Self-hosted IdP |
| HashiCorp Vault / OpenBao | OSS+SaaS | Yes | Secrets, dynamic creds, transit encryption |
| Doppler / Infisical / 1Password | SaaS | Yes | Secrets sync; CI-friendly |
| Cloudflare Zero Trust / Tailscale / Pomerium / Teleport | SaaS+OSS | Yes | ZTNA replacing VPNs |
| OPA / OpenFGA / Cedar | OSS | Yes | Policy-as-code authz; agent can author Rego/Cedar |
| AWS IAM Identity Center / Azure Entra ID / Google Cloud Identity | SaaS | Yes | Cloud IdP; STS for ephemeral creds |
| Snyk / GitHub Advanced Security / Dependabot | SaaS | Yes | SAST + SCA in PRs |

## Templates & scripts
See `templates.md` for OAuth, Vault, Istio mTLS, K8s NetworkPolicy templates. Inline secret-scan + denylist script for pre-commit:

```bash
#!/usr/bin/env bash
# secret-guard.sh — block obvious secret regexes; enforce gitleaks pass.
set -euo pipefail
PATTERN='(AKIA[0-9A-Z]{16}|aws_secret_access_key|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]+|-----BEGIN (RSA |EC )?PRIVATE KEY-----|sk-[A-Za-z0-9]{20,})'
if git diff --cached -U0 | grep -E "$PATTERN" > /dev/null; then
  echo "secret-guard: matched secret regex; aborting." >&2
  git diff --cached -U0 | grep -nE "$PATTERN" >&2 || true
  exit 1
fi
if command -v gitleaks > /dev/null 2>&1; then
  gitleaks protect --staged --redact -v
fi
```

## Best practices
- Always start with data classification (public / internal / confidential / regulated). Every control is justified by what data it protects.
- Prefer passkeys/FIDO2 + OIDC over passwords; deny legacy auth (basic, NTLM) at the gateway.
- Use short-lived credentials everywhere — STS, cert-rotation via SPIFFE/SPIRE, KMS-backed keys with TTL.
- Enforce least privilege via policy-as-code (OPA/Cedar/OpenFGA), tested with golden cases in CI.
- Treat the LLM agent as an untrusted insider: scope its tools narrowly, log every tool call, require human-in-loop for destructive or cross-boundary actions.
- Keep ADRs for every authn/authz decision; security deltas without ADRs are red flags.
- Rotate secrets via process, not policy; drill the rotation quarterly.

## AI-agent gotchas
- LLM-generated JWT validation often skips audience/issuer checks; require explicit `aud`/`iss`/`exp` validation in templates and tests.
- Agents add CORS `*` "to fix the error" — require a wildcard-ban check in CI.
- Prompt injection: any agent that ingests untrusted text must operate with reduced tool scope; agents that write code from external tickets are at high risk.
- Threat-model outputs from LLMs uniformly score "medium/medium" — force differentiation and require a top-N cutoff.
- Agents pull example secrets ("changeme", "password123") into configs — secret scanning at commit and pre-deploy is mandatory.
- Human-in-loop gates: identity provider config changes, IAM policy diffs, public surface (egress firewall, public bucket, new third-party integration), key/secret rotation.

## References
- https://owasp.org/www-project-top-ten/
- https://owasp.org/www-project-application-security-verification-standard/
- https://csrc.nist.gov/publications/detail/sp/800-207/final
- https://csrc.nist.gov/publications/detail/sp/1800-35/final
- https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics
- https://fidoalliance.org/specs/
- https://www.cisa.gov/zero-trust-maturity-model
- https://github.com/OWASP/CheatSheetSeries
