# LLM Prompts for C4 Diagrams

Effective prompts for AI-assisted architecture visualization using Claude, GPT-4, and other LLMs.

---

## Overview

LLMs can significantly accelerate C4 diagram creation, but require careful prompting to produce accurate, useful output. This guide provides tested prompts for each diagram type and output format.

### Key Principles

1. **Be specific about output format** - Structurizr DSL, PlantUML, or Mermaid
2. **Provide context** - System description, constraints, existing architecture
3. **One level at a time** - Don't ask for all four levels in one prompt
4. **Iterate and refine** - Start broad, then add detail
5. **Validate output** - LLMs can hallucinate technologies and patterns

### LLM Capabilities (2025)

| Model | Structurizr DSL | PlantUML | Mermaid | Quality |
|-------|-----------------|----------|---------|---------|
| Claude (Opus/Sonnet) | Excellent | Excellent | Good | High |
| GPT-4 | Good | Excellent | Excellent | High |
| GPT-4o | Good | Good | Good | Medium |
| Gemini Pro | Good | Good | Good | Medium |
| Local LLMs (70B+) | Fair | Good | Good | Variable |

---

## System Description Prompts

### Initial System Description Template

```markdown
**Prompt:**

I need to create C4 architecture diagrams for the following system:

**System Name:** [Name]

**Purpose:** [1-2 sentences describing what the system does]

**Users:**
- [User type 1]: [what they do]
- [User type 2]: [what they do]

**Key Features:**
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

**Technical Constraints:**
- [Constraint 1, e.g., "Must integrate with existing Oracle database"]
- [Constraint 2, e.g., "Cloud-native, deployed on AWS"]

**External Integrations:**
- [System 1]: [purpose]
- [System 2]: [purpose]

Please create a [Level 1/2/3] C4 diagram in [Structurizr DSL/PlantUML/Mermaid] format.
```

### Example: E-Commerce System Description

```markdown
**Prompt:**

I need to create C4 architecture diagrams for the following system:

**System Name:** ShopFlow E-Commerce Platform

**Purpose:** Multi-tenant e-commerce platform allowing merchants to create online stores and sell products to customers.

**Users:**
- Customers: Browse products, place orders, track shipments
- Merchants: Manage products, fulfill orders, view analytics
- Platform Admins: Manage tenants, monitor platform health

**Key Features:**
1. Product catalog with search and filtering
2. Shopping cart and checkout
3. Payment processing with multiple providers
4. Order management and fulfillment
5. Real-time inventory tracking
6. Analytics and reporting dashboard

**Technical Constraints:**
- Cloud-native on AWS
- Microservices architecture
- Event-driven for scalability
- Multi-tenant with data isolation
- PCI-DSS compliant for payments

**External Integrations:**
- Stripe: Payment processing
- SendGrid: Transactional emails
- Shippo: Shipping label generation
- Algolia: Product search
- Segment: Analytics

Please create a Level 1 System Context diagram in Structurizr DSL format.
```

---

## Level-Specific Prompts

### Level 1: System Context Diagram

**Basic Prompt:**
```markdown
Create a C4 Level 1 (System Context) diagram for [system name] in [format].

The system:
- [Brief description]
- Users: [list users]
- Integrates with: [list external systems]

Include:
- All user types as Person elements
- The main system as a Software System
- All external dependencies as External Systems
- Relationships with meaningful labels
```

**Detailed Prompt:**
```markdown
Create a C4 System Context diagram in Structurizr DSL format.

**System:** Online Banking System
**Description:** Allows customers to manage their bank accounts, transfer money, and pay bills online.

**Users:**
1. Personal Banking Customer - Views accounts, makes transfers
2. Business Banking Customer - Manages business accounts, bulk payments
3. Customer Service Rep - Assists customers, resolves issues

**External Systems:**
1. Core Banking System (internal) - Mainframe, account data
2. Payment Network - SWIFT/ACH transactions
3. Credit Bureau - Credit checks
4. Email Service - SendGrid for notifications
5. SMS Gateway - Twilio for 2FA

**Requirements:**
- Show all relationships with protocols where relevant
- Include brief descriptions for each element
- Use appropriate styling (External tag for external systems)
```

### Level 2: Container Diagram

**Basic Prompt:**
```markdown
Create a C4 Level 2 (Container) diagram for [system name] in [format].

The system contains:
- Frontend: [technologies]
- Backend: [technologies]
- Databases: [list]
- Other infrastructure: [queues, caches, etc.]

Show all inter-container communication with protocols.
```

