# Product Manager Workflows

## Workflow 1: Project Bootstrap

Full pipeline from idea to first task.

```
IDEA → CONCEPT → TECH STACK → MVP SCOPE → CONFIRMATION → BACKLOG → CONSTITUTION → TASK_000
```

### Output Structure

```
.aidocs/
├── constitution.md
├── roadmap.md
└── features/
    ├── backlog/{NN}-{feature}/spec.md
    └── 00-setup/tasks/todo/TASK_000_project_setup.md
```

### Phases

1. **Vision Brainstorm** - Apply Five Whys to get to real need
2. **Tech Stack Selection** - Frontend, backend, database
3. **MVP Definition** - Max 3-5 features, cut 50% nice-to-haves
4. **User Confirmation** - Present summary, get approval
5. **Backlog Creation** - Create feature specs
6. **Constitution** - Write project constitution
7. **TASK_000** - Setup task with project goals

### Bootstrap Execution Flow

```python
# Phase 1: Vision
AskUserQuestion(questions=[
    {"question": "Tell me about the project"},
])

# Phase 2: Tech Stack
AskUserQuestion([
    {"question": "Frontend?", "options": [
        {"label": "React + TypeScript"},
        {"label": "Next.js"},
        {"label": "None (API only)"}
    ]},
    {"question": "Backend?", "options": [
        {"label": "Python + Django"},
        {"label": "Python + FastAPI"},
        {"label": "Go"},
        {"label": "Node.js"}
    ]},
    {"question": "Database?", "options": [
        {"label": "PostgreSQL"},
        {"label": "SQLite"},
        {"label": "MongoDB"}
    ]}
])

# Phase 3: MVP Definition
Task(subagent_type="faion-mvp-scope-analyzer-agent",
     prompt=f"Analyze {product_type} competitors for MVP scope")

# Phase 4: Confirmation (MANDATORY)
# Present summary, get approval

# Phase 5: Create backlog and constitution
```

---

## Workflow 2: MLP Planning

Transform MVP to Most Lovable Product.

```
1. Analyze MVP scope (competitors)
2. Extract current state from specs
3. Find MLP gaps
4. Propose WOW features
5. Update specs with MLP reqs
6. Create implementation order
```

### Output Structure

```
product_docs/
├── mvp-scope-analysis.md
├── mlp-analysis-report.md
└── mlp-implementation-order.md
```

### MLP Execution Flow

```python
# MVP analysis first
Task(subagent_type="faion-mvp-scope-analyzer-agent",
     prompt=f"Analyze {product_type} competitors for MVP scope")

# MLP orchestrator handles all phases
Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: analyze
     project_path: {project_path}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: find-gaps
     project_path: {project_path}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: propose
     project_path: {project_path}
     product_type: {product_type}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: update
     project_path: {project_path}
     """)

Task(subagent_type="faion-mlp-agent",
     prompt=f"""
     mode: plan
     project_path: {project_path}
     """)
```

---

## Numbering Convention

| Type | Pattern | Example |
|------|---------|---------|
| Features | `{NN}-{name}` | `01-auth`, `02-payments` |
| Tasks | `TASK_{NNN}_*` | `TASK_001_setup` |
| Requirements | `FR-{NN}.{N}` | `FR-01.1` |
| Acceptance | `AC-{NN}.{N}` | `AC-01.1` |

---

*Product Manager Workflows v1.0*
