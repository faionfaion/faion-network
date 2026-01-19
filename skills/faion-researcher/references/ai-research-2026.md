# AI-Powered Research Best Practices 2026

## M-RES-021: AI Research Tools

### Problem

Manual research is slow and limited in scope.

### Solution: AI-Augmented Discovery

**AI Research Stack:**

| Stage | AI Tools |
|-------|----------|
| **Exploration** | Perplexity, ChatGPT, Claude |
| **Competitor Analysis** | Crayon, Klue, Kompyte |
| **User Sentiment** | Brandwatch, Sprout Social |
| **Market Data** | Statista AI, CB Insights |
| **Trend Analysis** | Exploding Topics, Google Trends |

**AI Research Workflow:**
```
1. Define research questions
2. AI-assisted broad exploration
3. Human curation of sources
4. AI synthesis of findings
5. Human analysis and insights
6. AI-generated report draft
7. Human review and finalization
```

**Best Practices:**
| Do | Don't |
|----|-------|
| Use AI for speed and breadth | Trust AI output blindly |
| Verify AI findings with primary sources | Skip human analysis |
| Combine multiple AI tools | Rely on single source |
| Document AI sources used | Hide AI involvement |

**Stats:** 95% of researchers now use AI tools regularly (2025).

---

## M-RES-022: Continuous Discovery

### Problem

Discovery treated as one-time project start activity.

### Solution: Ongoing Discovery Integration

**Continuous Discovery Habits:**

| Cadence | Activity | Output |
|---------|----------|--------|
| Daily | Review analytics, support tickets | Insight log |
| Weekly | User interviews (2-3) | Interview notes |
| Weekly | Competitor monitoring | Change log |
| Bi-weekly | Synthesis session | Updated assumptions |
| Monthly | Research review | Research report |

**Integration with Product:**
```
Discovery → Hypothesis → Experiment → Learn → Repeat
     ↑                                         |
     └─────────────────────────────────────────┘
```

**Key Principle:** Markets change fast, user needs evolve. Solutions that worked 6 months ago may not work today.

**Tools for Continuous Discovery:**
| Tool | Purpose |
|------|---------|
| Dovetail | Research repository |
| Notion | Knowledge base |
| Airtable | Insight tracking |
| EnjoyHQ | Research ops |
| Condens | Synthesis |

---

## M-RES-023: Problem Validation 2026

### Problem

Building products nobody needs.

### Solution: Evidence-Based Validation

**Validation Hierarchy:**
```
Strongest evidence:
├── 1. Users paid for solution (actual behavior)
├── 2. Users signed up/committed (commitment)
├── 3. Users engaged deeply with prototype (behavior)
├── 4. Users expressed strong interest (stated preference)
└── 5. Users said they have the problem (weakest)
```

**Mom Test Questions:**
> Ask about their life, not your idea.

| Instead of | Ask |
|------------|-----|
| "Would you use this?" | "How do you currently solve X?" |
| "Is this a problem for you?" | "Tell me about the last time you dealt with X" |
| "Would you pay $X?" | "What have you tried? What did it cost?" |

**Red Flags:**
- Compliments ("Great idea!")
- Hypotheticals ("I would definitely...")
- Generic statements ("Everyone needs this")

---

## M-RES-024: AI-Assisted Persona Building

### Problem

Personas based on assumptions, not data.

### Solution: Data-Driven Personas

**AI-Enhanced Persona Process:**
```
1. Aggregate user data (analytics, interviews, surveys)
2. AI clustering of behavioral patterns
3. AI-generated persona drafts
4. Human validation and refinement
5. Ongoing persona updates from new data
```

**Modern Persona Components:**

| Section | Traditional | 2026 Addition |
|---------|-------------|---------------|
| Demographics | Age, location | Digital behavior |
| Goals | What they want | JTBD framework |
| Pain points | Frustrations | Quantified impact |
| Behavior | How they act | Trigger analysis |
| Quotes | Representative | Sentiment patterns |

**JTBD Integration:**
```
When [situation],
I want to [motivation],
So I can [expected outcome].
```

---

## M-RES-025: Competitive Intelligence

### Problem

Point-in-time competitor snapshots become stale.

### Solution: Continuous Competitive Monitoring

**Monitoring Framework:**

| Signal | Tools | Frequency |
|--------|-------|-----------|
| Pricing changes | Manual + alerts | Weekly |
| Feature launches | Product Hunt, Twitter | Daily |
| Hiring patterns | LinkedIn | Monthly |
| Funding news | Crunchbase | Weekly |
| Customer reviews | G2, Capterra | Weekly |
| Content/SEO changes | Ahrefs, SEMrush | Monthly |

**AI-Powered Monitoring:**
```python
# Example monitoring setup
monitors = [
    CompetitorWebsite(url, check_changes=True),
    SocialMention(keywords, sentiment=True),
    ReviewSites(competitors, rating_alerts=True),
    JobPostings(competitors, roles=["Product", "Engineering"]),
    PricingPages(competitors, snapshot=True)
]
```

**Competitive Intelligence Outputs:**
| Output | Frequency | Audience |
|--------|-----------|----------|
| Weekly digest | Weekly | Product team |
| Threat assessment | Monthly | Leadership |
| Feature comparison | Quarterly | Sales, Marketing |
| Strategic report | Quarterly | Executive |

---

## M-RES-026: Market Sizing with AI

### Problem

TAM/SAM/SOM estimates are often finger-in-the-air.

### Solution: AI-Assisted Market Sizing

**Top-Down + Bottom-Up Triangulation:**
```
Top-Down:
Market reports → Industry size → Segment → Target
$100B market → 20% segment → 5% addressable = $1B

Bottom-Up:
# potential customers × average revenue = TAM
100K companies × $10K/year = $1B

Triangulate: If both approaches give similar numbers, confidence increases.
```

**AI Tools for Market Sizing:**
| Tool | Use |
|------|-----|
| Statista AI | Market reports, data |
| CB Insights | Company data, trends |
| Perplexity | Synthesis from multiple sources |
| ChatGPT/Claude | Calculation assistance |

**Market Sizing Checklist:**
- [ ] Define market boundaries clearly
- [ ] Use multiple data sources
- [ ] Bottom-up AND top-down estimates
- [ ] Document assumptions
- [ ] Include confidence ranges
- [ ] Update regularly

---

*AI Research Best Practices 2026*
*Sources: Looppanel, Qualtrics, Shopify Research Guide*
