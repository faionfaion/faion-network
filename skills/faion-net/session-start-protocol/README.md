# Session Start Protocol

**Auto-execute this protocol at the start of each session (unless user gives explicit task).**

---

## Step 1: Knowledge Freshness Check

**Calculate:** `gap = current_date - model_cutoff` (from system prompt)

**Output:** `Knowledge gap: ~{months} months. WebSearch needed for: {areas}`

**Fast-changing areas (use WebSearch):**
- Package versions (npm, pip, cargo, go)
- Framework APIs (React, Next.js, Django, FastAPI)
- Cloud pricing (AWS, GCP, Azure)
- AI models (new releases, pricing, limits)
- Security (CVEs, vulnerabilities)

---

## Step 2: Context Discovery (AskUserQuestion)

**MANDATORY: Ask these questions to route to correct skill:**

```python
AskUserQuestion([
    {
        "question": "What is the project status?",
        "header": "Project",
        "multiSelect": false,
        "options": [
            {"label": "New project (Recommended)", "description": "Starting from scratch, no code yet"},
            {"label": "Existing project", "description": "Has codebase, continuing development"},
            {"label": "Continue previous", "description": "Resume where we left off in this session"}
        ]
    },
    {
        "question": "What are we doing today?",
        "header": "Activity",
        "multiSelect": false,
        "options": [
            {"label": "Research/Planning", "description": "Ideas, market research, strategy, architecture"},
            {"label": "Documentation (SDD)", "description": "Specs, designs, implementation plans, tasks"},
            {"label": "Development", "description": "Write code, features, bug fixes, testing"},
            {"label": "DevOps/Marketing", "description": "Infrastructure, CI/CD, deployment, GTM, SEO"}
        ]
    }
])
```

---

## Step 3: Skill Routing

**Based on answers, route automatically:**

| Project | Activity | Primary Skill |
|---------|----------|---------------|
| New | Research/Planning | faion-researcher → faion-product-manager |
| New | Documentation | faion-sdd |
| New | Development | faion-software-architect → faion-sdd |
| Existing | Research/Planning | faion-product-manager or faion-software-architect |
| Existing | Documentation | faion-sdd |
| Existing | Development | faion-software-developer or faion-feature-executor |
| Existing | DevOps/Marketing | faion-devops-engineer or faion-marketing-manager |
| Continue | Any | Resume from memory or ask for context |

---

## Step 4: Execution Mode Selection

```python
AskUserQuestion([
    {
        "question": "How should I work on tasks?",
        "header": "Mode",
        "multiSelect": false,
        "options": [
            {"label": "YOLO Mode (Recommended)", "description": "Maximum autonomy. Execute completely without interruptions."},
            {"label": "Interactive Mode", "description": "Collaborative dialogue. Ask questions, validate decisions."}
        ]
    }
])
```

---

*Auto-Flow protocol for faion-net orchestrator*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement methodology | haiku | Pattern application and configuration |
| Review implementation | sonnet | Code analysis and verification |
| Design strategy | opus | Complex decision-making |

