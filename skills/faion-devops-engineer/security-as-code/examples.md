# Security as Code Examples

## OPA/Gatekeeper Examples

### Require Container Resource Limits

**ConstraintTemplate:**

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredresources
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredResources
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredresources

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits.cpu
          msg := sprintf("Container %v must have CPU limits", [container.name])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits.memory
          msg := sprintf("Container %v must have memory limits", [container.name])
        }
```

**Constraint:**

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredResources
metadata:
  name: require-resource-limits
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    excludedNamespaces:
      - kube-system
```

### Deny Privileged Containers

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sdenypriv
spec:
  crd:
    spec:
      names:
        kind: K8sDenyPrivileged
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sdenypriv

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          container.securityContext.privileged == true
          msg := sprintf("Privileged containers not allowed: %v", [container.name])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.initContainers[_]
          container.securityContext.privileged == true
          msg := sprintf("Privileged init containers not allowed: %v", [container.name])
        }
```

### Require Image from Trusted Registry

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8strustedregistry
spec:
  crd:
    spec:
      names:
        kind: K8sTrustedRegistry
      validation:
        openAPIV3Schema:
          type: object
          properties:
            registries:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8strustedregistry

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not trusted_registry(container.image)
          msg := sprintf("Image %v is not from a trusted registry", [container.image])
        }

        trusted_registry(image) {
          registry := input.parameters.registries[_]
          startswith(image, registry)
        }
```

## Kyverno Examples

### Require Labels

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-team-label
      match:
        resources:
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
        resources:
          kinds:
            - Deployment
            - StatefulSet
      validate:
        message: "Label 'environment' is required"
        pattern:
          metadata:
            labels:
              environment: "?*"
```

### Auto-Add Security Context

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-security-context
spec:
  rules:
    - name: add-run-as-non-root
      match:
        resources:
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

### Generate Network Policy

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: generate-network-policy
spec:
  rules:
    - name: default-deny-ingress
      match:
        resources:
          kinds:
            - Namespace
      generate:
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        name: default-deny-ingress
        namespace: "{{request.object.metadata.name}}"
        data:
          spec:
            podSelector: {}
            policyTypes:
              - Ingress
```

## Terraform Policy Examples

### Checkov Custom Policy

```python
# checkov/custom_policies/require_encryption.py
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories

class S3BucketEncryption(BaseResourceCheck):
    def __init__(self):
        name = "Ensure S3 bucket has encryption enabled"
        id = "CKV_CUSTOM_1"
        supported_resources = ['aws_s3_bucket']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories,
                        supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        # Check for server_side_encryption_configuration
        if 'server_side_encryption_configuration' in conf:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = S3BucketEncryption()
```

### OPA for Terraform

```rego
# terraform/policies/security.rego
package terraform.security

# Deny public S3 buckets
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.acl == "public-read"
  msg := sprintf("S3 bucket %v cannot be public", [resource.address])
}

# Require encryption for RDS
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_db_instance"
  not resource.change.after.storage_encrypted
  msg := sprintf("RDS instance %v must have encryption enabled", [resource.address])
}

# Require tagging
deny[msg] {
  resource := input.resource_changes[_]
  manageable_resource(resource.type)
  not resource.change.after.tags.Environment
  msg := sprintf("Resource %v must have Environment tag", [resource.address])
}

manageable_resource(type) {
  types := {"aws_instance", "aws_s3_bucket", "aws_rds_cluster", "aws_lambda_function"}
  types[type]
}
```

## Trivy Integration Examples

### GitHub Actions Workflow

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'

  trivy-iac:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy IaC scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'config'
          scan-ref: '.'
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
```

### Trivy Kubernetes Operator

```yaml
apiVersion: aquasecurity.github.io/v1alpha1
kind: ClusterComplianceReport
metadata:
  name: nsa-cis-benchmark
spec:
  cron: "0 */6 * * *"
  reportType: summary
  compliance:
    id: nsa
    title: NSA Kubernetes Hardening Guide
    description: National Security Agency Kubernetes Hardening Guidance
```

## Chef InSpec Examples

### CIS Kubernetes Benchmark

```ruby
# controls/kubernetes_cis.rb
control 'cis-kubernetes-1.1.1' do
  impact 1.0
  title 'Ensure API server pod specification file permissions'
  desc 'Ensure that the API server pod specification file has permissions of 644 or more restrictive'

  describe file('/etc/kubernetes/manifests/kube-apiserver.yaml') do
    it { should exist }
    its('mode') { should cmp <= 0644 }
    its('owner') { should eq 'root' }
    its('group') { should eq 'root' }
  end
end

control 'cis-kubernetes-1.2.1' do
  impact 1.0
  title 'Ensure anonymous auth is disabled'
  desc 'Disable anonymous requests to the API server'

  describe processes('kube-apiserver') do
    its('commands') { should include '--anonymous-auth=false' }
  end
end
```

### AWS CIS Benchmark

```ruby
# controls/aws_cis.rb
control 'cis-aws-2.1.1' do
  impact 1.0
  title 'Ensure S3 Bucket Policy is set to deny HTTP requests'

  aws_s3_buckets.bucket_names.each do |bucket|
    describe aws_s3_bucket(bucket_name: bucket) do
      it { should have_secure_transport_enabled }
    end
  end
end

control 'cis-aws-2.1.2' do
  impact 1.0
  title 'Ensure MFA Delete is enabled on S3 buckets'

  aws_s3_buckets.bucket_names.each do |bucket|
    describe aws_s3_bucket(bucket_name: bucket) do
      its('versioning_mfa_delete') { should eq true }
    end
  end
end
```

## Sigstore/Cosign Examples

### Sign Container Images

```bash
# Generate key pair (one-time)
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key myregistry/myapp:v1.0.0

# Verify image
cosign verify --key cosign.pub myregistry/myapp:v1.0.0
```

### Keyless Signing (OIDC)

```yaml
# GitHub Actions workflow
- name: Sign image with Cosign
  uses: sigstore/cosign-installer@main

- name: Sign the images with GitHub OIDC Token
  env:
    DIGEST: ${{ steps.build.outputs.digest }}
  run: |
    cosign sign --yes ghcr.io/myorg/myapp@${DIGEST}
```

### Kubernetes Admission with Cosign

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signature
spec:
  validationFailureAction: Enforce
  rules:
    - name: verify-signature
      match:
        resources:
          kinds:
            - Pod
      verifyImages:
        - image: "ghcr.io/myorg/*"
          key: |-
            -----BEGIN PUBLIC KEY-----
            MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
            -----END PUBLIC KEY-----
```
