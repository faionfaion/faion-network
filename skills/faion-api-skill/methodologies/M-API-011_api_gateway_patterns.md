# M-API-011: API Gateway Patterns

## Metadata
- **ID:** M-API-011
- **Category:** API
- **Difficulty:** Advanced
- **Tags:** [api, gateway, microservices, kong, aws]
- **Agent:** faion-api-agent

---

## Problem

With multiple microservices:
- Clients need to know about each service
- Cross-cutting concerns duplicated everywhere
- No central point for auth, rate limiting, logging
- Service discovery becomes complex
- Protocol translation needed (REST/GraphQL/gRPC)

An API Gateway solves these by providing a single entry point.

---

## Framework

### Step 1: Understand Gateway Responsibilities

| Responsibility | Description |
|----------------|-------------|
| Routing | Direct requests to correct service |
| Authentication | Validate tokens, API keys |
| Rate Limiting | Throttle requests |
| Load Balancing | Distribute traffic |
| Caching | Cache responses |
| Request/Response Transform | Modify payloads |
| Protocol Translation | REST to gRPC, etc. |
| Circuit Breaking | Prevent cascade failures |
| Logging/Monitoring | Centralized observability |

### Step 2: Choose Gateway Solution

| Solution | Type | Best For |
|----------|------|----------|
| Kong | Self-hosted | Flexibility, plugins |
| AWS API Gateway | Managed | AWS ecosystem |
| Nginx | Self-hosted | Simple routing |
| Traefik | Self-hosted | Kubernetes native |
| Cloudflare | Edge | Global distribution |
| Express Gateway | Self-hosted | Node.js teams |

### Step 3: Design Gateway Architecture

**Basic pattern:**

```
                    ┌─────────────┐
    Clients ───────>│ API Gateway │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Users    │    │ Orders   │    │ Products │
    │ Service  │    │ Service  │    │ Service  │
    └──────────┘    └──────────┘    └──────────┘
```

**BFF (Backend for Frontend):**

```
    Web App ────────> Web BFF ─────┐
                                   ▼
    Mobile App ─────> Mobile BFF ──┼──> Microservices
                                   ▲
    Admin ──────────> Admin BFF ───┘
```

### Step 4: Configure Kong Gateway

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  kong-database:
    image: postgres:13
    environment:
      POSTGRES_USER: kong
      POSTGRES_DB: kong
      POSTGRES_PASSWORD: kongpass

  kong-migration:
    image: kong:3.4
    command: kong migrations bootstrap
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: kongpass
    depends_on:
      - kong-database

  kong:
    image: kong:3.4
    environment:
      KONG_DATABASE: postgres
      KONG_PG_HOST: kong-database
      KONG_PG_PASSWORD: kongpass
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: 0.0.0.0:8001
    ports:
      - "8000:8000"  # Proxy
      - "8001:8001"  # Admin API
    depends_on:
      - kong-migration
```

**Configure services and routes:**

```bash
# Add Users service
curl -X POST http://localhost:8001/services \
  -d name=users-service \
  -d url=http://users:3000

# Add route
curl -X POST http://localhost:8001/services/users-service/routes \
  -d paths[]=/api/v1/users \
  -d strip_path=false

# Add Orders service
curl -X POST http://localhost:8001/services \
  -d name=orders-service \
  -d url=http://orders:3000

curl -X POST http://localhost:8001/services/orders-service/routes \
  -d paths[]=/api/v1/orders \
  -d strip_path=false
```

**Add plugins:**

```bash
# Rate limiting
curl -X POST http://localhost:8001/services/users-service/plugins \
  -d name=rate-limiting \
  -d config.minute=100 \
  -d config.policy=local

# JWT authentication
curl -X POST http://localhost:8001/services/users-service/plugins \
  -d name=jwt

# Request transformation
curl -X POST http://localhost:8001/services/users-service/plugins \
  -d name=request-transformer \
  -d config.add.headers=X-Request-ID:$(uuidgen)

# CORS
curl -X POST http://localhost:8001/plugins \
  -d name=cors \
  -d config.origins=* \
  -d config.methods=GET,POST,PUT,DELETE \
  -d config.headers=Authorization,Content-Type
