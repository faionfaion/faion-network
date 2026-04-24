# LLM Prompts for Security Testing

Effective prompts for LLM-assisted security testing, vulnerability detection, and remediation.

---

## Code Review Prompts

### General Security Review

```
Review the following code for security vulnerabilities. Focus on:
1. OWASP Top 10 2025 vulnerabilities
2. Input validation and sanitization
3. Authentication and authorization flaws
4. Cryptographic issues
5. Injection vulnerabilities
6. Error handling that leaks information

For each finding, provide:
- Vulnerability type and severity (Critical/High/Medium/Low)
- CWE ID if applicable
- Affected code lines
- Attack scenario
- Remediation with code example

Code:
```[paste code]```
```

### Authentication Review

```
Review this authentication implementation for security issues:
1. Password storage and hashing
2. Session management
3. Token generation and validation
4. Brute force protection
5. Account enumeration risks
6. Credential stuffing prevention
7. MFA implementation (if present)

Identify weaknesses and provide secure alternatives.

Code:
```[paste code]```
```

### Authorization Review

```
Analyze this authorization code for access control vulnerabilities:
1. Broken Object Level Authorization (BOLA/IDOR)
2. Broken Function Level Authorization
3. Missing authorization checks
4. Privilege escalation risks
5. RBAC/ABAC implementation flaws

For each endpoint/function, verify:
- Is authorization enforced server-side?
- Can users access other users' data?
- Are admin functions protected?

Code:
```[paste code]```
```

### API Security Review

```
Review this API endpoint for OWASP API Security Top 10 2023 vulnerabilities:
- API1: Broken Object Level Authorization
- API2: Broken Authentication
- API3: Broken Object Property Level Authorization
- API4: Unrestricted Resource Consumption
- API5: Broken Function Level Authorization
- API6: Unrestricted Access to Sensitive Flows
- API7: Server Side Request Forgery
- API8: Security Misconfiguration
- API9: Improper Inventory Management
- API10: Unsafe Consumption of APIs

Include rate limiting, input validation, and output filtering analysis.

API Code:
```[paste code]```
```

---

## Vulnerability-Specific Prompts

### SQL Injection Analysis

```
Analyze this database query code for SQL injection vulnerabilities:
1. Identify all user-controlled inputs that reach database queries
2. Check if parameterized queries/prepared statements are used
3. Detect string concatenation in queries
4. Identify ORM misuse patterns
5. Check for stored procedure injection

For each vulnerability found:
- Show the attack payload
- Demonstrate the exploit
- Provide the secure fix using parameterized queries

Code:
```[paste code]```
```

### XSS Analysis

```
Analyze this code for Cross-Site Scripting (XSS) vulnerabilities:
1. Stored XSS: User input stored and rendered later
2. Reflected XSS: User input immediately reflected
3. DOM-based XSS: Client-side JavaScript manipulation
4. Output encoding context (HTML, JS, CSS, URL)
5. Template injection risks

Check:
- Is output properly encoded for its context?
- Are dangerous functions used (innerHTML, dangerouslySetInnerHTML)?
- Is user input used in event handlers?
- Are Content-Security-Policy headers configured?

Code:
```[paste code]```
```

### SSRF Analysis

```
Review this code for Server-Side Request Forgery (SSRF) vulnerabilities:
1. Identify where user input controls URL/hostname
2. Check for URL validation and allowlisting
3. Detect internal IP address access (localhost, 169.254.x.x, 10.x.x.x)
4. Check redirect following behavior
5. Identify cloud metadata endpoint access risks (AWS, GCP, Azure)

Provide:
- Attack payloads for each SSRF vector
- Secure URL validation code
- Allowlist implementation

Code:
```[paste code]```
```

### Command Injection Analysis

```
Analyze this code for command injection vulnerabilities:
1. Identify shell command execution (subprocess, exec, system)
2. Check if user input reaches command arguments
3. Detect shell=True usage patterns
4. Identify path traversal in file operations
5. Check for argument injection (adding flags)

For each finding:
- Show the exploit command
- Demonstrate potential impact
- Provide secure alternative (avoid shell, use allowlist)

Code:
```[paste code]```
```

### Insecure Deserialization Analysis

```
Review this code for insecure deserialization vulnerabilities:
1. Identify deserialization of untrusted data
2. Detect dangerous libraries (pickle, yaml.load, unserialize)
3. Check for object injection in JSON/XML parsing
4. Identify gadget chain risks

Affected libraries to check:
- Python: pickle, yaml, marshal, shelve
- Java: ObjectInputStream, XMLDecoder, XStream
- PHP: unserialize, maybe_unserialize
- Node.js: serialize-javascript, node-serialize

Code:
```[paste code]```
```

