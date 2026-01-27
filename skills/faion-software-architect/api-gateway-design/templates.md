# API Gateway Templates

Copy-paste templates for common API gateway configurations.

## Kong Templates

### Basic Service and Route

```yaml
# kong-basic.yaml
_format_version: "3.0"
_transform: true

services:
  - name: my-service
    url: http://backend-service:8080
    connect_timeout: 5000
    read_timeout: 30000
    write_timeout: 30000
    retries: 3

routes:
  - name: my-route
    service: my-service
    paths:
      - /api/v1/resource
    methods:
      - GET
      - POST
      - PUT
      - DELETE
    strip_path: false
    preserve_host: true
```

### Rate Limiting Plugin

```yaml
# kong-rate-limiting.yaml
plugins:
  - name: rate-limiting
    config:
      minute: 100
      hour: 1000
      policy: local  # or 'redis' for distributed
      fault_tolerant: true
      hide_client_headers: false
      # For Redis policy:
      # redis_host: redis.internal
      # redis_port: 6379
      # redis_database: 0
      # redis_timeout: 2000

  # Per-route rate limiting
  - name: rate-limiting
    route: expensive-route
    config:
      minute: 10
      policy: local
```

### JWT Authentication

```yaml
# kong-jwt-auth.yaml
plugins:
  - name: jwt
    config:
      uri_param_names:
        - jwt
      cookie_names: []
      header_names:
        - authorization
      claims_to_verify:
        - exp
      key_claim_name: iss
      secret_is_base64: false
      run_on_preflight: true

consumers:
  - username: my-app
    custom_id: my-app-v1

jwt_secrets:
  - consumer: my-app
    key: my-issuer
    secret: my-jwt-secret
    algorithm: HS256
```

### API Key Authentication

```yaml
# kong-key-auth.yaml
plugins:
  - name: key-auth
    config:
      key_names:
        - apikey
        - x-api-key
      key_in_body: false
      key_in_header: true
      key_in_query: true
      hide_credentials: true
      run_on_preflight: true

consumers:
  - username: partner-acme
    custom_id: partner-001

keyauth_credentials:
  - consumer: partner-acme
    key: abc123xyz789
```

### Request Transformer

```yaml
# kong-request-transformer.yaml
plugins:
  - name: request-transformer
    config:
      add:
        headers:
          - "X-Gateway: kong"
          - "X-Correlation-ID: $(request_id)"
        querystring:
          - "gateway_version:1.0"
      remove:
        headers:
          - Cookie
          - Authorization
      rename:
        headers:
          - "X-Old-Header:X-New-Header"
      replace:
        headers:
          - "Host:backend.internal"
```

### Response Transformer

```yaml
# kong-response-transformer.yaml
plugins:
  - name: response-transformer
    config:
      add:
        headers:
          - "X-Response-Time: $(latencies.request)"
          - "X-Gateway-Version: 1.0"
      remove:
        headers:
          - Server
          - X-Powered-By
        json:
          - internal_id
          - debug_info
```

### Circuit Breaker (via Upstream)

```yaml
# kong-circuit-breaker.yaml
upstreams:
  - name: my-upstream
    slots: 10000
    healthchecks:
      active:
        healthy:
          interval: 5
          http_statuses:
            - 200
            - 302
          successes: 2
        unhealthy:
          interval: 5
          http_statuses:
            - 429
            - 500
            - 503
          tcp_failures: 2
          timeouts: 3
          http_failures: 3
      passive:
        healthy:
          http_statuses:
            - 200
            - 201
            - 202
            - 203
            - 204
          successes: 5
        unhealthy:
          http_statuses:
            - 429
            - 500
            - 503
          tcp_failures: 2
          timeouts: 3
          http_failures: 3
    targets:
      - target: backend-1.internal:8080
        weight: 100
      - target: backend-2.internal:8080
        weight: 100
```

### Prometheus Metrics

