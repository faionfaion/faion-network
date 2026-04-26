# Security as Code Examples

## SAST Examples

### Semgrep

**Basic CI Integration (GitHub Actions)**

```yaml
# .github/workflows/semgrep.yml
name: Semgrep
on:
  pull_request: {}
  push:
    branches: [main, master]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: semgrep/semgrep
    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        run: semgrep ci
        env:
          SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
```

**Custom Rule Example**

```yaml
# .semgrep/rules/no-hardcoded-secrets.yaml
rules:
  - id: hardcoded-password
    patterns:
      - pattern-either:
          - pattern: password = "..."
          - pattern: PASSWORD = "..."
          - pattern: passwd = "..."
    message: "Hardcoded password detected"
    languages: [python, javascript, typescript]
    severity: ERROR

  - id: hardcoded-api-key
    pattern-regex: '(?i)(api[_-]?key|apikey)\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']'
    message: "Possible hardcoded API key"
    languages: [generic]
    severity: WARNING
```

**Local Scan with Custom Rules**

```bash
# Scan with default rules
semgrep scan --config auto .

# Scan with custom rules
semgrep scan --config .semgrep/rules/ .

# Scan specific language
semgrep scan --config auto --include "*.py" .

# Output SARIF for GitHub Security
semgrep scan --config auto --sarif -o semgrep-results.sarif .
```

### CodeQL

**GitHub Actions Integration**

```yaml
# .github/workflows/codeql.yml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6AM

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read

    strategy:
      matrix:
        language: [javascript, python]

    steps:
      - uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
          queries: +security-extended,security-and-quality

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
```

### SonarQube

**Docker Compose Setup**

```yaml
# docker-compose.sonar.yml
version: "3.8"
services:
  sonarqube:
    image: sonarqube:lts-community
    ports:
      - "9000:9000"
    environment:
      - SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions

volumes:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:
```

**GitHub Actions Integration**

```yaml
# .github/workflows/sonar.yml
name: SonarQube
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v2
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

---

## DAST Examples

### OWASP ZAP

**GitHub Actions - Baseline Scan**

```yaml
# .github/workflows/zap-scan.yml
name: ZAP Scan
on:
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *'  # Daily 2AM

jobs:
  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: report_html.html
```

**ZAP Rules Configuration**

```tsv
# .zap/rules.tsv
# Rule ID	Action	Description
10010	IGNORE	Cookie No HttpOnly Flag (acceptable for this app)
10011	WARN	Cookie Without Secure Flag
10015	FAIL	Incomplete or No Cache-control Header Set
10016	IGNORE	Web Browser XSS Protection Not Enabled
10017	FAIL	Cross-Domain JavaScript Source File Inclusion
10019	FAIL	Content-Type Header Missing
```

**Full Scan with Authentication**

```yaml
# .github/workflows/zap-full.yml
name: ZAP Full Scan
on:
  workflow_dispatch:

jobs:
  zap-full:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.10.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: >-
            -config api.addrs.addr.name=.*
            -config api.addrs.addr.regex=true
```

### Nuclei

**GitHub Actions Integration**

```yaml
# .github/workflows/nuclei.yml
name: Nuclei Scan
on:
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * *'

jobs:
  nuclei:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Nuclei Scan
        uses: projectdiscovery/nuclei-action@main
        with:
          target: https://staging.example.com
          templates: cves,vulnerabilities,misconfigurations
          output: nuclei-output.txt
          sarif-export: nuclei-results.sarif

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: nuclei-results.sarif
```

**Custom Nuclei Template**

```yaml
# .nuclei/templates/custom-headers-check.yaml
id: missing-security-headers
info:
  name: Missing Security Headers
  author: security-team
  severity: medium
  tags: headers,security

http:
  - method: GET
    path:
      - "{{BaseURL}}"
    matchers-condition: or
    matchers:
      - type: word
        part: header
        negative: true
        words:
          - "X-Content-Type-Options"
        condition: and

      - type: word
        part: header
        negative: true
        words:
          - "X-Frame-Options"
```

---

## Container Scanning Examples

### Trivy

**GitHub Actions Integration**

```yaml
# .github/workflows/trivy.yml
name: Container Scan
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

**Comprehensive Trivy Scan**

```yaml
# .github/workflows/trivy-full.yml
name: Trivy Full Scan
on:
  push:
    branches: [main]

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Filesystem scan (IaC, secrets)
      - name: Trivy FS Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          trivy-config: trivy.yaml

      # Config scan (Dockerfile, K8s manifests)
      - name: Trivy Config Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH,MEDIUM'

      # Image scan
      - name: Build and Scan Image
        run: |
          docker build -t myapp:latest .
          trivy image --exit-code 1 --severity CRITICAL myapp:latest
```

**Trivy Configuration File**

```yaml
# trivy.yaml
severity:
  - CRITICAL
  - HIGH

exit-code: 1

ignore-unfixed: true

ignorefile: .trivyignore

cache-dir: .trivy-cache

db:
  skip-update: false

vulnerability:
  type:
    - os
    - library

secret:
  config: trivy-secret.yaml

misconfiguration:
  terraform:
    vars:
      - terraform.tfvars
```

**Trivy Ignore File**

```
# .trivyignore
# Ignore specific CVEs
CVE-2023-12345
CVE-2023-67890

# Ignore with expiration
CVE-2024-11111 exp:2024-12-31

# Ignore by package
pkg:npm/lodash@4.17.20
```

### Grype

**GitHub Actions Integration**