```

### Step 5: Configure AWS API Gateway

**Terraform configuration:**

```hcl
# api_gateway.tf
resource "aws_api_gateway_rest_api" "main" {
  name        = "my-api"
  description = "Main API Gateway"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

# Users resource
resource "aws_api_gateway_resource" "users" {
  rest_api_id = aws_api_gateway_rest_api.main.id
  parent_id   = aws_api_gateway_rest_api.main.root_resource_id
  path_part   = "users"
}

# GET /users
resource "aws_api_gateway_method" "get_users" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_resource.users.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id
}

resource "aws_api_gateway_integration" "get_users" {
  rest_api_id             = aws_api_gateway_rest_api.main.id
  resource_id             = aws_api_gateway_resource.users.id
  http_method             = aws_api_gateway_method.get_users.http_method
  type                    = "HTTP_PROXY"
  integration_http_method = "GET"
  uri                     = "http://${var.users_service_url}/users"
}

# Cognito authorizer
resource "aws_api_gateway_authorizer" "cognito" {
  name          = "cognito-authorizer"
  rest_api_id   = aws_api_gateway_rest_api.main.id
  type          = "COGNITO_USER_POOLS"
  provider_arns = [aws_cognito_user_pool.main.arn]
}

# Rate limiting via usage plan
resource "aws_api_gateway_usage_plan" "basic" {
  name = "basic-plan"

  api_stages {
    api_id = aws_api_gateway_rest_api.main.id
    stage  = aws_api_gateway_stage.prod.stage_name
  }

  throttle_settings {
    burst_limit = 100
    rate_limit  = 50
  }

  quota_settings {
    limit  = 10000
    period = "MONTH"
  }
}

# Deployment
resource "aws_api_gateway_deployment" "main" {
  rest_api_id = aws_api_gateway_rest_api.main.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.users.id,
      aws_api_gateway_method.get_users.id,
      aws_api_gateway_integration.get_users.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.main.id
  rest_api_id   = aws_api_gateway_rest_api.main.id
  stage_name    = "prod"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format          = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      responseLength = "$context.responseLength"
    })
  }
}
```

### Step 6: Implement Circuit Breaker

**Kong with circuit breaker:**

```bash
# Add circuit breaker plugin
curl -X POST http://localhost:8001/services/orders-service/plugins \
  -d name=circuit-breaker \
  -d config.window_size=10 \
  -d config.volume_threshold=5 \
  -d config.error_threshold_percentage=50 \
  -d config.timeout=60
```

**Custom implementation (Node.js):**

```javascript
// circuitBreaker.js
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 30000;
    this.state = 'CLOSED';
    this.failures = 0;
    this.lastFailureTime = null;
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime >= this.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    this.lastFailureTime = Date.now();

    if (this.failures >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }
}

// Usage in gateway
const ordersBreaker = new CircuitBreaker({
  failureThreshold: 5,
  resetTimeout: 30000
});

app.get('/api/v1/orders', async (req, res) => {
  try {
    const data = await ordersBreaker.execute(() =>
      axios.get('http://orders-service/orders')
    );
    res.json(data);
  } catch (error) {
    if (error.message === 'Circuit breaker is OPEN') {
      res.status(503).json({
        error: 'Service temporarily unavailable',
        retryAfter: 30
      });
    } else {
      res.status(500).json({ error: 'Internal error' });
    }
  }
});
```

### Step 7: Implement Request Aggregation

**GraphQL as aggregation layer:**

```javascript
// gateway/schema.js
const { ApolloServer, gql } = require('apollo-server-express');
const { RESTDataSource } = require('apollo-datasource-rest');

class UsersAPI extends RESTDataSource {
  constructor() {
    super();
    this.baseURL = 'http://users-service/';
  }

  async getUser(id) {
    return this.get(`users/${id}`);
  }
}

class OrdersAPI extends RESTDataSource {
  constructor() {
    super();
    this.baseURL = 'http://orders-service/';
  }

  async getOrdersByUser(userId) {
    return this.get(`orders?userId=${userId}`);
  }
}

const typeDefs = gql`
  type User {
    id: ID!
    email: String!
    name: String
    orders: [Order!]!
  }

  type Order {
    id: ID!
    total: Float!
    status: String!
  }

  type Query {
    user(id: ID!): User
  }
`;

const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return dataSources.usersAPI.getUser(id);
    }
  },
  User: {
    orders: async (user, _, { dataSources }) => {
      return dataSources.ordersAPI.getOrdersByUser(user.id);
    }
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  dataSources: () => ({
    usersAPI: new UsersAPI(),
    ordersAPI: new OrdersAPI()
  })
});
```

---

## Templates

### Gateway Configuration Checklist

```markdown
## API Gateway Setup

