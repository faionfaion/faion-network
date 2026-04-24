# API Gateway Design Examples

Real-world API gateway configurations for different scenarios and gateway solutions.

## Example 1: E-Commerce Platform

### Context

- Traffic: 50,000 RPS peak
- Clients: Web, iOS, Android, Partner APIs
- Backend: 15 microservices
- Requirements: High availability, PCI-DSS compliance

### Architecture

```
                    CDN (CloudFront/Cloudflare)
                              |
                    +--------------------+
                    |   Load Balancer    |
                    +--------------------+
                              |
         +--------------------+--------------------+
         |                    |                    |
    Web BFF Gateway    Mobile BFF Gateway    Partner Gateway
         |                    |                    |
    +----+----+          +----+----+          +----+----+
    |    |    |          |    |    |          |    |    |
  User Order Product   User Order Product   Order Product
  Svc  Svc   Svc       Svc  Svc   Svc       Svc   Svc
```

### Kong Configuration

```yaml
# kong.yaml - Declarative Configuration
_format_version: "3.0"
_transform: true

services:
  - name: users-service
    url: http://users-service.internal:8080
    connect_timeout: 5000
    read_timeout: 30000
    write_timeout: 30000
    retries: 3

  - name: orders-service
    url: http://orders-service.internal:8080
    connect_timeout: 5000
    read_timeout: 60000
    write_timeout: 60000
    retries: 2

  - name: products-service
    url: http://products-service.internal:8080
    connect_timeout: 5000
    read_timeout: 30000
    write_timeout: 30000
    retries: 3

routes:
  - name: users-route
    service: users-service
    paths:
      - /api/v1/users
      - /api/v1/auth
    methods:
      - GET
      - POST
      - PUT
      - DELETE
    strip_path: false
    preserve_host: true

  - name: orders-route
    service: orders-service
    paths:
      - /api/v1/orders
    methods:
      - GET
      - POST
      - PUT
    strip_path: false

  - name: products-route
    service: products-service
    paths:
      - /api/v1/products
      - /api/v1/categories
    methods:
      - GET
    strip_path: false

upstreams:
  - name: users-upstream
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
    targets:
      - target: users-service-1.internal:8080
        weight: 100
      - target: users-service-2.internal:8080
        weight: 100
      - target: users-service-3.internal:8080
        weight: 100

plugins:
  # Global rate limiting
  - name: rate-limiting
    config:
      minute: 1000
      policy: redis
      redis_host: redis.internal
      redis_port: 6379
      redis_database: 0
      fault_tolerant: true
      hide_client_headers: false
    enabled: true

  # JWT Authentication
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
    enabled: true

  # Request transformer - add correlation ID
  - name: correlation-id
    config:
      header_name: X-Correlation-ID
      generator: uuid
      echo_downstream: true

  # Prometheus metrics
  - name: prometheus
    config:
      per_consumer: true
      status_code_metrics: true
      latency_metrics: true
      bandwidth_metrics: true
      upstream_health_metrics: true

  # Request size limiting
  - name: request-size-limiting
    config:
      allowed_payload_size: 10
      size_unit: megabytes

consumers:
  - username: web-app
    custom_id: web-frontend-v1
  - username: ios-app
    custom_id: ios-v2.5
  - username: android-app
    custom_id: android-v2.5
  - username: partner-acme
    custom_id: partner-001
```

### Rate Limiting by Consumer

```yaml
# Per-consumer rate limits
plugins:
  - name: rate-limiting
    consumer: web-app
    config:
      minute: 10000
      policy: redis

  - name: rate-limiting
    consumer: ios-app
    config:
      minute: 5000
      policy: redis

  - name: rate-limiting
    consumer: partner-acme
    config:
      minute: 1000
      hour: 50000
      policy: redis
```

---

## Example 2: SaaS Multi-Tenant API

### Context

- Traffic: 10,000 RPS
- Multi-tenant architecture
- Tier-based rate limiting (Free, Pro, Enterprise)
- Requirements: Tenant isolation, usage tracking

### AWS API Gateway Configuration