```yaml
# kong-prometheus.yaml
plugins:
  - name: prometheus
    config:
      per_consumer: true
      status_code_metrics: true
      latency_metrics: true
      bandwidth_metrics: true
      upstream_health_metrics: true
```

### CORS Configuration

```yaml
# kong-cors.yaml
plugins:
  - name: cors
    config:
      origins:
        - https://app.example.com
        - https://admin.example.com
      methods:
        - GET
        - POST
        - PUT
        - DELETE
        - PATCH
        - OPTIONS
      headers:
        - Accept
        - Authorization
        - Content-Type
        - X-Request-ID
      exposed_headers:
        - X-Response-Time
        - X-RateLimit-Remaining
      credentials: true
      max_age: 3600
      preflight_continue: false
```

### Complete Production Template

```yaml
# kong-production.yaml
_format_version: "3.0"
_transform: true

services:
  - name: api-service
    url: http://api-backend:8080
    connect_timeout: 5000
    read_timeout: 30000
    write_timeout: 30000
    retries: 3

routes:
  - name: api-v1
    service: api-service
    paths:
      - /api/v1
    methods:
      - GET
      - POST
      - PUT
      - DELETE
      - PATCH
    strip_path: false
    preserve_host: true

upstreams:
  - name: api-backend-upstream
    slots: 10000
    healthchecks:
      active:
        healthy:
          interval: 5
          successes: 2
        unhealthy:
          interval: 5
          tcp_failures: 2
          http_failures: 3
      passive:
        healthy:
          successes: 5
        unhealthy:
          tcp_failures: 2
          http_failures: 3
    targets:
      - target: api-backend-1:8080
        weight: 100
      - target: api-backend-2:8080
        weight: 100

plugins:
  # Authentication
  - name: jwt
    service: api-service
    config:
      header_names:
        - authorization
      claims_to_verify:
        - exp
      key_claim_name: iss

  # Rate limiting
  - name: rate-limiting
    service: api-service
    config:
      minute: 1000
      policy: redis
      redis_host: redis.internal
      redis_port: 6379
      fault_tolerant: true

  # Request ID
  - name: correlation-id
    config:
      header_name: X-Correlation-ID
      generator: uuid
      echo_downstream: true

  # Metrics
  - name: prometheus
    config:
      per_consumer: true
      status_code_metrics: true
      latency_metrics: true

  # Security headers
  - name: response-transformer
    config:
      add:
        headers:
          - "X-Content-Type-Options: nosniff"
          - "X-Frame-Options: DENY"
          - "X-XSS-Protection: 1; mode=block"
      remove:
        headers:
          - Server
          - X-Powered-By

  # Request size limit
  - name: request-size-limiting
    config:
      allowed_payload_size: 10
      size_unit: megabytes

  # IP restriction (optional)
  # - name: ip-restriction
  #   config:
  #     allow:
  #       - 10.0.0.0/8
  #       - 192.168.0.0/16

consumers:
  - username: web-app
    custom_id: web-frontend-v1
  - username: mobile-app
    custom_id: mobile-v1
```

---

## AWS API Gateway Templates

### REST API with Lambda (CloudFormation)

