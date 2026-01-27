# C4 Model Examples

Real-world case studies and diagram examples across different domains.

## Example 1: E-Commerce Platform

### System Context

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ┌─────────┐          ┌─────────────────────────┐              │
│   │Customer │─────────▶│   E-Commerce Platform   │              │
│   │[Person] │  Browse, │   [Software System]     │              │
│   └─────────┘  order   │   Allows customers to   │              │
│                        │   browse and purchase   │              │
│   ┌─────────┐          │   products online       │              │
│   │  Admin  │─────────▶│                         │              │
│   │[Person] │ Manage   └───────────┬─────────────┘              │
│   └─────────┘ catalog              │                            │
│                                    │                            │
│              ┌─────────────────────┼─────────────────────┐      │
│              │                     │                     │      │
│              ▼                     ▼                     ▼      │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│   │  Payment Gateway │  │  Shipping API    │  │ Email Service│  │
│   │  [External]      │  │  [External]      │  │ [External]   │  │
│   │  Stripe/PayPal   │  │  FedEx/UPS       │  │ SendGrid     │  │
│   └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Container Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           E-Commerce Platform                                │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Web App       │    │   Mobile App    │    │   Admin Portal  │         │
│  │   [React]       │    │   [React Native]│    │   [React]       │         │
│  │   Customer UI   │    │   iOS/Android   │    │   Back-office   │         │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘         │
│           │                      │                      │                   │
│           └──────────────────────┼──────────────────────┘                   │
│                                  │                                          │
│                                  ▼                                          │
│                    ┌─────────────────────────┐                              │
│                    │      API Gateway        │                              │
│                    │      [Kong/AWS ALB]     │                              │
│                    │      Routes requests    │                              │
│                    └─────────────┬───────────┘                              │
│                                  │                                          │
│         ┌────────────────────────┼────────────────────────┐                 │
│         │                        │                        │                 │
│         ▼                        ▼                        ▼                 │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐          │
│  │ Product API  │    │   Order API      │    │   User API       │          │
│  │ [Python/     │    │   [Python/       │    │   [Python/       │          │
│  │  FastAPI]    │    │    FastAPI]      │    │    FastAPI]      │          │
│  │ Catalog mgmt │    │   Order workflow │    │   Auth & profile │          │
│  └──────┬───────┘    └────────┬─────────┘    └────────┬─────────┘          │
│         │                     │                       │                     │
│         ▼                     ▼                       ▼                     │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐          │
│  │ Product DB   │    │   Order DB       │    │   User DB        │          │
│  │ [PostgreSQL] │    │   [PostgreSQL]   │    │   [PostgreSQL]   │          │
│  └──────────────┘    └──────────────────┘    └──────────────────┘          │
│                                                                             │
│                    ┌─────────────────────────┐                              │
│                    │     Message Queue       │                              │
│                    │     [RabbitMQ]          │                              │
│                    │     Async processing    │                              │
│                    └─────────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Diagram (Order API)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Order API Container                             │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                           REST Controllers                            │   │
│  │  ┌─────────────┐  ┌─────────────────┐  ┌──────────────────────────┐  │   │
│  │  │OrderCtrl    │  │ CheckoutCtrl    │  │ WebhookCtrl              │  │   │
│  │  │[Controller] │  │ [Controller]    │  │ [Controller]             │  │   │
│  │  │CRUD orders  │  │ Cart→Order      │  │ Payment/Shipping events  │  │   │
│  │  └──────┬──────┘  └───────┬─────────┘  └───────────┬──────────────┘  │   │
│  └─────────┼─────────────────┼────────────────────────┼─────────────────┘   │
│            │                 │                        │                     │
│            └─────────────────┼────────────────────────┘                     │
│                              ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                           Services                                    │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │   │
│  │  │OrderService     │  │PaymentService   │  │NotificationService  │   │   │
│  │  │[Service]        │  │[Service]        │  │[Service]            │   │   │
│  │  │Order lifecycle  │  │Payment flow     │  │Email/SMS dispatch   │   │   │
│  │  └────────┬────────┘  └────────┬────────┘  └──────────┬──────────┘   │   │
│  └───────────┼────────────────────┼──────────────────────┼──────────────┘   │
│              │                    │                      │                  │
│              ▼                    ▼                      ▼                  │
│  ┌────────────────┐    ┌──────────────────┐    ┌─────────────────────────┐  │
│  │OrderRepository │    │ Stripe Client    │    │ Email Client            │  │
│  │[Repository]    │    │ [Gateway]        │    │ [Gateway]               │  │
│  │Data access     │    │ External API     │    │ SendGrid integration    │  │
│  └────────┬───────┘    └────────┬─────────┘    └────────────┬────────────┘  │
│           │                     │                           │               │
└───────────┼─────────────────────┼───────────────────────────┼───────────────┘
            │                     │                           │
            ▼                     ▼                           ▼
     ┌──────────────┐    ┌──────────────────┐    ┌────────────────────────┐
     │  Order DB    │    │ Payment Gateway  │    │ Email Service          │
     │  [PostgreSQL]│    │ [Stripe]         │    │ [SendGrid]             │
     └──────────────┘    └──────────────────┘    └────────────────────────┘
