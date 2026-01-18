---
description: "SDD Workflow Orchestrator - manage projects, features, specs, designs, implementation plans, tasks"
argument-hint: "[project] or [project/feature]"
hooks:
  PreToolUse:
    - matcher: ""
      hooks:
        - type: command
          command: ~/.claude/hooks/auto-update.sh
          once: true
---

# SDD Workflow Orchestrator

**Communication with user: User's language.**

## Workflow

```
IDEA DISCOVERY (optional):
  /faion-idea-discovery → brainstorm → validate pain → evaluate niche → idea-validation.md
                    ↓
NEW PROJECT:
  bootstrap → constitution.md → TASK_000_setup → Execute setup
                    ↓
PRODUCT RESEARCH (optional):
  /faion-product-research → market, competitors, personas, validation, pricing
                    ↓
GTM MANIFEST (optional):
  /faion-gtm-manifest → go-to-market strategy from research data
                    ↓
FEATURE DEVELOPMENT (with quality gates):
  backlog/ → [confidence-check] → grooming → todo/ → [parallelize] → in-progress/ → done/
     ↓                               ↓         ↓                          ↓            ↓
  spec.md                      + design    ready                    executing    [reflexion]
                               + tasks                                            archived
                    ↓
MLP PLANNING (optional):
  /faion-mlp-planning → gap analysis → update specs → WOW moments → impl order
```

## Phase 1-2: Select Project

```bash
ls -d aidocs/sdd/*/ 2>/dev/null | xargs -I{} basename {}
```

AskUserQuestion: "З яким проектом працюємо?" + "+ Новий проект"

## Phase 3: New Project

If new project:
1. Ask project name (kebab-case)
2. Ask if codebase exists:
   - **No codebase** → Call `faion-project-bootstrap` skill (full brainstorm + constitution + TASK_000)
   - **Has codebase** → Call `faion-writing-constitutions` skill (analysis mode)

**After bootstrap completes:**
- Constitution created: `aidocs/sdd/{project}/constitution.md`
- Roadmap created: `aidocs/sdd/{project}/roadmap.md`
- Setup task created: `aidocs/sdd/{project}/features/todo/00-setup/tasks/todo/TASK_000_project_setup.md`
- Offer: "Виконати TASK_000 зараз?" → `/faion-execute-task {project}/00-setup TASK_000`

## Phase 4: Select Feature

```bash
# List features by status
ls -d aidocs/sdd/{project}/features/in-progress/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/todo/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/backlog/*/ 2>/dev/null | xargs -I{} basename {}
ls -d aidocs/sdd/{project}/features/done/*/ 2>/dev/null | xargs -I{} basename {}
```

AskUserQuestion: "Що хочеш зробити?" options:
- 🚧 In-progress features (continue work)
- 📋 Todo features (start execution)
- 📝 Backlog features (needs grooming)
- ✅ Done features (review)
- "+ Нова фіча" (add to backlog)
- "📊 Backlog grooming" → Call `faion-backlog-grooming` skill
- "🔬 Product research" → Call `faion-product-research` skill
- "📊 GTM Manifest" → Call `faion-gtm-manifest` skill
- "💡 Idea discovery" → Call `faion-idea-discovery` skill
- "💖 MLP Planning" → Call `faion-mlp-planning` skill
- "🔧 Standalone tasks" (technical/one-off tasks)
- "📄 Product docs" (PRD, personas, etc.)

**If Backlog grooming:**
→ Call `faion-backlog-grooming` skill
→ Interactive session: prioritize, refine specs, create designs, generate tasks

**If Product research:**
→ Call `faion-product-research` skill
→ Options: market research, competitor analysis, user personas, problem validation, pricing
→ Writes to `product_docs/`

**If GTM Manifest:**
→ Requires: product research complete (market, competitors, personas, pricing)
→ Call `faion-gtm-manifest` skill
→ Writes to `product_docs/gtm-manifest/`

**If Idea discovery:**
→ Call `faion-idea-discovery` skill
→ Brainstorm ideas, research pain points, evaluate niches
→ Creates: `idea-validation.md`

