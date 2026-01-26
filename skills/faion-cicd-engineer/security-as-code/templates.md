# Security as Code Templates

## Complete GitHub Actions Security Pipeline

```yaml
# .github/workflows/security.yml
name: Security Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly scan Monday 6AM

permissions:
  contents: read
  security-events: write
  pull-requests: write

jobs:
  # ============================================
  # SAST - Static Application Security Testing
  # ============================================
  sast:
    name: SAST Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Semgrep Scan
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/default
            p/security-audit
            p/secrets
          generateSarif: true

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: semgrep.sarif

  # ============================================
  # SCA - Software Composition Analysis
  # ============================================
  sca:
    name: Dependency Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Trivy Dependency Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-sca.sarif'
          severity: 'CRITICAL,HIGH'
          vuln-type: 'library'

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-sca.sarif

  # ============================================
  # Secrets Scanning
  # ============================================
  secrets:
    name: Secrets Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Gitleaks Scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # ============================================
  # IaC Security Scan
  # ============================================
  iac:
    name: IaC Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Trivy Config Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-iac.sarif'
          severity: 'CRITICAL,HIGH,MEDIUM'

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-iac.sarif

  # ============================================
  # Container Security
  # ============================================
  container:
    name: Container Scan
    runs-on: ubuntu-latest
    needs: [sast, sca, secrets]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          load: true
          tags: app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Trivy Image Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'app:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-image.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-image.sarif

      # Generate SBOM
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          image: app:${{ github.sha }}
          artifact-name: sbom-${{ github.sha }}.spdx.json
          output-file: sbom.spdx.json

      - name: Upload SBOM
        uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.spdx.json

  # ============================================
  # DAST - Dynamic Application Security Testing
  # ============================================
  dast:
    name: DAST Scan
    runs-on: ubuntu-latest
    needs: [container]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Start Application
        run: |
          docker-compose -f docker-compose.test.yml up -d
          sleep 30  # Wait for app to start

      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'http://localhost:8080'
          rules_file_name: '.zap/rules.tsv'

      - name: Stop Application
        if: always()
        run: docker-compose -f docker-compose.test.yml down
```

---

## GitLab CI Security Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security
  - build
  - deploy

variables:
  TRIVY_CACHE_DIR: ".trivy-cache"
  SECURE_LOG_LEVEL: "debug"

# ============================================
# SAST
# ============================================
semgrep-sast:
  stage: security
  image: semgrep/semgrep
  script:
    - semgrep ci --sarif --output semgrep.sarif
  artifacts:
    reports:
      sast: semgrep.sarif
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# ============================================
# Secrets Detection
# ============================================
secret_detection:
  stage: security
  image:
    name: zricethezav/gitleaks:latest
    entrypoint: [""]
  script:
    - gitleaks detect --source . --report-format sarif --report-path gitleaks.sarif
  artifacts:
    reports:
      secret_detection: gitleaks.sarif
  allow_failure: false

# ============================================
# Dependency Scanning
# ============================================
dependency_scanning:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy fs --format sarif --output trivy-deps.sarif .
  artifacts:
    reports:
      dependency_scanning: trivy-deps.sarif

# ============================================
# Container Scanning
# ============================================
container_scanning:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  variables:
    IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  script:
    - trivy image --format sarif --output trivy-container.sarif $IMAGE
  artifacts:
    reports:
      container_scanning: trivy-container.sarif
  needs:
    - job: build
      artifacts: false

# ============================================
# IaC Scanning
# ============================================
iac_scanning:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy config --format sarif --output trivy-iac.sarif .
  artifacts:
    reports:
      sast: trivy-iac.sarif

# ============================================
# Build
# ============================================
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  needs:
    - semgrep-sast
    - secret_detection
    - dependency_scanning

# ============================================
# DAST (on staging)
# ============================================
dast:
  stage: deploy
  image: owasp/zap2docker-stable
  script:
    - zap-baseline.py -t $STAGING_URL -r zap-report.html
  artifacts:
    paths:
      - zap-report.html
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

---

## Trivy Configuration

```yaml
# trivy.yaml
# Full configuration for Trivy scanner

# Scan settings
scan:
  # Skip directories
  skip-dirs:
    - node_modules
    - vendor
    - .git
    - test

  # Skip files
  skip-files:
    - "**/*_test.go"
    - "**/test_*.py"

# Severity threshold
severity:
  - CRITICAL
  - HIGH

# Exit code on findings
exit-code: 1

# Ignore unfixed vulnerabilities
ignore-unfixed: true

# Ignore file path
ignorefile: .trivyignore

# Cache directory
cache-dir: .trivy-cache

# Database settings
db:
  skip-update: false

# Vulnerability settings
vulnerability:
  type:
    - os
    - library

# Secret scanning
secret:
  config: trivy-secret.yaml

# Misconfiguration settings
misconfiguration:
  # Terraform variables
  terraform:
    vars:
      - terraform.tfvars
      - terraform.tfvars.json

  # Helm values
  helm:
    values:
      - values.yaml
      - values-prod.yaml

  # Policy paths
  policy-paths:
    - policies/

# Output format
format: table

# Licensing
license:
  # Forbidden licenses
  forbidden:
    - GPL-3.0
    - AGPL-3.0
  # Ignored licenses
  ignored:
    - MIT
    - Apache-2.0
    - BSD-3-Clause
```

