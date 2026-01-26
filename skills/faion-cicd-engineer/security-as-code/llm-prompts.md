# Security as Code LLM Prompts

## SAST Prompts

### Generate Custom Semgrep Rules

```
Create a Semgrep rule that detects [vulnerability type] in [language].

Requirements:
- Pattern should match [specific code pattern]
- Severity: [critical/high/medium/low]
- Include message explaining the vulnerability
- Add fix suggestion if possible
- Include test cases (positive and negative)

Output format: YAML rule with comments
```

### Analyze SAST Findings

```
Analyze these SAST findings and provide:

1. Risk assessment for each finding
2. False positive likelihood (low/medium/high)
3. Prioritized remediation order
4. Code fix suggestions

Findings:
[paste SAST output]

Consider:
- Exploitability
- Data sensitivity
- Attack surface exposure
- Existing mitigations
```

### Create CodeQL Query

```
Write a CodeQL query for [language] that detects [vulnerability type].

Requirements:
- Query should find [specific pattern]
- Include metadata (name, description, severity)
- Optimize for performance
- Include query help documentation

Example vulnerable code:
[paste example]
```

---

## DAST Prompts

### Create ZAP Scan Configuration

```
Create a ZAP configuration for scanning [application type].

Application details:
- URL: [URL]
- Authentication: [type - form/OAuth/API key]
- Technology stack: [stack]
- Sensitive areas to exclude: [list]

Include:
1. Context configuration
2. Authentication setup
3. Scan policy (active/passive rules)
4. Alert filters
5. Reporting format
```

### Create Nuclei Templates

```
Create a Nuclei template to detect [vulnerability/misconfiguration].

Target: [application type]
Vulnerability: [description]
Detection method: [HTTP response, header, body pattern]

Include:
- Template metadata
- HTTP request configuration
- Matchers (status, word, regex)
- Extractors if needed
- Severity rating with justification
```

### Analyze DAST Results

```
Analyze these DAST scan results and provide:

1. True positive assessment for each finding
2. Business impact analysis
3. Reproduction steps
4. Remediation recommendations
5. Priority ranking

Findings:
[paste DAST output]

Application context:
- Type: [web app/API/SPA]
- Users: [internal/external]
- Data sensitivity: [level]
```

---

## Container Security Prompts

### Harden Dockerfile

```
Review and harden this Dockerfile for security:

```dockerfile
[paste Dockerfile]
```

Provide:
1. Security issues found
2. Hardened Dockerfile with comments
3. Multi-stage build optimization if applicable
4. Base image recommendations
5. Runtime security context suggestions
```

### Analyze Container Scan Results

```
Analyze these container vulnerability scan results:

[paste Trivy/Grype output]

Provide:
1. Risk assessment (exploitability, severity context)
2. Base image vs application dependency breakdown
3. Remediation priority order
4. Upgrade recommendations (with compatibility notes)
5. Vulnerabilities that can be ignored (with justification)
```

### Create .trivyignore File

```
Based on these vulnerability findings, create a .trivyignore file:

[paste vulnerability list]

For each ignored vulnerability, include:
- CVE ID
- Reason for ignoring (no fix available, false positive, mitigated elsewhere)
- Expiration date if temporary
- Risk acceptance owner

Format: .trivyignore with comments
```

---

## Policy as Code Prompts

### Create OPA/Rego Policy

```
Write an OPA Rego policy that enforces [requirement].

Context:
- Target: [Kubernetes/Terraform/CI/API]
- Input format: [describe input JSON structure]
- Requirement: [detailed policy requirement]

Include:
1. Package declaration
2. Default deny rule
3. Allow/deny rules with clear logic
4. Helper functions if needed
5. Unit tests
6. Documentation comments
```

### Convert Security Requirements to Kyverno

```
Convert these security requirements to Kyverno policies:

Requirements:
1. [requirement 1]
2. [requirement 2]
3. [requirement 3]

For each policy include:
- Policy metadata and annotations
- Match/exclude criteria
- Validation or mutation rules
- Meaningful error messages
- Background scan configuration
```

### Debug Rego Policy

