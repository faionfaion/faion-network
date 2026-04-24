# Validation Methods

Reference for problem validation and niche viability assessment methodologies.

---

## Table of Contents

1. [problem-validation](#problem-validation)
2. [pain-point-mining](#pain-point-mining)
3. [niche-viability-scoring](#niche-viability-scoring)

---

## problem-validation

### Problem
Entrepreneurs build solutions for problems that don't exist or aren't painful enough.

### Framework

**Validation Criteria:**

| Criterion | Threshold | How to Measure |
|-----------|-----------|----------------|
| **Frequency** | Weekly+ | "How often do you face this?" |
| **Intensity** | 7+/10 | "How painful is this? (1-10)" |
| **Willingness to Pay** | Yes | "Would you pay to solve this?" |
| **Search Behavior** | Exists | Check search volume |
| **Competition** | Exists | Someone trying to solve it |

**Evidence Types:**

| Type | Strength | Source |
|------|----------|--------|
| Verbatim quotes | Strong | Interviews |
| Forum discussions | Medium | Reddit, communities |
| Review complaints | Medium | App stores, G2 |
| Search volume | Medium | Google Trends, Ahrefs |
| Competitor existence | Weak | Market research |

**Validation Process:**
1. State the problem hypothesis
2. Define evidence needed
3. Collect evidence (10+ data points)
4. Assess against criteria
5. Decide: Proceed / Pivot / Kill

### Templates

**Problem Validation Report:**
```markdown
## Problem: {Statement}

### Hypothesis
{Who} struggles with {what} because {why}

### Evidence Collected

| Type | Source | Finding |
|------|--------|---------|
| Interview | User 1 | "I spend 3 hours/week on this" |
| Interview | User 2 | "Would pay $50/month" |
| Forum | Reddit | 50 upvotes on complaint post |
| Review | G2 | "Missing feature X" (repeated 10x) |
| Search | Google | "solve X problem" - 5K/month |

### Assessment

| Criterion | Score | Evidence |
|-----------|-------|----------|
| Frequency | Weekly | Interviews |
| Intensity | 8/10 | Interviews |
| WTP | Yes | 4/5 would pay |
| Search | Medium | 5K/month |
| Competition | Yes | 3 competitors |

### Decision
**PROCEED** - Strong problem-solution fit
```

### Examples

**Validated Problem:**
- Hypothesis: Freelancers struggle tracking time across projects
- Evidence: 8/10 interviews confirmed, avg 5 hrs/week lost
- Decision: Proceed to solution validation

### Agent
faion-research-agent (mode: validate)

---

## pain-point-mining

### Problem
Entrepreneurs don't know where customers express frustrations.

### Framework

**Mining Sources:**

| Source | Search Strategy | Signal Strength |
|--------|-----------------|-----------------|
| Reddit | "r/{niche} + frustrating/hate/problem" | High (honest) |
| Twitter/X | "{product} sucks" OR "wish {product}" | High (real-time) |
| App Reviews | 1-3 star reviews | High (specific) |
| Forums | Product-specific communities | Medium |
| Quora | "{problem} solution" | Medium |
| LinkedIn | Industry discussions | Low (filtered) |

**Search Queries:**
```
"{keyword} frustrating" site:reddit.com
"{competitor} alternative" site:reddit.com
"{product} review" 1-star
"I wish {tool} could"
"hate using {tool}"
"looking for {solution}"
```

**Analysis Process:**
1. Collect 50+ pain point mentions
2. Categorize by theme
3. Count frequency per theme
4. Note intensity language
5. Identify gaps in solutions

### Templates

**Pain Point Mining Report:**
```markdown
## Topic: {Area}

### Sources Searched
- Reddit: r/x, r/y, r/z
- App Store: {app1}, {app2}
- Forums: {forum1}

### Pain Points Identified

| Theme | Frequency | Sample Quote | Intensity |
|-------|-----------|--------------|-----------|
| Slow sync | 23 mentions | "Takes forever to sync" | High |
| Missing feature X | 15 mentions | "Why doesn't it have X?" | Medium |
| Expensive | 12 mentions | "Not worth $99/month" | High |

### Key Insights
1. {insight 1}
2. {insight 2}

### Opportunity
{What solution addresses top pain points}
```

### Examples

**Project Management Pain Mining:**
- Top pain: "Too many clicks to create task" (35 mentions)
- Opportunity: One-click task creation from anywhere

### Agent
faion-research-agent (mode: pains)

---

## niche-viability-scoring

### Problem
Entrepreneurs can't objectively assess if a niche is worth pursuing.

### Framework

**5 Criteria Model:**

| Criterion | Weight | 1-3 | 4-6 | 7-10 |
|-----------|--------|-----|-----|------|
| Market Size | 25% | <$10M | $10-100M | >$100M |
| Competition | 20% | Red ocean (10+) | Moderate (3-10) | Blue ocean (<3) |
| Barriers | 20% | High (capital, regulatory) | Medium | Low |
| Profitability | 20% | Thin margins (<20%) | OK (20-40%) | High (>40%) |
| Your Fit | 15% | No relevant skills | Some skills | Perfect match |

**Scoring Process:**
1. Research each criterion
2. Score 1-10 with justification
3. Apply weights
4. Calculate weighted average
5. Compare to thresholds

**Decision Thresholds:**
- 7.5-10: Strong opportunity
- 5.5-7.4: Proceed with caution
- 3.5-5.4: Significant risks
- <3.5: Pass

### Templates

**Niche Viability Scorecard:**
```markdown
## Niche: {Name}

| Criterion | Score | Weight | Weighted | Justification |
|-----------|-------|--------|----------|---------------|
| Market Size | 7 | 25% | 1.75 | $80M SAM |
| Competition | 6 | 20% | 1.20 | 5 competitors |
| Barriers | 8 | 20% | 1.60 | Technical only |
| Profitability | 7 | 20% | 1.40 | SaaS margins |
| Your Fit | 9 | 15% | 1.35 | 10 yrs experience |
| **Total** | | | **7.30** | |

### Decision
**PROCEED WITH CAUTION** - Good opportunity, watch competition

### Risk Mitigation
- {risk 1}: {mitigation}
- {risk 2}: {mitigation}
```

### Examples

**AI Writing Tool Niche:**
- Market: 8 ($200M)
- Competition: 4 (crowded)
- Barriers: 6 (ML expertise needed)
- Profitability: 7 (SaaS)
- Fit: 8 (ML background)
- **Total: 6.5 -> Proceed with differentiation**

### Agent
faion-research-agent (mode: niche)

---

*Validation Methods Reference | 3 methodologies*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Validation Methods | haiku | Task execution: applying established methodologies |