```yaml
# aws-api-gateway-rest.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: REST API Gateway with Lambda integration

Parameters:
  Environment:
    Type: String
    Default: dev
    AllowedValues: [dev, staging, prod]

Resources:
  ApiGateway:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: !Sub '${AWS::StackName}-api'
      Description: REST API Gateway
      EndpointConfiguration:
        Types:
          - REGIONAL

  ApiResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      RestApiId: !Ref ApiGateway
      ParentId: !GetAtt ApiGateway.RootResourceId
      PathPart: 'v1'

  UsersResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      RestApiId: !Ref ApiGateway
      ParentId: !Ref ApiResource
      PathPart: 'users'

  UsersMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      RestApiId: !Ref ApiGateway
      ResourceId: !Ref UsersResource
      HttpMethod: GET
      AuthorizationType: CUSTOM
      AuthorizerId: !Ref ApiAuthorizer
      Integration:
        Type: AWS_PROXY
        IntegrationHttpMethod: POST
        Uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${UsersFunction.Arn}/invocations'

  ApiAuthorizer:
    Type: AWS::ApiGateway::Authorizer
    Properties:
      Name: JWTAuthorizer
      Type: TOKEN
      RestApiId: !Ref ApiGateway
      AuthorizerUri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${AuthorizerFunction.Arn}/invocations'
      AuthorizerResultTtlInSeconds: 300
      IdentitySource: method.request.header.Authorization

  ApiDeployment:
    Type: AWS::ApiGateway::Deployment
    DependsOn: UsersMethod
    Properties:
      RestApiId: !Ref ApiGateway

  ApiStage:
    Type: AWS::ApiGateway::Stage
    Properties:
      StageName: !Ref Environment
      RestApiId: !Ref ApiGateway
      DeploymentId: !Ref ApiDeployment
      MethodSettings:
        - ResourcePath: '/*'
          HttpMethod: '*'
          ThrottlingBurstLimit: 1000
          ThrottlingRateLimit: 500
          CachingEnabled: false

  UsagePlan:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      UsagePlanName: !Sub '${AWS::StackName}-usage-plan'
      ApiStages:
        - ApiId: !Ref ApiGateway
          Stage: !Ref Environment
      Throttle:
        BurstLimit: 500
        RateLimit: 100
      Quota:
        Limit: 10000
        Period: DAY

Outputs:
  ApiEndpoint:
    Value: !Sub 'https://${ApiGateway}.execute-api.${AWS::Region}.amazonaws.com/${Environment}'
```

### HTTP API (Serverless Framework)

```yaml
# serverless.yml
service: my-api

provider:
  name: aws
  runtime: nodejs20.x
  region: ${opt:region, 'us-east-1'}
  stage: ${opt:stage, 'dev'}

  httpApi:
    cors:
      allowedOrigins:
        - https://app.example.com
      allowedHeaders:
        - Content-Type
        - Authorization
        - X-Request-ID
      allowedMethods:
        - GET
        - POST
        - PUT
        - DELETE
      allowCredentials: true
      maxAge: 3600

    authorizers:
      jwtAuthorizer:
        type: jwt
        identitySource: $request.header.Authorization
        issuerUrl: https://auth.example.com/
        audience:
          - api.example.com

functions:
  getUsers:
    handler: src/handlers/users.getAll
    events:
      - httpApi:
          path: /v1/users
          method: get
          authorizer:
            name: jwtAuthorizer

  createUser:
    handler: src/handlers/users.create
    events:
      - httpApi:
          path: /v1/users
          method: post
          authorizer:
            name: jwtAuthorizer

  getOrders:
    handler: src/handlers/orders.getAll
    events:
      - httpApi:
          path: /v1/orders
          method: get
          authorizer:
            name: jwtAuthorizer

custom:
  prune:
    automatic: true
    number: 3
```

### Usage Plan with API Keys

```yaml
# aws-usage-plan.yaml
Resources:
  FreeTierUsagePlan:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      UsagePlanName: free-tier
      Description: Free tier - limited usage
      ApiStages:
        - ApiId: !Ref ApiGateway
          Stage: !Ref Stage
      Throttle:
        BurstLimit: 10
        RateLimit: 1
      Quota:
        Limit: 100
        Period: DAY

  ProTierUsagePlan:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      UsagePlanName: pro-tier
      Description: Pro tier - standard usage
      ApiStages:
        - ApiId: !Ref ApiGateway
          Stage: !Ref Stage
      Throttle:
        BurstLimit: 100
        RateLimit: 50
      Quota:
        Limit: 10000
        Period: DAY

  EnterpriseTierUsagePlan:
    Type: AWS::ApiGateway::UsagePlan
    Properties:
      UsagePlanName: enterprise-tier
      Description: Enterprise tier - unlimited
      ApiStages:
        - ApiId: !Ref ApiGateway
          Stage: !Ref Stage
      Throttle:
        BurstLimit: 1000
        RateLimit: 500
      # No quota for enterprise

  ApiKey:
    Type: AWS::ApiGateway::ApiKey
    Properties:
      Name: partner-api-key
      Enabled: true

  UsagePlanKey:
    Type: AWS::ApiGateway::UsagePlanKey
    Properties:
      KeyId: !Ref ApiKey
      KeyType: API_KEY
      UsagePlanId: !Ref ProTierUsagePlan
```

