# Security as Code Templates

## Gatekeeper Setup

### Install Gatekeeper

```bash
# Add Gatekeeper Helm repo
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm repo update

# Install Gatekeeper
helm install gatekeeper/gatekeeper \
  --name-template=gatekeeper \
  --namespace gatekeeper-system \
  --create-namespace \
  --set replicas=3 \
  --set audit.replicas=1 \
  --set audit.logLevel=INFO \
  --set audit.auditInterval=60
```

### Base ConstraintTemplates

```yaml
# templates/k8s-required-labels.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
  annotations:
    description: "Requires specified labels on resources"
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
---
# templates/k8s-container-limits.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8scontainerlimits
  annotations:
    description: "Requires resource limits on containers"
spec:
  crd:
    spec:
      names:
        kind: K8sContainerLimits
      validation:
        openAPIV3Schema:
          type: object
          properties:
            cpu:
              type: string
            memory:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8scontainerlimits

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits.cpu
          msg := sprintf("Container %v has no CPU limit", [container.name])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits.memory
          msg := sprintf("Container %v has no memory limit", [container.name])
        }
---
# templates/k8s-deny-privileged.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sdenyprivileged
  annotations:
    description: "Denies privileged containers"
spec:
  crd:
    spec:
      names:
        kind: K8sDenyPrivileged
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sdenyprivileged

        violation[{"msg": msg}] {
          c := input_containers[_]
          c.securityContext.privileged == true
          msg := sprintf("Privileged container not allowed: %v", [c.name])
        }

        input_containers[c] {
          c := input.review.object.spec.containers[_]
        }

        input_containers[c] {
          c := input.review.object.spec.initContainers[_]
        }
```

### Base Constraints

```yaml
# constraints/require-labels.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-labels
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet", "DaemonSet"]
    excludedNamespaces:
      - kube-system
      - gatekeeper-system
  parameters:
    labels:
      - "app.kubernetes.io/name"
      - "app.kubernetes.io/version"
      - "team"
      - "environment"
---
# constraints/container-limits.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sContainerLimits
metadata:
  name: require-container-limits
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    excludedNamespaces:
      - kube-system
---
# constraints/deny-privileged.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sDenyPrivileged
metadata:
  name: deny-privileged-containers
spec:
  enforcementAction: deny
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    excludedNamespaces:
      - kube-system
```

## Kyverno Setup

### Install Kyverno

```bash
# Add Kyverno Helm repo
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

# Install Kyverno
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --set replicaCount=3 \
  --set backgroundController.replicas=2
```

### Base Policies

```yaml
# policies/require-labels.yaml
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
                - Deployment
                - StatefulSet
      validate:
        message: "Label 'team' is required"
        pattern:
          metadata:
            labels:
              team: "?*"
    - name: require-env-label
      match:
        any:
          - resources:
              kinds:
                - Deployment
                - StatefulSet
      validate:
        message: "Label 'environment' is required"
        pattern:
          metadata:
            labels:
              environment: "production|staging|development"
---
# policies/disallow-privileged.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: disallow-privileged-containers
  annotations:
    policies.kyverno.io/title: Disallow Privileged Containers
    policies.kyverno.io/category: Pod Security Standards
    policies.kyverno.io/severity: high
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: disallow-privileged
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "Privileged mode is disallowed"
        pattern:
          spec:
            containers:
              - securityContext:
                  privileged: "false"
            =(initContainers):
              - securityContext:
                  privileged: "false"
---
# policies/add-default-security-context.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-security-context
  annotations:
    policies.kyverno.io/title: Add Default Security Context
    policies.kyverno.io/category: Security
    policies.kyverno.io/severity: medium
spec:
  rules:
    - name: add-security-context
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
                  readOnlyRootFilesystem: true
                  capabilities:
                    drop:
                      - ALL
```

## CI/CD Security Pipeline

### GitHub Actions Template

```yaml
# .github/workflows/security.yml
name: Security Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  TRIVY_SEVERITY: CRITICAL,HIGH

jobs:
  # Static Analysis
  sast:
    name: Static Analysis
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

      - name: Run Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: auto

  # Dependency Scanning
  dependencies:
    name: Dependency Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner (dependencies)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-fs-results.sarif'
          severity: ${{ env.TRIVY_SEVERITY }}

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-fs-results.sarif'

  # IaC Scanning
  iac:
    name: IaC Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform,kubernetes,dockerfile
          output_format: sarif
          output_file_path: checkov-results.sarif
          soft_fail: false

      - name: Upload Checkov results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: checkov-results.sarif

      - name: Run Trivy IaC scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'
          format: 'table'
          exit-code: '1'
          severity: ${{ env.TRIVY_SEVERITY }}

  # Container Scanning
  container:
    name: Container Security Scan
    runs-on: ubuntu-latest
    needs: [sast, dependencies]
    steps:
      - uses: actions/checkout@v4

      - name: Build container image
        run: docker build -t ${{ github.repository }}:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: '${{ github.repository }}:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-image-results.sarif'
          severity: ${{ env.TRIVY_SEVERITY }}
          exit-code: '1'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-image-results.sarif'

  # Policy Check
  policy:
    name: Policy Compliance
    runs-on: ubuntu-latest
    needs: [iac]
    steps:
      - uses: actions/checkout@v4

      - name: Setup OPA
        uses: open-policy-agent/setup-opa@v2

      - name: Run OPA policy checks
        run: |
          opa eval --format pretty \
            --data policies/ \
            --input terraform/plan.json \
            "data.terraform.security.deny"

  # Sign & Push (main branch only)
  sign:
    name: Sign & Push
    runs-on: ubuntu-latest
    needs: [container, policy]
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Cosign
        uses: sigstore/cosign-installer@main

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}

      - name: Sign image
        run: |
          cosign sign --yes \
            ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}
```