**Detailed Prompt:**
```markdown
Create a C4 Container diagram in PlantUML format for the Online Banking System.

**Context:** This zooms into the "Online Banking System" from the System Context diagram.

**Containers:**

1. Web Application
   - Technology: React 18, TypeScript
   - Purpose: Customer-facing banking UI
   - Served as: Single Page Application

2. Mobile App
   - Technology: React Native
   - Purpose: iOS and Android banking app

3. API Gateway
   - Technology: Kong
   - Purpose: Authentication, rate limiting, routing

4. Account Service
   - Technology: Java 21, Spring Boot 3
   - Purpose: Account management, balances

5. Transfer Service
   - Technology: Java 21, Spring Boot 3
   - Purpose: Money transfers, payments

6. Notification Service
   - Technology: Python, FastAPI
   - Purpose: Email and SMS notifications

7. Account Database
   - Technology: PostgreSQL 16
   - Purpose: Account data, transactions

8. Session Cache
   - Technology: Redis 7
   - Purpose: Session management, rate limiting

9. Event Bus
   - Technology: Apache Kafka
   - Purpose: Async communication between services

**External Systems:** (from context diagram)
- Core Banking System
- Email Service (SendGrid)
- SMS Gateway (Twilio)

**Communication:**
- Web/Mobile -> API Gateway: HTTPS
- API Gateway -> Services: HTTP/gRPC
- Services -> Databases: SQL
- Services -> Kafka: Events
- Notification Service -> External: HTTPS

Generate complete PlantUML code with proper C4 includes and styling.
```

### Level 3: Component Diagram

**Basic Prompt:**
```markdown
Create a C4 Level 3 (Component) diagram for the [container name] container in [format].

This container is responsible for:
- [Responsibility 1]
- [Responsibility 2]

Show the internal components:
- Controllers/Handlers
- Services/Use Cases
- Repositories/Gateways
- External clients

Include connections to databases and external systems from the container diagram.
```

**Detailed Prompt:**
```markdown
Create a C4 Component diagram in Mermaid format for the Transfer Service container.

**Context:** The Transfer Service handles money transfers within the Online Banking System.

**Responsibilities:**
1. Process internal transfers between accounts
2. Handle external transfers (ACH, wire)
3. Validate transfer limits and compliance
4. Emit events for audit and notifications

**Components:**

Controllers (FastAPI Routers):
- TransferController: POST /transfers, GET /transfers/{id}
- WebhookController: Receives payment network callbacks

Services:
- TransferService: Core transfer logic, orchestration
- ValidationService: Limits, compliance checks
- FraudDetectionService: ML-based fraud scoring

Repositories:
- TransferRepository: SQLAlchemy, transfer records
- AccountRepository: Account balance queries

External Clients:
- PaymentNetworkClient: SWIFT/ACH integration
- AccountServiceClient: Internal account service
- KafkaProducer: Event publishing

**External Dependencies:**
- Transfer Database (PostgreSQL)
- Account Service (internal)
- Payment Network (external)
- Kafka (event bus)

Generate Mermaid C4Component code showing all components and their relationships.
```

---

## Supplementary Diagram Prompts

### Deployment Diagram

```markdown
Create a C4 Deployment diagram in Structurizr DSL for [system name] production environment.

**Infrastructure:**
- Cloud Provider: AWS
- Region: us-east-1
- Orchestration: EKS (Kubernetes 1.28)

**Containers to deploy:**
[List from container diagram]

**Infrastructure details:**
- Load Balancer: ALB
- Database: RDS PostgreSQL (Multi-AZ)
- Cache: ElastiCache Redis
- Message Queue: MSK (Managed Kafka)
- CDN: CloudFront
- Storage: S3

**Scaling:**
- Web pods: 3 replicas
- API pods: 5 replicas
- Worker pods: 2 replicas

Include network boundaries (VPC, subnets) and show how containers map to deployment nodes.
```

### Dynamic Diagram

```markdown
Create a C4 Dynamic diagram in PlantUML for the following user flow:

**Flow:** Customer makes a money transfer

**Steps:**
1. Customer opens transfer form in Web App
2. Customer submits transfer request
3. System validates the transfer
4. System checks fraud score
5. System processes the transfer
6. System sends confirmation notification
7. Customer sees success message

**Participants:**
- Customer (Person)
- Web Application
- API Gateway
- Transfer Service
- Account Service
- Notification Service
- Transfer Database
- Kafka

Number each step and show the request/response flow with appropriate labels.
```

