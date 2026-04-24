# Security as Code Checklist

## Pre-Implementation

- [ ] Inventory all applications and their tech stacks
- [ ] Identify compliance requirements (SOC2, HIPAA, PCI-DSS, etc.)
- [ ] Define security severity thresholds (Critical, High, Medium, Low)
- [ ] Choose tooling based on team expertise and budget
- [ ] Establish security champions in development teams

## SAST Implementation

### Tool Selection

- [ ] Evaluate tools for your language stack:
  - [ ] CodeQL (GitHub repos)
  - [ ] Semgrep (custom rules needed)
  - [ ] Snyk Code (open-source heavy)
  - [ ] SonarQube (code quality + security)

### Integration

- [ ] Configure IDE integration for immediate feedback
- [ ] Add SAST to pre-commit hooks (optional, may slow commits)
- [ ] Integrate into CI pipeline (PR checks)
- [ ] Configure severity thresholds for blocking
- [ ] Set up baseline to ignore existing issues (temporarily)
- [ ] Document custom rules and exceptions

### Maintenance

- [ ] Review and update custom rules quarterly
- [ ] Track false positive rate and tune rules
- [ ] Monitor scan performance and optimize
- [ ] Keep scanner versions updated

## DAST Implementation

### Tool Selection

- [ ] Choose based on needs:
  - [ ] OWASP ZAP (free, good for automation)
  - [ ] Nuclei (template-based, CI-friendly)
  - [ ] Burp Suite (deep testing, commercial)

### Integration

- [ ] Set up test environment for DAST scans
- [ ] Configure authentication for authenticated scans
- [ ] Define scan scope (exclude third-party, test data endpoints)
- [ ] Integrate into staging deployment pipeline
- [ ] Set up scheduled scans for continuous monitoring
- [ ] Configure alerting for new vulnerabilities

### Maintenance

- [ ] Update scan templates/rules regularly
- [ ] Review and triage findings weekly
- [ ] Track remediation SLAs
- [ ] Test scanner against known vulnerabilities

## Container Scanning

### Tool Selection

- [ ] Choose scanner:
  - [ ] Trivy (comprehensive, fast)
  - [ ] Grype (focused, SBOM-friendly)
  - [ ] Clair (registry integration)

### Integration

- [ ] Scan during image build (CI pipeline)
- [ ] Configure registry scanning (pre-deployment gate)
- [ ] Set vulnerability thresholds (block Critical/High)
- [ ] Generate and store SBOMs
- [ ] Configure base image updates automation
- [ ] Set up runtime scanning (if needed)

### Maintenance

- [ ] Update vulnerability databases regularly
- [ ] Monitor for new CVEs in production images
- [ ] Track base image age and plan updates
- [ ] Review and update ignore lists quarterly

## Policy as Code

### Tool Selection

- [ ] Choose policy engine:
  - [ ] OPA/Gatekeeper (complex policies, multi-system)
  - [ ] Kyverno (Kubernetes-native, YAML)

### Core Policies

- [ ] **Resource Limits**
  - [ ] CPU/memory limits required
  - [ ] No unlimited resource requests

- [ ] **Security Context**
  - [ ] No privileged containers
  - [ ] No root user (runAsNonRoot: true)
  - [ ] Read-only root filesystem
  - [ ] Drop all capabilities, add only needed

- [ ] **Networking**
  - [ ] Network policies required
  - [ ] No hostNetwork: true
  - [ ] No hostPort usage

- [ ] **Images**
  - [ ] Trusted registries only
  - [ ] No latest tag
  - [ ] Image digest pinning (optional)

- [ ] **Secrets**
  - [ ] No secrets in env vars (use mounted secrets)
  - [ ] External secrets operator integration

### Integration

- [ ] Deploy policy engine to cluster
- [ ] Start in audit mode (warn, don't block)
- [ ] Review violations and fix existing resources
- [ ] Gradually enable enforcement
- [ ] Document all policies with examples
- [ ] Version control all policies

### Maintenance

- [ ] Review policy violations weekly
- [ ] Update policies based on new threats
- [ ] Test policies in staging before production
- [ ] Conduct policy audits quarterly

## Secrets Management

- [ ] No secrets in source code
- [ ] Use secrets scanner (GitLeaks, TruffleHog, detect-secrets)
- [ ] Pre-commit hooks for secrets detection
- [ ] CI pipeline secrets scanning
- [ ] External secrets management (Vault, AWS Secrets Manager)
- [ ] Rotate secrets regularly
- [ ] Audit secrets access

## Supply Chain Security

- [ ] Software Composition Analysis (SCA) in CI
- [ ] Dependency vulnerability monitoring
- [ ] Automated dependency updates (Dependabot, Renovate)
- [ ] SBOM generation and storage
- [ ] Artifact signing (Sigstore, Cosign)
- [ ] Provenance attestation (SLSA)
- [ ] Lock file usage for dependencies

## Monitoring and Response

- [ ] Centralize security findings (SIEM, security dashboard)
- [ ] Define severity-based SLAs for remediation
- [ ] Automated ticket creation for findings
- [ ] Security metrics dashboard (MTTR, vulnerability trends)
- [ ] Incident response runbooks
- [ ] Regular security review meetings

## Compliance Automation

- [ ] Map controls to compliance frameworks
- [ ] Automate compliance evidence collection
- [ ] Generate compliance reports
- [ ] Maintain audit trail
- [ ] Regular compliance gap analysis

## Maturity Levels

### Level 1: Foundation

- [ ] SAST in CI (block on Critical)
- [ ] Container scanning (block on Critical)
- [ ] Secrets scanning pre-commit
- [ ] Basic dependency scanning

### Level 2: Intermediate

- [ ] SAST + DAST coverage
- [ ] Container scanning with SBOM
- [ ] Policy as Code (audit mode)
- [ ] Automated dependency updates
- [ ] Security dashboard

### Level 3: Advanced

- [ ] Full pipeline security gates
- [ ] Policy as Code (enforcement)
- [ ] Runtime security monitoring
- [ ] Supply chain signing
- [ ] Automated remediation
- [ ] SLSA Level 2+ compliance

### Level 4: Optimized

- [ ] AI-assisted vulnerability triage
- [ ] Predictive security analytics
- [ ] Auto-healing security issues
- [ ] Full SLSA Level 3 compliance
- [ ] Continuous compliance automation
