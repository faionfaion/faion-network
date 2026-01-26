# GitLab CI/CD Templates

## Minimal Starter

```yaml
# .gitlab-ci.yml - Minimal starter template
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - npm test

build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  script:
    - echo "Deploying..."
  environment:
    name: production
  when: manual
```

## Standard Node.js Pipeline

```yaml
# .gitlab-ci.yml - Node.js pipeline
variables:
  NODE_VERSION: "20"

default:
  image: node:${NODE_VERSION}-alpine

cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/

workflow:
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_TAG

stages:
  - install
  - test
  - build
  - deploy

install:
  stage: install
  script:
    - npm ci --cache .npm --prefer-offline
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour

lint:
  stage: test
  needs: [install]
  script:
    - npm run lint

test:
  stage: test
  needs: [install]
  script:
    - npm test -- --coverage
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  needs: [test, lint]
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

deploy-staging:
  stage: deploy
  needs: [build]
  script:
    - echo "Deploy to staging"
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  needs: [build]
  script:
    - echo "Deploy to production"
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

## Docker Build Template

```yaml
# .gitlab-ci.yml - Docker build and push
variables:
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  IMAGE_LATEST: $CI_REGISTRY_IMAGE:latest

stages:
  - build
  - scan
  - deploy

docker-build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_BUILDKIT: 1
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      docker build \
        --cache-from $IMAGE_LATEST \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --tag $IMAGE_TAG \
        --tag $IMAGE_LATEST \
        .
    - docker push $IMAGE_TAG
    - docker push $IMAGE_LATEST

trivy-scan:
  stage: scan
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  needs: [docker-build]
  script:
    - trivy image --exit-code 0 --severity HIGH,CRITICAL $IMAGE_TAG
    - trivy image --exit-code 1 --severity CRITICAL $IMAGE_TAG
  allow_failure: false

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  needs: [trivy-scan]
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG
    - kubectl rollout status deployment/app --timeout=5m
  environment:
    name: production
  when: manual
```

## Kubernetes Deployment Template

```yaml
# .gitlab-ci.yml - Kubernetes deployment
.kube-template:
  image: bitnami/kubectl:1.28
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL" --certificate-authority="$KUBE_CA_PEM_FILE"
    - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab --namespace=$KUBE_NAMESPACE
    - kubectl config use-context default

deploy-staging:
  extends: .kube-template
  stage: deploy
  variables:
    KUBE_URL: $STAGING_KUBE_URL
    KUBE_TOKEN: $STAGING_KUBE_TOKEN
    KUBE_NAMESPACE: staging
  environment:
    name: staging
    url: https://staging.example.com
    on_stop: stop-staging
  script:
    - kubectl apply -f k8s/staging/
    - kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE
    - kubectl rollout status deployment/app -n $KUBE_NAMESPACE --timeout=5m
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

stop-staging:
  extends: .kube-template
  stage: deploy
  variables:
    KUBE_NAMESPACE: staging
  environment:
    name: staging
    action: stop
  script:
    - kubectl scale deployment/app --replicas=0 -n $KUBE_NAMESPACE
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  extends: .kube-template
  stage: deploy
  variables:
    KUBE_URL: $PROD_KUBE_URL
    KUBE_TOKEN: $PROD_KUBE_TOKEN
    KUBE_NAMESPACE: production
  environment:
    name: production
    url: https://example.com
  script:
    - kubectl apply -f k8s/production/
    - kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE
    - kubectl rollout status deployment/app -n $KUBE_NAMESPACE --timeout=10m
  rules:
    - if: $CI_COMMIT_TAG
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

## Security Scanning Template

```yaml
# .gitlab-ci.yml - Security scanning
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml

stages:
  - build
  - test
  - security
  - deploy

# Override SAST to run earlier
sast:
  stage: security
  needs: []

dependency_scanning:
  stage: security
  needs: []

secret_detection:
  stage: security
  needs: []

container_scanning:
  stage: security
  needs: [docker-build]
  variables:
    CI_APPLICATION_REPOSITORY: $CI_REGISTRY_IMAGE
    CI_APPLICATION_TAG: $CI_COMMIT_SHA

# Custom security job
security-audit:
  stage: security
  script:
    - npm audit --audit-level=high
    - npx snyk test
  allow_failure: true
```

## Monorepo Template