---

## Traefik Templates

### Basic IngressRoute

```yaml
# traefik-ingress-basic.yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: my-api
  namespace: api
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/api/v1`)
      kind: Rule
      services:
        - name: backend-service
          port: 8080
  tls:
    certResolver: letsencrypt
```

### Middleware Chain

```yaml
# traefik-middleware-chain.yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: api-chain
  namespace: api
spec:
  chain:
    middlewares:
      - name: rate-limit
      - name: circuit-breaker
      - name: retry
      - name: secure-headers
      - name: compress

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: rate-limit
  namespace: api
spec:
  rateLimit:
    average: 100
    burst: 200
    period: 1s
    sourceCriterion:
      ipStrategy:
        depth: 1

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: circuit-breaker
  namespace: api
spec:
  circuitBreaker:
    expression: "NetworkErrorRatio() > 0.30 || ResponseCodeRatio(500, 600, 0, 600) > 0.25"
    checkPeriod: 10s
    fallbackDuration: 30s
    recoveryDuration: 60s

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: retry
  namespace: api
spec:
  retry:
    attempts: 3
    initialInterval: 100ms

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: secure-headers
  namespace: api
spec:
  headers:
    browserXssFilter: true
    contentTypeNosniff: true
    frameDeny: true
    stsIncludeSubdomains: true
    stsPreload: true
    stsSeconds: 31536000
    customRequestHeaders:
      X-Forwarded-Proto: https
    customResponseHeaders:
      X-Gateway: traefik

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: compress
  namespace: api
spec:
  compress:
    excludedContentTypes:
      - text/event-stream

---
# Apply chain to IngressRoute
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: my-api
  namespace: api
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/api/v1`)
      kind: Rule
      middlewares:
        - name: api-chain
      services:
        - name: backend-service
          port: 8080
  tls:
    certResolver: letsencrypt
```

### Strip Prefix and Rewrite

```yaml
# traefik-path-manipulation.yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: strip-api-v1
  namespace: api
spec:
  stripPrefix:
    prefixes:
      - /api/v1

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: add-prefix
  namespace: api
spec:
  addPrefix:
    prefix: /internal

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: replace-path-regex
  namespace: api
spec:
  replacePathRegex:
    regex: ^/api/v([0-9]+)/(.*)
    replacement: /v$1/$2
```

### Basic Auth

```yaml
# traefik-basic-auth.yaml
apiVersion: v1
kind: Secret
metadata:
  name: basic-auth-secret
  namespace: api
type: Opaque
data:
  # htpasswd -nb admin password | base64
  users: YWRtaW46JGFwcjEkLmcyUHBsVkgkM0tGM1lTaGdqQ1dTL1hHamw1UEhNMAo=

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: basic-auth
  namespace: api
spec:
  basicAuth:
    secret: basic-auth-secret
    removeHeader: true
```

### Forward Auth (External Authentication)

```yaml
# traefik-forward-auth.yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: forward-auth
  namespace: api
spec:
  forwardAuth:
    address: http://auth-service:8080/verify
    trustForwardHeader: true
    authResponseHeaders:
      - X-User-ID
      - X-User-Email
      - X-User-Roles
```

---

## Envoy Templates

### Basic Listener and Cluster

