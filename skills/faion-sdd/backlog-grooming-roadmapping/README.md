# Backlog Grooming & Roadmapping

Systematic approaches to backlog management, prioritization, and roadmap planning with LLM assistance.

---

## Overview

| Concept | Purpose | Update Frequency |
|---------|---------|------------------|
| **Backlog** | What could we build? All potential work | Weekly |
| **Roadmap** | What will we build when? Strategic view | Monthly/Quarterly |

### The Problem

Projects lose direction when:
- Feature requests pile up without prioritization
- No clear vision of where the product is going
- Teams work on low-impact items while important features wait
- Stakeholders don't know what's coming when

**Root cause:** No systematic backlog management and roadmap planning.

---

## Backlog Structure

### Lifecycle

```
IDEA --> VALIDATE --> SPECIFY --> DESIGN --> READY --> IN PROGRESS --> DONE
  |          |           |          |          |
 DROP      DROP        DROP       DROP       DEFER
```

### Folder Organization

```
.aidocs/
├── backlog/          # Ideas being validated/specified
├── todo/             # Ready for implementation
├── in-progress/      # Currently executing
└── done/             # Completed features
```

### Item States

| State | Description | Next Action |
|-------|-------------|-------------|
| **Idea** | Raw concept, not validated | Quick assessment |
| **Validated** | Worth exploring | Write spec |
| **Specified** | Has spec.md | Technical design |
| **Designed** | Has design.md | Create tasks |
| **Ready** | Has tasks, can start | Pull to sprint |

---

## Prioritization Frameworks

### RICE Scoring

Developed by Intercom for objective, data-driven prioritization.

| Factor | Question | Scale |
|--------|----------|-------|
| **R**each | How many users affected per quarter? | 1-10 (actual count) |
| **I**mpact | Impact per user? | 0.25 (minimal) to 3 (massive) |
| **C**onfidence | How confident in estimates? | 50%, 80%, 100% |
| **E**ffort | Person-months to complete | 0.5, 1, 2, 3, 6+ |

**Formula:** `RICE = (Reach x Impact x Confidence) / Effort`

**Best for:** Quarterly roadmap planning, feature prioritization, data-driven teams.

### MoSCoW Method

Created by Dai Clegg at Oracle for scope management.

| Category | Meaning | Allocation |
|----------|---------|------------|
| **Must** | Critical for release, non-negotiable | ~60% of scope |
| **Should** | Important but not critical | ~20% of scope |
| **Could** | Nice to have (vitamins, not painkillers) | ~20% of scope |
| **Won't** | Explicitly not in this release | Documented for future |

**Best for:** MVP scoping, releases with strict deadlines, resource constraints.

### Value vs Effort Matrix

```
HIGH VALUE
    |
    |  Quick Wins        Big Bets
    |  (Do first)        (Plan carefully)
    |--------------------+--------------------
    |  Fill-ins          Money Pits
    |  (Do if time)      (Avoid)
    |
    +-----------------------------------------> HIGH EFFORT
```

| Quadrant | Strategy |
|----------|----------|
| Quick Wins | Prioritize immediately |
| Big Bets | Invest time in planning |
| Fill-ins | Schedule when capacity allows |
| Money Pits | Deprioritize or eliminate |

### When to Use Which

| Situation | Framework |
|-----------|-----------|
| Quick sprint decisions | MoSCoW |
| Quarterly roadmap planning | RICE |
| Small team, lightweight process | Value vs Effort |
| Large team (50+ people) | RICE or Weighted Scoring |
| Strict deadline/resources | MoSCoW |

---

## Roadmap Types

### Now/Next/Later Roadmap

Time-horizon based, avoids specific dates. Ideal for fast-changing environments.

| Horizon | Timeframe | Commitment Level | Detail Level |
|---------|-----------|------------------|--------------|
| **Now** | This sprint/month | High (committed) | Features, tasks |
| **Next** | Next quarter | Medium (planned) | Themes, milestones |
| **Later** | 6-12 months | Low (exploratory) | Vision, goals |

**Benefits:**
- Removes date constraints
- Allows broad experimentation
- Only commits to immediate work
- Easy to communicate to stakeholders

### Quarterly/Time-Based Roadmap

```
Q1 2026              Q2 2026              Q3 2026
------------------------------------------------------------
[  Auth System  ]    [   Paywall   ]      [  AI Agents  ]
[ Landing Page ]     [ Content CMS ]      [ Mobile App  ]
                     [ Localization ]     [ Analytics   ]
```

**Best for:** Predictable environments, stakeholder reporting, resource planning.

### Theme-Based Roadmap

Organizes by strategic themes rather than time.

```
Theme: User Acquisition
├── Landing page optimization
├── SEO improvements
├── Social proof features
└── Referral program

Theme: Monetization
├── Stripe integration
├── Subscription tiers
├── Annual pricing
└── Enterprise tier
```

**Best for:** Strategy communication, cross-functional alignment.

### Outcome-Based Roadmap

