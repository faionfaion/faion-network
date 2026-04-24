# GitLab CI/CD Templates

Reusable job templates for common CI/CD patterns.

## Base Templates

### Default Configuration

```yaml
# default.yml - Include at top of .gitlab-ci.yml

default:
  image: node:22-alpine
  tags:
    - docker
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
      - api_failure
  interruptible: true
  before_script:
    - echo "Pipeline $CI_PIPELINE_ID, Job $CI_JOB_NAME"
```

### Workflow Rules

```yaml
# workflow.yml - Pipeline-level rules

workflow:
  rules:
    # Run on default branch
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    # Run on merge requests
    - if: $CI_MERGE_REQUEST_IID
    # Run on tags
    - if: $CI_COMMIT_TAG
    # Run on schedules
    - if: $CI_PIPELINE_SOURCE == "schedule"
    # Skip draft MRs (optional)
    - if: $CI_MERGE_REQUEST_TITLE =~ /^Draft:/
      when: never
```

## Build Templates

### Node.js Build

```yaml
.build-node:
  stage: build
  image: node:${NODE_VERSION:-22}-alpine
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - node_modules/
      - .npm/
    policy: pull-push
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 day

# Usage
build:
  extends: .build-node
  variables:
    NODE_VERSION: "22"
```

### Python Build

```yaml
.build-python:
  stage: build
  image: python:${PYTHON_VERSION:-3.12}-slim
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .pip-cache/
      - .venv/
  script:
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install --upgrade pip wheel
    - pip install -r requirements.txt
  artifacts:
    paths:
      - .venv/
    expire_in: 1 day

# Usage
build:
  extends: .build-python
  variables:
    PYTHON_VERSION: "3.12"
```

### Go Build

```yaml
.build-go:
  stage: build
  image: golang:${GO_VERSION:-1.23}
  variables:
    GOPATH: "$CI_PROJECT_DIR/.go"
    CGO_ENABLED: "0"
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .go/pkg/mod/
  script:
    - go mod download
    - go build -ldflags="-s -w" -o bin/app ./cmd/app
  artifacts:
    paths:
      - bin/
    expire_in: 1 day
```

### Docker Build

```yaml
.build-docker:
  stage: build
  image: docker:26
  services:
    - docker:26-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
    DOCKER_BUILDKIT: "1"
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    IMAGE_LATEST: $CI_REGISTRY_IMAGE:latest
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      docker build \
        --cache-from $IMAGE_LATEST \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --build-arg VERSION=$CI_COMMIT_SHA \
        --tag $IMAGE_TAG \
        --tag $IMAGE_LATEST \
        .
    - docker push $IMAGE_TAG
    - docker push $IMAGE_LATEST
```

## Test Templates

### Unit Test

```yaml
.test-unit:
  stage: test
  script:
    - npm run test:unit -- --coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    when: always
```

### Integration Test with Services

```yaml
.test-integration:
  stage: test
  services:
    - name: postgres:16
      alias: db
      variables:
        POSTGRES_DB: test
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
    - name: redis:7
      alias: redis
  variables:
    DATABASE_URL: "postgres://test:test@db:5432/test"
    REDIS_URL: "redis://redis:6379"
  script:
    - npm run test:integration
  artifacts:
    reports:
      junit: junit-integration.xml
    when: always
```

### E2E Test with Playwright

```yaml
.test-e2e:
  stage: test
  image: mcr.microsoft.com/playwright:v1.50.0-focal
  variables:
    BASE_URL: "http://localhost:3000"
  script:
    - npm ci
    - npm run test:e2e
  artifacts:
    when: always
    paths:
      - test-results/
      - playwright-report/
    reports:
      junit: junit-e2e.xml
```

### Lint Template

```yaml
.lint:
  stage: test
  script:
    - npm run lint
    - npm run format:check
    - npm run typecheck
  allow_failure: false
```

## Security Templates

### Security Scanning Bundle

```yaml
# security.yml - Include for full security scanning

include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/License-Scanning.gitlab-ci.yml

# Override container scanning
container_scanning:
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

### Trivy Scanner

```yaml
.trivy-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  variables:
    TRIVY_CACHE_DIR: ".trivycache/"
  cache:
    paths:
      - .trivycache/
  script:
    - trivy image --exit-code 0 --severity LOW,MEDIUM $IMAGE_TAG
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_TAG
  artifacts:
    reports:
      container_scanning: trivy-report.json
```

### License Compliance

```yaml
.license-scan:
  stage: security
  script:
    - npm audit --audit-level=high
    - npx license-checker --production --failOn "GPL;AGPL;LGPL"
  allow_failure: true
```

## Deploy Templates

### Kubernetes Deploy

```yaml
.deploy-k8s:
  stage: deploy
  image: bitnami/kubectl:${KUBERNETES_VERSION:-1.29}
  before_script:
    - |
      kubectl config set-cluster k8s \
        --server="$KUBE_URL" \
        --certificate-authority="$KUBE_CA_PEM_FILE"
      kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
      kubectl config set-context default \
        --cluster=k8s \
        --user=gitlab \
        --namespace=$KUBE_NAMESPACE
      kubectl config use-context default
  script:
    - kubectl set image deployment/$DEPLOYMENT_NAME $CONTAINER_NAME=$IMAGE_TAG
    - kubectl rollout status deployment/$DEPLOYMENT_NAME --timeout=5m
