# Product Manager Methodologies Summary

Quick reference for all 33 methodologies in this skill.

## Core Methodologies (18)

### MVP & MLP

| Methodology | Problem | Key Output | Agent |
|-------------|---------|------------|-------|
| mvp-scoping | Teams build too much before validation | Core problem, minimum features, 4-week constraint | faion-mvp-scope-analyzer-agent |
| mlp-planning | MVP works but users don't love it | WOW moments, delight features, MLP phases | faion-mlp-agent |

**MLP Dimensions:** Delight, Ease, Speed, Trust, Personality

### Feature Prioritization

| Methodology | Problem | Framework | Formula |
|-------------|---------|-----------|---------|
| feature-prioritization-rice | Too many features, limited resources | Reach, Impact, Confidence, Effort | `RICE = (R × I × C) / E` |
| feature-prioritization-moscow | Stakeholders disagree on priorities | Must, Should, Could, Won't | 60%/20%/10%/0% |

### Planning & Roadmaps

| Methodology | Problem | Solution |
|-------------|---------|----------|
| roadmap-design | No clear development direction | Now-Next-Later, milestones, 20% buffer |
| user-story-mapping | Features lack user context | Activities → Tasks → Releases |
| release-planning | Unclear work for upcoming sprint | Sprint goal, capacity, velocity |
| product-launch | No clear release timeline | Release goal, effort, sprints + 20% buffer |

### Goals & Metrics

| Methodology | Problem | Framework |
|-------------|---------|-----------|
| okr-setting | Goals are vague or unmeasurable | Objective + 3-5 Key Results + Initiatives |

### Discovery & Validation

| Methodology | Problem | Framework | Agent |
|-------------|---------|-----------|-------|
| problem-validation | Building solutions for non-problems | 5+ interviews, competitor analysis, search volume | faion-market-researcher-agent |
| product-discovery | Root cause not understood | Five Whys (5 levels deep) | faion-pm-agent |
| jobs-to-be-done | Features don't match user needs | When [situation], I want [motivation], So I can [outcome] | faion-persona-builder-agent |

### Business Models

| Methodology | Problem | Framework | Agent |
|-------------|---------|-----------|-------|
| business-model-research | Business model not structured | Lean Canvas (9 blocks) | faion-pm-agent |
| value-proposition-design | Product-market fit unclear | Customer segment + Value map | faion-market-researcher-agent |
| niche-evaluation | Too many opportunities | Weighted scoring (market size, competition, fit, monetization) | faion-market-researcher-agent |

### Operations

| Methodology | Problem | Solution |
|-------------|---------|----------|
| backlog-management | Backlog items unclear or oversized | DEEP principles, Definition of Ready |
| stakeholder-management | Features disconnected from goals | Goal → Actor → Impact → Deliverable |
| risk-assessment | Unknown risks in product decisions | Impact × Uncertainty matrix, test high-risk first |

---

## Extended Methodologies (15)

See individual files for full details:

### Discovery & Research
- [continuous-discovery.md](continuous-discovery.md) - Weekly customer touchpoints
- [continuous-discovery-habits.md](continuous-discovery-habits.md) - Building discovery muscle
- [feedback-management.md](feedback-management.md) - Collecting and managing user feedback

### Product Development
- [ai-native-product-development.md](ai-native-product-development.md) - AI-first product principles
- [agentic-ai-product-development.md](agentic-ai-product-development.md) - Agentic AI products
- [micro-mvps.md](micro-mvps.md) - Landing page, concierge, Wizard of Oz, video demo
- [minimum-product-frameworks.md](minimum-product-frameworks.md) - MVP/MLP/MMP/MAC/RAT/MDP/MVA/MFP/SLC

### Roadmaps & Strategy
- [outcome-based-roadmaps.md](outcome-based-roadmaps.md) - Outcome-driven roadmaps
- [outcome-based-roadmaps-advanced.md](outcome-based-roadmaps-advanced.md) - Advanced techniques
- [competitive-positioning.md](competitive-positioning.md) - Market positioning
- [portfolio-strategy.md](portfolio-strategy.md) - Multi-product portfolio

### Growth & Scale
- [product-led-growth.md](product-led-growth.md) - PLG strategy
- [experimentation-at-scale.md](experimentation-at-scale.md) - Scaling experiments
- [learning-speed-competitive-moat.md](learning-speed-competitive-moat.md) - Learning velocity advantage

### Operations & Lifecycle
- [product-lifecycle.md](product-lifecycle.md) - Intro/Growth/Maturity/Decline stages
- [product-operations.md](product-operations.md) - Product ops processes
- [product-analytics.md](product-analytics.md) - Analytics and measurement
- [product-explainability.md](product-explainability.md) - Making products transparent
- [spec-writing.md](spec-writing.md) - Writing effective specs
- [technical-debt-management.md](technical-debt-management.md) - Technical debt strategy
- [blurred-roles-team-evolution.md](blurred-roles-team-evolution.md) - Team structure evolution

---

## Quick Selection Guide

| Task | Use Methodology |
|------|-----------------|
| Define MVP | mvp-scoping |
| Add delight to MVP | mlp-planning |
| Choose next feature | feature-prioritization-rice or moscow |
| Create roadmap | roadmap-design, outcome-based-roadmaps |
| Set team goals | okr-setting |
| Validate idea | problem-validation, jobs-to-be-done |
| Launch product | product-launch |
| Manage backlog | backlog-management |
| Continuous improvement | continuous-discovery-habits |
| Scale experiments | experimentation-at-scale |

---

*Product Manager Methodologies v1.0*
*33 methodologies | 18 core + 15 extended*
