# Security as Code LLM Prompts

## Policy Generation

### OPA Rego Policy Generation

```
Generate an OPA Gatekeeper ConstraintTemplate and Constraint for the following requirement:

Requirement: [DESCRIBE POLICY REQUIREMENT]

Context:
- Kubernetes version: 1.28+
- Gatekeeper version: 3.14+
- Enforcement: [deny/dryrun/warn]
- Namespaces to exclude: [kube-system, gatekeeper-system]

Output:
1. ConstraintTemplate YAML with Rego policy
2. Constraint YAML with configuration
3. Test cases (valid and invalid resources)
4. Documentation comments explaining the policy logic
```

### Kyverno Policy Generation

```
Generate a Kyverno ClusterPolicy for the following security requirement:

Requirement: [DESCRIBE POLICY REQUIREMENT]

Policy type: [validate/mutate/generate/verifyImages]
Action on failure: [Enforce/Audit]
Background scan: [true/false]

Include:
1. Complete ClusterPolicy YAML
2. Kyverno annotations (title, category, severity)
3. Example resources that pass/fail
4. Message explaining violation
```

### Terraform Policy Generation

```
Generate OPA/Rego policies for Terraform plan validation:

Requirements:
1. [REQUIREMENT 1]
2. [REQUIREMENT 2]
3. [REQUIREMENT 3]

Target resources: [aws_instance, aws_s3_bucket, etc.]
Output format: Rego policy with deny rules
Include: Unit tests using OPA test framework
```

## Vulnerability Analysis

### Trivy Results Analysis

```
Analyze the following Trivy vulnerability scan results and provide:

1. Risk assessment (Critical/High/Medium/Low)
2. Prioritized remediation plan
3. Specific fix recommendations for each vulnerability
4. Estimated effort for remediation
5. Temporary mitigations if immediate fix not possible

Trivy output:
[PASTE TRIVY SCAN RESULTS]
```

### SBOM Vulnerability Assessment

```
Review this Software Bill of Materials (SBOM) and identify:

1. Dependencies with known vulnerabilities
2. Outdated packages requiring updates
3. License compliance issues
4. Supply chain risks
5. Recommendations for dependency management

SBOM (SPDX/CycloneDX format):
[PASTE SBOM CONTENT]
```

### Container Image Hardening

```
Analyze this Dockerfile and provide security hardening recommendations:

Dockerfile:
[PASTE DOCKERFILE]

Evaluate:
1. Base image security (is it minimal/distroless?)
2. User privileges (running as root?)
3. Secrets handling (hardcoded values?)
4. Multi-stage build optimization
5. Security scanning integration
6. Runtime security context

Output:
- Hardened Dockerfile
- Explanation of changes
- Additional security measures
```

## Compliance Automation

### Chef InSpec Profile Generation

```
Generate a Chef InSpec compliance profile for:

Standard: [CIS Benchmark / SOC2 / HIPAA / PCI-DSS / Custom]
Target: [Kubernetes / Linux / AWS / Docker]

Requirements:
1. [CONTROL 1]
2. [CONTROL 2]
3. [CONTROL 3]

Include:
1. inspec.yml metadata
2. controls/*.rb with impact scores
3. Test descriptions and remediation guidance
4. Profile dependencies if needed
```

### Compliance Gap Analysis

```
Perform a compliance gap analysis for the following configuration against [STANDARD]:

Configuration:
[PASTE TERRAFORM/KUBERNETES/SYSTEM CONFIG]

Provide:
1. Compliance score (percentage)
2. List of failing controls with severity
3. Specific remediation steps
4. Priority ranking for fixes
5. Estimated effort for each fix
```

### SOC2 Evidence Collection

```
Generate automated evidence collection scripts for SOC2 Trust Service Criteria:

TSC: [Security / Availability / Processing Integrity / Confidentiality / Privacy]
Controls to cover: [CC6.1, CC6.7, etc.]

Output:
1. Scripts to collect evidence (bash/python)
2. Expected output format
3. Audit trail logging
4. Frequency recommendations
```

## Security Architecture

### Zero Trust Architecture