### System Landscape Diagram

```markdown
Create a C4 System Landscape diagram in Structurizr DSL for [organization name].

**Organization:** FinTech Corp

**Software Systems:**
1. Online Banking System - Customer banking
2. Mobile Banking App - Mobile-first banking
3. Internal CRM - Customer relationship management
4. Risk Management System - Fraud detection, compliance
5. Data Warehouse - Analytics and reporting
6. Employee Portal - Internal tools

**External Systems:**
- Core Banking (legacy mainframe)
- Payment Networks (SWIFT, ACH)
- Credit Bureaus
- Regulatory Reporting

**User Groups:**
- Retail Customers
- Business Customers
- Customer Service
- Risk Analysts
- IT Operations

Show all systems and their high-level relationships.
```

---

## Iterative Refinement Prompts

### Adding Detail

```markdown
Take this existing C4 diagram:

[Paste current diagram code]

Please enhance it by:
1. Adding [missing element]
2. Including technology labels for all containers
3. Adding relationship labels with protocols
4. [Other specific improvements]

Keep the same format and style.
```

### Fixing Issues

```markdown
This C4 diagram has some issues:

[Paste diagram code]

Problems:
1. [Issue 1, e.g., "Missing relationship between X and Y"]
2. [Issue 2, e.g., "Wrong technology for database"]
3. [Issue 3, e.g., "Missing external system Z"]

Please fix these issues and return the corrected diagram.
```

### Converting Formats

```markdown
Convert this C4 diagram from [source format] to [target format]:

[Paste source diagram]

Preserve:
- All elements and their descriptions
- All relationships and labels
- Styling where possible

Target format requirements:
- [Any specific requirements for target format]
```

### Extracting from Code

```markdown
Based on this codebase structure, create a C4 Container diagram:

**Project Structure:**
```
myapp/
├── frontend/           # React SPA
│   ├── src/
│   └── package.json
├── backend/
│   ├── api/           # FastAPI
│   ├── worker/        # Celery workers
│   └── requirements.txt
├── docker-compose.yml
└── kubernetes/
    ├── api-deployment.yaml
    └── worker-deployment.yaml
```

**docker-compose.yml contents:**
```yaml
services:
  api:
    build: ./backend
    depends_on: [db, redis, rabbitmq]
  worker:
    build: ./backend
    command: celery worker
  db:
    image: postgres:16
  redis:
    image: redis:7
  rabbitmq:
    image: rabbitmq:3-management
```

Create a C4 Container diagram in Structurizr DSL that accurately represents this architecture.
```

---

## Format-Specific Prompts

### Structurizr DSL

```markdown
Create a Structurizr DSL workspace with the following requirements:

**System:** [Name]

**Views needed:**
1. System Context
2. Container Diagram
3. Component Diagram for [container]
4. Deployment Diagram for production

**Styling requirements:**
- Use standard C4 colors
- External systems should be gray
- Databases should use cylinder shape

**Documentation:**
- Include ADR section
- Add system documentation

Generate a complete workspace.dsl file.
```

### PlantUML

```markdown
Create a PlantUML C4 diagram with:

**Type:** [Context/Container/Component/Deployment]

**Requirements:**
- Use C4-PlantUML library (include statement)
- LAYOUT_WITH_LEGEND()
- Proper grouping with System_Boundary or Container_Boundary
- All relationships labeled

**Elements:**
[List elements]

Generate complete PlantUML code that can be rendered directly.
```

### Mermaid

```markdown
Create a Mermaid C4 diagram compatible with GitHub/GitLab rendering.

**Type:** [C4Context/C4Container/C4Component/C4Deployment]

**Note:** Mermaid C4 is experimental, use supported syntax only.

**Supported elements:**
- Person, Person_Ext
- System, System_Ext, System_Boundary
- Container, Container_Ext, Container_Boundary
- ContainerDb, ContainerQueue
- Component
- Deployment_Node

**Elements:**
[List elements]

Generate Mermaid code block that renders correctly.
```

---

## Validation Prompts

### Review Diagram

```markdown
Review this C4 diagram for correctness and completeness:

[Paste diagram]

Check for:
1. Missing elements (users, systems, containers)
2. Missing or unclear relationships
3. Incorrect abstraction level mixing
4. Missing technology labels
5. Unclear descriptions
6. Best practice violations

Provide specific feedback and suggestions for improvement.
```

### Architecture Review

