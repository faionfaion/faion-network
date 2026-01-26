# GitLab CI/CD Examples

## Complete Production Pipeline

```yaml
# .gitlab-ci.yml - Full production pipeline

variables:
  DOCKER_TLS_CERTDIR: "/certs"
  DOCKER_DRIVER: overlay2
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  IMAGE_LATEST: $CI_REGISTRY_IMAGE:latest
  KUBERNETES_VERSION: "1.29"
  NODE_VERSION: "22"

default:
  image: node:${NODE_VERSION}-alpine
  tags:
    - docker
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  interruptible: true

stages:
  - build
  - test
  - security
  - package
  - deploy
  - cleanup

# Global cache
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/
  policy: pull-push

# Pipeline rules
workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_TAG

# ============================================
# BUILD STAGE
# ============================================

build:
  stage: build
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 day
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

docker-build:
  stage: build
  image: docker:26
  services:
    - docker:26-dind
  variables:
    DOCKER_BUILDKIT: 1
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
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

# ============================================
# TEST STAGE
# ============================================

.test-template:
  stage: test
  needs:
    - build
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

unit-test:
  extends: .test-template
  services:
    - name: postgres:16
      alias: db
      variables:
        POSTGRES_DB: test
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
  variables:
    DATABASE_URL: "postgres://test:test@db:5432/test"
  script:
    - npm run test:unit -- --coverage
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/

integration-test:
  extends: .test-template
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

e2e-test:
  extends: .test-template
  image: mcr.microsoft.com/playwright:v1.50.0-focal
  services:
    - name: $IMAGE_TAG
      alias: app
      variables:
        NODE_ENV: test
  variables:
    BASE_URL: "http://app:3000"
  script:
    - npm run test:e2e
  artifacts:
    when: always
    paths:
      - test-results/
      - playwright-report/
    reports:
      junit: junit-e2e.xml
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_MERGE_REQUEST_IID
      changes:
        - "**/*.ts"
        - "**/*.tsx"

lint:
  stage: test
  needs:
    - build
  script:
    - npm run lint
    - npm run format:check
  allow_failure: false

# ============================================
# SECURITY STAGE
# ============================================

include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml

license-scan:
  stage: security
  needs:
    - build
  script:
    - npm audit --audit-level=high
    - npx license-checker --production --failOn "GPL;AGPL"
  allow_failure: true

trivy-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  needs:
    - docker-build
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_TAG
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# ============================================
# DEPLOY STAGE
# ============================================

.deploy-template:
  stage: deploy
  image: bitnami/kubectl:${KUBERNETES_VERSION}
  needs:
    - docker-build
    - unit-test
    - integration-test
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --certificate-authority="$KUBE_CA_PEM_FILE"
    - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab --namespace=$KUBE_NAMESPACE
    - kubectl config use-context default

deploy-staging:
  extends: .deploy-template
  variables:
    KUBE_URL: $STAGING_KUBE_URL
    KUBE_TOKEN: $STAGING_KUBE_TOKEN
    KUBE_NAMESPACE: staging
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop-staging
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE
    - kubectl rollout status deployment/app -n $KUBE_NAMESPACE --timeout=5m
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

stop-staging:
  extends: .deploy-template
  variables:
    KUBE_NAMESPACE: staging
    GIT_STRATEGY: none
  environment:
    name: staging
    action: stop
  script:
    - kubectl scale deployment/app --replicas=0 -n $KUBE_NAMESPACE
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  extends: .deploy-template
  variables:
    KUBE_URL: $PROD_KUBE_URL
    KUBE_TOKEN: $PROD_KUBE_TOKEN
    KUBE_NAMESPACE: production
  environment:
    name: production
    url: https://example.com
  script:
    # Canary deployment
    - kubectl set image deployment/app-canary app=$IMAGE_TAG -n $KUBE_NAMESPACE
    - kubectl rollout status deployment/app-canary -n $KUBE_NAMESPACE --timeout=5m
    # Wait for canary validation
    - sleep 300
    # Full rollout
    - kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE
    - kubectl rollout status deployment/app -n $KUBE_NAMESPACE --timeout=10m
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
    - if: $CI_COMMIT_TAG

# Review apps
review-app:
  stage: deploy
  image: bitnami/kubectl:${KUBERNETES_VERSION}
  needs:
    - docker-build
    - unit-test
  variables:
    REVIEW_NAMESPACE: review-$CI_MERGE_REQUEST_IID
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    url: https://$CI_MERGE_REQUEST_IID.review.example.com
    on_stop: stop-review
    auto_stop_in: 1 week
  script:
    - kubectl create namespace $REVIEW_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    - |
      cat <<EOF | kubectl apply -f -
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: app
        namespace: $REVIEW_NAMESPACE
      spec:
        replicas: 1
        selector:
          matchLabels:
            app: review-$CI_MERGE_REQUEST_IID
        template:
          metadata:
            labels:
              app: review-$CI_MERGE_REQUEST_IID
          spec:
            containers:
            - name: app
              image: $IMAGE_TAG
              ports:
              - containerPort: 3000
      EOF
  rules:
    - if: $CI_MERGE_REQUEST_IID

stop-review:
  stage: deploy
  image: bitnami/kubectl:${KUBERNETES_VERSION}
  variables:
    GIT_STRATEGY: none
    REVIEW_NAMESPACE: review-$CI_MERGE_REQUEST_IID
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    action: stop
  script:
    - kubectl delete namespace $REVIEW_NAMESPACE --ignore-not-found
  when: manual
  rules:
    - if: $CI_MERGE_REQUEST_IID

# ============================================
# CLEANUP STAGE
# ============================================

cleanup-registry:
  stage: cleanup
  image: alpine:latest
  script:
    - apk add --no-cache curl jq
    - |
      REPO_ID=$(curl -s -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories" | jq -r '.[0].id')
      curl -s -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories/$REPO_ID/tags?per_page=100" | \
        jq -r '.[10:] | .[].name' | \
        xargs -I {} curl -X DELETE -H "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/registry/repositories/$REPO_ID/tags/{}"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

## Parent-Child Pipeline (Monorepo)

```yaml
# .gitlab-ci.yml (parent)
stages:
  - trigger

