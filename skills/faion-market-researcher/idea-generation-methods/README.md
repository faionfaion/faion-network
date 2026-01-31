# Idea Generation Methods

Methods for discovering and validating startup ideas.

---

## idea-generation

### Problem
Aspiring entrepreneurs struggle to find viable startup ideas that match their skills and interests.

### Framework

| P | Question | Exploration |
|---|----------|-------------|
| **Pain** | What frustrates you daily? | List 5 daily annoyances, rate severity 1-10 |
| **Passion** | What do you love doing? | Activities you'd do for free, hobbies |
| **Profession** | What's broken in your industry? | Insider knowledge of inefficiencies |
| **Process** | What workflow is inefficient? | Tasks taking 10x longer than needed |
| **Platform** | What can be improved on existing platform? | Missing integrations, poor UX |
| **People** | Who do you know with problems? | Friends, family, colleagues complaints |
| **Product** | What product do you wish existed? | Tools you'd pay for immediately |

**Scoring:**
- For each P, generate 3-5 ideas
- Score each: Market size (1-5) + Your fit (1-5) + Urgency (1-5)
- Top 3 scores proceed to validation

### Templates

**Ideation Worksheet:**
```markdown
## Pain Ideas
1. {idea} - Score: {X}/15 - Notes: {why interesting}
2. {idea} - Score: {X}/15

## Passion Ideas
1. {idea} - Score: {X}/15

## Profession Ideas
1. {idea} - Score: {X}/15
...

## Top 3 to Validate
1. {idea} from {P} - Total: {X}/15
2. {idea} from {P} - Total: {X}/15
3. {idea} from {P} - Total: {X}/15
```

### Examples

| P | Example Idea | Score |
|---|--------------|-------|
| Pain | Meeting scheduling across timezones | 12/15 |
| Passion | Teaching coding to kids | 9/15 |
| Profession | Medical billing automation | 14/15 |

### Agent
faion-research-agent (mode: ideas)

---

## paul-graham-questions

### Problem
Entrepreneurs miss obvious opportunities hiding in plain sight.

### Framework

**4 Questions:**
1. **What's tedious but necessary?**
   - Tasks everyone hates but must do
   - High frequency, low satisfaction

2. **What's surprisingly hard to do?**
   - Should be simple but isn't
   - Indicates market failure

3. **What do you find yourself building for yourself?**
   - Personal tools that could scale
   - Validates genuine need

4. **What would you pay for that doesn't exist?**
   - Identifies willingness to pay
   - Validates business model

**Exploration Process:**
1. Spend 30 min per question
2. Write stream-of-consciousness
3. Circle recurring themes
4. Cross-reference with daily activities

### Templates

**PG Questions Journal:**
```markdown
## Question 1: Tedious but Necessary
### List
- Expense reports
- Code reviews
- Meeting scheduling
- ...

### Themes
- Administrative overhead
- Communication friction

### Top Ideas
- Automated expense categorization
- AI code review assistant
```

### Examples

**Successful Companies from PG Questions:**
- Dropbox: "Sync files is tedious" -> Tedious but necessary
- Stripe: "Payments are hard" -> Surprisingly hard
- Notion: "I built my own wiki" -> Built for yourself

### Agent
faion-research-agent (mode: ideas)

---

## pain-point-research

### Problem
Entrepreneurs overlook problems they face daily because they've normalized them.

### Framework

**Mining Techniques:**

1. **Complaint Audit** (1 week)
   - Log every complaint you make
   - Note frequency and intensity
   - Categorize: work, personal, tools

2. **Workaround Inventory**
   - List all workarounds you've built
   - Spreadsheets, scripts, processes
   - Time spent maintaining them

3. **Tool Stack Analysis**
   - List all tools you use
   - Rate satisfaction 1-5
   - Identify gaps between tools

4. **Time Tracker**
   - Track where time goes for 3 days
   - Identify time sinks
   - Calculate cost of inefficiency

**Scoring:**
| Factor | Weight |
|--------|--------|
| Frequency | 30% |
| Intensity | 30% |
| Current solutions | 20% |
| Your ability to solve | 20% |

### Templates

**Pain Point Log:**
```markdown
| Date | Complaint | Category | Freq | Intensity | Notes |
|------|-----------|----------|------|-----------|-------|
| 01/18 | Can't find file | Tools | Daily | 7/10 | Slack + Drive + Email |
| 01/18 | Meeting ran over | Work | Weekly | 5/10 | No time boundaries |
```

### Examples

- "I can never find that one Slack message" -> Search tool idea
- "Updating all docs after API change" -> Auto-sync documentation
- "Switching between 10 tabs" -> Dashboard aggregator

### Agent
faion-research-agent (mode: ideas)

---

## niche-evaluation

### Problem
Too many ideas, no objective way to prioritize.

### Framework

**Scoring Dimensions:**

| Dimension | 1-2 | 3-4 | 5 |
|-----------|-----|-----|---|
| **Market Size** | <$10M | $10M-$100M | >$100M |
| **Competition** | Red ocean, 10+ | Moderate, 3-10 | Blue ocean, <3 |
| **Barriers** | High (capital, regulatory) | Medium | Low |
| **Monetization** | Unclear | Possible | Obvious |
| **Your Fit** | No relevant skills | Some skills | Perfect match |

**Process:**
1. Score each idea 1-5 on all dimensions
2. Weight dimensions (optional)
3. Calculate total (max 25)
4. Rank ideas

**Decision Thresholds:**
- 20-25: Strong proceed
- 15-19: Proceed with caution
- 10-14: Needs pivot
- <10: Pass

### Templates

**Scoring Matrix:**
```markdown
| Idea | Market | Competition | Barriers | Monetization | Fit | Total |
|------|--------|-------------|----------|--------------|-----|-------|
| A | 4 | 3 | 4 | 5 | 4 | 20 |
| B | 5 | 2 | 3 | 4 | 3 | 17 |
| C | 3 | 4 | 5 | 3 | 5 | 20 |
```

### Examples

**SaaS Idea Scored:**
- Market: $500M (5)
- Competition: 5 competitors (3)
- Barriers: Technical only (4)
- Monetization: SaaS model (5)
- Fit: Developer background (4)
- **Total: 21/25 -> Strong proceed**

### Agent
faion-research-agent (mode: niche)

---

*Idea Generation Methods | 4 methodologies*
*Part of faion-researcher v1.3*