```

---

## Example 2: SaaS Analytics Platform

### System Context

**Scenario:** Multi-tenant analytics platform processing event data from customer applications.

```
Users:
- Product Manager: Views dashboards and reports
- Developer: Integrates SDK, configures events
- Data Analyst: Creates custom queries and exports

External Systems:
- Customer Applications: Send events via SDK
- Data Warehouse: BigQuery for advanced analytics
- Slack/Teams: Notifications and alerts
```

### Container Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Analytics Platform                                 │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                                 │
│  │  Dashboard UI   │    │   SDK/Client    │◄──── Customer Apps              │
│  │  [React/Next.js]│    │   [JavaScript]  │                                 │
│  │  Reports, viz   │    │   Event capture │                                 │
│  └────────┬────────┘    └────────┬────────┘                                 │
│           │                      │                                          │
│           ▼                      ▼                                          │
│  ┌─────────────────────────────────────────┐                                │
│  │            API Gateway [Kong]           │                                │
│  │         Auth, rate limiting, routing    │                                │
│  └───────────────────┬─────────────────────┘                                │
│                      │                                                      │
│    ┌─────────────────┼─────────────────────┐                                │
│    │                 │                     │                                │
│    ▼                 ▼                     ▼                                │
│  ┌──────────┐   ┌───────────┐   ┌────────────────┐                          │
│  │Query API │   │Ingestion  │   │ Management API │                          │
│  │[Go]      │   │API [Go]   │   │ [Python/Django]│                          │
│  │Analytics │   │Event      │   │ Users, orgs,   │                          │
│  │queries   │   │collection │   │ settings       │                          │
│  └────┬─────┘   └─────┬─────┘   └───────┬────────┘                          │
│       │               │                 │                                   │
│       │               ▼                 ▼                                   │
│       │     ┌─────────────────┐  ┌──────────────┐                           │
│       │     │  Kafka          │  │ PostgreSQL   │                           │
│       │     │  [Event Stream] │  │ [Metadata]   │                           │
│       │     └────────┬────────┘  └──────────────┘                           │
│       │              │                                                      │
│       │              ▼                                                      │
│       │     ┌─────────────────┐                                             │
│       │     │ Stream Processor│                                             │
│       │     │ [Flink/Spark]   │                                             │
│       │     │ Aggregations    │                                             │
│       │     └────────┬────────┘                                             │
│       │              │                                                      │
│       └──────────────┼──────────────────────────────────────────────────┐   │
│                      ▼                                                  │   │
│              ┌──────────────────┐                                       │   │
│              │   ClickHouse     │◄──────────────────────────────────────┘   │
│              │   [OLAP DB]      │                                           │
│              │   Fast analytics │                                           │
│              └──────────────────┘                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                      │
                      ▼
          ┌────────────────────┐
          │   BigQuery         │
          │   [External]       │
          │   Long-term storage│
          └────────────────────┘
```

