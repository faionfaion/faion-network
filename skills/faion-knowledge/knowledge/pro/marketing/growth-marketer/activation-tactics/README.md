---
id: activation-tactics
name: "Activation Tactics & Experiments"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Activation Tactics & Experiments

## Metadata

| Field | Value |
|-------|-------|
| **ID** | activation-tactics |
| **Name** | Activation Tactics & Experiments |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | activation-framework, activation-metrics, onboarding-flows, funnel-optimization |

---

## Activation Tactics

### Tactic 1: Progressive Onboarding

Instead of upfront setup, teach while doing.

```
BAD: 5 setup screens → empty product
GOOD: Skip setup → show value → setup when needed

Example:
1. User signs up
2. Immediately show sample project
3. Guide: "Try editing this task"
4. After value: "Now create your own project"
```

### Tactic 2: Templates and Presets

Reduce time to first value with starting points.

```
"Start with a template"

[ ] Blank project
[x] Marketing campaign
[x] Product launch
[x] Weekly planning
[x] Personal tasks

Users who use templates: 65% activation
Users who start blank: 35% activation
```

### Tactic 3: Activation Checklist

Guide users through setup with visible progress.

```
┌────────────────────────────────────┐
│ Getting Started (2/5)     ▓▓▓░░░   │
│ ──────────────────────────────────│
│ ✓ Create account                   │
│ ✓ Connect calendar                 │
│ ○ Create first event               │
│ ○ Share with someone              │
│ ○ Have first booking              │
└────────────────────────────────────┘
```

### Tactic 4: Empty State Design

Turn empty states into activation prompts.

```
BAD EMPTY STATE:
┌─────────────────────────────────┐
│         No projects yet         │
│                                 │
│         [Create Project]        │
└─────────────────────────────────┘

GOOD EMPTY STATE:
┌─────────────────────────────────┐
│    👋 Welcome, Sarah!           │
│                                 │
│    Create your first project    │
│    to get started               │
│                                 │
│ 💡 Tip: Start with a template   │
│    to see how others use [App]  │
│                                 │
│    [Start with Template]        │
│    [Create Blank Project]       │
└─────────────────────────────────┘
```

### Tactic 5: Time-to-Value Optimization

Minimize time from signup to Aha moment.

```
Current: Signup → 8 steps → Value (12 min)
Target:  Signup → 3 steps → Value (3 min)

Tactics:
- Remove optional steps
- Pre-fill with defaults
- Skip to core action
- Show value before config
```

### Tactic 6: Activation Emails

Re-engage users who did not activate.

```
EMAIL SEQUENCE:

Day 0 (2 hours): "Complete your setup"
- What they started
- Single CTA to continue

Day 1: "Here's what you can do"
- Top use cases
- Quick win action

Day 3: "Need help?"
- Video tutorial
- Support offer

Day 7: "Last chance"
- Limited trial reminder
- Success story
```

### Tactic 7: In-App Guidance

Help users discover next steps.

| Type | When to Use | Example |
|------|-------------|---------|
| Tooltips | First visit to feature | "Click here to add task" |
| Coach marks | Multi-step process | Pulsing dot on button |
| Slideouts | Complex features | Side panel tutorial |
| Videos | Better shown than told | Embedded Loom |
| Chat | User seems stuck | "Need help?" prompt |

---

## Activation Experiments

### Experiment Ideas

| Experiment | Target Metric | Expected Impact |
|------------|---------------|-----------------|
| Remove signup form fields | Signup → Step 2 | +10-20% |
| Add welcome video | Onboarding completion | +5-15% |
| Show templates first | Activation rate | +15-30% |
| Pre-fill sample data | Time to value | -50% |
| Add progress checklist | Activation rate | +10-25% |
| Simplify first action | Step N → Activation | +10-20% |
| Add tooltip guidance | Feature discovery | +5-15% |
| Send Day 1 email | D7 activation | +5-10% |

### Experiment Template