**If MLP Planning:**
→ Call `faion-mlp-planning` skill
→ Analyzes MVP specs, identifies MLP gaps, adds WOW moments
→ Creates: `mlp-analysis-report.md`, `mlp-implementation-order.md`

**If feature from backlog:**
→ Needs grooming first (spec, design, tasks)
→ Redirect to `faion-backlog-grooming` skill

**If feature from todo:**
→ Ready for execution
→ Offer: `/faion-execute-task` or `/faion-do-all-tasks`

**If feature from in-progress:**
→ Show task status, continue execution

**If new feature:**
1. Get next number from existing features
2. Call `faion-writing-specifications` skill
3. Create `features/backlog/{NN}-{feature}/spec.md`

**If Standalone tasks:**
1. List tasks from `tasks/{backlog,todo,in-progress,done}/`
2. Options:
   - Execute task from todo/
   - Create new standalone task
   - Move task between statuses

**If Product docs:**
1. List docs from `product_docs/`
2. Options:
   - View/edit existing doc
   - Create new doc (PRD, personas, competitive analysis, etc.)

## Phase 5: Feature Grooming (via skill)

When feature needs grooming:
1. Call `faion-backlog-grooming` skill with feature
2. Skill handles: spec refinement → design → tasks
3. Moves feature from backlog/ to todo/

## Phase 6: Feature Execution

When feature is in todo/ and ready:
1. Move to in-progress/
2. Execute tasks: `/faion-execute-task {project}/{feature} TASK_NNN`
3. Or batch: `/faion-do-all-tasks {project}/{feature}`

## Phase 7: Feature Completion

When all tasks done:
1. Move feature from in-progress/ to done/
2. Update roadmap.md status
3. Offer next feature

## Directory Structure

```
aidocs/sdd/{project}/
├── constitution.md
├── roadmap.md                       # Milestones, progress, risks
│
├── product_docs/                    # Product documentation
│   ├── idea-validation.md           # Idea validation & niche evaluation
│   ├── prd.md                       # Product Requirements Document
│   ├── market-research.md           # TAM/SAM/SOM, trends
│   ├── competitive-analysis.md      # Competitors analysis
│   ├── user-personas.md             # User personas
│   ├── problem-validation.md        # Problem validation evidence
│   ├── pricing-research.md          # Pricing benchmarks
│   ├── executive-summary.md         # Research synthesis
│   ├── mlp-analysis-report.md       # MLP gap analysis
│   ├── mlp-implementation-order.md  # MLP phases & WOW moments
│   └── gtm-manifest/                # Go-to-market strategy
│       └── gtm-manifest-full.md
│
├── tasks/                           # Standalone tasks (no feature)
│   ├── backlog/                     # Task ideas
│   ├── todo/                        # Ready to execute
│   ├── in-progress/                 # Being executed
│   └── done/                        # Completed
│
└── features/
    ├── backlog/                     # Features waiting for grooming
    │   └── {NN}-{feature}/
    │       ├── spec.md              # Draft or needs refinement
    │       └── tasks/
    │           └── backlog/         # Task ideas (optional)
    │
    ├── todo/                        # Features ready for execution
    │   └── {NN}-{feature}/
    │       ├── spec.md              # Approved
    │       ├── design.md            # Approved
    │       ├── implementation-plan.md
    │       └── tasks/
    │           ├── backlog/         # Task ideas
    │           ├── todo/            # Ready to execute
    │           ├── in-progress/     # Being executed
    │           └── done/            # Completed
    │
    ├── in-progress/                 # Features being worked on
    │   └── {NN}-{feature}/
    │       └── ... (same structure as todo)
    │
    └── done/                        # Completed features
        └── {NN}-{feature}/
            └── ... (archived)
```

## Standalone Tasks vs Feature Tasks

**Standalone tasks** (`tasks/`):
- One-off technical tasks (refactoring, upgrades, infra)
- Quick fixes without full spec/design
- Research spikes
- Don't belong to any feature

