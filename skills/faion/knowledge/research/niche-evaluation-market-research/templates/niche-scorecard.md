<!-- purpose: 5-factor weighted niche scorecard (market size, competition, accessibility, monetization, personal fit) with a decision band. -->
<!-- consumes: candidate niche definition + industry sources + competitor list, per AGENTS.md Prerequisites -->
<!-- produces: niche scorecard artefact feeding content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml (niche-formula, cited-sizing, verdict-single) -->
<!-- token-budget-impact: ~500-900 tokens when loaded as context -->

# Niche Evaluation Scorecard

## Niche: <name>

**One-sentence definition:** <product_type> for <specific_audience> who <specific_problem>

---

## 1. Market Size (Weight: 25%)

| Metric | Value | Source URL |
|--------|-------|------------|
| TAM | $X | [required — mark "unknown" if no source] |
| SAM | $X | <required> |
| SOM | $X | [calculation: TAM x capture assumption x years] |

- Google Trends direction: <growing_stable_declining>
- Keyword volume (primary terms): <x_searches_month> Source: <ahrefs_trends>
- Community 30-day post velocity: <x_posts_day> Source: <reddit_community_url>

**Score: [1-5]** — requires URL for score >= 4

---

## 2. Competition (Weight: 20%)

| Competitor | URL | Pricing | Strengths | Weaknesses | Source |
|------------|-----|---------|-----------|------------|--------|
| <name> | | $X | | | |

Long-tail competitors (IH/Etsy/Discord): <list>
Matrix position: <matrix_position>

**Score: [1-5]** — requires URL for score >= 4

---

## 3. Audience Accessibility (Weight: 15%)

| Channel | Present? | Size/activity | Score (1-5) |
|---------|----------|---------------|-------------|
| Reddit | Y/N | [members, X posts/day] | |
| Twitter/X | Y/N | [accounts, avg engagement] | |
| Podcasts | Y/N | <n_shows> | |
| Paid ads | Y/N | [CPM $X, audience size] | |
| Purchasing power | — | <x_budget_authority> | |

**Average Score: [X]** — target > 3.5

---

## 4. Monetization Potential (Weight: 20%)

| Model | Viable? | Price point | Evidence |
|-------|---------|-------------|----------|
| SaaS | Y/N | $X/mo | |
| One-time | Y/N | $X | |
| Service | Y/N | $X/hr | |
| Ads | Y/N | CPM $X | |

Willingness to pay evidence: [quote or source]

**Score: [1-5]**

---

## 5. Personal Fit (Weight: 20%)

**NOT scored by agent. Founder fills directly.**

| Factor | Score (1-5) |
|--------|-------------|
| Audience understanding | |
| Relevant skills | |
| Daily excitement | |
| Content creation ability | |
| Network connections | |

**Average: [X]** — if < 3, reject regardless of total

---

## Final Calculation

| Factor | Weight | Score | Weighted |
|--------|--------|-------|----------|
| Market Size | 25% | X | X |
| Competition | 20% | X | X |
| Accessibility | 15% | X | X |
| Monetization | 20% | X | X |
| Personal Fit | 20% | FOUNDER INPUT | X |
| **TOTAL** | 100% | | **X** |

**Decision band:**
- > 4.0: Excellent, proceed to problem-validation
- 3.5-4.0: Good, validate further
- 3.0-3.5: Risky, improve weak areas first
- < 3.0: Reconsider or pivot

**Decision:** [ ] Proceed [ ] Needs improvement in: <areas> [ ] Reconsider