```yaml
# .gitlab-ci.yml - Monorepo with multiple services
stages:
  - test
  - build
  - deploy

.service-template:
  rules:
    - changes:
        - $SERVICE_PATH/**/*
        - shared/**/*

# API Service
api-test:
  extends: .service-template
  stage: test
  variables:
    SERVICE_PATH: services/api
  script:
    - cd services/api && npm test

api-build:
  extends: .service-template
  stage: build
  variables:
    SERVICE_PATH: services/api
  needs: [api-test]
  script:
    - cd services/api && docker build -t $CI_REGISTRY_IMAGE/api:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE/api:$CI_COMMIT_SHA

# Web Service
web-test:
  extends: .service-template
  stage: test
  variables:
    SERVICE_PATH: services/web
  script:
    - cd services/web && npm test

web-build:
  extends: .service-template
  stage: build
  variables:
    SERVICE_PATH: services/web
  needs: [web-test]
  script:
    - cd services/web && docker build -t $CI_REGISTRY_IMAGE/web:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE/web:$CI_COMMIT_SHA

# Deploy all changed services
deploy:
  stage: deploy
  script:
    - ./scripts/deploy-changed-services.sh
  environment:
    name: production
  when: manual
```

## Review Apps Template

```yaml
# .gitlab-ci.yml - Review apps
.review-template:
  image: bitnami/kubectl:1.28
  variables:
    REVIEW_NAMESPACE: review-$CI_MERGE_REQUEST_IID
    REVIEW_HOST: $CI_MERGE_REQUEST_IID.review.example.com

review-deploy:
  extends: .review-template
  stage: deploy
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    url: https://$REVIEW_HOST
    on_stop: review-stop
    auto_stop_in: 1 week
  script:
    - kubectl create namespace $REVIEW_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
    - envsubst < k8s/review/deployment.yaml | kubectl apply -f -
    - envsubst < k8s/review/service.yaml | kubectl apply -f -
    - envsubst < k8s/review/ingress.yaml | kubectl apply -f -
    - kubectl rollout status deployment/app -n $REVIEW_NAMESPACE --timeout=5m
  rules:
    - if: $CI_MERGE_REQUEST_IID

review-stop:
  extends: .review-template
  stage: deploy
  variables:
    GIT_STRATEGY: none
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    action: stop
  script:
    - kubectl delete namespace $REVIEW_NAMESPACE --ignore-not-found
  when: manual
  rules:
    - if: $CI_MERGE_REQUEST_IID
```

## Scheduled Jobs Template

```yaml
# .gitlab-ci.yml - Scheduled jobs
stages:
  - scheduled

# Nightly cleanup
cleanup-old-images:
  stage: scheduled
  script:
    - ./scripts/cleanup-old-images.sh
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables:
        SCHEDULE_TYPE: cleanup

# Weekly security scan
weekly-security-scan:
  stage: scheduled
  script:
    - npm audit
    - trivy image $CI_REGISTRY_IMAGE:latest
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables:
        SCHEDULE_TYPE: security

# Performance benchmark
performance-test:
  stage: scheduled
  script:
    - k6 run tests/performance/load-test.js
  artifacts:
    paths:
      - results/
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables:
        SCHEDULE_TYPE: performance
```

## Notification Template

```yaml
# .gitlab/ci/notifications.yml
.notify-success:
  after_script:
    - |
      curl -X POST "$SLACK_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"Pipeline succeeded: $CI_PROJECT_NAME ($CI_COMMIT_REF_NAME)\"}"

.notify-failure:
  after_script:
    - |
      if [ "$CI_JOB_STATUS" == "failed" ]; then
        curl -X POST "$SLACK_WEBHOOK" \
          -H "Content-Type: application/json" \
          -d "{\"text\": \"Pipeline failed: $CI_PROJECT_NAME ($CI_COMMIT_REF_NAME)\"}"
      fi

deploy-production:
  extends: .notify-success
  # ... rest of job config
```

## Caching Strategies

```yaml
# Fallback cache with multiple keys
cache:
  - key:
      files:
        - package-lock.json
    paths:
      - node_modules/
    policy: pull-push
  - key: fallback-cache
    paths:
      - node_modules/
    policy: pull

# Distributed cache (S3)
variables:
  CACHE_TYPE: s3
  S3_SERVER_ADDRESS: s3.amazonaws.com
  S3_BUCKET_NAME: gitlab-runner-cache
  S3_BUCKET_LOCATION: us-east-1
```

## Matrix Jobs Template

```yaml
# .gitlab-ci.yml - Matrix builds
test:
  stage: test
  image: node:$NODE_VERSION
  script:
    - npm test
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "22"]
        RUNNER: ["linux", "macos"]

build:
  stage: build
  script:
    - docker build --platform $PLATFORM -t $CI_REGISTRY_IMAGE:$TAG .
  parallel:
    matrix:
      - PLATFORM: linux/amd64
        TAG: amd64
      - PLATFORM: linux/arm64
        TAG: arm64
```
