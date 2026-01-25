# Research Workflows

Detailed workflow documentation for faion-researcher skill.

---

## Workflow: Idea Discovery

### Overview
Sequential workflow for generating and validating startup/product ideas.

### Flow Diagram

```
1. Gather Context (AskUserQuestion)
   - Skills, interests, resources
   |
   v
2. Generate Ideas (mode: ideas)
   - Apply 7 Ps framework + other methods
   |
   v
3. User Selection (AskUserQuestion)
   - Pick 3-5 ideas to research
   |
   v
4. Pain Point Research (mode: pains)
   - Reddit, forums, reviews mining
   |
   v
5. Niche Evaluation (mode: niche)
   - Market size, competition, barriers
   |
   v
6. Present Results
   |
   +-- User selects idea? --> YES --> Write to product_docs/idea-validation.md
   |                      --> NO  --> Loop back to step 2
```

### Context Gathering Questions

```
Question 1: "What are your skills/experience?"
Options: Software development | Design/UX | Marketing/Sales | Domain expertise

Question 2: "What motivates you?"
Options: Solve my own problem | Big market opportunity | Passion project | Side income

Question 3: "How much time can you invest?"
Options: Nights & weekends | Part-time (20h/week) | Full-time
```

---

## Workflow: Product Research

### Overview
Comprehensive research workflow for existing product concepts.

### Flow Diagram

```
1. Parse project from ARGUMENTS
2. Read: constitution.md, roadmap.md
3. AskUserQuestion: modules + mode (quick/deep)
4. Run agents SEQUENTIALLY (not parallel)
5. Write executive-summary.md
```

### Module Selection

```python
AskUserQuestion(
    questions=[{
        "question": "Which modules to run?",
        "multiSelect": True,
        "options": [
            {"label": "Market Research", "description": "TAM/SAM/SOM, trends"},
            {"label": "Competitors", "description": "Features, pricing"},
            {"label": "Personas", "description": "Pain points, JTBD"},
            {"label": "Validation", "description": "Problem evidence"},
            {"label": "Pricing", "description": "Benchmarks"}
        ]
    }]
)
```

### Research Modes

| Mode | Searches | Depth |
|------|----------|-------|
| Quick | 3-5 | Surface-level trends |
| Deep | 8-12 | Detailed analysis |

---

## Workflow: Project Naming

### Overview
Generate and validate project/product names with domain availability.

### Flow Diagram

```
1. Gather Concept (AskUserQuestion)
   - Description, tone (Professional/Playful/Technical/Premium)
   |
   v
2. Generate Names (mode: names)
   - 15-20 candidates using 7 strategies
   |
   v
3. User Selection (AskUserQuestion, multiSelect)
   - Select favorites or "generate more"
   |
   v
4. Check Domains (faion-domain-checker-agent)
   - .com, .io, .co, GitHub, Twitter
   |
   v
5. Present Results
   |
   +-- Final selected? --> YES --> Update constitution.md
   |                   --> NO  --> Loop to step 2
```

### Naming Strategies

| Strategy | Description | Example |
|----------|-------------|---------|
| Descriptive | What it does | DropBox |
| Invented | Made-up word | Spotify |
| Compound | Two words | Facebook |
| Metaphor | Symbolic meaning | Amazon |
| Portmanteau | Blended words | Pinterest |
| Alliteration | Same sound | PayPal |
| Acronym | Letter combination | IBM |

### Name Scoring

| Factor | Points |
|--------|--------|
| .com available | 10 |
| .io available | 5 |
| No trademark | 5 |
| GitHub available | 3 |
| Twitter available | 3 |
| Easy to spell | 2 |
| **Max Total** | **28** |

---

## Workflow Rules

### Sequential Execution
- **Run agents ONE BY ONE** (sequential, not parallel)
- Each agent must complete before next starts
- Prevents rate limiting and ensures data quality

### Data Quality
- Agents must cite sources with URLs
- If data not found → write "Data not available"
- No speculation or made-up data

### Research Depth
- **Quick mode:** 3-5 searches per topic
- **Deep mode:** 8-12 searches per topic

---

## Next Steps After Research

After research complete, offer:
- "Create GTM Manifest?" → Call `faion-marketing-manager`
- "Create spec.md?" → Call `faion-sdd`
- "Start development?" → Call `faion-software-developer`

---

*Reference: SKILL.md sections 167-272*