---

## Example 3: Banking System (Classic Simon Brown Example)

### System Context

This is the classic example from Simon Brown's C4 model documentation.

```
Actors:
- Personal Banking Customer: Views account, makes payments
- Customer Service Staff: Assists customers

External Systems:
- Mainframe Banking System: Core banking, accounts
- Email System: Sends notifications
```

### Container Diagram (Internet Banking)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Internet Banking System                               │
│                                                                             │
│  ┌─────────────────┐                    ┌─────────────────┐                 │
│  │   Web App       │                    │   Mobile App    │                 │
│  │   [Java/Spring] │                    │   [Xamarin]     │                 │
│  │   Delivers SPA  │                    │   iOS/Android   │                 │
│  └────────┬────────┘                    └────────┬────────┘                 │
│           │                                      │                          │
│           └──────────────────┬───────────────────┘                          │
│                              │                                              │
│                              ▼                                              │
│                    ┌─────────────────────┐                                  │
│                    │   Single-Page App   │                                  │
│                    │   [JavaScript/      │                                  │
│                    │    Angular]         │                                  │
│                    │   Banking UI        │                                  │
│                    └─────────┬───────────┘                                  │
│                              │                                              │
│                              ▼                                              │
│                    ┌─────────────────────┐                                  │
│                    │   API Application   │                                  │
│                    │   [Java/Spring MVC] │                                  │
│                    │   Backend services  │                                  │
│                    └─────────┬───────────┘                                  │
│                              │                                              │
│              ┌───────────────┼───────────────┐                              │
│              │               │               │                              │
│              ▼               ▼               ▼                              │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐                │
│    │  Database    │  │  Mainframe   │  │  Email System    │                │
│    │  [Oracle]    │  │  [External]  │  │  [External]      │                │
│    │  User data   │  │  Core banking│  │  Notifications   │                │
│    └──────────────┘  └──────────────┘  └──────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Example 4: Microservices - Food Delivery Platform