```yaml
# .github/workflows/grype.yml
name: Grype Scan
on:
  push:
    branches: [main]

jobs:
  grype:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan with Grype
        uses: anchore/scan-action@v4
        id: scan
        with:
          image: myapp:${{ github.sha }}
          fail-build: true
          severity-cutoff: high

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: ${{ steps.scan.outputs.sarif }}
```

**Generate SBOM with Syft + Scan with Grype**

```yaml
# .github/workflows/sbom-scan.yml
name: SBOM and Vulnerability Scan
on:
  push:
    branches: [main]

jobs:
  sbom-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Image
        run: docker build -t myapp:latest .

      # Generate SBOM
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: myapp:latest
          artifact-name: sbom.spdx.json
          output-file: sbom.spdx.json

      # Scan SBOM
      - name: Scan SBOM
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
          grype sbom:sbom.spdx.json --fail-on high
```

---

## Policy as Code Examples

### OPA (Open Policy Agent)

**Basic Rego Policy - No Privileged Containers**

```rego
# policies/kubernetes/no-privileged.rego
package kubernetes.admission

import rego.v1

deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.containers
    container.securityContext.privileged == true
    msg := sprintf("Container '%s' must not run as privileged", [container.name])
}

deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.initContainers
    container.securityContext.privileged == true
    msg := sprintf("Init container '%s' must not run as privileged", [container.name])
}
```

**Require Resource Limits**

```rego
# policies/kubernetes/resource-limits.rego
package kubernetes.admission

import rego.v1

deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.containers
    not container.resources.limits.memory
    msg := sprintf("Container '%s' must have memory limits", [container.name])
}

deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.containers
    not container.resources.limits.cpu
    msg := sprintf("Container '%s' must have CPU limits", [container.name])
}
```

**Trusted Registry Policy**

```rego
# policies/kubernetes/trusted-registry.rego
package kubernetes.admission

import rego.v1

trusted_registries := {
    "gcr.io/my-project",
    "docker.io/myorg",
    "ghcr.io/myorg"
}

deny contains msg if {
    input.request.kind.kind == "Pod"
    some container in input.request.object.spec.containers
    not any_trusted_registry(container.image)
    msg := sprintf("Container '%s' uses untrusted registry: %s", [container.name, container.image])
}

any_trusted_registry(image) if {
    some registry in trusted_registries
    startswith(image, registry)
}
```

**OPA Policy Testing**

```rego
# policies/kubernetes/no-privileged_test.rego
package kubernetes.admission

import rego.v1

test_deny_privileged_container if {
    result := deny with input as {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "spec": {
                    "containers": [{
                        "name": "nginx",
                        "securityContext": {"privileged": true}
                    }]
                }
            }
        }
    }
    count(result) > 0
}

test_allow_non_privileged_container if {
    result := deny with input as {
        "request": {
            "kind": {"kind": "Pod"},
            "object": {
                "spec": {
                    "containers": [{
                        "name": "nginx",
                        "securityContext": {"privileged": false}
                    }]
                }
            }
        }
    }
    count(result) == 0
}
```

### OPA Gatekeeper

**Constraint Template**

```yaml
# gatekeeper/templates/k8srequiredlabels.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
```

**Constraint**

```yaml
# gatekeeper/constraints/require-labels.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-label
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace", "Pod"]
    excludedNamespaces: ["kube-system", "gatekeeper-system"]
  parameters:
    labels:
      - "team"
      - "environment"
```

### Kyverno

**Require Labels Policy**

```yaml
# kyverno/policies/require-labels.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
  annotations:
    policies.kyverno.io/title: Require Labels
    policies.kyverno.io/category: Best Practices
    policies.kyverno.io/severity: medium
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: require-team-label
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "The label 'team' is required."
        pattern:
          metadata:
            labels:
              team: "?*"
```

**Disallow Privileged Containers**

```yaml
# kyverno/policies/disallow-privileged.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: deny-privileged
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Privileged containers are not allowed."
        pattern:
          spec:
            containers:
              - securityContext:
                  privileged: "false"
            =(initContainers):
              - securityContext:
                  privileged: "false"
```

**Add Default Security Context**

```yaml
# kyverno/policies/add-security-context.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-securitycontext
spec:
  rules:
    - name: add-securitycontext
      match:
        any:
          - resources:
              kinds:
                - Pod
      mutate:
        patchStrategicMerge:
          spec:
            securityContext:
              runAsNonRoot: true
              seccompProfile:
                type: RuntimeDefault
            containers:
              - (name): "*"
                securityContext:
                  allowPrivilegeEscalation: false
                  capabilities:
                    drop:
                      - ALL
```

---

## Secrets Scanning Examples

### GitLeaks

**GitHub Actions Integration**

```yaml
# .github/workflows/gitleaks.yml
name: Gitleaks
on:
  pull_request:
  push:
    branches: [main]

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Pre-commit Hook**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

### detect-secrets

**Pre-commit Configuration**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

**Initialize Baseline**

```bash
# Create baseline (ignores existing secrets)
detect-secrets scan > .secrets.baseline

# Audit baseline
detect-secrets audit .secrets.baseline
```

---

## Supply Chain Security

### Sigstore/Cosign

**Sign Container Image**

```yaml
# .github/workflows/sign-image.yml
name: Build and Sign
on:
  push:
    tags: ['v*']

jobs:
  build-sign:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Install Cosign
        uses: sigstore/cosign-installer@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push
        id: build
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}

      - name: Sign Image
        run: |
          cosign sign --yes ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}
```

**Verify Signed Image**

```bash
# Verify with keyless signing
cosign verify \
  --certificate-identity "https://github.com/myorg/myrepo/.github/workflows/build.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  ghcr.io/myorg/myapp:latest
```
