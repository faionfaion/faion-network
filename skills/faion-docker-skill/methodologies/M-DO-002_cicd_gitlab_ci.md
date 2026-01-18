# M-DO-002: CI/CD with GitLab CI

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Beginner
- **Tags:** #devops, #cicd, #gitlab, #methodology
- **Agent:** faion-devops-agent

---

## Problem

GitLab projects need integrated CI/CD. Without pipelines, manual testing and deployment create inconsistency and risk across teams.

## Promise

After this methodology, you will build GitLab CI pipelines that test, build, and deploy automatically. Your team will ship faster with confidence.

## Overview

GitLab CI uses `.gitlab-ci.yml` for pipeline configuration. It integrates with GitLab's container registry, environments, and deployment features.

---

## Framework

### Step 1: Pipeline Structure

```yaml
# .gitlab-ci.yml

# Define stages (executed in order)
stages:
  - test
  - build
  - deploy

# Global defaults
default:
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

# Global variables
variables:
  NODE_ENV: test
```

### Step 2: Basic Jobs

```yaml
# Test job
test:
  stage: test
  script:
    - npm ci
    - npm run lint
    - npm test
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

# Build job
build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
  only:
    - main
    - tags
```

### Step 3: Docker Build

```yaml
build-docker:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - |
      if [ "$CI_COMMIT_BRANCH" == "main" ]; then
        docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
        docker push $CI_REGISTRY_IMAGE:latest
      fi
  only:
    - main
    - tags
```

### Step 4: Environments

```yaml
deploy-staging:
  stage: deploy
  script:
    - ./deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-production:
  stage: deploy
  script:
    - ./deploy.sh production
  environment:
    name: production
    url: https://example.com
  when: manual  # Requires manual trigger
  only:
    - main
```

### Step 5: Rules and Conditions

```yaml
# Modern rules syntax (replaces only/except)
test:
  stage: test
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_TAG
  script:
    - npm test

# With changes filter
build:
  stage: build
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      changes:
        - src/**/*
        - package*.json
  script:
    - npm run build

# Never run on schedules
deploy:
  stage: deploy
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      when: never
    - if: $CI_COMMIT_BRANCH == "main"
  script:
    - ./deploy.sh
```

### Step 6: Matrix Builds

```yaml
test:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "22"]
        DATABASE: ["postgres", "mysql"]
  image: node:${NODE_VERSION}-alpine
  services:
    - name: ${DATABASE}:latest
      alias: db
  script:
    - npm ci
    - npm test
```

---

## Templates

### Complete Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

default:
  image: node:20-alpine

variables:
  npm_config_cache: "$CI_PROJECT_DIR/.npm"

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .npm/
    - node_modules/

# Templates for reuse
.deploy-template:
  image: alpine:latest
  before_script:
    - apk add --no-cache curl openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | ssh-add -

# Jobs
lint:
  stage: test
  script:
    - npm ci
    - npm run lint

test:
  stage: test
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml

build:
  stage: build
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 day
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_TAG

deploy-staging:
  extends: .deploy-template
  stage: deploy
  script:
    - ./scripts/deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-production:
  extends: .deploy-template
  stage: deploy
  script:
    - ./scripts/deploy.sh production
  environment:
    name: production
    url: https://example.com
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Kubernetes Deployment

```yaml
deploy-k8s:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
    entrypoint: [""]
  script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --certificate-authority="$KUBE_CA_PEM"
    - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab
    - kubectl config use-context default
    - kubectl set image deployment/myapp myapp=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  environment:
    name: production
    kubernetes:
      namespace: production
```

### Multi-Project Pipelines

```yaml
# Trigger downstream pipeline
trigger-deploy:
  stage: deploy
  trigger:
    project: group/deploy-project
    branch: main
    strategy: depend
  variables:
    DEPLOY_VERSION: $CI_COMMIT_SHA

# Include from other projects
include:
  - project: 'group/ci-templates'
    ref: main
    file: '/templates/nodejs.yml'
```

---

## Examples

### Security Scanning

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

# Override defaults
sast:
  stage: test
  variables:
    SAST_EXCLUDED_PATHS: "node_modules,dist"

container_scanning:
  stage: test
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

### Review Apps

```yaml
deploy-review:
  stage: deploy
  script:
    - deploy-review-app.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop-review
  rules:
    - if: $CI_MERGE_REQUEST_IID

stop-review:
  stage: deploy
  script:
    - delete-review-app.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
  rules:
    - if: $CI_MERGE_REQUEST_IID
```

---

## Common Mistakes

1. **Not using cache** - Slow pipelines from repeated downloads
2. **Missing artifacts** - Build outputs lost between stages
3. **Only/except deprecated** - Use rules syntax instead
4. **No environment cleanup** - Review apps accumulate
5. **Hardcoded secrets** - Use CI/CD variables

---

## Checklist

- [ ] Stages defined in order
- [ ] Cache configured for dependencies
- [ ] Artifacts passed between stages
- [ ] Docker builds use GitLab registry
- [ ] Environments with URLs
- [ ] Production deploys are manual
- [ ] Security scanning enabled
- [ ] Review apps for MRs

---

## Next Steps

- M-DO-001: GitHub Actions
- M-DO-003: Docker Basics
- M-DO-005: Kubernetes Basics

---

*Methodology M-DO-002 v1.0*