```markdown
## Experiment: [Name]

### Hypothesis
If we [change], then activation rate will increase by [X%]
because [reasoning].

### Variants
- Control: Current experience
- Treatment: [New experience]

### Sample Size
- Users per variant: 2,000
- Duration: 14 days
- Statistical power: 80%

### Metrics
- Primary: Day 7 activation rate
- Secondary: Time to activation, retention

### Results
| Variant | Activation | Time to Value |
|---------|------------|---------------|
| Control | | |
| Treatment | | |

### Decision
[Ship / Iterate / Kill]
```

---

## Templates

### Activation Checklist Configuration

```yaml
# Activation checklist config
checklist:
  title: "Get started with [Product]"
  items:
    - id: profile
      label: "Complete your profile"
      action: "/settings/profile"
      required: false

    - id: first_project
      label: "Create your first project"
      action: "/projects/new"
      required: true

    - id: invite
      label: "Invite a team member"
      action: "/team/invite"
      required: false

    - id: first_task
      label: "Complete a task"
      action: null  # Triggered by event
      required: true
      activation_event: true  # This = activated

  completion_reward:
    type: "confetti"
    message: "You're all set! 🎉"
```

### Activation Email Sequence

```markdown
# Activation Email Sequence

## Email 1: Welcome (Immediate)
**Subject:** Welcome to [Product]! Here's your first step
**Send:** On signup
**Content:**
- Personalized welcome
- Single clear CTA: "Create your first [X]"
- Expected time: "Takes 2 minutes"

## Email 2: Quick Win (Day 1)
**Subject:** Quick win: Do this in 5 minutes
**Send:** 24h after signup, if not activated
**Content:**
- Focus on single use case
- Step-by-step with images
- Social proof: "10,000 users did this today"

## Email 3: Help Offer (Day 3)
**Subject:** Need help getting started?
**Send:** 72h after signup, if not activated
**Content:**
- Video tutorial
- Book onboarding call option
- FAQ links

## Email 4: Last Push (Day 7)
**Subject:** Your trial is waiting...
**Send:** 7d after signup, if not activated
**Content:**
- Recap value proposition
- Success story from similar user
- Direct support CTA
```

---

## Implementation Checklist

- [ ] Select 3-5 tactics to implement first
- [ ] Design activation checklist
- [ ] Create email sequence
- [ ] Add in-app guidance (tooltips)
- [ ] Design better empty states
- [ ] Create templates/presets
- [ ] Implement progressive onboarding
- [ ] Set up A/B testing framework
- [ ] Run first experiment
- [ ] Analyze results
- [ ] Iterate and optimize

---

## Tools

| Purpose | Tools |
|---------|-------|
| Onboarding flows | Appcues, Pendo, Userflow |
| In-app guidance | Chameleon, Whatfix |
| Email sequences | Customer.io, Intercom |
| A/B testing | Optimizely, LaunchDarkly |
| Session recording | Hotjar, FullStory, LogRocket |
| Funnel analysis | Amplitude, Mixpanel, Posthog |

---

## Further Reading

- Samuel Hulick, "The Elements of User Onboarding"
- Wes Bush, "Product-Led Growth" (PLG activation)
- Reforge, "Activation and Retention" course
- Nir Eyal, "Hooked" (habit formation)

---

## Related Methodologies

- **activation-framework:** Activation framework and path optimization
- **activation-metrics:** Activation metrics definition and measurement
- **onboarding-flows:** Onboarding flow design and optimization
- **funnel-optimization:** Funnel Optimization (activation funnel)
- **product-led-growth:** Product-Led Growth (activation is PLG core)

---

*Methodology: activation-tactics | Growth | faion-growth-agent*

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Pull analytics data from Mixpanel, format report | haiku | Data extraction and formatting |
| Analyze A/B test results for statistical significance | sonnet | Statistical analysis and interpretation |
| Generate cohort retention curve analysis | sonnet | Data interpretation and visualization |
| Design growth loop for new product vertical | opus | Strategic design with multiple levers |
| Recommend optimization tactics for viral coefficient | sonnet | Metrics understanding and recommendations |
| Plan AARRR framework for pre-launch phase | opus | Comprehensive growth strategy |
| Implement custom analytics event tracking schema | sonnet | Technical setup and validation |