```
Debug this Rego policy that isn't working as expected:

```rego
[paste policy]
```

Input that should [pass/fail]:
```json
[paste input]
```

Expected behavior: [describe]
Actual behavior: [describe]

Provide:
1. Issue identification
2. Fixed policy
3. Explanation of the fix
4. Test cases to verify
```

### Create Gatekeeper Constraint Template

```
Create an OPA Gatekeeper constraint template for:

Requirement: [policy requirement]
Parameters needed: [list parameters]
Target resources: [Kubernetes resource types]

Include:
1. ConstraintTemplate with Rego
2. Example Constraint using the template
3. Test resources (passing and failing)
4. Documentation
```

---

## Security Pipeline Prompts

### Design Security Pipeline

```
Design a comprehensive security pipeline for:

Application:
- Type: [web app/API/microservices]
- Languages: [list]
- CI/CD: [GitHub Actions/GitLab CI/Jenkins]
- Container runtime: [Docker/Kubernetes]
- Cloud: [AWS/GCP/Azure]

Include:
1. Pipeline stages with tools
2. Gate criteria for each stage
3. Notification/alerting strategy
4. Remediation workflow
5. Metrics to track
```

### Integrate Security Tool

```
Create integration configuration for [security tool] in [CI/CD platform].

Requirements:
- Scan on: [events - PR, push, schedule]
- Severity threshold: [level]
- Output format: [SARIF/JSON/custom]
- Fail build on: [criteria]
- Notifications: [where to send]

Include:
1. CI/CD configuration file
2. Tool configuration file
3. Ignore/baseline file if needed
4. Documentation
```

### Create Security Metrics Dashboard

```
Design a security metrics dashboard for DevSecOps:

Data sources:
- SAST: [tool]
- DAST: [tool]
- Container scanning: [tool]
- Policy engine: [tool]

Include metrics for:
1. Vulnerability trends (by severity, age, type)
2. MTTR (Mean Time to Remediate)
3. Security coverage (% of repos scanned)
4. Policy compliance rate
5. Security debt
6. SLA compliance

Output: Grafana dashboard JSON or Prometheus queries
```

---

## Incident Response Prompts

### Analyze Security Finding

```
Analyze this security finding for incident response:

Finding:
[paste finding details]

Context:
- Environment: [dev/staging/prod]
- Application: [name]
- Exposure: [internal/external]

Provide:
1. Severity assessment
2. Potential impact
3. Immediate actions needed
4. Root cause analysis approach
5. Long-term remediation
6. Detection improvements
```

### Create Security Runbook

```
Create a security incident runbook for:

Scenario: [vulnerability type discovered in production]
Example: SQL injection found by DAST in customer-facing API

Include:
1. Triage steps
2. Containment actions
3. Investigation checklist
4. Remediation steps
5. Communication templates
6. Post-incident review items
```

---

## Compliance Prompts

### Map Controls to Security Tools

```
Map these compliance controls to security automation:

Framework: [SOC2/PCI-DSS/HIPAA/CIS]
Controls:
- [control 1]
- [control 2]
- [control 3]

For each control provide:
1. Automated tool/check
2. Configuration needed
3. Evidence collection method
4. Audit frequency
5. Gap if automation not possible
```

### Generate Compliance Evidence

```
Generate compliance evidence report from these security scan results:

Framework: [compliance framework]
Period: [date range]
Scans: [list of scan types and tools]

Results:
[paste scan summaries]

Generate:
1. Executive summary
2. Control-by-control status
3. Vulnerability statistics
4. Remediation status
5. Exceptions and risk acceptances
6. Recommendations
```

---

## Best Practices Review Prompts

### Review Security Configuration

```
Review this security configuration for best practices:

Tool: [SAST/DAST/container scanner/policy engine]
Configuration:
[paste config]

Evaluate:
1. Coverage adequacy
2. Threshold appropriateness
3. Performance optimization
4. False positive management
5. Integration completeness
6. Missing security checks

Provide improved configuration with explanations.
```

### Security Architecture Review

```
Review this application's security architecture:

Architecture:
[describe or paste diagram]

Components:
- [component 1]
- [component 2]

Data flows:
- [flow 1]
- [flow 2]

Evaluate:
1. Attack surface analysis
2. Defense in depth
3. Security controls gaps
4. Recommended security tools
5. Policy enforcement points
6. Monitoring coverage
```