```yaml
# serverless.yml
service: saas-api-gateway

provider:
  name: aws
  runtime: nodejs20.x
  region: us-east-1
  stage: ${opt:stage, 'dev'}

  apiGateway:
    shouldStartNameWithService: true
    metrics: true

  environment:
    STAGE: ${self:provider.stage}
    REGION: ${self:provider.region}

custom:
  apiGatewayThrottling:
    maxRequestsPerSecond: 10000
    maxConcurrentRequests: 5000

resources:
  Resources:
    # API Gateway
    ApiGatewayRestApi:
      Type: AWS::ApiGateway::RestApi
      Properties:
        Name: ${self:service}-${self:provider.stage}
        Description: SaaS Multi-Tenant API
        EndpointConfiguration:
          Types:
            - REGIONAL

    # Usage Plans
    FreeTierUsagePlan:
      Type: AWS::ApiGateway::UsagePlan
      Properties:
        UsagePlanName: free-tier
        Description: Free tier - 100 requests/day
        ApiStages:
          - ApiId: !Ref ApiGatewayRestApi
            Stage: ${self:provider.stage}
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
        Description: Pro tier - 10000 requests/day
        ApiStages:
          - ApiId: !Ref ApiGatewayRestApi
            Stage: ${self:provider.stage}
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
          - ApiId: !Ref ApiGatewayRestApi
            Stage: ${self:provider.stage}
        Throttle:
          BurstLimit: 1000
          RateLimit: 500

    # Custom Authorizer
    TenantAuthorizer:
      Type: AWS::ApiGateway::Authorizer
      Properties:
        Name: TenantAuthorizer
        Type: TOKEN
        RestApiId: !Ref ApiGatewayRestApi
        AuthorizerUri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${TenantAuthorizerFunction.Arn}/invocations'
        AuthorizerResultTtlInSeconds: 300
        IdentitySource: method.request.header.Authorization

    # WAF Association
    WebACLAssociation:
      Type: AWS::WAFv2::WebACLAssociation
      Properties:
        ResourceArn: !Sub 'arn:aws:apigateway:${AWS::Region}::/restapis/${ApiGatewayRestApi}/stages/${self:provider.stage}'
        WebACLArn: !Ref ApiWebACL

    # WAF WebACL
    ApiWebACL:
      Type: AWS::WAFv2::WebACL
      Properties:
        Name: api-gateway-waf
        Scope: REGIONAL
        DefaultAction:
          Allow: {}
        Rules:
          - Name: RateLimitRule
            Priority: 1
            Action:
              Block: {}
            Statement:
              RateBasedStatement:
                Limit: 2000
                AggregateKeyType: IP
            VisibilityConfig:
              SampledRequestsEnabled: true
              CloudWatchMetricsEnabled: true
              MetricName: RateLimitRule
          - Name: SQLInjectionRule
            Priority: 2
            OverrideAction:
              None: {}
            Statement:
              ManagedRuleGroupStatement:
                VendorName: AWS
                Name: AWSManagedRulesSQLiRuleSet
            VisibilityConfig:
              SampledRequestsEnabled: true
              CloudWatchMetricsEnabled: true
              MetricName: SQLInjectionRule
        VisibilityConfig:
          SampledRequestsEnabled: true
          CloudWatchMetricsEnabled: true
          MetricName: ApiWebACL

functions:
  tenantAuthorizer:
    handler: src/authorizers/tenant.handler
    timeout: 5
    memorySize: 256

  getUsers:
    handler: src/handlers/users.getAll
    events:
      - http:
          path: /v1/tenants/{tenantId}/users
          method: get
          authorizer:
            name: tenantAuthorizer
            resultTtlInSeconds: 300
          request:
            parameters:
              paths:
                tenantId: true
```

### Lambda Authorizer Example

```javascript
// src/authorizers/tenant.js
exports.handler = async (event) => {
  const token = event.authorizationToken?.replace('Bearer ', '');

  if (!token) {
    throw new Error('Unauthorized');
  }

  try {
    const decoded = await verifyToken(token);
    const tenantId = decoded.tenant_id;
    const tier = decoded.tier || 'free';

    return {
      principalId: decoded.sub,
      policyDocument: {
        Version: '2012-10-17',
        Statement: [{
          Action: 'execute-api:Invoke',
          Effect: 'Allow',
          Resource: event.methodArn.replace(/\/[^/]+\/[^/]+$/, '/*/*')
        }]
      },
      context: {
        tenantId,
        tier,
        userId: decoded.sub,
        email: decoded.email
      }
    };
  } catch (error) {
    throw new Error('Unauthorized');
  }
};
```