```

### Helm Deploy

```yaml
.deploy-helm:
  stage: deploy
  image: alpine/helm:3.14
  before_script:
    - helm repo add stable https://charts.helm.sh/stable
    - helm repo update
  script:
    - |
      helm upgrade --install $RELEASE_NAME ./chart \
        --namespace $KUBE_NAMESPACE \
        --set image.tag=$CI_COMMIT_SHA \
        --set image.repository=$CI_REGISTRY_IMAGE \
        --values ./chart/values-${CI_ENVIRONMENT_NAME}.yaml \
        --wait --timeout 10m
```

### SSH Deploy

```yaml
.deploy-ssh:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client rsync
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh && chmod 700 ~/.ssh
    - echo "$SSH_KNOWN_HOSTS" > ~/.ssh/known_hosts
  script:
    - rsync -avz --delete dist/ $SSH_USER@$SSH_HOST:$DEPLOY_PATH/
    - ssh $SSH_USER@$SSH_HOST "cd $DEPLOY_PATH && ./restart.sh"
```

## Environment Templates

### Staging Environment

```yaml
.deploy-staging:
  extends: .deploy-k8s
  variables:
    KUBE_URL: $STAGING_KUBE_URL
    KUBE_TOKEN: $STAGING_KUBE_TOKEN
    KUBE_NAMESPACE: staging
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop-staging
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### Production Environment

```yaml
.deploy-production:
  extends: .deploy-k8s
  variables:
    KUBE_URL: $PROD_KUBE_URL
    KUBE_TOKEN: $PROD_KUBE_TOKEN
    KUBE_NAMESPACE: production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
    - if: $CI_COMMIT_TAG
```

### Review App

```yaml
.review-app:
  stage: deploy
  variables:
    REVIEW_NAMESPACE: review-$CI_MERGE_REQUEST_IID
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    url: https://$CI_MERGE_REQUEST_IID.review.example.com
    on_stop: stop-review
    auto_stop_in: 1 week
  rules:
    - if: $CI_MERGE_REQUEST_IID

.stop-review:
  stage: deploy
  variables:
    GIT_STRATEGY: none
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    action: stop
  script:
    - kubectl delete namespace review-$CI_MERGE_REQUEST_IID --ignore-not-found
  when: manual
  rules:
    - if: $CI_MERGE_REQUEST_IID
```

## Utility Templates

### Notifications

```yaml
.notify-slack:
  after_script:
    - |
      if [ "$CI_JOB_STATUS" == "success" ]; then
        COLOR="good"
        STATUS="succeeded"
      else
        COLOR="danger"
        STATUS="failed"
      fi
      curl -X POST "$SLACK_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{
          \"attachments\": [{
            \"color\": \"$COLOR\",
            \"title\": \"Pipeline $STATUS\",
            \"text\": \"$CI_PROJECT_NAME - $CI_COMMIT_REF_NAME\",
            \"fields\": [
              {\"title\": \"Job\", \"value\": \"$CI_JOB_NAME\", \"short\": true},
              {\"title\": \"Pipeline\", \"value\": \"<$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\", \"short\": true}
            ]
          }]
        }"
```

### Cleanup Registry

```yaml
.cleanup-registry:
  stage: cleanup
  image: alpine:latest
  script:
    - apk add --no-cache curl jq
    - |
      REPO_ID=$(curl -s -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories" | \
        jq -r '.[0].id')

      # Keep last N images
      curl -s -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories/$REPO_ID/tags" | \
        jq -r '.[10:] | .[].name' | \
        xargs -I {} curl -X DELETE -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories/$REPO_ID/tags/{}"
  when: manual
```

## Rules Templates

### Common Rule Patterns

```yaml
# Rules for different scenarios

.rules-default-branch:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

.rules-merge-request:
  rules:
    - if: $CI_MERGE_REQUEST_IID

.rules-tag:
  rules:
    - if: $CI_COMMIT_TAG

.rules-schedule:
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"

.rules-changes-src:
  rules:
    - changes:
        - "src/**/*"
        - "package.json"
        - "package-lock.json"

.rules-manual-prod:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
    - if: $CI_COMMIT_TAG
      when: manual
```

## Usage Example

```yaml
# .gitlab-ci.yml

include:
  - local: .gitlab/ci/default.yml
  - local: .gitlab/ci/workflow.yml
  - local: .gitlab/ci/security.yml

stages:
  - build
  - test
  - security
  - deploy

build:
  extends: .build-node

test:
  extends: .test-unit
  needs:
    - build

lint:
  extends: .lint
  needs:
    - build

deploy-staging:
  extends: .deploy-staging
  needs:
    - test
    - lint

deploy-production:
  extends: .deploy-production
  needs:
    - deploy-staging
```

## Sources

- [GitLab CI/CD YAML Syntax Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab CI/CD Templates](https://docs.gitlab.com/ee/ci/examples/)
- [GitLab best practices](https://www.hostinger.com/tutorials/gitlab-best-practices)