### Routing
- [ ] Services registered
- [ ] Routes configured
- [ ] Path stripping configured
- [ ] Method restrictions

### Security
- [ ] Authentication configured
- [ ] API key management
- [ ] CORS settings
- [ ] SSL/TLS termination

### Traffic Management
- [ ] Rate limiting per tier
- [ ] Circuit breakers
- [ ] Load balancing
- [ ] Retry policies

### Observability
- [ ] Access logging
- [ ] Metrics collection
- [ ] Distributed tracing
- [ ] Health checks

### Deployment
- [ ] Blue-green deployment ready
- [ ] Canary release support
- [ ] Rollback procedures
```

### Kong Configuration (declarative)

```yaml
# kong.yml
_format_version: "3.0"

services:
  - name: users-service
    url: http://users:3000
    routes:
      - name: users-route
        paths:
          - /api/v1/users
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          policy: local
      - name: jwt
      - name: cors
        config:
          origins: ["*"]
          methods: [GET, POST, PUT, DELETE]

  - name: orders-service
    url: http://orders:3000
    routes:
      - name: orders-route
        paths:
          - /api/v1/orders
        strip_path: false
    plugins:
      - name: rate-limiting
        config:
          minute: 50
      - name: jwt

consumers:
  - username: web-app
    jwt_secrets:
      - key: web-app-key
        secret: ${JWT_SECRET}
```

---

## Examples

### Complete Gateway with Express

```javascript
// gateway/index.js
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require('express-rate-limit');
const jwt = require('express-jwt');
const cors = require('cors');

const app = express();

// CORS
app.use(cors({
  origin: ['https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Authorization', 'Content-Type']
}));

// Global rate limiting
app.use(rateLimit({
  windowMs: 60 * 1000,
  max: 100
}));

// JWT authentication
const authenticate = jwt({
  secret: process.env.JWT_SECRET,
  algorithms: ['HS256']
}).unless({ path: ['/health', '/api/v1/auth/login'] });

app.use(authenticate);

// Service routes
const services = {
  users: process.env.USERS_SERVICE_URL,
  orders: process.env.ORDERS_SERVICE_URL,
  products: process.env.PRODUCTS_SERVICE_URL
};

// Proxy to Users service
app.use('/api/v1/users', createProxyMiddleware({
  target: services.users,
  pathRewrite: { '^/api/v1/users': '/users' },
  onProxyReq: (proxyReq, req) => {
    if (req.user) {
      proxyReq.setHeader('X-User-ID', req.user.sub);
    }
    proxyReq.setHeader('X-Request-ID', req.id);
  }
}));

// Proxy to Orders service
app.use('/api/v1/orders', createProxyMiddleware({
  target: services.orders,
  pathRewrite: { '^/api/v1/orders': '/orders' },
  onProxyReq: (proxyReq, req) => {
    if (req.user) {
      proxyReq.setHeader('X-User-ID', req.user.sub);
    }
  }
}));

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Error handler
app.use((err, req, res, next) => {
  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({
      error: { code: 'UNAUTHORIZED', message: 'Invalid token' }
    });
  }
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Internal error' }
  });
});

app.listen(3000);
```

---

## Common Mistakes

1. **Single point of failure**
   - Gateway becomes bottleneck
   - Run multiple instances, use load balancing

2. **Too much logic in gateway**
   - Business logic in gateway
   - Keep gateway thin, delegate to services

3. **No caching strategy**
   - All requests hit backend
   - Cache static/semi-static responses

4. **Ignoring latency**
   - Gateway adds latency
   - Monitor and optimize

5. **No fallbacks**
   - Services down = gateway errors
   - Implement circuit breakers, fallbacks

---

## Next Steps

1. **Start simple** - Nginx or Express proxy
2. **Add authentication** - Centralized JWT validation
3. **Add rate limiting** - Per-client limits
4. **Implement circuit breakers** - Fault tolerance
5. **Add observability** - Logging, metrics, tracing

---

## Related Methodologies

- [M-API-005: API Authentication](./M-API-005_api_authentication.md)
- [M-API-006: Rate Limiting](./M-API-006_rate_limiting.md)
- [M-API-010: API Monitoring](./M-API-010_api_monitoring.md)

---

*Methodology: API Gateway Patterns*
*Version: 1.0*
*Agent: faion-api-agent*
