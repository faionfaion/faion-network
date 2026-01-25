# Agent Invocation Reference

Quick reference for invoking faion-researcher agents.

---

## Agent Overview

| Agent | Model | Purpose | Modes |
|-------|-------|---------|-------|
| faion-research-agent | opus | Research orchestrator | ideas, market, competitors, pains, personas, validate, niche, pricing, names |
| faion-domain-checker-agent | sonnet | Domain availability verification | - |

---

## Invocation Syntax

### General Pattern
```python
Task(
    subagent_type="faion-research-agent (mode: {mode})",
    prompt="[Specific instruction with context]"
)
```

---

## Mode-Specific Invocations

### Idea Generation
```python
Task(
    subagent_type="faion-research-agent (mode: ideas)",
    prompt="Generate ideas using 7 Ps framework for: {context}"
)
```

**Context should include:**
- User skills/expertise
- Available time
- Motivation (solve own problem, big market, passion)

**Output:** 15-20 idea candidates

---

### Market Research
```python
Task(
    subagent_type="faion-research-agent (mode: market)",
    prompt="Research TAM/SAM/SOM for {product}"
)
```

**Required context:**
- Product description
- Target geography
- Industry/vertical

**Output:** market-research.md

---

### Competitor Analysis
```python
Task(
    subagent_type="faion-research-agent (mode: competitors)",
    prompt="Analyze competitors for {product}"
)
```

**Required context:**
- Product description
- Key features
- Target market

**Output:** competitive-analysis.md

---

### Pain Point Mining
```python
Task(
    subagent_type="faion-research-agent (mode: pains)",
    prompt="Research pain points for: {idea}"
)
```

**Sources to search:**
- Reddit communities
- Forums (Hacker News, ProductHunt)
- Review sites (G2, Capterra)
- Social media (Twitter, LinkedIn)

**Output:** pain-points.md

---

### Persona Building
```python
Task(
    subagent_type="faion-research-agent (mode: personas)",
    prompt="Create personas using JTBD for {product}"
)
```

**Required context:**
- Product description
- Target market
- Known user segments

**Output:** user-personas.md

---

### Problem Validation
```python
Task(
    subagent_type="faion-research-agent (mode: validate)",
    prompt="Validate problem: {problem_statement}"
)
```

**Validation criteria:**
- Frequency (weekly+)
- Intensity (7+/10)
- Willingness to pay
- Search volume
- Competition exists

**Output:** problem-validation.md

---

### Niche Evaluation
```python
Task(
    subagent_type="faion-research-agent (mode: niche)",
    prompt="Evaluate niche viability for: {idea}"
)
```

**Scoring criteria:**
- Market size
- Competition level
- Entry barriers
- Profitability potential
- Personal fit

**Output:** niche-evaluation.md

---

### Pricing Research
```python
Task(
    subagent_type="faion-research-agent (mode: pricing)",
    prompt="Research pricing for {product}"
)
```

**Analysis includes:**
- Competitor pricing models
- Pricing tiers
- Value metrics
- Regional pricing
- Discounting strategies

**Output:** pricing-research.md

---

### Project Naming
```python
Task(
    subagent_type="faion-research-agent (mode: names)",
    prompt="Generate names for {product_description}"
)
```

**Context should include:**
- Product description
- Target audience
- Tone (Professional/Playful/Technical/Premium)

**Output:** name-candidates.md (15-20 names)

---

### Domain Check
```python
Task(
    subagent_type="faion-domain-checker-agent",
    prompt="Check availability for: {name}"
)
```

**Checks:**
- .com domain
- .io domain
- .co domain
- GitHub username
- Twitter handle

**Output:** Availability report with scoring

---

## Multi-Mode Workflows

### Full Research Package
```python
# Run sequentially, not parallel
modes = ["market", "competitors", "personas", "validate", "pricing"]

for mode in modes:
    Task(
        subagent_type=f"faion-research-agent (mode: {mode})",
        prompt=f"Research {mode} for {product}"
    )
```

### Idea Validation
```python
# 1. Generate ideas
Task(
    subagent_type="faion-research-agent (mode: ideas)",
    prompt="Generate ideas for: {context}"
)

# 2. User selects 3-5 ideas

# 3. Research pain points
for idea in selected_ideas:
    Task(
        subagent_type="faion-research-agent (mode: pains)",
        prompt=f"Research pain points for: {idea}"
    )

# 4. Evaluate niches
for idea in selected_ideas:
    Task(
        subagent_type="faion-research-agent (mode: niche)",
        prompt=f"Evaluate niche for: {idea}"
    )
```

---

## Error Handling

| Error | Action |
|-------|--------|
| No ideas resonate | Try different framework, ask about hobbies |
| No pain points found | Broaden search, try adjacent problems |
| High competition | Look for underserved segment |
| User rejects all ideas | Generate more with different angle |
| All .com taken | Suggest .io, check premium domains |
| Trademark conflict | Remove name, note reason |
| Data not found | Mark as "Data not available", continue |

---

## Research Modes

| Mode | Searches | Depth | Use Case |
|------|----------|-------|----------|
| Quick | 3-5 | Surface-level | Fast validation, early exploration |
| Deep | 8-12 | Detailed analysis | Full research, critical decisions |

**Default:** Quick mode (unless specified otherwise)

---

## Output Locations

All research outputs go to `.aidocs/product_docs/`:

```
.aidocs/product_docs/
├── idea-validation.md         # ideas mode
├── market-research.md          # market mode
├── competitive-analysis.md     # competitors mode
├── pain-points.md              # pains mode
├── user-personas.md            # personas mode
├── problem-validation.md       # validate mode
├── niche-evaluation.md         # niche mode
├── pricing-research.md         # pricing mode
├── name-candidates.md          # names mode
└── executive-summary.md        # full research package
```

---

## Best Practices

### Sequential Execution
- **Always run agents sequentially**, not parallel
- Each agent should complete before next starts
- Prevents rate limiting and ensures data quality

### Source Citations
- All agents must cite sources with URLs
- Use markdown links: `[Source Name](URL)`
- Include access date if time-sensitive

### Data Quality
- If data not found → write "Data not available"
- No speculation or made-up data
- Cross-reference multiple sources when possible

### Context Passing
- Each subsequent agent should have access to previous outputs
- Reference earlier research in later prompts
- Build on insights rather than starting fresh

---

*Reference: SKILL.md sections 348-429*
