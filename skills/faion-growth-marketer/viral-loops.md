---
id: viral-loops
name: "Viral Loops & Types"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Viral Loops & Types

## Metadata

| Field | Value |
|-------|-------|
| **ID** | viral-loops |
| **Name** | Viral Loops & Types |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | viral-metrics, viral-optimization, growth-loops |

---

## The Viral Loop

```
1. USER JOINS
   New user experiences value
           ↓
2. TRIGGER
   User encounters share moment
           ↓
3. INVITATION
   User sends invite to friends
           ↓
4. CONVERSION
   Friend clicks and signs up
           ↓
5. REPEAT
   New user goes through same loop
```

---

## Types of Viral Loops

### 1. Word of Mouth (WOM)

Users naturally tell others about your product.

```
User → Tells friend → Friend signs up
```

**Examples:** Exceptional products (Notion, Figma)

**Characteristics:**
- Low i (not everyone tells)
- High c (strong recommendation)
- Typical K: 0.1-0.5

**When to use:**
- Product is genuinely exceptional
- Strong brand or unique value prop
- Natural share moments exist

### 2. Inherent Virality

Product requires others to function.

```
User → Needs to collaborate → Invites colleague
```

**Examples:** Slack, Zoom, Figma, Google Docs

**Characteristics:**
- High i (must invite to use)
- High c (clear need)
- Typical K: 0.5-2.0

**When to use:**
- Collaboration tools
- Team products
- Multi-player experiences

### 3. Artificial Virality (Incentivized)

Rewards for referrals.

```
User → Gets reward for inviting → Sends many invites
```

**Examples:** Dropbox, Uber, Airbnb

**Characteristics:**
- High i (motivated by reward)
- Lower c (less authentic)
- Typical K: 0.3-1.0

**When to use:**
- Need quick user acquisition
- High LTV justifies incentive cost
- Clear referral value for both parties

### 4. Content Virality

User-generated content spreads.

```
User → Creates content → Content shared → Viewer signs up
```

**Examples:** TikTok, YouTube, Instagram

**Characteristics:**
- Variable i (depends on content quality)
- Low c (many views, few signups)
- Typical K: 0.1-0.5

**When to use:**
- Content creation platforms
- Social networks
- Entertainment products

### 5. Outbreak Virality

Product spreads through networks.

```
User → Installs → Automatically invites contacts
```

**Examples:** Old Hotmail signature, early LinkedIn

**Characteristics:**
- Very high i (automated)
- Low c (impersonal)
- Can be seen as spam

**When to use:**
- Use with caution (can damage brand)
- Best for early-stage network effects
- Ensure value is clear

---

## Loop Selection by Product Type

| Product Type | Best Loop Type |
|--------------|----------------|
| Collaboration tool | Inherent |
| Consumer app | Content + WOM |
| Marketplace | Incentivized |
| Productivity tool | WOM + Inherent |
| Social network | Content + Inherent |
| B2B SaaS | WOM + Incentivized |
| Gaming | Content + WOM |

---

## Examples

### Example 1: Dropbox Referral Program

**The legendary referral program:**

```
Incentive: 500MB free storage for both parties

Results:
- i = 2.1 invites per user (avg)
- c = 35% conversion rate
- K = 0.735

Impact:
- 60% of signups came from referrals
- Grew from 100K to 4M users in 15 months
```

**Why it worked:**

1. Clear value (storage is tangible)
2. Two-sided incentive (both benefit)
3. Easy sharing (multiple channels)
4. Trusted (friend recommendation)

### Example 2: Slack Inherent Virality

**Built-in virality:**

```
Viral loop:
1. User joins team workspace
2. Needs to collaborate with colleague
3. Invites colleague to channel
4. Colleague invites their team

Results:
- Teams naturally expand
- Department → Company → Partners
- K > 1 within organizations
```

**Why it worked:**

1. Product requires others
2. Value increases with users
3. Low friction invite
4. Clear purpose for invite

### Example 3: PayPal Incentivized Referral

**Early growth hack:**

```
Incentive: $10 for referrer + $10 for new user

Results:
- Rapid user acquisition
- 7-10% daily growth at peak
- $60M spent on referrals

Cost calculation:
- CAC via referral: $20
- LTV: $300+
- ROI: 15x
```

**Lessons:**

1. Cash incentives work but are expensive
2. Must have high LTV to justify
3. Attracts some fraud
4. Good for cold start, reduce over time

### Example 4: Wordle Content Virality

**Viral through shareable content:**

```
Viral loop:
1. User plays game
2. Gets result (colored squares)
3. Shares result on Twitter
4. Friends see, want to play
5. Visit site, play, share

Virality mechanics:
- Universal format (everyone sees same puzzle)
- No spoilers (squares don't reveal answer)
- Social competition (compare with friends)
- Daily habit (same puzzle each day)
```

---

## Referral Program Design Template

```markdown
# Referral Program Specification

## Incentive Structure

| Action | Referrer Gets | Invitee Gets |
|--------|---------------|--------------|
| Signup | - | $10 credit |
| First purchase | $20 credit | - |
| Becomes paid | $50 credit | - |

## Mechanics

1. User accesses "Refer a Friend" from dashboard
2. Gets unique link: yourapp.com/r/USERCODE
3. Shares via: email, SMS, social, copy link
4. Invitee clicks → lands on personalized page
5. Invitee signs up → both get credited

## Tracking

- Referral code in URL: ?ref=USERCODE
- Attribution window: 30 days
- Credit expiration: 90 days

## Fraud Prevention

- Max 50 referrals per user
- One referral credit per household
- Manual review for 10+ referrals/day
```

---

## Share Moments by Loop Type

### Word of Mouth
- User achieves goal
- User discovers unexpected value
- User solves major problem

### Inherent
- User needs collaboration
- User wants to share work
- User requires team input

### Incentivized
- User completes onboarding
- User reaches usage milestone
- User in referral prompt location

### Content
- User creates something
- User achieves result
- User wants recognition

---

## Further Reading

- Andrew Chen, "The Cold Start Problem"
- Sean Ellis, "Hacking Growth"
- David Skok, "Lessons Learned - Viral Marketing"
- Adam Penenberg, "Viral Loop"

---

## Related Methodologies

- **viral-metrics:** K-factor calculation and tracking
- **viral-optimization:** Optimization experiments for viral loops
- **growth-loops:** General growth loop framework
- **retention-loops:** Retention loops (retention feeds virality)

---

*Methodology: viral-loops | Growth | faion-growth-agent*