---

## Example 3: Kubernetes-Native with Traefik

### Context

- Kubernetes cluster
- GitOps workflow (ArgoCD)
- 20+ microservices
- Requirements: Auto-discovery, middleware chain

### Traefik IngressRoute Configuration

```yaml
# traefik-config.yaml
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
  name: compress
  namespace: api
spec:
  compress:
    excludedContentTypes:
      - text/event-stream

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
    customResponseHeaders:
      X-Correlation-ID: "{{uuid}}"

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: strip-prefix-v1
  namespace: api
spec:
  stripPrefix:
    prefixes:
      - /api/v1

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: jwt-auth
  namespace: api
spec:
  plugin:
    jwt:
      secret: "${JWT_SECRET}"
      alg: HS256
      iss: "https://auth.example.com"
      headerName: Authorization
      headerPrefix: Bearer

---
# IngressRoute for Users Service
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: users-api
  namespace: api
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/api/v1/users`)
      kind: Rule
      middlewares:
        - name: rate-limit
        - name: circuit-breaker
        - name: retry
        - name: secure-headers
        - name: jwt-auth
        - name: strip-prefix-v1
      services:
        - name: users-service
          port: 8080
          weight: 100
          passHostHeader: true
          healthCheck:
            path: /health
            interval: 10s
            timeout: 3s
  tls:
    certResolver: letsencrypt
    domains:
      - main: api.example.com

---
# IngressRoute for Orders Service
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: orders-api
  namespace: api
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/api/v1/orders`)
      kind: Rule
      middlewares:
        - name: rate-limit
        - name: circuit-breaker
        - name: retry
        - name: secure-headers
        - name: jwt-auth
        - name: strip-prefix-v1
      services:
        - name: orders-service
          port: 8080
          weight: 100
  tls:
    certResolver: letsencrypt

---
# Health check route (no auth)
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: health-check
  namespace: api
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`api.example.com`) && Path(`/health`)
      kind: Rule
      services:
        - name: health-service
          port: 8080
  tls:
    certResolver: letsencrypt
```

### Traefik Dynamic Configuration

```yaml
# traefik-dynamic.yaml
http:
  routers:
    api-router:
      rule: "Host(`api.example.com`)"
      service: api-service
      entryPoints:
        - websecure
      middlewares:
        - rate-limit
        - circuit-breaker
        - retry
        - secure-headers
      tls:
        certResolver: letsencrypt

  services:
    api-service:
      loadBalancer:
        healthCheck:
          path: /health
          interval: "10s"
          timeout: "3s"
        sticky:
          cookie:
            name: server_id
            secure: true
            httpOnly: true
        servers:
          - url: "http://backend-1:8080"
          - url: "http://backend-2:8080"
          - url: "http://backend-3:8080"

  middlewares:
    rate-limit:
      rateLimit:
        average: 100
        burst: 200

    circuit-breaker:
      circuitBreaker:
        expression: "NetworkErrorRatio() > 0.30"

    retry:
      retry:
        attempts: 3
        initialInterval: 100ms

    secure-headers:
      headers:
        browserXssFilter: true
        contentTypeNosniff: true
        frameDeny: true
        stsIncludeSubdomains: true
        stsSeconds: 31536000
```

---

## Example 4: Envoy with Service Mesh (Istio)

### Context

- Service mesh architecture
- Zero-trust security model
- mTLS everywhere
- Canary deployments

### Envoy Configuration