```markdown
As a software architect, review this C4 diagram:

[Paste diagram]

**Context:** [Brief context about the system]

Evaluate:
1. Does the architecture support the stated requirements?
2. Are there any obvious scalability concerns?
3. Are there missing components (caching, queuing, etc.)?
4. Is the technology stack appropriate?
5. Are there security concerns visible?

Provide actionable recommendations.
```

---

## Multi-Agent Workflow Prompts

### Agent 1: Context Extractor

```markdown
You are a Context Agent. Extract the system context from this description:

[System description or requirements document]

Output a structured summary:
1. System name and purpose
2. User types and their goals
3. External system dependencies
4. Key functional areas

Format as JSON for the next agent.
```

### Agent 2: Container Designer

```markdown
You are a Container Agent. Based on this context:

[Output from Context Agent]

Design the container architecture:
1. Identify frontend containers
2. Identify backend services
3. Identify data stores
4. Identify infrastructure components

Output container definitions with technologies and responsibilities.
Format as JSON for the diagram generator.
```

### Agent 3: Diagram Generator

```markdown
You are a Diagram Generator Agent. Create a C4 diagram from:

[Output from Container Agent]

Generate in [Structurizr DSL/PlantUML/Mermaid] format.
Include all elements and relationships from the input.
Apply standard C4 styling.
```

---

## Prompt Engineering Tips

### Do's

1. **Specify output format explicitly**
   - "Generate in Structurizr DSL format"
   - "Output as PlantUML with C4 includes"

2. **Provide complete context**
   - System purpose
   - User types
   - External dependencies
   - Technical constraints

3. **Ask for one level at a time**
   - Start with System Context
   - Then zoom into Container
   - Then Component for specific containers

4. **Include examples of desired output**
   - "Similar to the banking example in C4 documentation"
   - Paste a template and ask to fill in

5. **Request validation**
   - "Check that all relationships are bidirectional where appropriate"
   - "Verify all containers connect to at least one other element"

### Don'ts

1. **Don't ask for all levels at once**
   - Results in shallow, incomplete diagrams

2. **Don't be vague about technologies**
   - "Use appropriate database" → "Use PostgreSQL 16"

3. **Don't skip the context**
   - LLM needs domain knowledge to make good choices

4. **Don't accept first output blindly**
   - Validate against actual architecture
   - Check for hallucinated APIs or patterns

5. **Don't mix abstraction levels in prompts**
   - Don't ask for components in a container diagram

---

## Common Issues and Fixes

### Issue: Over-complicated architecture

**Symptom:** LLM suggests microservices for a simple CRUD app

**Fix prompt:**
```markdown
Simplify this architecture. The system has:
- < 100 users
- Simple CRUD operations
- Single development team

Recommend a simpler architecture appropriate for this scale.
```

### Issue: Missing relationships

**Symptom:** Elements exist but aren't connected

**Fix prompt:**
```markdown
This diagram has orphaned elements. Add relationships for:
- [Element 1] - how does it communicate?
- [Element 2] - what does it connect to?

Ensure every element has at least one relationship.
```

### Issue: Wrong abstraction level

**Symptom:** Classes appear in Container diagram

**Fix prompt:**
```markdown
This diagram mixes abstraction levels. In a Container diagram:
- Remove class-level details
- Aggregate into logical containers
- Focus on deployable units

Refactor to proper C4 Level 2.
```

### Issue: Hallucinated technologies

**Symptom:** LLM invents APIs or suggests non-existent libraries

**Fix prompt:**
```markdown
Verify all technologies mentioned are real and current (2025):
[List technologies from diagram]

Replace any fictional or outdated technologies with real alternatives.
```

---

## Integration with Development Workflow

### PR Description Generation

```markdown
Generate a PR description that includes C4 diagram changes.

**Code changes:**
[Summary of code changes]

**Architecture impact:**
[How does this change the architecture?]

Generate:
1. Updated C4 diagram (diff if possible)
2. ADR if architectural decision was made
3. PR description explaining the changes
```

### Documentation Generation

```markdown
Based on this C4 workspace:

[Paste Structurizr DSL]

Generate:
1. Architecture overview document (Markdown)
2. Component documentation for each service
3. Data flow documentation
4. Integration guide for new developers
```

### Code Generation from Diagrams

```markdown
Based on this C4 Container diagram:

[Paste diagram]

Generate boilerplate code structure for [Python/TypeScript/Go]:
1. Project structure matching containers
2. Interface definitions for inter-service communication
3. Docker Compose for local development
4. Basic API skeletons
```
