---
id: content-audit-process
name: "Content Audit - Process"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Content Audit - Process

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #content-audit #content-strategy
- **Agent:** faion-ux-researcher-agent
- **Related:** content-audit-basics.md

---

## Process

### Step 1: Define Scope and Goals

**Questions:**
- What content are we auditing? (All pages, blog only, help center)
- What do we want to learn? (What exists, what's performing)
- How will we use results? (Migration, strategy, cleanup)

**Set evaluation criteria:**
- Accuracy
- Relevance
- Quality
- Performance
- Accessibility
- SEO

### Step 2: Gather Content Inventory

**Automated methods:**
- Use site crawler (Screaming Frog, Sitebulb)
- Export from CMS
- Use sitemap

**Manual additions:**
- PDFs and downloads
- Gated content
- Dynamic content
- Legacy systems

### Step 3: Create Spreadsheet Structure

Columns to include:

| Category | Fields |
|----------|--------|
| **Identification** | URL, ID, Title |
| **Metadata** | Author, Date, Type |
| **Taxonomy** | Category, Tags |
| **Status** | Published, Draft |
| **Metrics** | Pageviews, Bounce rate |
| **Evaluation** | Quality score, Action |

### Step 4: Evaluate Each Piece

For each content item, assess:

```
Questions:
- Is it accurate and up-to-date?
- Is it relevant to users?
- Is it well-written?
- Does it perform well?
- Is it accessible?
- Is it SEO-optimized?
```

### Step 5: Assign Actions

| Action | When to use |
|--------|-------------|
| **Keep** | High quality, performing well |
| **Update** | Good content, needs refresh |
| **Consolidate** | Duplicate or overlap |
| **Rewrite** | Poor quality, important topic |
| **Remove** | Outdated, irrelevant, low value |
| **Review** | Needs further evaluation |

### Step 6: Report and Recommend

Summarize findings:
- Total content count
- Content by type
- Content by action
- Priority recommendations

---

## Report Template

```markdown
# Content Audit Report

**Date:** [Date]
**Scope:** [What was audited]
**Auditor:** [Name]

## Executive Summary

**Total content pieces:** [Number]
**Date range:** [Oldest to newest content]

**Key finding:** [Most important insight]

## Content Inventory Overview

### By Type
| Type | Count | % of Total |
|------|-------|------------|
| Blog posts | 150 | 40% |
| Product pages | 50 | 13% |
| Help articles | 100 | 27% |
| Other | 75 | 20% |
| **Total** | **375** | **100%** |

### By Age
| Age | Count | % of Total |
|-----|-------|------------|
| < 1 year | 100 | 27% |
| 1-2 years | 120 | 32% |
| 2-3 years | 80 | 21% |
| > 3 years | 75 | 20% |

### By Action Needed
| Action | Count | % of Total |
|--------|-------|------------|
| Keep | 100 | 27% |
| Update | 125 | 33% |
| Consolidate | 40 | 11% |
| Rewrite | 35 | 9% |
| Remove | 75 | 20% |

## Quality Analysis

### Average Scores
| Criteria | Average Score |
|----------|--------------|
| Accuracy | 3.2 |
| Relevance | 3.8 |
| Quality | 3.0 |
| **Overall** | **3.3** |

### Problem Areas
1. [Area 1]: [Issue description]
2. [Area 2]: [Issue description]

### Strengths
1. [Strength 1]
2. [Strength 2]

## Performance Insights

### Top Performing Content
| Title | Pageviews | Bounce Rate |
|-------|-----------|-------------|
| [Title 1] | 10,000 | 35% |
| [Title 2] | 8,500 | 40% |

### Underperforming Content
| Title | Pageviews | Issue |
|-------|-----------|-------|
| [Title 1] | 50 | Outdated |
| [Title 2] | 30 | Poor SEO |

## Recommendations

### Immediate (1-2 weeks)
1. Remove [X] outdated pages
2. Update [Y] critical content

### Short-term (1-3 months)
1. Consolidate duplicate content
2. Improve [category] quality

### Long-term (3-6 months)
1. Develop content governance
2. Create editorial calendar

## Next Steps

- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]

## Appendix

- Full content inventory (spreadsheet)
- Detailed evaluation notes
```

---

## Examples

### Example 1: Blog Audit Findings

**Finding:** 40% of blog posts are 3+ years old

**Issues:**
- Screenshots show old UI
- Pricing information outdated
- Links broken

**Recommendation:** Update top 20 posts by traffic, archive low-traffic posts over 3 years.

### Example 2: Help Center Audit

**Finding:** 15 articles cover similar topics with different answers

**Issues:**
- Confusing for users
- SEO competition between pages
- Maintenance overhead

**Recommendation:** Consolidate into 5 comprehensive guides.

---

## Checklist

Before audit:
- [ ] Scope defined
- [ ] Goals established
- [ ] Tools selected
- [ ] Spreadsheet template ready
- [ ] Evaluation criteria defined

During audit:
- [ ] Complete inventory gathered
- [ ] Metadata collected
- [ ] Analytics added
- [ ] Each item evaluated
- [ ] Actions assigned
- [ ] Priorities set

After audit:
- [ ] Report created
- [ ] Recommendations prioritized
- [ ] Actions assigned to owners
- [ ] Timeline established
- [ ] Follow-up scheduled

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Content Audit - Process | haiku | Task execution: applying established methodologies |

## Sources

- [Content Audit Process Guide](https://www.nngroup.com/articles/content-audits/) - Nielsen Norman Group
- [Step-by-Step Content Audit](https://www.contentharmony.com/blog/content-audit-guide/) - Content Harmony tutorial
- [Dyno Mapper Content Audit](https://dynomapper.com/blog/19-ux/254-content-inventory) - Tool-based approach
- [HubSpot Content Audit](https://blog.hubspot.com/marketing/content-audit) - Marketing perspective
- [Content Strategy Toolkit](https://gathercontent.com/content-strategy-toolkit) - GatherContent resources
