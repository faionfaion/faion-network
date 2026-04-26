# SDD Workflow Examples

## Purpose

Real-world examples demonstrating SDD workflow application across different project types and scales.

---

## Example 1: SaaS MVP (Full Workflow)

### Context

Solo founder building a task management tool for freelancers.

### Phase 0: Constitution

```markdown
# constitution.md

## Tech Stack
- Frontend: Next.js 14, TypeScript, Tailwind CSS
- Backend: Next.js API routes, Prisma ORM
- Database: PostgreSQL (Supabase)
- Auth: Supabase Auth
- Hosting: Vercel

## Standards
- Test coverage: 70% minimum
- Commit format: conventional commits
- Code style: ESLint + Prettier defaults
```

### Phase 1: Specification

```markdown
# spec.md

## Problem Statement
Freelancers waste time with complex project management tools designed for teams.
They need simple task tracking with time logging.

## Personas
- **Alex**: Solo web developer, 10-15 active projects

## Functional Requirements

### FR-1: Task Management
Users can create, edit, delete tasks with title and description.

**AC-1.1:** Given a logged-in user, when they click "Add Task", then a task creation form appears.
**AC-1.2:** Given a task form, when user submits with title, then task appears in task list.

### FR-2: Time Tracking
Users can log time spent on tasks.

**AC-2.1:** Given a task, when user clicks "Start Timer", then timer begins counting.
**AC-2.2:** Given a running timer, when user clicks "Stop", then time entry is saved.

### FR-3: Project Organization
Users can group tasks into projects.

**AC-3.1:** Given projects exist, when user creates a task, they can assign it to a project.

## MVP Scope
- Task CRUD
- Single-user (no collaboration)
- Basic time tracking (start/stop)
- 5 projects max

## Out of Scope (v1)
- Team collaboration
- Invoicing
- Mobile app
- Calendar integration
```

### Phase 2: Design

```markdown
# design.md

## Architecture Decisions

### AD-1: Monolithic Next.js
**Context:** Solo developer, rapid iteration needed.
**Decision:** Use Next.js for both frontend and API.
**Rationale:** Single deployment, shared types, faster development.

### AD-2: Supabase Backend
**Context:** Need auth, database, real-time without custom infra.
**Decision:** Use Supabase for auth and PostgreSQL.
**Rationale:** Generous free tier, excellent DX, built-in auth.

## File Structure
```
src/
├── app/
│   ├── page.tsx              # Dashboard
│   ├── projects/
│   │   └── [id]/page.tsx     # Project view
│   └── api/
│       ├── tasks/route.ts
│       └── projects/route.ts
├── components/
│   ├── TaskCard.tsx
│   ├── TaskForm.tsx
│   └── Timer.tsx
└── lib/
    ├── supabase.ts
    └── types.ts
```

## Data Model
```sql
projects (id, user_id, name, created_at)
tasks (id, project_id, title, description, status, created_at)
time_entries (id, task_id, started_at, ended_at, duration_minutes)
```
```

### Phase 3: Implementation Plan

```markdown
# implementation-plan.md

## Wave 1: Foundation (No dependencies)
| Task | Description | Complexity |
|------|-------------|------------|
| TASK-001 | Setup Next.js project with Supabase | Medium |
| TASK-002 | Create database schema and migrations | Low |
| TASK-003 | Setup authentication flow | Medium |

## Wave 2: Core Features (Depends on Wave 1)
| Task | Description | Complexity |
|------|-------------|------------|
| TASK-004 | Implement task CRUD API | Medium |
| TASK-005 | Build TaskCard and TaskForm components | Medium |
| TASK-006 | Create dashboard page with task list | Low |

## Wave 3: Time Tracking (Depends on TASK-004)
| Task | Description | Complexity |
|------|-------------|------------|
| TASK-007 | Implement Timer component | Medium |
| TASK-008 | Create time entries API | Low |
| TASK-009 | Add time display to TaskCard | Low |

## Wave 4: Polish (Depends on Wave 2, 3)
| Task | Description | Complexity |
|------|-------------|------------|
| TASK-010 | Add project filtering | Low |
| TASK-011 | Implement responsive design | Low |
| TASK-012 | Write E2E tests for critical paths | Medium |
```

### Outcome

**Without SDD approach:**
- Started coding authentication
- Got distracted by UI details
- 3 weeks later: half-working app with features nobody asked for

**With SDD approach:**
- Clear scope from day 1
- Parallel work possible (Wave 1 tasks)
- MVP delivered in 2 weeks
- Focused on validated requirements

---

## Example 2: API Integration (Medium Project)

### Context

Adding Stripe payments to existing application.

### Quick Spec (15-minute waterfall)

```markdown
# spec-stripe-integration.md

## Problem
Need to accept payments for premium features.

## Requirements
- FR-1: User can enter payment details
- FR-2: System processes one-time payments
- FR-3: System stores payment status
- FR-4: Premium features unlock after payment

## AC
- AC-1: Stripe Checkout redirects user
- AC-2: Webhook updates user status
- AC-3: Premium routes check payment status
```

### Quick Design

```markdown
# design-stripe-integration.md

## AD-1: Stripe Checkout (hosted)
Use Stripe Checkout instead of embedded form.
Rationale: Less PCI compliance burden, faster implementation.

## Files to Change
- CREATE: src/app/api/checkout/route.ts
- CREATE: src/app/api/webhooks/stripe/route.ts
- MODIFY: src/lib/auth.ts (add premium check)
- MODIFY: prisma/schema.prisma (add payment_status)

## API Flow
1. Frontend calls /api/checkout
2. Backend creates Stripe session
3. User redirects to Stripe
4. Stripe sends webhook on success
5. Backend updates user.payment_status
```

