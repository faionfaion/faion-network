# M-DO-020: Container Registry

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #docker, #registry, #ecr, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Docker Hub rate limits block CI/CD. Images scattered across registries are hard to manage. No vulnerability scanning exposes security risks.

## Promise

After this methodology, you will manage container images with private registries. Images will be scanned, versioned, and securely distributed.

## Overview

Container registries store Docker images. AWS ECR, GitHub Container Registry, and self-hosted options provide private storage with access control.

---

## Framework

### Step 1: AWS ECR Setup

```bash
# Create repository
aws ecr create-repository \
  --repository-name myapp \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256

# Get login command
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t myapp:latest .
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

```hcl
# Terraform ECR
resource "aws_ecr_repository" "app" {
  name                 = "myapp"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Environment = var.environment
  }
}

# Lifecycle policy
resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Expire untagged after 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# Repository policy for cross-account access
resource "aws_ecr_repository_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowPull"
        Effect    = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.target_account}:root"
        }
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
      }
    ]
  })
}
```

### Step 2: GitHub Container Registry

```bash
# Login
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and push
docker build -t ghcr.io/owner/myapp:latest .
docker push ghcr.io/owner/myapp:latest

# Pull (public)
docker pull ghcr.io/owner/myapp:latest
```

```yaml
# GitHub Actions workflow
name: Build and Push

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Step 3: Docker Hub

```bash
# Login
docker login -u username

# Build and push
docker build -t username/myapp:latest .
docker push username/myapp:latest

# With organization
docker build -t myorg/myapp:latest .
docker push myorg/myapp:latest
```

```yaml
# GitHub Actions with Docker Hub
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            username/myapp:latest
            username/myapp:${{ github.sha }}
```

### Step 4: Self-Hosted Registry

```yaml
# docker-compose.yml
version: "3.9"

services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
    volumes:
      - registry_data:/var/lib/registry
      - ./auth:/auth

  registry-ui:
    image: joxit/docker-registry-ui:latest
    ports:
      - "8080:80"
    environment:
      REGISTRY_TITLE: My Registry
      REGISTRY_URL: http://registry:5000
      DELETE_IMAGES: true

volumes:
  registry_data:
```

```bash
# Create htpasswd file
mkdir auth
docker run --rm --entrypoint htpasswd registry:2 -Bbn user password > auth/htpasswd

# Push to self-hosted
docker tag myapp:latest localhost:5000/myapp:latest
docker push localhost:5000/myapp:latest
```

### Step 5: Vulnerability Scanning

```bash
# AWS ECR scan results
aws ecr describe-image-scan-findings \
  --repository-name myapp \
  --image-id imageTag=latest

# Trivy (standalone)
trivy image myapp:latest

# Trivy in CI
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:latest
```

```yaml
# GitHub Actions with Trivy
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'HIGH,CRITICAL'

- name: Upload Trivy scan results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

### Step 6: Image Signing

```bash
# Install cosign
brew install sigstore/tap/cosign

# Generate key pair
cosign generate-key-pair

# Sign image
cosign sign --key cosign.key ghcr.io/owner/myapp:latest

# Verify signature
cosign verify --key cosign.pub ghcr.io/owner/myapp:latest
```

```yaml
# GitHub Actions with cosign
- name: Sign the images
  env:
    COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
    COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
  run: |
    cosign sign --key env://COSIGN_PRIVATE_KEY \
      ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.build.outputs.digest }}
```

---

## Templates

### Multi-Architecture Build

```yaml
name: Multi-arch Build

on:
  push:
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.ref_name }}
            ghcr.io/${{ github.repository }}:latest
```

### Kubernetes ImagePullSecrets

```yaml
# Create secret
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>

---
# Use in deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      imagePullSecrets:
        - name: regcred
      containers:
        - name: app
          image: 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
```

---

## Common Mistakes

1. **Using :latest in production** - Pin specific versions
2. **No lifecycle policy** - Registry fills up
3. **No vulnerability scanning** - Security risks hidden
4. **Sharing credentials** - Use service accounts
5. **No image signing** - Can't verify authenticity

---

## Checklist

- [ ] Private registry configured
- [ ] Lifecycle policy for cleanup
- [ ] Vulnerability scanning enabled
- [ ] Image signing implemented
- [ ] Access policies defined
- [ ] Multi-arch builds (if needed)
- [ ] CI/CD integration
- [ ] Pull secrets for Kubernetes

---

## Next Steps

- M-DO-003: Docker Basics
- M-DO-005: Kubernetes Basics
- M-DO-001: GitHub Actions

---

*Methodology M-DO-020 v1.0*