**Feature tasks** (`features/{status}/{NN}-{feature}/tasks/`):
- Part of feature implementation
- Have spec.md and design.md as context
- Follow implementation-plan.md

## Feature Lifecycle

```
backlog/  →  todo/  →  in-progress/  →  done/
   ↓           ↓            ↓             ↓
 draft      groomed     executing     archived
 spec       spec+       tasks
            design+
            tasks
```

## Task Lifecycle (within feature)

```
tasks/backlog/  →  tasks/todo/  →  tasks/in-progress/  →  tasks/done/
      ↓               ↓                  ↓                    ↓
  task ideas      refined &         being executed        completed
                  ready
```

## Numbering Convention

- Feature directories: `{NN}-{name}` (00, 01, 02, ...)
- Tasks: `TASK_{NNN}_*` (000, 001, 002, ...)
- Requirements: `FR-{NN}.{N}` (FR-01.1, FR-01.2, ...)
- Acceptance Criteria: `AC-{NN}.{N}` (AC-01.1, AC-01.2, ...)

## Quality Assurance

### Confidence Check (before each phase)
```
Pre-Spec:     Problem validated? Market gap? Target audience?
Pre-Design:   Requirements clear? AC testable? No contradictions?
Pre-Task:     Architecture decided? No duplicates? Dependencies mapped?
Pre-Impl:     Task clear? Approach decided? No blockers?
```
**Threshold:** ≥90% proceed, 70-89% clarify, <70% stop

### Hallucination Prevention (before marking done)
1. Tests passing? → Show actual output
2. Requirements met? → List each with evidence
3. No assumptions? → Show documentation
4. Evidence exists? → Provide test results, code changes

### Reflexion Learning (after completion)
- Success → Store pattern in `~/.sdd/memory/patterns_learned.jsonl`
- Failure → Store error + solution in `~/.sdd/memory/mistakes_learned.jsonl`
- Metrics → Track in `~/.sdd/memory/workflow_metrics.jsonl`

## Memory System

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Successful patterns (PAT-NNN)
├── mistakes_learned.jsonl    # Errors + solutions (ERR-NNN)
├── workflow_metrics.jsonl    # Task execution metrics
└── session_context.md        # Current session state
```

Use `/faion-reflexion` to record and learn.

## 3-Layer Architecture

```
Layer 1: Domain Skills (8) ─ orchestrators
    ↓ call
Layer 2: Agents (58) ─ executors
    ↓ use