### System Landscape

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Food Delivery Company                              │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              │
│  │ Customer App    │  │ Restaurant App  │  │ Driver App      │              │
│  │ [Mobile/Web]    │  │ [Tablet/Web]    │  │ [Mobile]        │              │
│  │ Order food      │  │ Manage orders   │  │ Deliveries      │              │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘              │
│           │                    │                    │                       │
│           └────────────────────┼────────────────────┘                       │
│                                ▼                                            │
│                    ┌─────────────────────┐                                  │
│                    │ Food Delivery       │                                  │
│                    │ Platform            │                                  │
│                    │ [Core System]       │                                  │
│                    └─────────┬───────────┘                                  │
│                              │                                              │
│         ┌────────────────────┼────────────────────┐                         │
│         ▼                    ▼                    ▼                         │
│  ┌──────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ CRM System   │  │ Analytics       │  │ Finance System  │                │
│  │ [Internal]   │  │ Platform        │  │ [Internal]      │                │
│  │ Customer     │  │ [Internal]      │  │ Payments,       │                │
│  │ support      │  │ Metrics, KPIs   │  │ settlements     │                │
│  └──────────────┘  └─────────────────┘  └─────────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│ Payment      │ │ Maps API │ │ SMS/Push     │
│ Gateway      │ │ [Google] │ │ Notifications│
│ [Stripe]     │ │          │ │ [Twilio]     │
└──────────────┘ └──────────┘ └──────────────┘
```

### Container Diagram (Food Delivery Platform)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Food Delivery Platform                                │
│                                                                             │
│  ┌─────────────┐                                                            │
│  │ API Gateway │ ◄─── Customer App, Restaurant App, Driver App              │
│  │ [Kong]      │                                                            │
│  └──────┬──────┘                                                            │
│         │                                                                   │
│   ┌─────┴─────┬─────────────┬─────────────┬─────────────┐                  │
│   │           │             │             │             │                  │
│   ▼           ▼             ▼             ▼             ▼                  │
│ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│ │User     │ │Order    │ │Restaurant│ │Delivery  │ │Payment   │            │
│ │Service  │ │Service  │ │Service   │ │Service   │ │Service   │            │
│ │[Go]     │ │[Go]     │ │[Go]      │ │[Go]      │ │[Go]      │            │
│ │Auth,    │ │Order    │ │Menu,     │ │Routing,  │ │Payments, │            │
│ │profiles │ │workflow │ │inventory │ │tracking  │ │refunds   │            │
│ └────┬────┘ └────┬────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘            │
│      │           │           │            │            │                   │
│      │           │           │            │            │                   │
│      ▼           ▼           ▼            ▼            ▼                   │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐             │
│ │User DB  │ │Order DB │ │Rest. DB │ │Redis     │ │Payment DB│             │
│ │[Postgres│ │[Postgres│ │[Postgres│ │[Cache +  │ │[Postgres]│             │
│ └─────────┘ └─────────┘ └─────────┘ │ Geo]     │ └──────────┘             │
│                                     └──────────┘                           │
│                                                                            │
│      ┌─────────────────────────────────────────────────┐                   │
│      │                   Kafka                          │                   │
│      │            [Event Streaming]                     │                   │
│      │    order.created, delivery.assigned, etc.        │                   │
│      └─────────────────────────────────────────────────┘                   │
│                          │                                                  │
│            ┌─────────────┼─────────────┐                                   │
│            ▼             ▼             ▼                                   │
│      ┌──────────┐ ┌──────────┐ ┌──────────┐                                │
│      │Notif.    │ │Analytics │ │Search    │                                │
│      │Service   │ │Service   │ │Service   │                                │
│      │[Python]  │ │[Python]  │ │[Go]      │                                │
│      │Push/SMS  │ │Metrics   │ │Elastic-  │                                │
│      │          │ │ingestion │ │search    │                                │
│      └──────────┘ └──────────┘ └──────────┘                                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Example 5: AI/ML Platform

### Container Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ML Platform                                     │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                                 │
│  │  ML Studio UI   │    │  Jupyter Hub    │                                 │
│  │  [React]        │    │  [JupyterHub]   │                                 │
│  │  Experiment     │    │  Notebooks      │                                 │
│  │  management     │    │  for data sci   │                                 │
│  └────────┬────────┘    └────────┬────────┘                                 │
│           │                      │                                          │
│           └──────────────────────┼──────────────────────────────────────┐   │
│                                  ▼                                      │   │
│                    ┌─────────────────────────┐                          │   │
│                    │      ML API             │                          │   │
│                    │      [Python/FastAPI]   │                          │   │
│                    │      Experiment, model  │                          │   │
│                    │      management         │                          │   │
│                    └─────────────┬───────────┘                          │   │
│                                  │                                      │   │
│         ┌────────────────────────┼────────────────────────┐             │   │
│         │                        │                        │             │   │
│         ▼                        ▼                        ▼             │   │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐       │   │
│  │ MLflow       │    │ Feature Store    │    │ Model Registry   │       │   │
│  │ [MLflow]     │    │ [Feast]          │    │ [MLflow]         │       │   │
│  │ Experiment   │    │ Feature          │    │ Model versioning │       │   │
│  │ tracking     │    │ management       │    │ & deployment     │       │   │
│  └──────┬───────┘    └────────┬─────────┘    └────────┬─────────┘       │   │
│         │                     │                       │                 │   │
│         ▼                     ▼                       ▼                 │   │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐       │   │
│  │ PostgreSQL   │    │ Redis            │    │ S3/MinIO         │       │   │
│  │ [Metadata]   │    │ [Online Store]   │    │ [Artifact Store] │       │   │
│  └──────────────┘    └──────────────────┘    └──────────────────┘       │   │
│                                                                         │   │
│  ┌─────────────────────────────────────────────────────────────────────┐│   │
│  │                    Kubernetes Cluster                                ││   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────────┐ ││   │
│  │  │ Training   │  │ Training   │  │ Inference  │  │ Inference      │ ││   │
│  │  │ Job 1      │  │ Job 2      │  │ Service A  │  │ Service B      │ ││   │
│  │  │ [PyTorch]  │  │ [TensorFlow│  │ [TorchServe│  │ [Triton]       │ ││   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────────┘ ││   │
│  └─────────────────────────────────────────────────────────────────────┘│   │
│                                                                         │   │
│  ┌──────────────────────────────────────────────────────────────────┐   │   │
│  │                    Data Lake [S3/Delta Lake]                     │◄──┘   │
│  │                    Training data, model artifacts                │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Example 6: Dynamic Diagram - Order Checkout Flow

### Scenario: Customer places an order

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Order Checkout Flow                                    │
│                                                                          │
│  1. Customer → Web App: Click "Checkout"                                 │
│  2. Web App → API Gateway: POST /orders/checkout                         │
│  3. API Gateway → Order Service: Create order                            │
│  4. Order Service → User Service: Validate user                          │
│  5. Order Service → Product Service: Check inventory                     │
│  6. Order Service → Payment Service: Process payment                     │
│  7. Payment Service → Stripe: Charge card                                │
│  8. Stripe → Payment Service: Payment confirmed                          │
│  9. Payment Service → Order Service: Payment success                     │
│  10. Order Service → Kafka: Publish order.created                        │
│  11. Notification Service ← Kafka: Consume event                         │
│  12. Notification Service → Email Service: Send confirmation             │
│  13. Order Service → API Gateway: Order response                         │
│  14. API Gateway → Web App: Order confirmation                           │
│  15. Web App → Customer: Display confirmation                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

Sequence:

Customer    Web App    Gateway    Order Svc    Payment    Stripe    Kafka
    │          │          │           │           │         │         │
    │──1──────▶│          │           │           │         │         │
    │          │────2────▶│           │           │         │         │
    │          │          │─────3────▶│           │         │         │
    │          │          │           │◄───4,5───▶│(User,Product)     │
    │          │          │           │─────6────▶│         │         │
    │          │          │           │           │───7────▶│         │
    │          │          │           │           │◄───8────│         │
    │          │          │           │◄────9─────│         │         │
    │          │          │           │───────────10───────▶│         │
    │          │          │◄────13────│           │         │         │
    │          │◄───14────│           │           │         │         │
    │◄───15────│          │           │           │         │         │
```