## Terraform Policy Template

### Checkov Configuration

```yaml
# .checkov.yaml
compact: true
framework:
  - terraform
  - kubernetes
  - dockerfile
check:
  - CKV_AWS_*
  - CKV_K8S_*
  - CKV_DOCKER_*
skip-check:
  - CKV_AWS_999  # Example skip
soft-fail: false
output:
  - cli
  - sarif
download-external-modules: true
```

### OPA Terraform Policies

```rego
# policies/terraform/main.rego
package terraform

import future.keywords.in

# Deny resources without required tags
deny[msg] {
  resource := input.resource_changes[_]
  taggable_resource(resource.type)
  not has_required_tags(resource)
  msg := sprintf("%s '%s' missing required tags", [resource.type, resource.address])
}

taggable_resource(type) {
  taggable_types := {
    "aws_instance",
    "aws_s3_bucket",
    "aws_rds_cluster",
    "aws_lambda_function",
    "aws_ecs_service"
  }
  type in taggable_types
}

has_required_tags(resource) {
  tags := resource.change.after.tags
  required := {"Environment", "Team", "Owner"}
  provided := {t | tags[t]}
  count(required - provided) == 0
}

# Deny public S3 buckets
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.acl in {"public-read", "public-read-write"}
  msg := sprintf("S3 bucket '%s' cannot be public", [resource.address])
}

# Require encryption
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  not resource.change.after.server_side_encryption_configuration
  msg := sprintf("S3 bucket '%s' must have encryption", [resource.address])
}

# Deny unencrypted RDS
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  not resource.change.after.storage_encrypted
  msg := sprintf("RDS '%s' must have encryption enabled", [resource.address])
}
```

## Chef InSpec Profile Template

```ruby
# inspec.yml
name: security-baseline
title: Security Baseline Profile
version: 1.0.0
summary: Security baseline for production systems
supports:
  - platform-family: linux
  - platform-family: unix

depends:
  - name: linux-baseline
    url: https://github.com/dev-sec/linux-baseline
  - name: cis-kubernetes-benchmark
    url: https://github.com/dev-sec/cis-kubernetes-benchmark
```

```ruby
# controls/security_baseline.rb
control 'security-1' do
  impact 1.0
  title 'Ensure SSH root login is disabled'
  desc 'Root login via SSH should be disabled'

  describe sshd_config do
    its('PermitRootLogin') { should eq 'no' }
  end
end

control 'security-2' do
  impact 1.0
  title 'Ensure password authentication is disabled'
  desc 'SSH password authentication should be disabled'

  describe sshd_config do
    its('PasswordAuthentication') { should eq 'no' }
  end
end

control 'security-3' do
  impact 0.7
  title 'Ensure firewall is active'
  desc 'System firewall should be enabled'

  describe service('ufw') do
    it { should be_installed }
    it { should be_enabled }
    it { should be_running }
  end
end

control 'security-4' do
  impact 1.0
  title 'Ensure audit logging is enabled'
  desc 'Audit daemon should be running'

  describe service('auditd') do
    it { should be_installed }
    it { should be_enabled }
    it { should be_running }
  end
end
```

## SBOM Generation Template

```yaml
# .github/workflows/sbom.yml
name: Generate SBOM

on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  sbom:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Generate SBOM with Syft
        uses: anchore/sbom-action@v0
        with:
          image: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: spdx-json
          output-file: sbom.spdx.json

      - name: Generate CycloneDX SBOM
        uses: anchore/sbom-action@v0
        with:
          image: ghcr.io/${{ github.repository }}:${{ github.sha }}
          format: cyclonedx-json
          output-file: sbom.cyclonedx.json

      - name: Attach SBOM to release
        if: github.event_name == 'release'
        uses: softprops/action-gh-release@v1
        with:
          files: |
            sbom.spdx.json
            sbom.cyclonedx.json

      - name: Attest SBOM with Cosign
        run: |
          cosign attest --yes \
            --predicate sbom.spdx.json \
            --type spdxjson \
            ghcr.io/${{ github.repository }}:${{ github.sha }}
```
