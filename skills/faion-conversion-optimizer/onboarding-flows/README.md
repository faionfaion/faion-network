---
id: onboarding-flows
name: "User Onboarding Flow Design"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# User Onboarding Flow Design

## Metadata

| Field | Value |
|-------|-------|
| **ID** | onboarding-flows |
| **Name** | User Onboarding Flow Design |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | activation-metrics, activation-framework, activation-tactics, product-led-growth |

---

## Overview

User onboarding is the critical first experience that guides new users from signup to activation. Great onboarding reduces friction, demonstrates value quickly, and sets users up for long-term success.

**Goal:** Get users to their first "Aha moment" as quickly as possible.

---

## Onboarding Principles

### 1. Show Value Before Asking for Work

```
BAD: Setup form → Empty product → Figure it out
GOOD: Sample data → Quick win → Customize
```

### 2. Progressive Disclosure

Don't overwhelm users with everything at once.

```
Session 1: Core action only
Session 2: Related feature
Session 3: Advanced capabilities
```

### 3. Contextual Learning

Teach features when users need them, not upfront.

```
BAD: "Here are 20 features you can use"
GOOD: User tries to share → Show sharing options
```

### 4. Remove Optional Steps

Every additional step loses users.

```
Current: 8 steps (50% complete all)
Optimized: 3 steps (85% complete all)
= 70% more activated users
```

---

## Onboarding Flow Patterns

### Pattern 1: Template-First

Start with pre-built example, let users customize.

**Best for:** Tools with configurable workflows

```
1. Signup
2. "Choose a template" (show 4-6 popular)
3. Template loads with sample data
4. "Try editing this task" (guided)
5. "Great! Now create your own"
```

**Example:** Notion, Trello, Canva

### Pattern 2: Wizard Onboarding

Step-by-step guided setup.

**Best for:** Products needing configuration

```
1. Signup
2. "Tell us about your team" (1-2 questions)
3. "Connect your tools" (integrations)
4. "You're ready!" → Show dashboard
```

**Example:** Slack, Asana, Zapier

### Pattern 3: Interactive Tutorial

Learn by doing with guided tasks.

**Best for:** Products with spatial UI or complex interactions

```
1. Signup
2. Interactive demo environment
3. "Click here to..." (tooltips)
4. Complete mini-tutorial
5. Real environment unlocked
```

**Example:** Figma, Photoshop, Duolingo

### Pattern 4: Self-Serve Exploration

Minimal guidance, let users explore.

**Best for:** Simple, intuitive products

```
1. Signup
2. Brief welcome message
3. Product with helpful tooltips
4. Optional help center
```

**Example:** Instagram, Twitter, Pinterest

### Pattern 5: Concierge Onboarding

High-touch personal onboarding.

**Best for:** Enterprise B2B, complex products

```
1. Signup
2. Schedule onboarding call
3. 1-on-1 setup session
4. Ongoing check-ins
```

**Example:** Salesforce, SAP, enterprise tools

---

## Onboarding Flow Design

### Step 1: Map User Intent

Different users have different goals.

| User Segment | Primary Intent | Optimal Path |
|--------------|----------------|--------------|
| Individual user | Personal productivity | Personal template |
| Team admin | Team collaboration | Team setup wizard |
| Evaluator | Compare features | Feature tour |
| Power user | Advanced use case | Skip to advanced |

### Step 2: Design for Each Segment

**Segment at signup:**

```
"What brings you here?"

[ ] Personal use
[ ] Team collaboration
[ ] Just exploring
```

**Route to appropriate onboarding:**
- Personal → Quick start template
- Team → Team setup wizard
- Exploring → Interactive demo

### Step 3: Define Critical Path

What's the minimum viable onboarding?

```
CRITICAL PATH (must complete):
1. Signup
2. First value action
3. Activation event

OPTIONAL (can skip):
- Profile completion
- Feature tour
- Integrations
```

### Step 4: Add Motivation

Show progress and celebrate wins.

```
┌──────────────────────────────┐
│ Getting Started (2/3) ▓▓░    │
│ ─────────────────────────── │
│ ✓ Created account            │
│ ✓ Imported data              │
│ → Complete your first task   │
└──────────────────────────────┘
```

---

## Onboarding UI Patterns

### Welcome Modal

```
┌───────────────────────────────────┐
│     Welcome to [Product]!         │
│                                   │
│  We'll get you set up in 2 min    │
│                                   │
│  [Get Started]  [Skip Tutorial]   │
└───────────────────────────────────┘
```

**When to use:** Product needs brief explanation

**Best practices:**
- Keep it under 50 words
- Single clear CTA
- Allow skip option
- Show estimated time

### Tooltip Tour

```
  ┌─────────────────────┐
  │ Click here to       │
  │ create your first   │
  │ project             │
  └────────┬────────────┘
           │
      [Button]
```

**When to use:** Point out key UI elements

**Best practices:**
- Highlight one thing at a time
- Use contextual triggers
- Allow dismissal
- Don't block the UI

### Progress Checklist

```
┌────────────────────────────┐
│ Quick Start (2/5)          │
│ ──────────────────────────│
│ ✓ Connect calendar         │
│ ✓ Create first event       │
│ → Share your link          │
│ ○ Get your first booking   │
│ ○ Customize your page      │
└────────────────────────────┘
```

**When to use:** Multi-step setup process

**Best practices:**
- 3-7 items max
- Clear completion criteria
- Show progress bar
- Celebrate completion

### Empty States

