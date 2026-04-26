# C4 Model Checklist

Step-by-step checklists for creating effective C4 diagrams at each level.

## Pre-Diagram Preparation

### Gather Information

- [ ] Identify the software system to document
- [ ] List all stakeholders and their information needs
- [ ] Collect existing documentation (if any)
- [ ] Interview team members familiar with the system
- [ ] Review codebase structure (for existing systems)
- [ ] Identify external system dependencies
- [ ] Document integration points and protocols

### Define Scope

- [ ] Determine which C4 levels are needed
- [ ] Identify target audience for each diagram
- [ ] Choose tooling (Structurizr, PlantUML, Mermaid, draw.io)
- [ ] Establish naming conventions
- [ ] Set up version control for diagrams

---

## Level 1: System Context Diagram

### Elements Identification

- [ ] Define the software system being documented
- [ ] List all user types/personas
- [ ] Identify external systems (integrations, dependencies)
- [ ] Note any external APIs consumed
- [ ] Document external databases/storage accessed

### System Definition

- [ ] Name the system clearly
- [ ] Write 1-2 sentence description
- [ ] Identify system boundaries

### Users/Personas

- [ ] List each user type
- [ ] Add role description for each
- [ ] Document what each user does with the system

### External Systems

- [ ] Name each external system
- [ ] Specify if owned by organization or third-party
- [ ] Document integration type (API, file, database)

### Relationships

- [ ] Draw arrow from each user to system
- [ ] Label with action (e.g., "views reports", "manages orders")
- [ ] Draw arrows to/from external systems
- [ ] Label with protocol and purpose

### Quality Check

- [ ] System is clearly named and described
- [ ] All major users are represented
- [ ] External dependencies are visible
- [ ] Relationships have meaningful labels
- [ ] Diagram fits on one page
- [ ] Non-technical stakeholders can understand it

---

## Level 2: Container Diagram

### Container Identification

- [ ] List all web applications
- [ ] List all API services
- [ ] List all databases
- [ ] List message queues/brokers
- [ ] List file storage systems
- [ ] List mobile applications
- [ ] List batch jobs/workers
- [ ] List serverless functions

### For Each Container

- [ ] Assign clear name
- [ ] Specify technology stack (e.g., "React", "FastAPI", "PostgreSQL")
- [ ] Write responsibility description
- [ ] Determine if it's internal or external

### Container Communication

- [ ] Map synchronous calls (REST, gRPC, GraphQL)
- [ ] Map asynchronous communication (events, queues)
- [ ] Map database connections
- [ ] Map file system access
- [ ] Map external API calls

### Relationships

- [ ] Draw arrows between containers
- [ ] Label with protocol (HTTP/REST, gRPC, WebSocket)
- [ ] Include port numbers if relevant
- [ ] Note async vs sync communication
- [ ] Connect users to their entry points

### System Boundary

- [ ] Draw system boundary box
- [ ] All internal containers inside boundary
- [ ] External systems outside boundary
- [ ] Users outside boundary

### Quality Check

- [ ] Each container has name + technology + description
- [ ] All databases/storage are included
- [ ] Communication protocols are labeled
- [ ] 5-15 containers maximum per diagram
- [ ] Developers understand the tech choices
- [ ] No containers are orphaned (unconnected)

---

## Level 3: Component Diagram

### Scope Definition

- [ ] Choose ONE container to zoom into
- [ ] Document the container's responsibility
- [ ] Identify the main purpose of the component diagram

### Component Identification

- [ ] List controllers/handlers/endpoints
- [ ] List services/use cases
- [ ] List repositories/data access
- [ ] List domain entities (if significant)
- [ ] List external clients/adapters
- [ ] List utility/helper components

### For Each Component

- [ ] Assign descriptive name
- [ ] Specify type (Controller, Service, Repository, etc.)
- [ ] Write brief responsibility description
- [ ] Note any frameworks/libraries used

### Internal Dependencies

- [ ] Map controller-to-service dependencies
- [ ] Map service-to-repository dependencies
- [ ] Map service-to-service dependencies
- [ ] Document shared utilities usage

### External Connections

- [ ] Show which components connect to databases
- [ ] Show which components call external APIs
- [ ] Show which components publish/consume events
- [ ] Show incoming connections from other containers

### Quality Check

- [ ] Focused on single container
- [ ] Components represent logical groupings (not classes)
- [ ] Clear separation of concerns visible
- [ ] External dependencies shown at boundaries
- [ ] 5-15 components maximum
- [ ] Helps developers navigate the codebase

---

## Level 4: Code Diagram (Optional)

### When to Create

- [ ] Highly complex domain logic
- [ ] Onboarding for critical subsystems
- [ ] Auto-generation is available
- [ ] Design documentation before implementation

### If Created Manually

