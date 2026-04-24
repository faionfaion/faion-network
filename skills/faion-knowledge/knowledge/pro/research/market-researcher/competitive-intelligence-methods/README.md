# Competitive Intelligence Methods

Reference for competitor analysis and intelligence gathering methodologies.

---

## Table of Contents

1. [competitor-analysis](#competitor-analysis)
2. [competitive-intelligence](#competitive-intelligence)

---

## competitor-analysis

### Problem
Entrepreneurs underestimate competition or miss indirect competitors.

### Framework

**Competitor Types:**

| Type | Definition | Example |
|------|------------|---------|
| Direct | Same solution, same customer | Slack vs Teams |
| Indirect | Different solution, same problem | Slack vs Email |
| Substitute | Alternative approach entirely | Slack vs In-person |
| Potential | Could enter market | Apple into wearables |

**Mapping Process:**

1. **Identify all competitors** (aim for 15-20)
2. **Categorize by type**
3. **Assess each:**
   - Founded, funding, team size
   - Pricing model
   - Key features
   - Positioning

4. **Plot on matrix:**
   - X-axis: Price (low -> high)
   - Y-axis: Features (simple -> complex)

5. **Find whitespace**

### Templates

**Competitive Landscape:**
```markdown
## Direct Competitors

| Name | Founded | Funding | Pricing | Differentiator |
|------|---------|---------|---------|----------------|
| {name} | 2020 | $10M | $99/mo | Feature X |
| {name} | 2018 | $50M | $199/mo | Enterprise |

## Indirect Competitors

| Name | How they compete | Weakness |
|------|-----------------|----------|
| {name} | {explanation} | {gap} |

## Market Position Map

High Price
    |
    |     [Enterprise A]
    |                      [Our opportunity]
    |  [Competitor B]
    |
Low Price ---------------------- High Features

## Whitespace Identified
- {gap 1}: {description}
- {gap 2}: {description}
```

### Examples

**Project Management Tools:**
- Direct: Asana, Monday, ClickUp
- Indirect: Spreadsheets, Slack, Email
- Whitespace: AI-native PM for solopreneurs

### Agent
faion-research-agent (mode: competitors)

---

## competitive-intelligence

### Problem
Entrepreneurs don't know which features are missing in the market.

### Framework

**Analysis Process:**

1. **Feature Inventory**
   - List all features across top 5 competitors
   - Categorize: Core, Differentiator, Nice-to-have

2. **Feature Matrix**
   - Competitors as columns
   - Features as rows
   - Mark: Has (Y), Partial (P), Missing (N)

3. **Gap Identification**
   - Features no one has
   - Features only 1-2 have (opportunity)
   - Features everyone has (table stakes)

4. **Gap Validation**
   - Is this gap intentional (hard, unprofitable)?
   - Do customers want it? (check reviews)
   - Can we build it better?

### Templates

**Feature Matrix:**
```markdown
| Feature | Us | Comp A | Comp B | Comp C | Gap? |
|---------|-------|--------|--------|--------|------|
| Core 1 | Y | Y | Y | Y | No (table stakes) |
| Core 2 | Y | Y | P | Y | No |
| Diff 1 | Y | N | N | P | Yes - Opportunity |
| Diff 2 | P | Y | Y | N | Build out |
| Nice 1 | N | N | N | N | Validate demand |
```

**Gap Validation:**
```markdown
## Gap: {Feature Name}

### Evidence
- Reviews mentioning need: X
- Forum discussions: X links
- Search volume: X/month

### Why Competitors Don't Have It
- {reason}: Technical difficulty / Low priority / Not aware

### Our Advantage
- {why we can build it}

### Recommendation
- Pursue / Investigate / Skip
```

### Examples

**Email Marketing Tools Gap:**
- Gap: Native A/B testing for subject lines
- Evidence: 50+ feature requests in Mailchimp community
- Why missing: Requires ML infrastructure
- Our advantage: Have ML expertise

### Agent
faion-research-agent (mode: competitors)

---

*Competitive Intelligence Methods Reference | 2 methodologies*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Research methodology | sonnet | Framework design |
| Data collection | haiku | Data gathering |