trigger-microservices:
  stage: trigger
  trigger:
    include:
      - local: services/api/.gitlab-ci.yml
        rules:
          - changes:
              - services/api/**/*
      - local: services/web/.gitlab-ci.yml
        rules:
          - changes:
              - services/web/**/*
      - local: services/worker/.gitlab-ci.yml
        rules:
          - changes:
              - services/worker/**/*
    strategy: depend
```

## Dynamic Child Pipeline

```yaml
# Generate pipeline dynamically
generate-pipeline:
  stage: build
  script:
    - |
      cat > generated-pipeline.yml << 'EOF'
      stages:
        - deploy
      EOF

      for service in $(find services -maxdepth 1 -mindepth 1 -type d); do
        name=$(basename $service)
        cat >> generated-pipeline.yml << EOF

      deploy-$name:
        stage: deploy
        script:
          - echo "Deploying $name"
          - ./deploy.sh $name
      EOF
      done
  artifacts:
    paths:
      - generated-pipeline.yml

trigger-generated:
  stage: deploy
  needs:
    - generate-pipeline
  trigger:
    include:
      - artifact: generated-pipeline.yml
        job: generate-pipeline
    strategy: depend
```

## Multi-Project Pipeline

```yaml
# Trigger downstream project
trigger-deploy:
  stage: deploy
  variables:
    IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    UPSTREAM_PROJECT: $CI_PROJECT_PATH
    UPSTREAM_COMMIT: $CI_COMMIT_SHA
  trigger:
    project: devops/kubernetes-deployments
    branch: main
    strategy: depend
```

## Matrix/Parallel Testing

```yaml
# Test multiple versions in parallel
test:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "22"]
        DATABASE: ["postgres:15", "postgres:16"]
  image: node:${NODE_VERSION}
  services:
    - name: ${DATABASE}
      alias: db
  script:
    - npm ci
    - npm test
```

## Auto DevOps Configuration

```yaml
# Using Auto DevOps with customization
include:
  - template: Auto-DevOps.gitlab-ci.yml

variables:
  AUTO_DEVOPS_PLATFORM_TARGET: EKS
  KUBE_INGRESS_BASE_DOMAIN: example.com
  POSTGRES_ENABLED: "true"
  STAGING_ENABLED: "true"
  CANARY_ENABLED: "true"
  INCREMENTAL_ROLLOUT_MODE: manual

  # Performance tuning
  AUTO_DEVOPS_BUILD_IMAGE_CNB_BUILDER: paketobuildpacks/builder:base
  AUTO_DEVOPS_BUILD_IMAGE_CNB_ENABLED: "true"

# Override Auto DevOps jobs
build:
  variables:
    BUILDPACK_URL: https://github.com/heroku/heroku-buildpack-nodejs

production:
  rules:
    - if: $CI_COMMIT_TAG
      when: manual
```

## Python/Django Pipeline

```yaml
variables:
  PYTHON_VERSION: "3.12"
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

default:
  image: python:${PYTHON_VERSION}-slim

stages:
  - build
  - test
  - deploy

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .pip-cache/
    - .venv/

build:
  stage: build
  script:
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install --upgrade pip
    - pip install -r requirements.txt
  artifacts:
    paths:
      - .venv/
    expire_in: 1 hour

test:
  stage: test
  needs:
    - build
  services:
    - name: postgres:16
      alias: db
  variables:
    DATABASE_URL: "postgres://postgres:postgres@db:5432/test"
    DJANGO_SETTINGS_MODULE: "config.settings.test"
  script:
    - source .venv/bin/activate
    - python manage.py migrate
    - pytest --cov=. --cov-report=xml --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  coverage: '/TOTAL.*\s+(\d+%)/'

lint:
  stage: test
  needs:
    - build
  script:
    - source .venv/bin/activate
    - ruff check .
    - mypy .
```

## Go Pipeline

```yaml
variables:
  GO_VERSION: "1.23"
  GOPATH: "$CI_PROJECT_DIR/.go"

default:
  image: golang:${GO_VERSION}

stages:
  - build
  - test
  - deploy

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .go/pkg/mod/

build:
  stage: build
  script:
    - go mod download
    - CGO_ENABLED=0 go build -ldflags="-s -w" -o bin/app ./cmd/app
  artifacts:
    paths:
      - bin/
    expire_in: 1 day

test:
  stage: test
  needs: []  # Run parallel to build
  script:
    - go mod download
    - go test -v -race -coverprofile=coverage.out ./...
    - go tool cover -func=coverage.out
  coverage: '/total:\s+\(statements\)\s+(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

lint:
  stage: test
  needs: []
  image: golangci/golangci-lint:latest
  script:
    - golangci-lint run --timeout 5m
```

## Sources

- [Top 15 GitLab CI/CD Pipeline Examples](https://www.devopstraininginstitute.com/blog/top-15-gitlab-cicd-pipeline-examples)
- [GitLab CI/CD Pipeline: Complete Deployment Automation Guide for 2025](https://ploy.cloud/blog/gitlab-cicd-pipeline-deployment-guide-2025/)
- [GitLab CI/CD Examples](https://docs.gitlab.com/ee/ci/examples/)
