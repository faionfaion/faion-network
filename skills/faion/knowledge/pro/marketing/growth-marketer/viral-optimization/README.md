---
id: viral-optimization
name: "Viral Loop Optimization"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Viral Loop Optimization

## Metadata

| Field | Value |
|-------|-------|
| **ID** | viral-optimization |
| **Name** | Viral Loop Optimization |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | viral-metrics, viral-loops, ab-testing-framework |

---

## Improving Your K-factor

### Step 1: Measure Current K

Track these metrics:

| Metric | Description | How to Track |
|--------|-------------|--------------|
| Invites sent | Total invitations | Count invite events |
| Invites per user | Average i | Total invites / Active users |
| Invite clicks | Recipients who clicked | UTM tracking |
| Invite signups | Recipients who signed up | Referral attribution |
| Conversion rate | c = signups / invites sent | Calculate ratio |

### Step 2: Find Your Viral Loop Type

Which type fits your product?

| Product Type | Best Loop Type |
|--------------|----------------|
| Collaboration tool | Inherent |
| Consumer app | Content + WOM |
| Marketplace | Incentivized |
| Productivity tool | WOM + Inherent |
| Social network | Content + Inherent |

See **viral-loops.md** for detailed loop types.

### Step 3: Optimize Invites (i)

**Identify share moments:**

1. Achievement (completed goal, milestone)
2. Discovery (found something great)
3. Social (want to connect with friend)
4. Help (need someone to use with)

**Create friction-free sharing:**

```
Bad: Navigate to settings → Find invite → Copy link → Paste
Good: [Share] button → One tap to send
```

### Step 4: Optimize Conversion (c)

**Landing page for invites:**

```
Good invite landing page:
1. [Avatar] John invited you to [Product]
2. "Join 50,000 people using [Product] to [benefit]"
3. [Sign up with Google] - one click
4. Preview of what they get
```

**Reduce friction:**

- Pre-fill email from invite
- One-click signup (Google, Apple)
- Show value before signup
- Mobile-optimized

---

## K-factor Optimization Experiments

### Experiment Ideas

| Experiment | Metric | Expected Impact |
|------------|--------|-----------------|
| Add share button post-achievement | i | +30% |
| Two-sided referral incentive | Both | +50% |
| Personal invite (name + photo) | c | +25% |
| One-click signup for invitees | c | +40% |
| Contact import for bulk invite | i | +100% |
| Share milestone badges | i | +20% |
| Social proof on invite page | c | +15% |

### A/B Test Template

```markdown
## K-factor Experiment: [Name]

### Hypothesis
If we [change], then K-factor will increase by [X%]
because [reason].

### Variants
- Control: Current invite flow
- Treatment: [New flow]

### Metrics
- Primary: K-factor
- Secondary: Invites sent (i), Conversion rate (c)

### Sample Size
- Users: 10,000 per variant
- Duration: 14 days

### Results
| Variant | i | c | K | Change |
|---------|---|---|---|--------|
| Control | | | | - |
| Treatment | | | | |

### Decision
[Winner / Need more data / No significant difference]
```

---

## Optimization Tactics by Component

### Increasing Invites (i)

| Tactic | Description | Difficulty | Impact |
|--------|-------------|------------|--------|
| Achievement triggers | Share after completing milestone | Easy | High |
| Multi-channel sharing | Email, SMS, social, copy link | Medium | Medium |
| Contact import | Bulk invite from contacts | Hard | High |
| Viral content | Shareable results, badges | Medium | High |
| Team features | Require collaboration | Hard | Very High |
| Referral incentives | Rewards for inviting | Easy | Medium |

### Increasing Conversion (c)

| Tactic | Description | Difficulty | Impact |
|--------|-------------|------------|--------|
| Personal invites | "John invited you" vs generic | Easy | High |
| Social proof | "5 friends use this" | Medium | High |
| Clear value prop | Why should they join? | Easy | High |
| One-click signup | Google/Apple SSO | Medium | High |
| Invitee incentive | "$10 when you join" | Easy | Medium |
| Preview value | Show what they'll get | Medium | Medium |
| Mobile optimization | Fast mobile signup | Hard | High |

---

## Implementation Checklist

