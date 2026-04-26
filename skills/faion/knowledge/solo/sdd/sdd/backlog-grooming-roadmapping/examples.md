# Backlog & Roadmap Examples

Practical examples of RICE scoring, roadmap formats, and prioritization decisions.

---

## RICE Scoring Examples

### Example 1: Social Login (High Priority)

**Feature:** Add social login (Google, GitHub)

| Factor | Value | Rationale |
|--------|-------|-----------|
| **Reach** | 8 | 80% of users would use it (based on competitor data) |
| **Impact** | 1 | Medium impact - convenience, not core value |
| **Confidence** | 80% | Good data from competitors, clear implementation |
| **Effort** | 1 | ~1 person-month (OAuth2 integration) |

**RICE Score = (8 x 1 x 0.8) / 1 = 6.4**

**Decision:** High priority - good reach, reasonable effort.

---

### Example 2: Dark Mode (Low Priority)

**Feature:** Add dark mode theme

| Factor | Value | Rationale |
|--------|-------|-----------|
| **Reach** | 3 | 30% of users requested |
| **Impact** | 0.5 | Low impact - cosmetic preference |
| **Confidence** | 100% | Clear requirement, known implementation |
| **Effort** | 0.5 | ~2 weeks (CSS variables + toggle) |

**RICE Score = (3 x 0.5 x 1.0) / 0.5 = 3.0**

**Decision:** Lower priority than social login (6.4 > 3.0), despite faster implementation.

---

### Example 3: AI-Powered Search (Medium Priority)

**Feature:** Semantic search with embeddings

| Factor | Value | Rationale |
|--------|-------|-----------|
| **Reach** | 6 | 60% of active users search weekly |
| **Impact** | 2 | High impact - significantly improves UX |
| **Confidence** | 50% | New technology, uncertain user adoption |
| **Effort** | 3 | ~3 person-months (embeddings, vector DB, UI) |

**RICE Score = (6 x 2 x 0.5) / 3 = 2.0**

**Decision:** Medium priority - high potential but low confidence. Consider smaller experiment first.

---

### Example 4: Enterprise SSO (Strategic)

**Feature:** SAML/OIDC for enterprise customers

| Factor | Value | Rationale |
|--------|-------|-----------|
| **Reach** | 2 | Only 20 enterprise prospects |
| **Impact** | 3 | Massive - enables enterprise deals ($50k+ ARR each) |
| **Confidence** | 80% | Clear requirement from sales pipeline |
| **Effort** | 2 | ~2 person-months (SAML + admin UI) |

**RICE Score = (2 x 3 x 0.8) / 2 = 2.4**

**Decision:** Strategic priority - low reach but high revenue impact. Consider alongside RICE score.

---

## Prioritization Comparison

| Feature | Reach | Impact | Confidence | Effort | RICE | Priority |
|---------|-------|--------|------------|--------|------|----------|
| Social Login | 8 | 1 | 80% | 1 | **6.4** | P1 |
| Dark Mode | 3 | 0.5 | 100% | 0.5 | **3.0** | P3 |
| AI Search | 6 | 2 | 50% | 3 | **2.0** | P2 |
| Enterprise SSO | 2 | 3 | 80% | 2 | **2.4** | P1 (strategic) |

**Key insight:** RICE alone doesn't capture strategic value. Enterprise SSO has lower score but unlocks new market segment.

---

## Now/Next/Later Roadmap Example

### SaaS Product Roadmap

```
NOW (Jan-Feb 2026)                          Committed
------------------------------------------------------------
[x] User authentication v2              [==========] 100%
[ ] Stripe billing integration          [======    ] 60%
[ ] Dashboard redesign                  [===       ] 30%

NEXT (Q1 2026)                              Planned
------------------------------------------------------------
[ ] Team collaboration features
[ ] API rate limiting
[ ] Mobile-responsive improvements
[ ] Analytics dashboard v1

LATER (Q2-Q3 2026)                          Exploratory
------------------------------------------------------------
[ ] AI-powered recommendations
[ ] White-label solution
[ ] Mobile native app
[ ] Enterprise tier with SSO
```

---

## Quarterly Roadmap Example

### Q1 2026: faion.net Platform

```
JANUARY: Foundation
--------------------------------------------------------------
Week 1-2: Framework Content
  [x] Create domain skills (8)
  [x] Write methodologies (282)
  [x] Update agents (29)

Week 3-4: Landing Page
  [ ] Design landing page
  [ ] Implement Gatsby frontend
  [ ] Deploy to production

FEBRUARY: Core Product
--------------------------------------------------------------
Week 1-2: Backend API
  [ ] Set up Django
  [ ] Implement auth endpoints
  [ ] Deploy to Hetzner

Week 3-4: Paywall System
  [ ] Stripe integration
  [ ] Subscription tiers
  [ ] Payment flows

MARCH: Content & Launch
--------------------------------------------------------------
Week 1-2: Content Platform
  [ ] Methodology viewer
  [ ] Search functionality
  [ ] Progress tracking

Week 3-4: Localization
  [ ] 8 language support
  [ ] Translation pipeline
  [ ] Regional pricing
```

