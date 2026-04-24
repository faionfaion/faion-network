# Market Analysis

Methods for market research, sizing, trend analysis, and competitive intelligence.

---

## market-research-tam-sam-som

### Problem
Entrepreneurs can't quantify market opportunity or set realistic targets.

### Framework

**Definitions:**
- **TAM** (Total Addressable Market): Everyone who could buy
- **SAM** (Serviceable Addressable Market): Those you can reach
- **SOM** (Serviceable Obtainable Market): Realistic Year 1 target

**Calculation Methods:**

1. **Top-Down:**
   - Start with industry reports
   - Apply filters (geography, segment)
   - Risk: Often inflated

2. **Bottom-Up:**
   - Count potential customers
   - Multiply by price point
   - Risk: May miss segments

3. **Value Theory:**
   - Calculate value created
   - Apply capture rate (1-10%)
   - Most defensible

**SOM Reality Check:**
- Typical SOM = 1-5% of SAM in Year 1
- With unfair advantage: 5-10%
- With viral growth: 10-20%

### Templates

**Market Sizing:**
```markdown
## TAM
- Global market: $XX billion
- Growth: X% CAGR
- Source: {report name}

## SAM
- Geographic focus: {regions}
- Segment focus: {segments}
- SAM = $XX million

## SOM (Year 1)
- Target customers: X
- Average revenue: $Y
- SOM = $Z million
- % of SAM: X%

## Assumptions
1. {assumption 1}
2. {assumption 2}
```

### Examples

**HR SaaS:**
- TAM: $30B (global HR software)
- SAM: $500M (US SMB HR)
- SOM: $2M (500 customers x $4K)
- SOM % of SAM: 0.4%

### Agent
faion-research-agent (mode: market)

---

## trend-analysis

### Problem
Entrepreneurs miss timing opportunities or build for declining markets.

### Framework

**Trend Categories:**

| Category | Timeframe | Examples |
|----------|-----------|----------|
| Macro | 5-10 years | AI adoption, remote work |
| Industry | 2-5 years | No-code tools, creator economy |
| Micro | 6-24 months | Specific tech adoption |

**Analysis Framework:**

1. **Growth Drivers**
   - What accelerates this trend?
   - Technology, regulation, demographics

2. **Adoption Curve**
   - Where are we? (Innovators -> Early Adopters -> Majority)
   - Sweet spot: Early Majority

3. **Threats**
   - What could reverse this trend?
   - Competition, regulation, substitutes

4. **Timing Assessment**
   - Too early: Education cost too high
   - Just right: Market aware, solutions emerging
   - Too late: Established winners

### Templates

**Trend Analysis:**
```markdown
## Trend: {Name}

### Overview
- Stage: {Emerging | Growing | Mature | Declining}
- Growth rate: X% annually
- Market size: $X billion

### Drivers
1. {driver} - Impact: High/Medium/Low
2. {driver} - Impact: High/Medium/Low

### Threats
1. {threat} - Likelihood: High/Medium/Low
2. {threat} - Likelihood: High/Medium/Low

### Timing Assessment
- Current stage: Early Majority
- Window: 2-3 years
- Recommendation: {proceed/wait/pivot}
```

### Examples

**AI Coding Assistants (2026):**
- Stage: Early Majority
- Growth: 45% CAGR
- Window: Now optimal
- Threat: Large players (GitHub, OpenAI)

### Agent
faion-research-agent (mode: market)

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

*Market Analysis | 5 methodologies*
*Part of faion-researcher v1.3*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Market size calculation | sonnet | TAM/SAM analysis |
| Market segmentation | sonnet | Segment identification |
| Trend identification | sonnet | Pattern recognition |