### Task List

```markdown
## Tasks
- [ ] TASK-S1: Add payment_status to User model
- [ ] TASK-S2: Create checkout API endpoint
- [ ] TASK-S3: Create webhook handler
- [ ] TASK-S4: Add premium route guard
- [ ] TASK-S5: Create upgrade button component
- [ ] TASK-S6: Test complete flow
```

---

## Example 3: Content Product (Non-Code SDD)

### Context

Creating an online course on prompt engineering.

### Specification

```markdown
# spec.md

## Problem
Developers struggle with LLM prompts but existing courses are overpriced ($200+).

## Validation Evidence
- 50+ Reddit comments asking "how to write prompts"
- No comprehensive beginner-friendly guide
- Competitors charge $149-$499

## Product Requirements

### FR-1: Course Structure
- 10 modules, progressive difficulty
- Each module: video (10-15 min) + text + exercises

### FR-2: Templates
- 50 reusable prompt templates
- Organized by use case (coding, writing, analysis)

### FR-3: Pricing
- $49 (undercut market)
- 30-day money back guarantee

## Success Criteria
- 100 sales in first month
- < 5% refund rate
- 4.5+ rating average
```

### Design

```markdown
# design.md

## Platform Decision
**AD-1:** Host on Teachable (no custom code)
Rationale: Built-in payments, hosting, student management.

## Content Creation Stack
- Write in Notion (collaboration, versioning)
- Record with Loom (quick, simple)
- Edit with Descript (transcription, cleanup)

## Module Structure
```
Module X: [Topic]
├── Lesson video (Loom)
├── Written summary (Notion → Teachable)
├── 5 prompt templates
└── Exercise with solution
```
```

### Implementation Plan

```markdown
## Wave 1: Content (Parallel)
- Module 1-3 content creation
- Template collection (25 templates)

## Wave 2: Content (Parallel)
- Module 4-7 content creation
- Template collection (25 templates)

## Wave 3: Final Modules
- Module 8-10 content creation
- All templates reviewed

## Wave 4: Platform Setup
- Teachable course setup
- Sales page copy
- Payment integration

## Wave 5: Launch
- Beta testers (10 people)
- Feedback incorporation
- Public launch
```

---

## Example 4: Bug Fix (Skip SDD)

### Context

Users report login button not working on Safari.

### Why Skip SDD

- Clear problem definition (bug report)
- Small scope (single component)
- Quick verification (test on Safari)
- No architecture impact

### Direct Approach

```
1. Reproduce bug on Safari
2. Identify cause (CSS or JS issue)
3. Fix
4. Test on Safari, Chrome, Firefox
5. Write regression test
6. Commit with clear message
```

---

## Example 5: Exploratory Prototype (Spike)

### Context

Evaluating whether to use AI-powered search in the product.

### Why Spike Instead of SDD

- Unknown feasibility
- Testing hypothesis, not building feature
- Throwaway code expected
- Learning is the goal

### Spike Approach

```markdown
## Spike: AI Search Feasibility

### Question
Can we implement semantic search with acceptable latency (<500ms)?

### Experiments
1. Test OpenAI embeddings API
2. Test local embedding model (sentence-transformers)
3. Test Pinecone vs pgvector

### Timebox
2 days maximum

### Output
Decision document: go/no-go for full implementation
If go: create proper spec.md
```

---

## Anti-Examples: What Not to Do

### Anti-Example 1: Over-Engineering Spec

**Bad:** 50-page spec for a contact form

```markdown
# DON'T DO THIS
## FR-1: Contact Form Field Validation
### FR-1.1: Email Field
#### FR-1.1.1: Email Format Validation
##### FR-1.1.1.1: RFC 5322 Compliance
...
```

**Better:** Simple spec with essential requirements

```markdown
# DO THIS
## FR-1: Contact Form
- Name field (required, max 100 chars)
- Email field (required, valid format)
- Message field (required, max 2000 chars)
- Submit sends email to support@example.com
```

### Anti-Example 2: Skipping Design

**Bad:** Jump from spec to code

```
Spec (what) → ??? → Code
Result: Inconsistent architecture, refactoring needed
```

**Better:** Brief design for medium+ projects

```
Spec (what) → Design (how) → Code
Result: Consistent patterns, clear module boundaries
```

### Anti-Example 3: Monolithic Tasks

**Bad:** Single task for entire feature

```markdown
- [ ] TASK-001: Implement user authentication
```

**Better:** Decomposed tasks

```markdown
- [ ] TASK-001: Create user database schema
- [ ] TASK-002: Implement registration endpoint
- [ ] TASK-003: Implement login endpoint
- [ ] TASK-004: Add JWT token generation
- [ ] TASK-005: Create auth middleware
- [ ] TASK-006: Build login form component
```

---

## Decision Matrix: When to Use What

| Project Size | Approach | Time Investment |
|--------------|----------|-----------------|
| Tiny (< 2h) | Direct coding | 0 min planning |
| Small (2h - 1d) | 15-min waterfall | 15 min planning |
| Medium (1d - 1w) | Lightweight SDD | 1-2h planning |
| Large (1w+) | Full SDD | 4-8h planning |
| Spike/Prototype | Timeboxed exploration | Spike doc only |

---

*Examples | SDD Foundation | Version 1.0*