---

## Example 7: Deployment Diagram

### Production Deployment (AWS)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              AWS Cloud                                       │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         us-east-1 Region                               │  │
│  │                                                                        │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                    VPC (10.0.0.0/16)                             │  │  │
│  │  │                                                                  │  │  │
│  │  │  ┌─────────────────────────────────────────────────────────┐    │  │  │
│  │  │  │              Public Subnets                              │    │  │  │
│  │  │  │  ┌─────────────┐         ┌─────────────┐                │    │  │  │
│  │  │  │  │ ALB         │         │ NAT Gateway │                │    │  │  │
│  │  │  │  │ [Load Bal.] │         │             │                │    │  │  │
│  │  │  │  └──────┬──────┘         └─────────────┘                │    │  │  │
│  │  │  └─────────┼───────────────────────────────────────────────┘    │  │  │
│  │  │            │                                                     │  │  │
│  │  │  ┌─────────▼───────────────────────────────────────────────┐    │  │  │
│  │  │  │              Private Subnets                             │    │  │  │
│  │  │  │                                                          │    │  │  │
│  │  │  │  ┌───────────────────────────────────────────────────┐  │    │  │  │
│  │  │  │  │            EKS Cluster                             │  │    │  │  │
│  │  │  │  │                                                    │  │    │  │  │
│  │  │  │  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │  │    │  │  │
│  │  │  │  │  │ Web App  │ │ API Pods │ │ Worker   │           │  │    │  │  │
│  │  │  │  │  │ Pods (3) │ │ (5)      │ │ Pods (2) │           │  │    │  │  │
│  │  │  │  │  │ [React]  │ │ [FastAPI]│ │ [Celery] │           │  │    │  │  │
│  │  │  │  │  └──────────┘ └──────────┘ └──────────┘           │  │    │  │  │
│  │  │  │  │                                                    │  │    │  │  │
│  │  │  │  └───────────────────────────────────────────────────┘  │    │  │  │
│  │  │  │                                                          │    │  │  │
│  │  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │    │  │  │
│  │  │  │  │ RDS          │  │ ElastiCache  │  │ MSK (Kafka)  │   │    │  │  │
│  │  │  │  │ [PostgreSQL] │  │ [Redis]      │  │              │   │    │  │  │
│  │  │  │  │ Multi-AZ     │  │ Cluster      │  │ 3 brokers    │   │    │  │  │
│  │  │  │  └──────────────┘  └──────────────┘  └──────────────┘   │    │  │  │
│  │  │  │                                                          │    │  │  │
│  │  │  └──────────────────────────────────────────────────────────┘    │  │  │
│  │  │                                                                  │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                                                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │  │
│  │  │ S3           │  │ CloudFront   │  │ Route 53     │                 │  │
│  │  │ [Assets]     │  │ [CDN]        │  │ [DNS]        │                 │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                 │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Open Source Project Examples