- [ ] Define your viral loop type
- [ ] Instrument invite tracking (sent, clicked, converted)
- [ ] Calculate baseline K-factor
- [ ] Identify natural share moments in product
- [ ] Design referral program (if applicable)
- [ ] A/B test invite copy and design
- [ ] Optimize invite landing page
- [ ] Reduce signup friction for invitees
- [ ] Track K-factor weekly
- [ ] Run optimization experiments

---

## Optimization by Product Stage

### Pre-Launch
- [ ] Design viral loop into product
- [ ] Plan tracking infrastructure
- [ ] Create invite landing page

### Launch (0-1K users)
- [ ] Measure baseline K-factor
- [ ] Identify top referrers
- [ ] Test different invite channels

### Growth (1K-10K users)
- [ ] Optimize invite conversion
- [ ] Add share moments
- [ ] Run A/B tests on incentives

### Scale (10K+ users)
- [ ] Automate viral loop tracking
- [ ] Segment by user cohorts
- [ ] Advanced personalization

---

## Advanced Tactics

### Personalization

**Personalize invites by:**
- User's achievement level
- Social graph data
- Past invite behavior
- Industry/segment

**Example:**
```
Generic: "Try [Product]"
Personal: "John just completed 100 tasks in [Product] and wants you to join his team"
```

### Multi-step Incentives

Instead of one-time reward, create escalating incentives:

| Referrals | Referrer Reward |
|-----------|----------------|
| 1 | $10 credit |
| 5 | $50 credit + badge |
| 10 | $100 credit + premium feature |
| 50 | Lifetime premium |

### Viral Content Templates

Make content inherently shareable:

```
✅ Include branding (watermark, logo)
✅ Make it visual (images, charts)
✅ Add social comparison ("Beat 67% of users")
✅ Include CTA ("Create your own at...")
✅ No spoilers (don't reveal full value)
```

---

## Monitoring & Iteration

### Weekly Review

1. Check K-factor trend
2. Analyze invite funnel
3. Identify drop-off points
4. Review top referrers
5. Plan next experiment

### Monthly Deep Dive

1. Cohort analysis by signup source
2. Retention of referred users
3. LTV of referred vs organic
4. Channel performance
5. Fraud detection

### Quarterly Strategy

1. Review loop type effectiveness
2. Major product changes to improve virality
3. Incentive structure optimization
4. Competitive analysis

---

## Red Flags

| Warning Sign | What It Means | Action |
|--------------|---------------|--------|
| K declining | Viral loop broken | Urgent investigation |
| i dropping | Fewer invites sent | Add share moments |
| c dropping | Lower conversion | Optimize landing page |
| High fraud | Fake signups | Strengthen validation |
| Low quality referrals | Referred users churn fast | Adjust incentives |

---

## Case Study: Optimizing Referral Flow

### Before
```
User completes task
  ↓ (30% see prompt)
Referral prompt in settings
  ↓ (5% click)
Generic invite form
  ↓ (2% send invites)
Generic landing page
  ↓ (10% convert)

K = 0.30 × 0.05 × 2 × 0.10 = 0.0003
```

### After
```
User completes task
  ↓ (100% see modal)
Celebration modal with share button
  ↓ (25% click)
One-click share (pre-filled)
  ↓ (50% send invites)
Personal landing page
  ↓ (30% convert)

K = 1.0 × 0.25 × 0.50 × 0.30 = 0.0375

125x improvement
```

**Changes made:**
1. Moved prompt to achievement moment (natural trigger)
2. Made sharing one-click (reduced friction)
3. Personalized invite message (higher send rate)
4. Personalized landing page (higher conversion)

---

## Tools

| Purpose | Tools |
|---------|-------|
| Referral tracking | ReferralCandy, Viral Loops, Friendbuy |
| Attribution | Branch, AppsFlyer, Adjust |
| Analytics | Mixpanel, Amplitude |
| A/B testing | Optimizely, LaunchDarkly |
| Social sharing | AddThis, ShareThis |

---

## Related Methodologies

- **viral-metrics:** K-factor calculation and dashboard
- **viral-loops:** Types of viral loops
- **ab-testing-framework:** A/B testing methodology
- **growth-loops:** General growth loop framework

---

*Methodology: viral-optimization | Growth | faion-growth-agent*

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