```yaml
# envoy-basic.yaml
static_resources:
  listeners:
    - name: listener_0
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 8080
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                codec_type: AUTO
                route_config:
                  name: local_route
                  virtual_hosts:
                    - name: backend
                      domains: ["*"]
                      routes:
                        - match:
                            prefix: "/"
                          route:
                            cluster: backend_cluster
                http_filters:
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router

  clusters:
    - name: backend_cluster
      type: STRICT_DNS
      lb_policy: ROUND_ROBIN
      load_assignment:
        cluster_name: backend_cluster
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: backend-service
                      port_value: 8080
```

### Rate Limiting

```yaml
# envoy-rate-limit.yaml
http_filters:
  - name: envoy.filters.http.local_ratelimit
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
      stat_prefix: http_local_rate_limiter
      token_bucket:
        max_tokens: 1000
        tokens_per_fill: 100
        fill_interval: 1s
      filter_enabled:
        runtime_key: local_rate_limit_enabled
        default_value:
          numerator: 100
          denominator: HUNDRED
      filter_enforced:
        runtime_key: local_rate_limit_enforced
        default_value:
          numerator: 100
          denominator: HUNDRED
      response_headers_to_add:
        - append: false
          header:
            key: x-local-rate-limit
            value: 'true'
```

### Circuit Breaker and Outlier Detection

```yaml
# envoy-circuit-breaker.yaml
clusters:
  - name: backend_cluster
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    circuit_breakers:
      thresholds:
        - priority: DEFAULT
          max_connections: 1000
          max_pending_requests: 1000
          max_requests: 1000
          max_retries: 3
          track_remaining: true
    outlier_detection:
      consecutive_5xx: 5
      consecutive_gateway_failure: 5
      interval: 10s
      base_ejection_time: 30s
      max_ejection_percent: 50
      enforcing_consecutive_5xx: 100
      enforcing_success_rate: 100
      success_rate_minimum_hosts: 3
      success_rate_request_volume: 100
      success_rate_stdev_factor: 1900
```

### JWT Authentication

```yaml
# envoy-jwt-auth.yaml
http_filters:
  - name: envoy.filters.http.jwt_authn
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.jwt_authn.v3.JwtAuthentication
      providers:
        auth0:
          issuer: "https://auth.example.com/"
          audiences:
            - "api.example.com"
          remote_jwks:
            http_uri:
              uri: "https://auth.example.com/.well-known/jwks.json"
              cluster: auth_cluster
              timeout: 5s
            cache_duration: 600s
          forward: true
          forward_payload_header: x-jwt-payload
      rules:
        - match:
            prefix: /api/v1
          requires:
            provider_name: auth0
        - match:
            prefix: /health
```

---

## Apollo Router Templates

### Basic Configuration

```yaml
# router.yaml
supergraph:
  introspection: true
  listen: 0.0.0.0:4000

cors:
  origins:
    - https://app.example.com
  allow_credentials: true

headers:
  all:
    request:
      - propagate:
          matching: "x-.*"

override_subgraph_url:
  users: http://users-subgraph:4001/graphql
  products: http://products-subgraph:4002/graphql
  orders: http://orders-subgraph:4003/graphql
```

### With Authentication and Telemetry

```yaml
# router-production.yaml
supergraph:
  introspection: false
  listen: 0.0.0.0:4000

sandbox:
  enabled: false

homepage:
  enabled: false

cors:
  origins:
    - https://app.example.com
    - https://admin.example.com
  allow_credentials: true

headers:
  all:
    request:
      - propagate:
          matching: "x-.*"
      - insert:
          name: "x-gateway-timestamp"
          value: "{{ now }}"

limits:
  max_depth: 15
  max_height: 200
  max_aliases: 30
  max_root_fields: 20

apq:
  enabled: true

traffic_shaping:
  all:
    timeout: 30s
  subgraphs:
    users:
      timeout: 10s
    products:
      timeout: 15s
    orders:
      timeout: 20s

telemetry:
  instrumentation:
    spans:
      mode: spec_compliant
    instruments:
      default_requirement_level: recommended
  exporters:
    tracing:
      otlp:
        enabled: true
        endpoint: http://otel-collector:4317
        protocol: grpc
    metrics:
      prometheus:
        enabled: true
        listen: 0.0.0.0:9090
        path: /metrics

authentication:
  router:
    jwt:
      jwks:
        - url: https://auth.example.com/.well-known/jwks.json
      header_name: Authorization
      header_value_prefix: Bearer
```