Layer 3: Technical Skills (25) ─ tools
```

## Domain Skills (Layer 1) - Orchestrators

Route requests to appropriate domain skill based on user intent:

| Skill | Purpose | Methodologies |
|-------|---------|---------------|
| faion-sdd-domain-skill | SDD workflow: specs, design, tasks, quality gates | 8 |
| faion-research-domain-skill | Research: ideas, market, competitors, personas | 20 |
| faion-product-domain-skill | Product: roadmap, MVP/MLP, prioritization | 18 |
| faion-development-domain-skill | Development: Python, JS, backend, DevOps | 68 |
| faion-marketing-domain-skill | Marketing: GTM, landing, content, ads | 72 |
| faion-pmbok-domain-skill | PMBOK 7/8: performance domains, principles | 20 |
| faion-babok-domain-skill | BABOK v3: knowledge areas, techniques | 18 |
| faion-ux-domain-skill | UX: Nielsen Norman, research, usability | 32 |

## Technical Skills (Layer 3) - Tools

### Development (5)
- faion-python-skill (Django, FastAPI, pytest)
- faion-javascript-skill (React, Node, TypeScript)
- faion-backend-skill (Go, Ruby, PHP, Java, C#, Rust)
- faion-api-skill (REST, GraphQL, OpenAPI)
- faion-testing-skill (Unit, Integration, E2E)

### DevOps (4)
- faion-aws-cli-skill (S3, EC2, Lambda, etc.)
- faion-k8s-cli-skill (Kubernetes operations)
- faion-terraform-skill (Infrastructure as code)
- faion-docker-skill (Containers, compose)

### Marketing (3)
- faion-meta-ads-skill (Meta Ads API)
- faion-google-ads-skill (Google Ads API)
- faion-analytics-skill (GA4, Plausible)

### AI/LLM (11)
- faion-langchain-skill (LangChain/LangGraph)
- faion-llamaindex-skill (RAG, indexing)
- faion-vector-db-skill (Qdrant, Weaviate, pgvector)
- faion-embeddings-skill (OpenAI, Mistral)
- faion-openai-api-skill (GPT-4, DALL-E, Whisper)
- faion-claude-api-skill (Claude, tool use)
- faion-gemini-api-skill (Gemini multimodal)
- faion-image-gen-skill (DALL-E, FLUX, SD)
- faion-video-gen-skill (Sora, Runway)
- faion-audio-skill (TTS/STT, ElevenLabs, Whisper)
- faion-finetuning-skill (LoRA/QLoRA)

### Other (2)
- faion-browser-automation-skill (Puppeteer, Playwright)
- faion-pm-tools-skill (Jira, ClickUp, Linear, GitHub)

## Agents (Layer 2) - Executors (58 total)

### Research & Discovery (10)
faion-idea-generator, faion-market-researcher, faion-competitor-analyzer, faion-persona-builder, faion-pricing-researcher, faion-niche-evaluator, faion-pain-point-researcher, faion-problem-validator, faion-name-generator, faion-domain-checker

### SDD & Review (6)
faion-task-creator, faion-task-executor, faion-tasks-reviewer, faion-spec-reviewer, faion-design-reviewer, faion-impl-plan-reviewer

### MLP (6)
faion-mvp-scope-analyzer, faion-mlp-spec-analyzer, faion-mlp-gap-finder, faion-mlp-spec-updater, faion-mlp-feature-proposer, faion-mlp-impl-planner

### Development (7)
faion-code-agent, faion-test-agent, faion-devops-agent, faion-browser-agent, faion-api-agent, faion-api-designer, faion-dev-component-developer, faion-dev-design-brainstormer, faion-dev-storybook-manager

### Marketing (7)
faion-ads-agent, faion-content-agent, faion-email-agent, faion-social-agent, faion-landing-analyzer, faion-landing-copywriter, faion-landing-designer

### Standards (4)
faion-pm-agent, faion-ba-agent, faion-ux-researcher-agent, faion-usability-agent

### AI/LLM (14)
faion-rag-agent, faion-embedding-agent, faion-prompt-engineer-agent, faion-image-generator-agent, faion-image-editor-agent, faion-video-generator-agent, faion-tts-agent, faion-stt-agent, faion-voice-agent-builder-agent, faion-finetuner-agent, faion-cost-optimizer-agent, faion-multimodal-agent, faion-llm-cli-agent, faion-autonomous-agent-builder-agent

### Quality & Expert (4)
faion-hallucination-checker, faion-seo-agent, faion-hooks-expert

## Legacy Skills (archived)

Old granular skills merged into domain skills:
- faion-writing-specifications → faion-sdd-domain-skill
- faion-writing-design-docs → faion-sdd-domain-skill
- faion-writing-implementation-plan → faion-sdd-domain-skill
- faion-backlog-grooming → faion-sdd-domain-skill
- faion-product-research → faion-research-domain-skill
- faion-gtm-manifest → faion-marketing-domain-skill
- faion-mlp-planning → faion-product-domain-skill
- etc. (see _archived/ for full list)

## Commands (User Entry Points)

| Command | Purpose |
|---------|---------|
| `/sdd` | **Single entry point** - all SDD workflow starts here |
| `/faion-net {project}` | Work with specific project |
| `/faion-net {project}/{feature}` | Work with specific feature |

**All operations are accessed through `/sdd`:**
- Task execution → `/sdd` → select feature → execute task
- Task creation → `/sdd` → select feature → create tasks
- Reviews → `/sdd` → select feature → review
- Grooming → `/sdd` → backlog grooming
- Research → `/sdd` → product research

**Skills are internal** (user-invocable: false) - orchestrated by `/sdd`.