### Shopify Architecture (Modular Monolith to Services)

Shopify's architecture evolved from Rails monolith to modular monolith, demonstrating C4 principles:

**System Context:**
- Merchants (manage stores)
- Customers (shop online)
- External: Payment processors, shipping carriers, apps

**Containers:**
- Shopify Admin (React)
- Storefront (Liquid templating)
- Core API (Ruby/Rails)
- Checkout Service (extracted microservice)
- Background Jobs (Sidekiq)

**Key Insight:** Shopify extracted high-scale components (checkout, payments) as services while keeping most functionality in modular monolith.

### Netflix Architecture

**System Context:**
- Subscribers (watch content)
- Content creators (upload)
- External: CDN, device manufacturers

**Containers:**
- Mobile/TV apps
- API Gateway (Zuul)
- Hundreds of microservices
- Cassandra clusters
- Kafka event streaming
- S3 content storage

**Key Insight:** Netflix uses C4-style documentation internally, with each team owning their service's architecture documentation.

### Stripe Architecture

**System Context:**
- Merchants (integrate payments)
- End users (make payments)
- External: Card networks, banks

**Containers:**
- API service (Ruby)
- Dashboard (React)
- Payment processing engine
- Risk/fraud detection
- Reporting and analytics

**Key Insight:** Stripe emphasizes clear API boundaries in their architecture, which maps well to C4 container diagrams.

---

## Best Practices from Examples

### Patterns Observed

1. **API Gateway Pattern:** All examples use an API gateway for routing and authentication
2. **Database per Service:** Microservices examples show isolated databases
3. **Event Streaming:** Kafka/message queues for async communication
4. **Clear Boundaries:** System boundary boxes make scope obvious

### Common Mistakes to Avoid

1. **Too Many Containers:** Keep to 10-15 max per diagram
2. **Missing Technologies:** Always label with specific tech (not just "database")
3. **Unclear Flow:** Number steps in dynamic diagrams
4. **Orphaned Elements:** Every element should connect to something

### Diagram Evolution

| Phase | Focus |
|-------|-------|
| Design | System Context + rough Container diagram |
| Development | Refined Container + Component for complex areas |
| Production | Add Deployment diagrams |
| Maintenance | Update as architecture changes |