---

## Docker Compose for Local Development

### Kong + PostgreSQL

```yaml
# docker-compose-kong.yaml
version: '3.8'

services:
  kong-database:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: kong
    volumes:
      - kong-db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "kong"]
      interval: 10s
      timeout: 5s
      retries: 5

  kong-migrations:
    image: kong:3.4
    command: kong migrations bootstrap
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kong
    depends_on:
      kong-database:
        condition: service_healthy

  kong:
    image: kong:3.4
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_USER: kong
      KONG_PG_PASSWORD: kong
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8000:8000"
      - "8001:8001"
    depends_on:
      kong-migrations:
        condition: service_completed_successfully
    healthcheck:
      test: ["CMD", "kong", "health"]
      interval: 10s
      timeout: 5s
      retries: 5

  konga:
    image: pantsel/konga:latest
    environment:
      NODE_ENV: development
    ports:
      - "1337:1337"
    depends_on:
      kong:
        condition: service_healthy

volumes:
  kong-db-data:
```

### Traefik

```yaml
# docker-compose-traefik.yaml
version: '3.8'

services:
  traefik:
    image: traefik:v3.0
    command:
      - --api.insecure=true
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.letsencrypt.acme.httpchallenge=true
      - --certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web
      - --certificatesresolvers.letsencrypt.acme.email=admin@example.com
      - --certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json
      - --metrics.prometheus=true
      - --accesslog=true
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik-certs:/letsencrypt

  backend:
    image: my-backend:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`api.example.com`)"
      - "traefik.http.routers.backend.entrypoints=websecure"
      - "traefik.http.routers.backend.tls.certresolver=letsencrypt"
      - "traefik.http.services.backend.loadbalancer.server.port=8080"

volumes:
  traefik-certs:
```

---

## OpenAPI Extension for Gateway Config

```yaml
# openapi-gateway-extensions.yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0

x-kong-plugin-rate-limiting:
  minute: 100
  policy: local

x-kong-plugin-jwt: {}

paths:
  /users:
    get:
      summary: List users
      x-kong-plugin-rate-limiting:
        minute: 1000
      responses:
        '200':
          description: Success

  /users/{id}:
    get:
      summary: Get user by ID
      x-kong-plugin-request-transformer:
        add:
          headers:
            - "X-User-Request: true"
      responses:
        '200':
          description: Success
```

---

## Prometheus Alert Rules

```yaml
# prometheus-alerts.yaml
groups:
  - name: api-gateway-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on API Gateway"
          description: "Error rate is {{ $value | printf \"%.2f\" }}%"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p95 latency on API Gateway"
          description: "p95 latency is {{ $value | printf \"%.2f\" }}s"

      - alert: RateLimitExceeded
        expr: |
          sum(rate(rate_limit_exceeded_total[5m])) > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High rate of rate limit exceeded"
          description: "{{ $value }} requests/sec being rate limited"

      - alert: CircuitBreakerOpen
        expr: |
          circuit_breaker_state{state="open"} == 1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Circuit breaker is open"
          description: "Circuit breaker for {{ $labels.service }} is open"

      - alert: UpstreamUnhealthy
        expr: |
          upstream_health{status="unhealthy"} == 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Upstream service unhealthy"
          description: "Upstream {{ $labels.upstream }} is unhealthy"
```
