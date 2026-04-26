# Spec Example Ecommerce Cart Checklist

## Phase 1: Recognize Full Specification Scope

- [ ] Complex multi-step feature (add, update, remove, persist)
- [ ] Multiple personas with different needs
- [ ] Both happy path and error scenarios
- [ ] Non-functional requirements critical
- [ ] Enterprise or mission-critical feature
- [ ] Use full spec template, not condensed

## Phase 2: Complete Reference Documents Section

- [ ] Link constitution.md for tech decisions
- [ ] Link related completed features (Product Catalog, User Auth)
- [ ] Create table with Document, Path, Sections
- [ ] For cart feature: reference Done features it depends on
- [ ] Set foundations for design and implementation

## Phase 3: Write Comprehensive Problem Statement

- [ ] WHO: Multiple personas (Sarah, Mike) with different needs
- [ ] PROBLEM: Each persona's specific frustration
- [ ] IMPACT: Business consequence (e.g., 2.1% to 3.5% conversion)
- [ ] SOLUTION: Persistent cart with quantity management
- [ ] SUCCESS METRIC: Quantified conversion improvement

## Phase 4: Create Multiple User Personas

- [ ] Persona 1: Busy Parent (Sarah) - quick shopper
- [ ] Persona 2: Deal Hunter (Mike) - price conscious
- [ ] Each with Role, Goal, Pain Points, Context
- [ ] Personas should have different needs for features
- [ ] Drive different design decisions

## Phase 5: Write Multiple User Stories

- [ ] US-001: Add to Cart (MVP backbone)
- [ ] US-002: Update Quantity (MVP backbone)
- [ ] US-003: Remove from Cart (MVP backbone)
- [ ] US-004: Persistent Cart (MVP backbone)
- [ ] Additional Phase 2 stories for future features
- [ ] Each story traces to persona and acceptance criteria
- [ ] Assign story point estimates

## Phase 6: Write Multiple Functional Requirements

- [ ] FR-001: Add products with one click
- [ ] FR-002: Real-time price calculation
- [ ] FR-003: Update quantities (1-99)
- [ ] FR-004: Remove items
- [ ] FR-005: Persist for logged-in users
- [ ] FR-006: Local storage for guests
- [ ] Each FR includes validation rules
- [ ] Each traces to user story

## Phase 7: Create Non-Functional Requirements

- [ ] NFR-001: Performance (<200ms p95 for add)
- [ ] NFR-002: Scalability (50k concurrent users)
- [ ] NFR-003: Availability (<1 min RTO for recovery)
- [ ] NFR-004: Usability (1 click from any page)
- [ ] Each NFR specific and measurable

## Phase 8: Write Comprehensive Acceptance Criteria

- [ ] AC-001: Add product to empty cart (happy path)
- [ ] AC-002: Add same product increases quantity
- [ ] AC-003: Update quantity in cart
- [ ] AC-004: Remove product from cart
- [ ] AC-005: Persistent cart for logged-in users
- [ ] AC-006: Guest cart persistence (local storage)
- [ ] Use specific values (e.g., "$25.00", not "valid price")
- [ ] Each scenario: Given → When → Then

## Phase 9: Create Coverage Checklist

- [ ] Happy path covered (successful scenarios)
- [ ] Error handling covered (validation failures)
- [ ] Boundary conditions covered (min/max quantities)
- [ ] Security scenarios noted (cart tampering)
- [ ] Performance scenarios noted (large carts)
- [ ] Accessibility scenarios noted (if applicable)

## Phase 10: Define Out of Scope

- [ ] Save for Later - deferred to Phase 2
- [ ] Share Cart (URL) - deferred to Phase 3
- [ ] Cart Price Alerts - not planned
- [ ] Multi-currency Support - v2.0
- [ ] For each: state reason and timeline
- [ ] Use explicit table format

## Phase 11: Document Assumptions & Constraints

- [ ] Assumptions: prices change, users understand current prices, carts expire
- [ ] Constraints: max 50 items/cart, max 99 quantity, 5MB local storage
- [ ] Technical constraints from platform
- [ ] Business constraints

## Phase 12: Create Dependencies Section

- [ ] Internal: Product Catalog feature (must be done)
- [ ] Internal: User Authentication (for logged-in cart)
- [ ] External: PostgreSQL database
- [ ] External: Redis for cart caching
- [ ] Show relationships clearly

## Phase 13: Document Related Features

- [ ] Feature 01-product-catalog: Dependency (Done)
- [ ] Feature 02-user-auth: Dependency (Done)
- [ ] Feature 04-checkout: Blocking relationship (Todo)
- [ ] Show how this feature enables downstream features

## Phase 14: Add Recommended Skills & Methodologies

- [ ] faion-software-developer: Implementation
- [ ] faion-ux-ui-designer: Cart UI/UX components
- [ ] List specific methodologies: State Management, Micro-interactions
- [ ] Help team select right approaches

## Phase 15: Include Appendix Sections

- [ ] Wireframes: Link to Figma or design tools
- [ ] Data Models: Preliminary model definitions
- [ ] API Contracts: Preliminary request/response schemas
- [ ] Visual aids for complex features

## Phase 16: Quality Gate for Complex Specs

- [ ] Problem statement is comprehensive and clear
- [ ] Multiple personas defined with detail
- [ ] User stories comprehensive (10+ stories OK for complex)
- [ ] Functional requirements cover all scenarios (15-20 OK)
- [ ] Non-functional requirements address all critical attributes
- [ ] Acceptance criteria extensive (6-10 scenarios)
- [ ] Out of scope prevents future scope creep
- [ ] Dependencies fully documented
- [ ] No implementation details
- [ ] Spec follows structure and is ready for design