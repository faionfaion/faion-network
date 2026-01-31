# Product Manager Agents

## Agent 1: faion-mvp-scope-analyzer-agent

**Purpose:** MVP scope via competitor analysis

**When to Use:**
- Defining MVP scope for new product
- Analyzing competitor features
- Determining minimum feature set

**Input:**
- Product type (e.g., "SaaS project management tool")
- Target market/segment
- Competitive context

**Output:**
- Competitor feature analysis
- MVP feature recommendations
- Scope boundary recommendations

**Example Usage:**
```python
Task(
    subagent_type="faion-mvp-scope-analyzer-agent",
    prompt="Analyze SaaS project management tools for MVP scope. Target: small teams (5-15 people), focus on task tracking and collaboration."
)
```

---

## Agent 2: faion-mlp-agent

**Purpose:** MLP orchestrator with 5 modes

**Modes:**

### Mode: analyze
Extract current MVP state from existing specs.

**Input:** Project path
**Output:** Current MVP features analysis

```python
Task(
    subagent_type="faion-mlp-agent",
    prompt="""
    mode: analyze
    project_path: /home/faion/Projects/my-project
    """
)
```

### Mode: find-gaps
Identify gaps between MVP and MLP.

**Input:** Project path, MVP analysis
**Output:** Gap analysis report

```python
Task(
    subagent_type="faion-mlp-agent",
    prompt="""
    mode: find-gaps
    project_path: /home/faion/Projects/my-project
    """
)
```

### Mode: propose
Propose WOW features for MLP.

**Input:** Project path, product type, gaps
**Output:** WOW feature proposals with MLP dimensions

```python
Task(
    subagent_type="faion-mlp-agent",
    prompt="""
    mode: propose
    project_path: /home/faion/Projects/my-project
    product_type: SaaS project management tool
    """
)
```

### Mode: update
Update specs with MLP requirements.

**Input:** Project path, proposed features
**Output:** Updated specification files

```python
Task(
    subagent_type="faion-mlp-agent",
    prompt="""
    mode: update
    project_path: /home/faion/Projects/my-project
    """
)
```

### Mode: plan
Create implementation order for MLP features.

**Input:** Project path, updated specs
**Output:** Implementation order document

```python
Task(
    subagent_type="faion-mlp-agent",
    prompt="""
    mode: plan
    project_path: /home/faion/Projects/my-project
    """
)
```

---

## Agent Selection Guide

| Task | Agent | Mode |
|------|-------|------|
| Define MVP scope | faion-mvp-scope-analyzer-agent | - |
| Analyze current MVP | faion-mlp-agent | analyze |
| Find MLP gaps | faion-mlp-agent | find-gaps |
| Propose WOW features | faion-mlp-agent | propose |
| Update specs with MLP | faion-mlp-agent | update |
| Plan MLP implementation | faion-mlp-agent | plan |

---

## MLP Dimensions Reference

**Delight:** Micro-interactions, animations, polish
**Ease:** Intuitive UX, zero friction
**Speed:** Instant feedback, fast performance
**Trust:** Security signals, reliability
**Personality:** Brand voice, memorable moments

---

*Product Manager Agents v1.0*
*2 agents | 5 MLP modes*