---

## Kyverno Policy Set

```yaml
# kyverno/policies/baseline-security.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: baseline-security
  annotations:
    policies.kyverno.io/title: Baseline Security Policy
    policies.kyverno.io/category: Pod Security
    policies.kyverno.io/severity: high
    policies.kyverno.io/description: >-
      Enforces baseline security requirements for all pods.
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    # ----------------------------------------
    # Disallow privileged containers
    # ----------------------------------------
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

    # ----------------------------------------
    # Require non-root user
    # ----------------------------------------
    - name: require-run-as-non-root
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Containers must run as non-root user."
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
            containers:
              - securityContext:
                  runAsNonRoot: true

    # ----------------------------------------
    # Disallow privilege escalation
    # ----------------------------------------
    - name: deny-privilege-escalation
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Privilege escalation is not allowed."
        pattern:
          spec:
            containers:
              - securityContext:
                  allowPrivilegeEscalation: false
            =(initContainers):
              - securityContext:
                  allowPrivilegeEscalation: false

    # ----------------------------------------
    # Drop all capabilities
    # ----------------------------------------
    - name: drop-all-capabilities
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Containers must drop all capabilities."
        pattern:
          spec:
            containers:
              - securityContext:
                  capabilities:
                    drop:
                      - ALL
            =(initContainers):
              - securityContext:
                  capabilities:
                    drop:
                      - ALL

    # ----------------------------------------
    # Require read-only root filesystem
    # ----------------------------------------
    - name: require-readonly-rootfs
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Root filesystem must be read-only."
        pattern:
          spec:
            containers:
              - securityContext:
                  readOnlyRootFilesystem: true

---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: require-limits
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "CPU and memory limits are required."
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"

---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: validate-registries
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Images must be from trusted registries."
        pattern:
          spec:
            containers:
              - image: "gcr.io/* | docker.io/myorg/* | ghcr.io/myorg/*"
            =(initContainers):
              - image: "gcr.io/* | docker.io/myorg/* | ghcr.io/myorg/*"

---
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: disallow-latest
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Using 'latest' tag is not allowed. Specify a version tag."
        pattern:
          spec:
            containers:
              - image: "!*:latest"
            =(initContainers):
              - image: "!*:latest"
```

---

## OPA Gatekeeper Policy Library

```yaml
# gatekeeper/templates/k8sdisallowedtags.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sdisallowedtags
spec:
  crd:
    spec:
      names:
        kind: K8sDisallowedTags
      validation:
        openAPIV3Schema:
          type: object
          properties:
            tags:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sdisallowedtags

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          tag := [tag | tag := input.parameters.tags[_]; contains(container.image, concat(":", ["", tag]))]
          count(tag) > 0
          msg := sprintf("Container '%s' uses disallowed tag: %v", [container.name, tag])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.initContainers[_]
          tag := [tag | tag := input.parameters.tags[_]; contains(container.image, concat(":", ["", tag]))]
          count(tag) > 0
          msg := sprintf("Init container '%s' uses disallowed tag: %v", [container.name, tag])
        }

---
# gatekeeper/constraints/disallow-latest.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sDisallowedTags
metadata:
  name: disallow-latest-tag
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    excludedNamespaces:
      - kube-system
      - gatekeeper-system
  parameters:
    tags:
      - "latest"
```

---

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # Secrets detection
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # SAST with Semgrep
  - repo: https://github.com/semgrep/semgrep
    rev: v1.52.0
    hooks:
      - id: semgrep
        args: ['--config', 'auto', '--error']

  # Dockerfile linting
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint

  # YAML linting
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.33.0
    hooks:
      - id: yamllint
        args: ['-c', '.yamllint.yml']

  # Terraform security
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
      - id: terraform_trivy

  # Kubernetes manifests
  - repo: https://github.com/stackrox/kube-linter
    rev: v0.6.8
    hooks:
      - id: kube-linter
```

---

## Security Dashboard (Grafana)

```json
{
  "dashboard": {
    "title": "Security Overview",
    "panels": [
      {
        "title": "Critical Vulnerabilities by Repository",
        "type": "barchart",
        "datasource": "prometheus",
        "targets": [
          {
            "expr": "sum by (repository) (security_vulnerabilities_total{severity=\"critical\"})",
            "legendFormat": "{{repository}}"
          }
        ]
      },
      {
        "title": "Vulnerability Trend",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum by (severity) (security_vulnerabilities_total)",
            "legendFormat": "{{severity}}"
          }
        ]
      },
      {
        "title": "Policy Violations",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(gatekeeper_violations)"
          }
        ]
      },
      {
        "title": "Mean Time to Remediate (MTTR)",
        "type": "gauge",
        "targets": [
          {
            "expr": "avg(security_remediation_time_hours)"
          }
        ]
      },
      {
        "title": "Security Scan Coverage",
        "type": "piechart",
        "targets": [
          {
            "expr": "count by (scan_type) (security_scans_total)"
          }
        ]
      }
    ]
  }
}
```