```yaml
# envoy-config.yaml
admin:
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 9901

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
                            prefix: "/api/v1/users"
                          route:
                            cluster: users_service
                            timeout: 30s
                            retry_policy:
                              retry_on: "5xx,reset,connect-failure"
                              num_retries: 3
                              per_try_timeout: 10s
                              retry_back_off:
                                base_interval: 0.1s
                                max_interval: 1s
                        - match:
                            prefix: "/api/v1/orders"
                          route:
                            cluster: orders_service
                            timeout: 60s
                            retry_policy:
                              retry_on: "5xx,reset"
                              num_retries: 2
                        - match:
                            prefix: "/api/v1/products"
                          route:
                            cluster: products_service
                            timeout: 30s
                http_filters:
                  # Rate limiting
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
                  # JWT Authentication
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
                      rules:
                        - match:
                            prefix: /api/v1
                          requires:
                            provider_name: auth0
                        - match:
                            prefix: /health
                  # Router
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router

  clusters:
    - name: users_service
      type: STRICT_DNS
      lb_policy: ROUND_ROBIN
      circuit_breakers:
        thresholds:
          - priority: DEFAULT
            max_connections: 1000
            max_pending_requests: 1000
            max_requests: 1000
            max_retries: 3
      outlier_detection:
        consecutive_5xx: 5
        interval: 10s
        base_ejection_time: 30s
        max_ejection_percent: 50
      health_checks:
        - timeout: 5s
          interval: 10s
          unhealthy_threshold: 3
          healthy_threshold: 2
          http_health_check:
            path: /health
      load_assignment:
        cluster_name: users_service
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: users-service
                      port_value: 8080

    - name: orders_service
      type: STRICT_DNS
      lb_policy: ROUND_ROBIN
      circuit_breakers:
        thresholds:
          - priority: DEFAULT
            max_connections: 500
            max_pending_requests: 500
            max_requests: 500
      outlier_detection:
        consecutive_5xx: 5
        interval: 10s
        base_ejection_time: 30s
      load_assignment:
        cluster_name: orders_service
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: orders-service
                      port_value: 8080

    - name: products_service
      type: STRICT_DNS
      lb_policy: ROUND_ROBIN
      load_assignment:
        cluster_name: products_service
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: products-service
                      port_value: 8080

    - name: auth_cluster
      type: STRICT_DNS
      lb_policy: ROUND_ROBIN
      transport_socket:
        name: envoy.transport_sockets.tls
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext
      load_assignment:
        cluster_name: auth_cluster
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: auth.example.com
                      port_value: 443
```

### Istio Virtual Service

```yaml
# istio-virtual-service.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-gateway
  namespace: api
spec:
  hosts:
    - api.example.com
  gateways:
    - api-gateway
  http:
    # Canary deployment for users service
    - match:
        - uri:
            prefix: /api/v1/users
          headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: users-service
            subset: canary
            port:
              number: 8080
          weight: 100
      retries:
        attempts: 3
        perTryTimeout: 10s
        retryOn: 5xx,reset,connect-failure
      timeout: 30s

    # Production users service
    - match:
        - uri:
            prefix: /api/v1/users
      route:
        - destination:
            host: users-service
            subset: stable
            port:
              number: 8080
          weight: 90
        - destination:
            host: users-service
            subset: canary
            port:
              number: 8080
          weight: 10
      retries:
        attempts: 3
        perTryTimeout: 10s
      timeout: 30s

    # Orders service
    - match:
        - uri:
            prefix: /api/v1/orders
      route:
        - destination:
            host: orders-service
            port:
              number: 8080
      retries:
        attempts: 2
        perTryTimeout: 20s
      timeout: 60s

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: users-service
  namespace: api
spec:
  host: users-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
```

---

## Example 5: GraphQL Federation with Apollo Router

### Context

- GraphQL API
- Multiple subgraphs (Users, Products, Orders, Reviews)
- Requirements: Federation, performance, caching

### Apollo Router Configuration

```yaml
# router.yaml
supergraph:
  introspection: true
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

# Subgraph configuration
override_subgraph_url:
  users: http://users-subgraph:4001/graphql
  products: http://products-subgraph:4002/graphql
  orders: http://orders-subgraph:4003/graphql
  reviews: http://reviews-subgraph:4004/graphql

# Rate limiting
limits:
  max_depth: 15
  max_height: 200
  max_aliases: 30
  max_root_fields: 20

# Caching
apq:
  enabled: true

# Response caching
preview_entity_cache:
  enabled: true
  redis:
    urls:
      - redis://redis:6379
    ttl: 300s

# Traffic shaping
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
    reviews:
      timeout: 10s

# Circuit breaker
health_check:
  enabled: true
  health_check_interval: 10s

# Telemetry
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

# Authentication
authentication:
  router:
    jwt:
      jwks:
        - url: https://auth.example.com/.well-known/jwks.json
      header_name: Authorization
      header_value_prefix: Bearer

# Coprocessor for custom logic
coprocessor:
  url: http://coprocessor:8080
  timeout: 2s
  router:
    request:
      headers: true
      body: false
    response:
      headers: true
      body: false
```

