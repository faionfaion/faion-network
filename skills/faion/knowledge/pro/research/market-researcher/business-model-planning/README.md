# Business Model Planning

Methods for evaluating niche viability, business models, value propositions, and pricing strategies.

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

## business-model-research

### Problem
Entrepreneurs compete in crowded markets instead of creating new ones.

### Framework

**Red vs Blue Ocean:**

| Red Ocean | Blue Ocean |
|-----------|------------|
| Compete in existing market | Create uncontested space |
| Beat the competition | Make competition irrelevant |
| Exploit existing demand | Create new demand |
| Value-cost trade-off | Break value-cost trade-off |

**Four Actions Framework:**

| Action | Question | Result |
|--------|----------|--------|
| **Eliminate** | What factors can we eliminate? | Remove costly/unnecessary |
| **Reduce** | What can we reduce below standard? | Simplify |
| **Raise** | What can we raise above standard? | Differentiate |
| **Create** | What new factors can we create? | Innovate |

**Strategy Canvas:**
- X-axis: Key competing factors
- Y-axis: Offering level (low to high)
- Plot competitors and your new curve

### Templates

**Blue Ocean Canvas:**
```markdown
## Industry: {Name}

### Current Red Ocean Factors
| Factor | Industry Level | Customer Value |
|--------|---------------|----------------|
| Price | High | Medium |
| Features | Many | Low (unused) |
| Support | 24/7 | Low (rarely needed) |

### Four Actions

#### Eliminate
- {factor}: Why? {reason}

#### Reduce
- {factor}: From {X} to {Y}

#### Raise
- {factor}: From {X} to {Y}

#### Create
- {new factor}: {description}

### New Value Curve
[Strategy canvas visualization]

### Blue Ocean Opportunity
{Description of uncontested space}
```

### Examples

**Cirque du Soleil:**
- Eliminated: Animals, star performers, aisle concessions
- Reduced: Fun/humor, thrill/danger
- Raised: Unique venue, refined watching environment
- Created: Theme, artistic music/dance, multiple productions

### Agent
faion-research-agent (mode: niche)

---

## value-proposition-design

### Problem
Products don't clearly match customer needs.

### Framework

**Two Parts:**

**1. Customer Profile (right side):**
- Customer Jobs (tasks, problems)
- Pains (obstacles, risks)
- Gains (desired outcomes)

**2. Value Map (left side):**
- Products & Services (what we offer)
- Pain Relievers (how we reduce pains)
- Gain Creators (how we create gains)

**FIT = Pain Relievers address Pains + Gain Creators enable Gains**

**Prioritization:**
- Focus on pains rated 8+/10
- Focus on gains customers measure success by
- Ignore "nice to have" pains/gains

### Templates

**Value Proposition Canvas:**
```markdown
## Customer Segment: {Name}

### Customer Profile

#### Jobs
- Functional: {job}
- Emotional: {job}
- Social: {job}

#### Pains (ranked by intensity)
1. {pain} - 9/10
2. {pain} - 8/10
3. {pain} - 6/10

#### Gains (ranked by relevance)
1. {gain} - Essential
2. {gain} - Expected
3. {gain} - Desired

### Value Map

#### Products & Services
- {product/feature}
- {product/feature}

#### Pain Relievers
- {pain 1} -> {how we relieve it}
- {pain 2} -> {how we relieve it}

#### Gain Creators
- {gain 1} -> {how we create it}
- {gain 2} -> {how we create it}

### FIT Assessment
- Pain coverage: 2/3 top pains addressed
- Gain coverage: 2/3 top gains enabled
- **FIT Score: 80%**
```

### Examples

**Freelancer Invoicing Tool:**
- Pain: Takes too long to create invoice (9/10)
- Pain Reliever: Auto-generate from time tracking
- Gain: Get paid faster
- Gain Creator: Automated payment reminders

### Agent
faion-research-agent (mode: personas)

---

## pricing-research

### Problem
Entrepreneurs choose wrong pricing models that limit growth or revenue.

### Framework

**Pricing Models:**

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| **Freemium** | High volume, low marginal cost | Viral growth | Low conversion (2-5%) |
| **Subscription** | Recurring value | Predictable revenue | Churn risk |
| **Usage-based** | Variable consumption | Scales with value | Unpredictable revenue |
| **One-time** | Complete product | Simple | No recurring revenue |
| **Tiered** | Diverse segments | Captures more value | Complex |
| **Per-seat** | Team tools | Clear pricing | Resistance to add users |

**Selection Criteria:**

| Factor | Question |
|--------|----------|
| Value delivery | Continuous or one-time? |
| Usage patterns | Consistent or variable? |
| Customer type | Individual or team? |
| Competition | What do they charge? |
| Marginal cost | Cost to serve additional user? |

**Pricing Research:**
1. List top 5 competitors' pricing
2. Calculate value delivered
3. Survey willingness to pay (Van Westendorp)
4. Test with early users

### Templates

**Pricing Strategy:**
```markdown
## Product: {Name}

### Competitor Pricing

| Competitor | Model | Price Range | Notes |
|------------|-------|-------------|-------|
| {name} | Subscription | $X-Y/mo | |
| {name} | Freemium | Free-$X | |

### Value Analysis
- Cost of problem: $X/month
- Time saved: X hours/month
- Value captured: 10-20% of savings

### Recommended Model
**Tiered Subscription**

### Pricing Tiers

| Tier | Price | Features | Target |
|------|-------|----------|--------|
| Free | $0 | {features} | Try before buy |
| Pro | $19/mo | {features} | Individuals |
| Team | $49/mo | {features} | Small teams |
| Enterprise | Custom | {features} | Large orgs |

### Justification
- Freemium drives awareness
- Pro captures 80% of revenue
- Enterprise for large accounts
```

### Examples

**SaaS Pricing Decision:**
- Model: Tiered subscription
- Free: 1 project, basic features
- Pro ($19): Unlimited projects
- Team ($49/user): Collaboration features
- Justification: Match competitor pricing, capture team value

### Agent
faion-research-agent (mode: pricing)

---

*Business Model Planning | 4 methodologies*
*Part of faion-researcher v1.3*

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Business model canvas | sonnet | Strategic planning |
| Revenue projection | sonnet | Financial forecasting |