```
┌──────────────────────────────┐
│  👋 Your dashboard is empty  │
│                              │
│  Get started by:             │
│  • Creating your first task  │
│  • Importing from [Tool]     │
│  • Starting with a template  │
│                              │
│     [Create Task]            │
└──────────────────────────────┘
```

**When to use:** After core setup, before content

**Best practices:**
- Explain why it's empty
- Offer 2-3 starting actions
- Use visuals/illustrations
- Make primary action obvious

---

## Measuring Onboarding Success

### Key Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Onboarding completion | % who finish setup | >80% |
| Time to complete | Minutes from signup | <5 min |
| Step completion rate | % completing each step | >90% per step |
| Activation rate | % reaching Aha moment | >50% D0 |

### Drop-off Analysis

Track where users abandon:

```
STEP                  COMPLETION   DROP
────────────────────────────────────────
1. Signup                 100%     -
2. Email verify            85%     15%  ← High drop
3. Profile setup           75%     10%
4. First action            60%     15%  ← High drop
5. Activated               55%      5%
```

**Focus on:** Steps with >10% drop-off

---

## Optimization Tactics

### Tactic 1: Reduce Steps

```
Before: 7 steps (40% complete)
After: 3 steps (75% complete)
= 87% more activated users
```

### Tactic 2: Make Steps Optional

```
REQUIRED:
- Email
- First action

OPTIONAL (can complete later):
- Profile photo
- Preferences
- Integrations
```

### Tactic 3: Pre-fill with Defaults

```
Instead of: "Choose your timezone"
Use: Auto-detect timezone (allow change)
```

### Tactic 4: Show Example First

```
Instead of: Empty form
Show: Pre-filled example (click to edit)
```

### Tactic 5: Celebrate Completion

```
On activation:
- Confetti animation
- Success message
- Unlock next feature
```

---

## Common Onboarding Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Too many steps | 50%+ drop-off | Reduce to 3-5 essential |
| Generic for all users | Low relevance | Segment by intent |
| Feature tour upfront | Overwhelming | Teach contextually |
| Required profile setup | Delays value | Make optional |
| No progress indication | Users feel lost | Add checklist/progress |
| Can't skip | Frustrates power users | Always allow skip |

---

## Onboarding Email Sequence

Support onboarding with timely emails.

### Sequence Structure

```
TRIGGER: User signup
GOAL: Complete activation

Email 1 (Immediate): Welcome + first action
Email 2 (Day 1): Quick win tutorial
Email 3 (Day 3): Feature highlight
Email 4 (Day 7): Success story

STOP SENDING: When user activates
```

### Email Templates

See: [activation-tactics.md](activation-tactics.md) for detailed email templates

---

## Testing Onboarding

### A/B Test Ideas

| Test | Hypothesis |
|------|------------|
| 3 steps vs 5 steps | Fewer steps → higher completion |
| Template vs blank | Template → faster activation |
| Video vs text | Video → better understanding |
| Checklist vs wizard | Checklist → more flexible |
| Skip option vs required | Skip → less friction |

### User Testing

Watch 10+ users go through onboarding:
- Where do they get stuck?
- What questions do they ask?
- What do they skip?
- How long does it take?

---

## Implementation Checklist

- [ ] Define activation event
- [ ] Map all user segments
- [ ] Design critical path (3-5 steps)
- [ ] Create onboarding UI (modals, tooltips, checklist)
- [ ] Add progress tracking
- [ ] Set up email sequence
- [ ] Track completion metrics
- [ ] Watch user sessions
- [ ] Run A/B tests
- [ ] Iterate weekly

---

## Tools

| Purpose | Tools |
|---------|-------|
| Onboarding flows | Appcues, Pendo, Userflow |
| In-app guidance | Chameleon, Whatfix, Userpilot |
| Email sequences | Customer.io, Intercom, Loops |
| User testing | Hotjar, FullStory, Maze |
| Analytics | Amplitude, Mixpanel, Posthog |

---

## Related Methodologies

- **activation-metrics:** Define what success looks like
- **activation-framework:** Framework for activation optimization
- **activation-tactics:** Tactics to improve activation
- **product-led-growth:** PLG relies on great onboarding
- **funnel-optimization:** Onboarding is a critical funnel

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Map funnel metrics and baseline metrics | haiku | Direct query of existing data |
| A/B test hypothesis generation and prioritization | sonnet | Reasoning about impact/confidence/ease |
| Landing page copywriting and design feedback | sonnet | Creative iteration, user psychology |
| Funnel optimization campaign setup | opus | Complex multi-funnel strategy, org-wide impact |
| Free trial flow analysis and recommendations | sonnet | Understanding conversion psychology |
| PLG product strategy and feature design | opus | Architecture decisions, product-market fit |
| Onboarding flow user testing interpretation | sonnet | Qualitative analysis and recommendations |

---

## Sources

- [The Elements of User Onboarding (Samuel Hulick)](https://www.useronboard.com/user-onboarding-teardowns/)
- [Onboarding Patterns (Appcues)](https://www.appcues.com/blog/user-onboarding-best-practices)
- [Progressive Disclosure in UX (Nielsen Norman Group)](https://www.nngroup.com/articles/progressive-disclosure/)
- [Product-Led Growth Onboarding (Reforge)](https://www.reforge.com/blog/product-led-growth-onboarding)
- [Onboarding Metrics Guide (Mixpanel)](https://mixpanel.com/blog/user-onboarding-metrics/)

---

*Methodology: onboarding-flows | Growth | faion-growth-agent*
