# Security as Code Checklist

## Policy as Code Implementation

### Foundation

- [ ] Select policy engine (OPA/Gatekeeper vs Kyverno)
- [ ] Set up policy repository with version control
- [ ] Define policy naming conventions
- [ ] Establish policy review process (PR-based)
- [ ] Configure policy testing framework

### OPA/Gatekeeper Setup

- [ ] Install Gatekeeper in Kubernetes cluster
- [ ] Create ConstraintTemplate CRDs
- [ ] Define Constraint resources
- [ ] Enable audit mode for existing resources
- [ ] Configure enforcement mode for new resources
- [ ] Set up policy violation alerts

### Kyverno Setup

- [ ] Install Kyverno in Kubernetes cluster
- [ ] Create ClusterPolicy resources
- [ ] Configure validate/mutate/generate rules
- [ ] Enable policy reporting
- [ ] Set up admission webhook exceptions

### Terraform Policy

- [ ] Choose policy tool (Sentinel, OPA, Checkov)
- [ ] Create policies for:
  - [ ] Resource tagging requirements
  - [ ] Encryption at rest
  - [ ] Network security (no public IPs)
  - [ ] IAM least privilege
  - [ ] Cost controls (instance sizes)
- [ ] Integrate with CI/CD pipeline
- [ ] Configure `terraform plan` policy checks

## Vulnerability Scanning

### Container Scanning

- [ ] Install Trivy or equivalent scanner
- [ ] Configure base image scanning
- [ ] Set up application dependency scanning
- [ ] Define severity thresholds (CRITICAL, HIGH)
- [ ] Create exception/allow-list process
- [ ] Integrate with container registry

### IaC Scanning

- [ ] Install Checkov or tfsec
- [ ] Scan Terraform/Pulumi configurations
- [ ] Scan Kubernetes manifests/Helm charts
- [ ] Scan Dockerfiles
- [ ] Configure custom rules for organization
- [ ] Set up baseline for existing violations

### CI/CD Integration

- [ ] Add scanning to PR checks
- [ ] Configure fail conditions (severity levels)
- [ ] Set up SARIF reporting
- [ ] Integrate with GitHub Security tab
- [ ] Configure Dependabot/Renovate for dependencies
- [ ] Add SAST scanning (SonarQube, Semgrep)

### Runtime Scanning

- [ ] Set up continuous cluster scanning
- [ ] Configure scheduled image scans
- [ ] Enable admission controller scanning
- [ ] Set up vulnerability notifications
- [ ] Create remediation SLAs by severity

## Compliance Automation

### Framework Selection

- [ ] Identify compliance requirements (SOC2, HIPAA, PCI-DSS, GDPR)
- [ ] Choose compliance tool (InSpec, Drata, Vanta)
- [ ] Map controls to technical requirements
- [ ] Create compliance-as-code profiles

### Chef InSpec Setup

- [ ] Install InSpec
- [ ] Select relevant CIS benchmarks
- [ ] Customize profiles for environment
- [ ] Set up scheduled compliance scans
- [ ] Configure reporting dashboard
- [ ] Create remediation playbooks

### Continuous Compliance

- [ ] Automate evidence collection
- [ ] Set up compliance drift detection
- [ ] Configure compliance violation alerts
- [ ] Create audit-ready reports
- [ ] Establish compliance review cadence

## Supply Chain Security

### SBOM (Software Bill of Materials)

- [ ] Generate SBOMs for all containers
- [ ] Store SBOMs in artifact registry
- [ ] Set up SBOM vulnerability monitoring
- [ ] Define SBOM update process

### Artifact Signing

- [ ] Set up Sigstore/Cosign
- [ ] Configure image signing in CI/CD
- [ ] Enable signature verification on deployment
- [ ] Establish key management process

### SLSA (Supply-chain Levels for Software Artifacts)

- [ ] Assess current SLSA level
- [ ] Implement build provenance
- [ ] Configure hermetic builds
- [ ] Enable artifact attestation

## Operational Security

### Secrets Management

- [ ] Select secrets manager (Vault, AWS Secrets Manager)
- [ ] Migrate hardcoded secrets
- [ ] Set up secret rotation
- [ ] Configure dynamic secrets where possible
- [ ] Enable secret scanning in repos

### Network Security

- [ ] Define network policies
- [ ] Implement Zero Trust networking
- [ ] Configure service mesh (Istio, Linkerd)
- [ ] Enable mTLS between services
- [ ] Set up network policy enforcement

### Monitoring & Alerting

- [ ] Configure security event logging
- [ ] Set up SIEM integration
- [ ] Create security dashboards
- [ ] Define incident response playbooks
- [ ] Enable runtime threat detection

## Governance

### Documentation

- [ ] Document all security policies
- [ ] Create policy exception process
- [ ] Establish security review guidelines
- [ ] Define security metrics/KPIs

### Training

- [ ] Train developers on secure coding
- [ ] Train ops on security tools
- [ ] Conduct regular security awareness
- [ ] Run tabletop exercises

### Review Cadence

- [ ] Weekly: Review new vulnerabilities
- [ ] Monthly: Audit policy violations
- [ ] Quarterly: Compliance review
- [ ] Annually: Full security assessment