---

## Test Generation Prompts

### Generate Security Test Cases

```
Generate comprehensive security test cases for this endpoint:

Endpoint: [METHOD] /api/[path]
Request body: [schema]
Authentication: [type]
Authorization: [rules]

Generate tests for:
1. Authentication bypass attempts
2. Authorization failures (IDOR, privilege escalation)
3. Input validation (boundary values, special characters)
4. Injection attacks (SQL, NoSQL, command, XSS)
5. Rate limiting verification
6. Error handling security
7. Business logic abuse

Use pytest/Jest format with descriptive test names.
Include attack payloads and expected responses.
```

### Generate OWASP Top 10 Tests

```
Generate a complete OWASP Top 10 2025 test suite for this application:

Application description: [describe app]
Tech stack: [Python/FastAPI, Node.js/Express, etc.]
Authentication method: [JWT, session, etc.]

For each OWASP category, generate:
1. At least 3 specific test cases
2. Realistic attack payloads
3. Expected security responses
4. Pass/fail assertions

Use the provided testing framework and fixtures.
```

### Generate API Security Tests

```
Based on this OpenAPI/Swagger specification, generate security tests:

```[paste OpenAPI spec]```

Generate tests for:
1. Authentication on all protected endpoints
2. Authorization per-endpoint and per-operation
3. Rate limiting for sensitive operations
4. Input validation for all parameters
5. BOLA/IDOR for object access
6. Sensitive data exposure in responses
7. Security headers validation

Output as executable test code.
```

---

## Remediation Prompts

### Fix Vulnerability

```
The following code has a [vulnerability type] vulnerability.
Provide a secure fix that:
1. Completely addresses the vulnerability
2. Maintains the original functionality
3. Follows security best practices
4. Uses the existing framework/library patterns
5. Includes input validation where appropriate

Also provide a test case to verify the fix.

Vulnerable code:
```[paste code]```

Vulnerability description: [describe the issue]
```

### Secure Implementation Request

```
Implement a secure version of [feature] with:

Requirements:
- [list functional requirements]

Security requirements:
1. Input validation (type, length, format, allowlist)
2. Output encoding (context-appropriate)
3. Authentication (if applicable)
4. Authorization (RBAC/ABAC)
5. Logging security events
6. Error handling (no info leakage)
7. Rate limiting (if applicable)

Tech stack: [specify]
Include unit tests for security scenarios.
```

### Security Header Configuration

```
Generate secure HTTP header configuration for:

Framework: [Express/FastAPI/Django/etc.]
Deployment: [Docker/AWS/Cloudflare/etc.]

Include:
1. Content-Security-Policy (strict)
2. Strict-Transport-Security
3. X-Content-Type-Options
4. X-Frame-Options
5. Referrer-Policy
6. Permissions-Policy
7. CORS configuration

Provide both code configuration and explanation of each header.
```

---

## CI/CD Security Prompts

### GitHub Actions Security Workflow

```
Generate a GitHub Actions security workflow that:
1. Runs on every PR and push to main
2. Includes SAST (Semgrep, language-specific linter)
3. Includes secret scanning (TruffleHog or Gitleaks)
4. Includes dependency scanning (Snyk or npm audit)
5. Fails on critical/high severity findings
6. Uploads reports as artifacts
7. Posts summary to PR

Tech stack: [Python/Node.js/Go/etc.]
Include configuration files for each tool.
```

### Container Security Scanning

```
Create a container security pipeline that:
1. Builds the Docker image
2. Scans base image for vulnerabilities (Trivy)
3. Checks Dockerfile for misconfigurations
4. Validates no secrets in image layers
5. Checks for least-privilege container settings
6. Generates SBOM

Output as GitHub Actions or GitLab CI configuration.
Include Dockerfile security checklist.
```

### Infrastructure Security Check

```
Generate Terraform/CloudFormation security checks:
1. No hardcoded secrets
2. Encryption at rest enabled
3. Encryption in transit (TLS)
4. Least privilege IAM policies
5. Security groups with minimal exposure
6. Logging enabled
7. Public access blocked where appropriate

Include:
- Checkov/tfsec rules
- CI/CD integration
- Remediation for common issues
```

---

## Threat Modeling Prompts

### STRIDE Analysis