---

## Theme-Based Roadmap Example

### User Acquisition Theme

```
Theme: User Acquisition
Priority: P0 (Critical for growth)
Timeline: Q1-Q2 2026

Initiatives:
├── Landing Page Optimization
│   ├── A/B test hero messaging
│   ├── Add social proof section
│   ├── Optimize page speed
│   └── Mobile experience improvements
│
├── SEO Foundation
│   ├── Technical SEO audit
│   ├── Content pillar pages (5)
│   ├── Internal linking structure
│   └── Schema markup implementation
│
├── Conversion Optimization
│   ├── Streamline signup flow
│   ├── Add progress indicators
│   ├── Email validation improvements
│   └── Welcome email sequence
│
└── Analytics Setup
    ├── Event tracking (Mixpanel)
    ├── Conversion funnel analysis
    ├── User journey mapping
    └── Weekly metrics dashboard
```

### Monetization Theme

```
Theme: Monetization
Priority: P1 (After acquisition)
Timeline: Q2-Q3 2026

Initiatives:
├── Payment Infrastructure
│   ├── Stripe integration
│   ├── Subscription management
│   ├── Invoice generation
│   └── Tax handling (Stripe Tax)
│
├── Pricing Strategy
│   ├── Tier structure (Free/Pro/Team)
│   ├── Annual discount (20%)
│   ├── Regional pricing
│   └── Pricing page design
│
├── Upgrade Flows
│   ├── In-app upgrade prompts
│   ├── Feature comparison table
│   ├── Trial-to-paid automation
│   └── Dunning management
│
└── Enterprise
    ├── Custom pricing model
    ├── SSO/SAML support
    ├── Contract management
    └── Dedicated support tier
```

---

## MoSCoW Categorization Example

### Feature Release: MVP v1.0

**Release Goal:** Launch minimum viable product for early adopters

| Category | Features | Scope % |
|----------|----------|---------|
| **Must Have** | | 60% |
| | User authentication (email/password) | |
| | Core methodology viewer | |
| | Basic search | |
| | Mobile-responsive layout | |
| **Should Have** | | 20% |
| | Social login (Google) | |
| | Favorites/bookmarks | |
| | Progress tracking | |
| **Could Have** | | 20% |
| | Dark mode | |
| | PDF export | |
| | Email notifications | |
| **Won't Have** | | Documented |
| | Team collaboration | Future v2.0 |
| | AI recommendations | Future v2.0 |
| | Mobile native app | Future v3.0 |
| | Offline mode | Deferred indefinitely |

---

## Roadmap Change Documentation

### Example: Deprioritizing Mobile App

**Date:** 2026-01-15

**Change:** Mobile native app moved from Q2 to Later (TBD)

**Reason:**
- User research showed 85% desktop usage
- PWA covers mobile needs adequately
- Resources needed for enterprise features
- Enterprise revenue opportunity: $200k ARR potential

**Impact:**
- 3 enterprise deals can now close in Q2
- Mobile users continue with PWA
- Revisit mobile app decision in Q3 review

**Stakeholder Communication:**
- Marketing: Updated messaging (desktop-first)
- Sales: Enterprise features prioritized
- Users: PWA improvements planned

---

## Grooming Session Output Example

### Session: 2026-01-20

**Attendees:** Product Owner, Tech Lead, 3 Engineers

**Duration:** 45 minutes

#### New Ideas Reviewed

| ID | Title | Decision | Reason |
|----|-------|----------|--------|
| BL-045 | Add CSV export | Keep | Multiple user requests |
| BL-046 | Blockchain integration | Drop | No clear user need |
| BL-047 | Keyboard shortcuts | Keep | Developer segment values |

#### Priority Changes

| ID | Title | Old | New | Reason |
|----|-------|-----|-----|--------|
| BL-032 | API rate limiting | P2 | P1 | Abuse incidents increasing |
| BL-018 | Dark mode | P2 | P3 | Lower than expected demand |

#### Items Refined

| ID | Title | Changes |
|----|-------|---------|
| BL-029 | Team billing | Added acceptance criteria for pro-rating |
| BL-033 | SSO support | Broke into 3 sub-tasks |

#### Next Sprint Candidates

| Priority | ID | Title | Complexity |
|----------|-----|-------|------------|
| 1 | BL-032 | API rate limiting | Medium |
| 2 | BL-029 | Team billing | High |
| 3 | BL-045 | CSV export | Low |

#### Action Items

- [ ] Product Owner: Get legal review on team billing terms
- [ ] Tech Lead: Spike on rate limiting approach
- [ ] Designer: Wireframes for team billing UI
