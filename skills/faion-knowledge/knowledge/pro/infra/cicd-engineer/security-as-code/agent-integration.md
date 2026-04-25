# Agent Integration — Security as Code (DevSecOps)

## When to use
- Wiring SAST, SCA, secret scanning, container scanning, IaC scanning, and DAST into a CI/CD pipeline as enforceable gates.
- Generating an SBOM (CycloneDX or SPDX) per build and tracking dependencies/vulns over time.
- Codifying compliance/admission policies (Kyverno, OPA Gatekeeper, Conftest) in Git and enforcing on every cluster apply.
- Standing up a "security PR bot" that auto-opens fixes for known-vulnerable dependencies.
- Running runtime threat detection and feeding findings back into the pipeline as policy.

## When NOT to use
- Greenfield exploration where requirements are still fluid — false-positive volume will drown the team.
- Pen-testing engagements — hire humans, don't auto-DAST a live target without scope.
- One-off scripts / scratch repos — overhead exceeds value.
- Replacing security review for novel architectures — automation catches known patterns, not design flaws.
- Compliance audits that require human attestation — automation is evidence, not the auditor.

## Where it fails / limitations
- Signal-to-noise: SAST/DAST emit thousands of findings; without triage rules and severity gating the team ignores them all.
- Vulnerability data lag: NVD and OSV databases lag, especially for ecosystem-specific advisories; relying on a single source misses things.
- License compliance is half-known: SCA tools struggle with vendored or unknown-license code.
- Container scanners flag base-image CVEs the app doesn't actually use; reachability analysis (Snyk, Endor Labs) reduces this but isn't perfect.
- Policy-as-code drift: policies authored at platform team level become out of sync with what app teams actually deploy; need contract-test approach.
- Secret scanners miss bespoke patterns and re-flag rotated secrets endlessly.
- AI-driven autofix PRs sometimes "fix" by changing test expectations rather than the code; review required.

## Agentic workflow
Treat security-as-code as a graph: source → build → image → cluster → runtime, each with its scanner and a policy gate. Agents add value at three points: (1) authoring the pipeline (CI YAML, policy CRDs); (2) triage — converting raw scanner JSON into actionable diffs with reachability/exploitability evidence; (3) autofix PRs gated on test pass + human approval. Never auto-merge security fixes; always require human review even when CI is green. Pin tool versions and rule packs — silent rule-pack updates create flaky CI.

### Recommended subagents
- `faion-sdd-executor-agent` — implement scanner integration with quality gates and review.
- `password-scrubber-agent` — sanitize secret-scanner false positives before logging.
- Custom `vuln-triage-agent` — reads SBOM + scanner JSON + repo manifests, returns prioritized list with reachability assessment.
- Custom `policy-author` — generates Kyverno/OPA rules from a plain-English security requirement and unit tests for the rule.
- Custom `dep-fix-bot` — opens single-purpose PRs upgrading vulnerable dependencies, runs full test suite before requesting review.

### Prompt pattern
"You are a vuln-triage agent. Input: Trivy JSON + the project's `package.json`/`go.mod`. For each CVE: (1) severity, (2) is the vulnerable function reachable from the app's entry points (yes/no/unknown), (3) recommended action (`upgrade`, `pin`, `accept-risk`, `replace`). Return JSON sorted by severity then reachability. Refuse to mark any CRITICAL as `accept-risk`."

"You are a Kyverno policy author. Requirement: 'no container may run as root or with privilege escalation; images must come from `ghcr.io/our-org/*` or `gcr.io/distroless/*`'. Output a `ClusterPolicy` with `validate` rules and a sample `kyverno test` directory with allow/deny fixtures."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `semgrep` | Pattern-based SAST, custom rules | https://semgrep.dev/docs/ |
| `codeql` | Semantic SAST (GitHub) | https://codeql.github.com/ |
| `bandit` (Python), `gosec` (Go), `brakeman` (Rails) | Language SAST | per-language docs |
| `trivy` | All-in-one: container, IaC, secret, SBOM | https://trivy.dev/ |
| `grype` + `syft` | SBOM + vuln scanning | https://github.com/anchore/grype |
| `snyk` CLI | SCA + container + IaC | https://docs.snyk.io/ |
| `gitleaks` / `trufflehog` | Secret scanning | https://github.com/gitleaks/gitleaks |
| `tfsec` / `checkov` / `kics` / `terrascan` | IaC scanning | https://github.com/aquasecurity/tfsec |
| `kubeaudit` / `kubescape` / `kube-bench` | K8s posture | https://github.com/kubescape/kubescape |
| `conftest` | Rego policy testing | https://www.conftest.dev/ |
| `kyverno` CLI | Kyverno policy testing | https://kyverno.io/docs/kyverno-cli/ |
| `cosign` | Image signing/verification (Sigstore) | https://docs.sigstore.dev/cosign/overview/ |
| `nuclei` | DAST templates / vuln scanner | https://docs.projectdiscovery.io/tools/nuclei |
| `zap` (OWASP ZAP) | DAST | https://www.zaproxy.org/ |
| `falco` | Runtime threat detection | https://falco.org/ |
| `vulncheck` / `osv-scanner` | OSV-backed SCA | https://google.github.io/osv-scanner/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Snyk | SaaS | Yes — API + CLI | Strong autofix PRs; license risk on free tier scale |
| GitHub Advanced Security (CodeQL, Dependabot, secret scan) | SaaS | Yes — API | Native if already on GitHub |
| GitLab Ultimate (SAST/DAST/Container/Secret) | SaaS | Yes — pipeline templates | Native if on GitLab |
| Sonatype Nexus IQ / Lifecycle | SaaS | Yes — API | Strong policy + waiver workflow |
| JFrog Xray | SaaS | Yes — API | Deep Artifactory integration |
| Wiz / Orca / Lacework / Aqua / Sysdig | SaaS CNAPP | Yes — API | Cloud + container + runtime |
| Aqua Trivy + Tracee | OSS | Yes | Self-hosted scanner + runtime |
| OPA / Gatekeeper / Kyverno | OSS | Yes — CRDs | K8s policy enforcement |
| Sigstore (cosign + Rekor + Fulcio) | OSS | Yes — CLI/API | Signing + transparency log |
| Endor Labs / Phylum | SaaS | Yes — API | Reachability-aware SCA |
| Semgrep AppSec Platform | SaaS | Yes — API | Hosted Semgrep with rule management |
| Tenable.io / Qualys VMDR | SaaS | Yes — API | Network/host vuln scanning |