### Users Subgraph (Apollo Server)

```typescript
// users-subgraph/src/index.ts
import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { gql } from 'graphql-tag';

const typeDefs = gql`
  extend schema
    @link(url: "https://specs.apollo.dev/federation/v2.3",
          import: ["@key", "@shareable", "@external", "@requires"])

  type Query {
    user(id: ID!): User
    users(limit: Int, offset: Int): [User!]!
    me: User
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User!
  }

  type User @key(fields: "id") {
    id: ID!
    email: String!
    name: String!
    avatar: String
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  input CreateUserInput {
    email: String!
    name: String!
  }

  input UpdateUserInput {
    name: String
    avatar: String
  }

  scalar DateTime
`;

const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return dataSources.usersAPI.getUser(id);
    },
    users: async (_, { limit = 10, offset = 0 }, { dataSources }) => {
      return dataSources.usersAPI.getUsers({ limit, offset });
    },
    me: async (_, __, { user, dataSources }) => {
      if (!user) return null;
      return dataSources.usersAPI.getUser(user.id);
    },
  },
  User: {
    __resolveReference: async (user, { dataSources }) => {
      return dataSources.usersAPI.getUser(user.id);
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema({ typeDefs, resolvers }),
});

await server.start();
```

### Products Subgraph with User Extension

```typescript
// products-subgraph/src/index.ts
const typeDefs = gql`
  extend schema
    @link(url: "https://specs.apollo.dev/federation/v2.3",
          import: ["@key", "@shareable", "@external", "@requires"])

  type Query {
    product(id: ID!): Product
    products(categoryId: ID, limit: Int, offset: Int): [Product!]!
    searchProducts(query: String!): [Product!]!
  }

  type Product @key(fields: "id") {
    id: ID!
    name: String!
    description: String
    price: Float!
    currency: String!
    category: Category!
    seller: User!
    reviews: [Review!]!
    averageRating: Float
    createdAt: DateTime!
  }

  type Category @key(fields: "id") {
    id: ID!
    name: String!
    products: [Product!]!
  }

  # Extend User from users subgraph
  extend type User @key(fields: "id") {
    id: ID! @external
    products: [Product!]!  # Products sold by this user
  }

  # Stub for Review from reviews subgraph
  type Review @key(fields: "id", resolvable: false) {
    id: ID!
  }

  scalar DateTime
`;

const resolvers = {
  Product: {
    __resolveReference: async (product, { dataSources }) => {
      return dataSources.productsAPI.getProduct(product.id);
    },
    seller: (product) => ({ __typename: 'User', id: product.sellerId }),
    reviews: (product) =>
      product.reviewIds?.map(id => ({ __typename: 'Review', id })) || [],
  },
  User: {
    products: async (user, _, { dataSources }) => {
      return dataSources.productsAPI.getProductsBySeller(user.id);
    },
  },
};
```

---

## Example 6: APISIX High-Performance Gateway

### Context

- High throughput requirements (100k+ RPS)
- Plugin-based architecture
- Dashboard management
- Multi-tenancy

### APISIX Configuration

```yaml
# apisix.yaml
apisix:
  node_listen:
    - 9080
  enable_ipv6: false
  enable_admin: true
  admin_key:
    - name: admin
      key: edd1c9f034335f136f87ad84b625c8f1
      role: admin

nginx_config:
  error_log: /dev/stderr
  error_log_level: warn
  http:
    enable_access_log: true
    access_log: /dev/stdout
    access_log_format: '{"@timestamp":"$time_iso8601","client_ip":"$remote_addr","request":"$request","status":$status,"body_bytes_sent":$body_bytes_sent,"request_time":$request_time,"upstream_response_time":"$upstream_response_time"}'

etcd:
  host:
    - "http://etcd:2379"
  prefix: /apisix
  timeout: 30

plugins:
  - api-breaker
  - authz-keycloak
  - basic-auth
  - batch-requests
  - consumer-restriction
  - cors
  - echo
  - fault-injection
  - grpc-transcode
  - hmac-auth
  - http-logger
  - ip-restriction
  - jwt-auth
  - kafka-logger
  - key-auth
  - limit-conn
  - limit-count
  - limit-req
  - openid-connect
  - prometheus
  - proxy-cache
  - proxy-mirror
  - proxy-rewrite
  - rate-limiting
  - redirect
  - referer-restriction
  - request-id
  - request-validation
  - response-rewrite
  - serverless-pre-function
  - sls-logger
  - tcp-logger
  - udp-logger
  - uri-blocker
  - wolf-rbac
  - zipkin
  - opentelemetry

plugin_attr:
  prometheus:
    export_addr:
      ip: 0.0.0.0
      port: 9091
  opentelemetry:
    trace_id_source: x-request-id
    resource:
      service.name: APISIX
    collector:
      address: otel-collector:4317
      request_timeout: 3

---
# Routes configuration
routes:
  - id: users-api
    uri: /api/v1/users/*
    name: users-service
    upstream_id: users-upstream
    plugins:
      jwt-auth:
        key: user-key
        secret: my-secret-key
        algorithm: HS256
      limit-count:
        count: 1000
        time_window: 60
        key_type: var
        key: remote_addr
        rejected_code: 429
        rejected_msg: '{"error": "rate limit exceeded"}'
        policy: redis
        redis_host: redis
        redis_port: 6379
      api-breaker:
        break_response_code: 503
        unhealthy:
          http_statuses:
            - 500
            - 502
            - 503
          failures: 3
        healthy:
          http_statuses:
            - 200
          successes: 1
      prometheus:
        prefer_name: true
      request-id:
        header_name: X-Request-ID
        include_in_response: true

  - id: orders-api
    uri: /api/v1/orders/*
    name: orders-service
    upstream_id: orders-upstream
    plugins:
      jwt-auth: {}
      limit-count:
        count: 500
        time_window: 60
        key_type: var
        key: consumer_name
      proxy-cache:
        cache_strategy: memory
        cache_zone: disk_cache_one
        cache_key:
          - "$uri"
          - "-"
          - "$request_method"
        cache_bypass:
          - "$arg_bypass"
        cache_method:
          - GET
        cache_http_status:
          - 200
          - 304
        cache_ttl: 300

  - id: products-api
    uri: /api/v1/products/*
    name: products-service
    upstream_id: products-upstream
    plugins:
      key-auth: {}
      limit-req:
        rate: 100
        burst: 50
        key: remote_addr
      response-rewrite:
        headers:
          X-Gateway: APISIX
          X-Upstream-Time: "$upstream_response_time"

upstreams:
  - id: users-upstream
    name: users-service
    type: roundrobin
    hash_on: vars
    scheme: http
    retries: 3
    retry_timeout: 5
    timeout:
      connect: 5
      send: 30
      read: 30
    checks:
      active:
        type: http
        http_path: /health
        healthy:
          interval: 5
          successes: 2
        unhealthy:
          interval: 5
          http_failures: 3
    nodes:
      - host: users-service-1
        port: 8080
        weight: 100
      - host: users-service-2
        port: 8080
        weight: 100

  - id: orders-upstream
    name: orders-service
    type: roundrobin
    retries: 2
    nodes:
      - host: orders-service
        port: 8080
        weight: 100

  - id: products-upstream
    name: products-service
    type: least_conn
    retries: 3
    nodes:
      - host: products-service-1
        port: 8080
        weight: 100
      - host: products-service-2
        port: 8080
        weight: 100
      - host: products-service-3
        port: 8080
        weight: 100

consumers:
  - username: web-app
    plugins:
      jwt-auth:
        key: web-app-key
        algorithm: HS256

  - username: mobile-app
    plugins:
      jwt-auth:
        key: mobile-app-key
        algorithm: HS256

  - username: partner-api
    plugins:
      key-auth:
        key: partner-api-key-abc123
```

---

## Summary: When to Use Each Gateway

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| AWS-native, serverless | AWS API Gateway | Native integration, auto-scaling |
| Multi-cloud, plugin needs | Kong | Extensive ecosystem, flexible |
| Kubernetes, GitOps | Traefik | Native K8s support, declarative |
| Service mesh, high perf | Envoy + Istio | Zero-trust, fine-grained control |
| GraphQL federation | Apollo Router | Purpose-built, query planning |
| Maximum throughput | APISIX | Highest performance benchmarks |
| Enterprise API mgmt | Apigee | Full lifecycle, monetization |
