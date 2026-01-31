# User Validation Methods

Methods for understanding users through personas, JTBD, problem validation, and pain point mining.

---

## jobs-to-be-done

### Problem
Features don't connect to real user motivations.

### Framework

**JTBD Statement:**
```
When I [situation/trigger],
I want to [motivation/action],
So I can [expected outcome/benefit].
```

**Job Dimensions:**

| Dimension | Question | Example |
|-----------|----------|---------|
| Functional | What task? | Send invoice |
| Emotional | How feel? | Confident, professional |
| Social | How perceived? | Reliable, organized |

**Job Mapping Process:**
1. Identify situation triggers
2. Map functional jobs
3. Uncover emotional jobs (harder)
4. Discover social jobs (hardest)
5. Prioritize by frequency + importance

**Hiring/Firing Framework:**
- Why do customers "hire" solutions?
- Why do they "fire" (abandon) solutions?
- What makes them switch?

### Templates

**JTBD Canvas:**
```markdown
## Job: {Name}

### Situation/Trigger
When I {situation}...

### Functional Job
I want to {action}...

### Emotional Job
So I can feel {emotion}...

### Social Job
And be seen as {perception}...

### Current Solutions
- {solution 1}: Hired because {reason}, fired because {reason}
- {solution 2}: Hired because {reason}, fired because {reason}

### Our Opportunity
We can {do X better} by {approach}
```

### Examples

**Invoicing Software JTBD:**
- Situation: When I finish a project for a client
- Functional: I want to send a professional invoice quickly
- Emotional: So I can feel confident I'll get paid
- Social: And be seen as a legitimate business

### Agent
faion-research-agent (mode: personas)

---

## persona-building

### Problem
Teams build for abstract "users" rather than specific people with distinct needs.

### Framework

**Persona Components:**

| Component | Description | Source |
|-----------|-------------|--------|
| Demographics | Age, role, income, location | Analytics, surveys |
| Behaviors | Tools used, habits, workflows | Interviews, observation |
| Pain Points | Top 3-5 frustrations | Interviews, support tickets |
| Goals | What success looks like | Interviews |
| Quote | Representative statement | Verbatim from interview |

**Persona Types:**

| Type | Priority | Focus |
|------|----------|-------|
| Primary | 1 | Design for this person |
| Secondary | 2 | Consider their needs |
| Negative | Exclude | Explicitly not for them |

**Creation Process:**
1. Conduct 5-10 user interviews
2. Identify patterns (cluster similar users)
3. Create 2-3 personas (not more)
4. Validate with team
5. Post visibly (always reference)

### Templates

**Persona Template:**
```markdown
# Persona: {Name} ({Type})

## Photo
[Stock photo representing this person]

## Demographics
- **Age:** 32
- **Role:** Product Manager at startup
- **Income:** $120K
- **Location:** San Francisco
- **Tech savviness:** High

## Behaviors
- Works 50+ hours/week
- Uses: Slack, Notion, Figma, Jira
- Checks phone first thing in morning
- Reads newsletters over coffee

## Pain Points
1. Too many tools, context switching
2. Stakeholder alignment meetings
3. Data scattered across systems

## Goals
- Ship features faster
- Better work-life balance
- Get promoted to Director

## Quote
"I spend more time coordinating than creating."

## Jobs To Be Done
- When I [situation], I want to [action], so I can [outcome]
```

### Examples

**SaaS Personas:**
1. Primary: "Startup Sarah" - PM at early-stage startup
2. Secondary: "Enterprise Eric" - PM at Fortune 500
3. Negative: "Agency Alex" - Freelance consultant

### Agent
faion-research-agent (mode: personas)

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

*User Validation Methods | 4 methodologies*
*Part of faion-researcher v1.3*