## Templates & scripts
See `templates.md` for GitHub Actions / GitLab CI / Jenkins pipelines. Inline minimal pipeline gate:

```yaml
# .github/workflows/security-gate.yml
name: security-gate
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    permissions: { contents: read, security-events: write, pull-requests: write }
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with: { config: p/ci, generateSarif: "1" }
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          scanners: vuln,secret,misconfig
          severity: CRITICAL,HIGH
          exit-code: "1"
          format: sarif
          output: trivy.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: trivy.sarif }
      - name: SBOM
        uses: anchore/sbom-action@v0
        with: { format: cyclonedx-json, output-file: sbom.cdx.json }
      - uses: actions/upload-artifact@v4
        with: { name: sbom, path: sbom.cdx.json }
```

## Best practices
- Block on CRITICAL+HIGH only at first; expose MEDIUM/LOW as informational. Tighten over time.
- Pin scanner image digests and rule-pack versions; bump on a schedule, not silently.
- Reachability-aware SCA (Endor, Snyk Reachability, Semgrep) reduces false positives 70-90% for libraries.
- Sign every image with Sigstore `cosign`; verify in admission controller (Kyverno `verifyImages`).
- Generate an SBOM (CycloneDX) per build, store as immutable artifact, attach to release.
- Secret scanning on every commit + history rewrite when leaks land in `main`.
- IaC scanning (`tfsec`/`checkov`) before plan; treat policy violations as compile errors.
- Policy-as-code unit tests: `conftest verify` / `kyverno test` runs in CI alongside app tests.
- Runtime detection (Falco/Tracee) feeds SIEM; tune to baseline before alerting.
- Maintain an exception register with expiry; no permanent waivers.
- License policy: deny by default; allowlist a known-good set (MIT, Apache-2.0, BSD-3-Clause, MPL-2.0).

## AI-agent gotchas
- Auto-fix bots regress functionality: they upgrade a transitive dep across a major version and break the build silently — require full test pass and human review.
- Severity inflation: CVSS scores often overestimate real risk; agents that gate on CVSS alone block trivial PRs.
- Secret scanner false positives: high-entropy strings flagged as keys; agents need to whitelist patterns explicitly, not pattern-disable globally.
- Policy author hallucinations: LLM emits Kyverno that uses fields that don't exist or wrong API version; require `kyverno test` in CI.
- Prompt injection via dependency README: an attacker-controlled README can change LLM behavior during scan triage; fence inputs.
- Container CVE noise: agents recommend "upgrade base image" without checking the upstream maintainers haven't shipped a fix yet — verify availability first.
- DAST against prod: agents that "just probe a few URLs" can trip rate limits, alarms, or even compliance violations; always scope to staging.
- SBOM format mixing: CycloneDX vs SPDX — pick one and stick to it; tools downstream are picky.
- Signing key handling: cosign keys committed to repo by accident — use keyless OIDC signing in CI.

## References
- OWASP DevSecOps Maturity Model: https://owasp.org/www-project-devsecops-maturity-model/
- Sigstore: https://www.sigstore.dev/
- CycloneDX SBOM spec: https://cyclonedx.org/
- SLSA supply-chain levels: https://slsa.dev/
- OPA / Gatekeeper: https://www.openpolicyagent.org/docs/
- Kyverno: https://kyverno.io/
- Trivy: https://trivy.dev/
- Semgrep: https://semgrep.dev/
- OSV.dev: https://osv.dev/
- NIST SSDF: https://csrc.nist.gov/Projects/ssdf
