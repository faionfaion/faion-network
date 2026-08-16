<!-- purpose: Competitor landscape table -- direct/indirect competitors, substitutes, potential entrants, whitespace candidates. -->
<!-- consumes: competitor list + evidence URLs per category -->
<!-- produces: Markdown competitor landscape table -->
<!-- depends-on: none -->
<!-- token-budget-impact: ~350-500 tokens when loaded as context -->

## Competitor Landscape: <category>

**Date:** YYYY-MM-DD | **Seed:** <category_name> | **Axes:** <x_axis_label> vs <y_axis_label>

### Direct Competitors (same solution, same customer)

| Name | Founded | Funding | Pricing | Positioning (≤140 chars) | Evidence URLs |
|------|---------|---------|---------|--------------------------|---------------|
| [Name] | YYYY | $X | $X/mo | <positioning> | [URL1, URL2] |

### Indirect Competitors (different solution, same problem)

| Name | How they compete | Weakness | Evidence URLs |
|------|-----------------|----------|---------------|
| [Name] | <explanation> | <gap> | [URL1, URL2] |

### Substitutes (alternative approach entirely)

| Name/behavior | How customers use it instead | Evidence |
|--------------|------------------------------|----------|
| Spreadsheets | Manual tracking, no cost | <interview_quote> |
| "Do nothing" | [description] | <support_ticket_theme> |

### Potential Competitors (could enter market)

| Name | Signal | Entry vector | Evidence URL | Date |
|------|--------|-------------|-------------|------|
| [Name] | [job posting / beta / acquisition] | <how> | <url> | YYYY-MM-DD |

### Whitespace Candidates

| Cell position | Why empty (hypothesis) | Demand evidence needed |
|--------------|----------------------|------------------------|
| [description] | [technical / regulatory / unprofitable / unaware] | [what to validate] |

**Rule:** Never act on a whitespace cell without demand evidence from review mining or interviews.