```
Perform STRIDE threat modeling for:

System description: [describe system]
Components: [list components]
Data flows: [describe data flows]
Trust boundaries: [describe boundaries]

For each component, analyze:
- Spoofing: Can identity be faked?
- Tampering: Can data be modified?
- Repudiation: Can actions be denied?
- Information Disclosure: Can data leak?
- Denial of Service: Can service be disrupted?
- Elevation of Privilege: Can access be escalated?

Output:
1. Threat table with risk ratings
2. Prioritized mitigation strategies
3. Security test cases for each threat
```

### Attack Surface Analysis

```
Analyze the attack surface for:

Application type: [web app/API/mobile backend/etc.]
Authentication: [method]
Data handled: [types of sensitive data]
External integrations: [list]

Identify:
1. Entry points (endpoints, file uploads, websockets)
2. Trust boundaries
3. Privilege levels
4. Data stores
5. External dependencies

For each entry point, list:
- Potential attack vectors
- Required authentication/authorization
- Input validation requirements
- Recommended security controls
```

---

## Dependency Analysis Prompts

### Vulnerable Dependency Analysis

```
Analyze this dependency vulnerability report and provide:

1. Risk assessment for each vulnerability
   - Exploitability (is there public exploit?)
   - Impact on our application
   - Attack vector (network/local)

2. Prioritization based on:
   - CVSS score
   - Whether we use the vulnerable function
   - Ease of exploitation

3. Remediation plan:
   - Upgrade path (if available)
   - Alternative packages
   - Temporary mitigations

Vulnerability report:
```[paste report]```
```

### SBOM Security Review

```
Review this Software Bill of Materials (SBOM) for security concerns:

1. Identify high-risk dependencies
2. Flag outdated packages
3. Check license compliance
4. Identify packages with known vulnerabilities
5. Suggest alternatives for problematic packages

SBOM:
```[paste SBOM]```
```

---

## Incident Response Prompts

### Vulnerability Triage

```
Triage this security vulnerability finding:

Finding:
```[paste finding]```

Provide:
1. Severity classification (Critical/High/Medium/Low)
2. CVSS v3.1 score estimation
3. Attack complexity analysis
4. Business impact assessment
5. Recommended response timeline
6. Immediate mitigation steps
7. Long-term remediation plan
```

### Security Incident Analysis

```
Analyze this potential security incident:

Log entries:
```[paste logs]```

Determine:
1. Is this a true positive or false positive?
2. What type of attack is this?
3. What was the attack vector?
4. Was the attack successful?
5. What is the scope of impact?
6. Immediate containment steps
7. Evidence to preserve
8. Recommended response actions
```

---

## Prompt Engineering Tips

### Effective Security Prompts

**DO:**
- Provide complete code context
- Specify the tech stack and framework
- Include data flow information
- Ask for severity ratings
- Request remediation with code examples
- Specify output format (test code, report, etc.)

**DON'T:**
- Ask to "find all vulnerabilities" without context
- Provide partial code snippets
- Skip authentication/authorization context
- Forget to specify the framework version
- Ask for time estimates

### Context Template

```
## Context
- Language/Framework: [e.g., Python 3.11 / FastAPI 0.100]
- Authentication: [e.g., JWT with RS256]
- Database: [e.g., PostgreSQL with SQLAlchemy]
- Deployment: [e.g., Docker on AWS ECS]
- Compliance: [e.g., SOC2, GDPR]

## Code
```[paste code]```

## Specific Concerns
[List any specific areas you want analyzed]

## Expected Output
[Specify format: test code, report, fix, etc.]
```

### Iterative Refinement

1. **First pass:** General security review
2. **Second pass:** Deep dive on specific vulnerability type
3. **Third pass:** Generate test cases
4. **Fourth pass:** Review remediation

---

## LLM Limitations

### What LLMs Cannot Do

- Execute dynamic security tests
- Access runtime behavior
- Detect business logic flaws without context
- Replace manual penetration testing
- Guarantee complete coverage
- Access external vulnerability databases in real-time

### When to Use Human Review

- Complex authentication flows
- Multi-step business logic attacks
- Infrastructure security decisions
- Compliance-related security controls
- Incident response decisions
- Security architecture reviews

### Verification Requirements

Always verify LLM security findings:
1. Confirm vulnerability is exploitable
2. Test remediation actually fixes the issue
3. Check for regressions in functionality
4. Validate against actual security tools
5. Have senior engineer review critical fixes

---

*These prompts are starting points. Customize based on your specific application, tech stack, and security requirements.*