```
Design a Zero Trust security architecture for:

Application: [DESCRIBE APPLICATION]
Infrastructure: [Kubernetes / Cloud / Hybrid]
Current state: [DESCRIBE CURRENT SECURITY]

Include:
1. Network segmentation strategy
2. Identity and access management
3. Service mesh configuration (Istio/Linkerd)
4. Policy enforcement points
5. Monitoring and alerting
6. Implementation roadmap
```

### Security Controls Mapping

```
Map security controls to technical implementations:

Framework: [NIST CSF / ISO 27001 / CIS Controls]
Environment: [Kubernetes / AWS / GCP / Azure]

For each control provide:
1. Technical implementation
2. Tools/technologies to use
3. Policy as code implementation
4. Monitoring/alerting setup
5. Evidence collection method
```

## Incident Response

### Security Incident Analysis

```
Analyze the following security incident and provide response recommendations:

Incident details:
- Type: [DESCRIBE INCIDENT]
- Affected systems: [LIST SYSTEMS]
- Timeline: [WHEN DETECTED/STARTED]
- Current impact: [DESCRIBE IMPACT]

Provide:
1. Immediate containment steps
2. Investigation checklist
3. Evidence preservation commands
4. Root cause analysis approach
5. Remediation plan
6. Post-incident improvements
```

### Policy Violation Response

```
Analyze this policy violation and recommend response:

Violation: [DESCRIBE VIOLATION]
Policy: [WHICH POLICY VIOLATED]
Resource: [AFFECTED RESOURCE]
Severity: [CRITICAL/HIGH/MEDIUM/LOW]

Provide:
1. Immediate actions needed
2. Root cause analysis
3. Remediation steps
4. Policy improvement suggestions
5. Monitoring enhancements
```

## DevSecOps Pipeline

### Pipeline Security Review

```
Review this CI/CD pipeline for security best practices:

Pipeline configuration:
[PASTE PIPELINE YAML]

Evaluate:
1. Secrets management
2. Dependency scanning
3. SAST/DAST integration
4. Container security
5. IaC scanning
6. Artifact signing
7. Supply chain security

Output:
- Security gaps identified
- Improved pipeline configuration
- Additional tools/steps to add
```

### Shift-Left Security Integration

```
Design security integration for early development stages:

Development environment: [IDE / Local / Cloud Dev]
Languages: [LIST LANGUAGES]
Frameworks: [LIST FRAMEWORKS]
CI/CD: [GitHub Actions / GitLab / Jenkins]

Provide:
1. Pre-commit hooks for security
2. IDE security plugins
3. Local scanning tools
4. PR security checks
5. Security feedback loops
6. Developer training recommendations
```

## Supply Chain Security

### SLSA Assessment

```
Assess current build process against SLSA levels:

Build system: [DESCRIBE BUILD SYSTEM]
Artifact storage: [DESCRIBE ARTIFACT STORAGE]
Current practices: [DESCRIBE CURRENT PRACTICES]

Provide:
1. Current SLSA level assessment
2. Gap analysis for each level
3. Roadmap to reach SLSA Level 3
4. Required tooling changes
5. Process improvements
```

### Dependency Security Review

```
Review dependencies for security concerns:

Package manager: [npm / pip / maven / go mod]
Lock file:
[PASTE LOCK FILE CONTENT]

Analyze:
1. Known vulnerabilities
2. Unmaintained packages
3. Typosquatting risks
4. License issues
5. Excessive permissions
6. Update recommendations
```

## Monitoring & Observability

### Security Monitoring Setup

```
Design security monitoring for:

Infrastructure: [DESCRIBE INFRASTRUCTURE]
Current monitoring: [DESCRIBE EXISTING TOOLS]
Compliance requirements: [LIST REQUIREMENTS]

Provide:
1. Security metrics to track
2. Alert rules (Prometheus/Grafana)
3. Dashboard design
4. Log aggregation strategy
5. SIEM integration
6. Incident escalation workflow
```

### Runtime Security Detection

```
Configure runtime security detection for Kubernetes:

Cluster details: [DESCRIBE CLUSTER]
Workload types: [DESCRIBE WORKLOADS]
Compliance: [REQUIREMENTS]

Provide:
1. Falco rules for threat detection
2. Network policy monitoring
3. Anomaly detection setup
4. Alert routing configuration
5. Response automation
```