- [ ] Focus on key classes only
- [ ] Show inheritance hierarchies
- [ ] Show important associations
- [ ] Use standard UML notation
- [ ] Keep to critical paths only

### Recommendation

- [ ] Prefer auto-generation from IDE
- [ ] Update automatically via tooling
- [ ] Link to source code location

---

## Supplementary: System Landscape Diagram

### When to Create

- [ ] Multiple systems in organization
- [ ] Portfolio/enterprise view needed
- [ ] Cross-team dependencies exist

### Elements

- [ ] List all software systems (yours and others)
- [ ] Identify system owners/teams
- [ ] Map system-to-system dependencies
- [ ] Include all user groups

### Quality Check

- [ ] Shows organizational scope
- [ ] Dependencies between systems clear
- [ ] System ownership indicated
- [ ] Useful for enterprise architecture discussions

---

## Supplementary: Dynamic Diagram

### When to Create

- [ ] Complex request flows need documentation
- [ ] Event sequences are non-obvious
- [ ] Debugging/troubleshooting documentation
- [ ] API documentation enhancement

### Scenario Selection

- [ ] Choose specific use case/feature
- [ ] Define start and end points
- [ ] Identify all participating elements

### Sequence Documentation

- [ ] Number each step
- [ ] Show caller and callee for each step
- [ ] Include request/response data types
- [ ] Note synchronous vs asynchronous
- [ ] Mark error handling paths

### Quality Check

- [ ] Single scenario per diagram
- [ ] Steps are numbered sequentially
- [ ] Time flows top-to-bottom or left-to-right
- [ ] All participating elements shown
- [ ] Useful for understanding runtime behavior

---

## Supplementary: Deployment Diagram

### When to Create

- [ ] Production deployment documentation
- [ ] Multi-environment setup (dev, staging, prod)
- [ ] Infrastructure decision documentation
- [ ] Operations/SRE handoff

### Infrastructure Elements

- [ ] List cloud providers/regions
- [ ] List Kubernetes clusters/namespaces
- [ ] List VMs/compute instances
- [ ] List managed services (RDS, CloudSQL, etc.)
- [ ] List CDNs/load balancers
- [ ] List network boundaries/VPCs

### Mapping

- [ ] Map each container to deployment node
- [ ] Show replicas/scaling configuration
- [ ] Document network paths
- [ ] Show firewall/security group boundaries
- [ ] Include monitoring/logging infrastructure

### Quality Check

- [ ] Matches actual infrastructure
- [ ] Network topology clear
- [ ] Security boundaries visible
- [ ] Useful for ops and infrastructure teams
- [ ] Updated when infrastructure changes

---

## Review and Maintenance

### Peer Review

- [ ] Architecture team review
- [ ] Development team review
- [ ] Verify accuracy against implementation
- [ ] Check for missing elements
- [ ] Validate with stakeholders

### Documentation Integration

- [ ] Link from README/documentation
- [ ] Reference in ADRs
- [ ] Include in onboarding materials
- [ ] Add to architecture wiki

### Maintenance Schedule

- [ ] Review quarterly (minimum)
- [ ] Update after major changes
- [ ] Include in sprint planning (architecture stories)
- [ ] Integrate diagram generation in CI/CD

### Version Control

- [ ] Store diagram source in repository
- [ ] Track changes with commits
- [ ] Generate images automatically
- [ ] Archive old versions

---

## Tooling Setup Checklist

### Structurizr

- [ ] Install Structurizr Lite or CLI
- [ ] Create workspace.dsl file
- [ ] Configure export formats
- [ ] Set up automatic image generation
- [ ] Configure themes (if using)

### PlantUML

- [ ] Install PlantUML processor
- [ ] Include C4-PlantUML library
- [ ] Configure VS Code extension (optional)
- [ ] Set up image generation pipeline

### Mermaid

- [ ] Verify rendering platform support
- [ ] Test C4 syntax compatibility
- [ ] Configure styling options
- [ ] Set up preview workflow

### draw.io

- [ ] Download C4 shape library
- [ ] Import into draw.io
- [ ] Configure export settings
- [ ] Set up version control for .drawio files

---

## Quick Reference: Element Counts

| Diagram Type | Recommended | Maximum |
|--------------|-------------|---------|
| System Context | 3-5 | 10 |
| Container | 5-10 | 15 |
| Component | 5-10 | 15 |
| Dynamic | 5-15 steps | 20 |
| Deployment | 5-10 nodes | 20 |

## Quick Reference: Must-Have Labels

| Element | Required Labels |
|---------|-----------------|
| System | Name, Description |
| Container | Name, Technology, Description |
| Component | Name, Type/Technology, Description |
| Relationship | Purpose/Action, Protocol (for containers) |
| Deployment Node | Name, Technology, Instance count |