Focuses on business outcomes, not features.

| Outcome | Key Results | Initiatives |
|---------|-------------|-------------|
| Increase activation | +20% trial-to-paid | Onboarding flow, email drip |
| Reduce churn | -15% monthly churn | Usage analytics, alerts |
| Expand revenue | +30% ARPU | Premium tier, add-ons |

**Best for:** OKR-driven teams, product-led growth.

---

## Grooming Best Practices

### Timing

- **Weekly grooming:** 30-60 minutes
- **Schedule:** 3/4 through each sprint
- **Attendees:** Product Owner, Dev Team, Scrum Master

### Session Structure

1. **Review new ideas** (10 min)
   - Quick assessment: worth exploring?
   - Move to validated or drop

2. **Prioritize backlog** (20 min)
   - Review top 20 items
   - Re-score based on new information
   - Adjust order

3. **Refine upcoming items** (20 min)
   - Add detail to next sprint's items
   - Clarify acceptance criteria
   - Identify dependencies

4. **Cleanup** (10 min)
   - Archive old items
   - Remove duplicates
   - Update estimates

### Key Principles

| Principle | Why |
|-----------|-----|
| Don't refine too far ahead | Requirements change, effort wasted |
| Only 1-3 items as P0 | Everything can't be "most important" |
| Maintain "Won't do" list | Explicit decisions prevent revisiting |
| Separate grooming from status | Focus on prioritization, not updates |
| Regularly archive old items | Keep backlog manageable |

---

## LLM-Assisted Backlog Work

### What LLMs Do Well

| Task | How LLM Helps |
|------|---------------|
| **Thought clarification** | Act as product coach, refine thinking |
| **Gap analysis** | "What'd I miss?" - identify variations, edge cases |
| **Risk identification** | Surface assumptions, potential issues |
| **Story generation** | Transform ideas into well-structured items |
| **Acceptance criteria** | Generate comprehensive AC from requirements |
| **Template filling** | Convert rough notes to formatted documents |

### What LLMs Cannot Do

| Limitation | Why |
|------------|-----|
| Strategic prioritization | Lacks business context, customer relationships |
| True value assessment | Cannot understand user pain deeply |
| Stakeholder negotiation | Requires human judgment, politics |
| Final decision-making | Product ownership is human responsibility |

### Caution: AI Confidence Trap

LLMs produce polished, persuasive text that can mask uncertainty:

> "Our brains have cognitive biases with AI. It's easy to get an LLM to produce polished text that looks like certainty. This can mislead developers into thinking 'This isn't a hypothesis. Don't ask questions here.'" - Humanizing Work

**Mitigation:**
- Mark AI-generated content as hypothesis
- Include confidence levels
- Encourage team questions
- Treat AI output as starting point, not final answer

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too many P0s | Only 1-3 items can be "most important" |
| Roadmap as commitment | Roadmap is plan, not promise - update as you learn |
| Never dropping items | Regularly archive old, irrelevant items |
| Grooming as status meeting | Focus on prioritization, not updates |
| No "Won't do" list | Explicitly document what you're NOT doing |
| Over-relying on AI output | Treat as hypothesis, validate with users |

---

## Related Files

| File | Content |
|------|---------|
| [checklist.md](checklist.md) | Grooming session checklist |
| [examples.md](examples.md) | RICE scoring, roadmap examples |
| [templates.md](templates.md) | Backlog item, roadmap templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for backlog/roadmap work |

---

## Resources

### Prioritization Frameworks
- [RICE Prioritization](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) - Intercom's original framework
- [MoSCoW Prioritization](https://www.productplan.com/glossary/moscow-prioritization/) - ProductPlan overview
- [Prioritization Frameworks](https://www.atlassian.com/agile/product-management/prioritization-framework) - Atlassian guide

### Backlog Management
- [Product Backlog Refinement](https://nextagile.ai/blogs/agile/product-backlog-refinement/) - NextAgile guide (2026)
- [Backlog Grooming Best Practices](https://everhour.com/blog/backlog-grooming/) - Everhour
- [What is a Product Backlog](https://www.scrum.org/resources/what-is-a-product-backlog) - Official Scrum Guide

### Roadmapping
- [Now-Next-Later Roadmaps](https://productschool.com/blog/product-strategy/now-next-later-roadmap) - Product School
- [Why I Invented Now-Next-Later](https://www.prodpad.com/blog/invented-now-next-later-roadmap/) - ProdPad origin story
- [Product Roadmap Templates](https://www.aha.io/roadmapping/guide/templates/product-roadmap) - Aha! templates

### AI in Product Management
- [AI in Backlog Management](https://thedigitalprojectmanager.com/productivity/ai-in-backlog-management/) - Practical applications
- [AI Backlog Pitfalls](https://www.humanizingwork.com/2-ai-backlog-pitfalls-to-watch-out-for/) - Humanizing Work
- [PM Prompts Repository](https://github.com/deanpeters/product-manager-prompts) - GitHub collection
