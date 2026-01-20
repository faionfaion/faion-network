---
id: problem-validation
name: "Problem Validation"
domain: RES
skill: faion-researcher
category: "research"
---

# Problem Validation

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Beginner |
| **Tags** | #research, #validation, #problem |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-problem-validator-agent |

---

## Problem

Entrepreneurs build solutions to problems that don't exist or aren't severe enough. Common failures:
- "I think people need this" without evidence
- Building for months, then discovering no demand
- Confusing "nice to have" with "must have"
- Validating with friends who say "great idea!"

**The root cause:** No rigorous process to test if the problem is real and worth solving.

---

## Framework

### What is Problem Validation?

Problem validation is gathering evidence that a real problem exists, affects enough people, and they're willing to pay for a solution. It answers: "Is this problem worth solving?"

### The Problem Validation Pyramid

```
                    /\
                   /  \
                  / $$ \      3. Willingness to Pay
                 /------\
                /        \
               / Severity  \   2. Problem Severity
              /------------\
             /              \
            /   Existence    \  1. Problem Exists
           /------------------\
```

You must validate each level before moving up.

### Level 1: Problem Existence

**Question:** Do people actually have this problem?

**Evidence Types:**
- Forum posts, Reddit threads complaining
- App store reviews mentioning the issue
- Google searches for solutions
- Existing products (means problem exists)
- Your own experience

**Minimum evidence:** 10+ independent sources mentioning the problem.

### Level 2: Problem Severity

**Question:** Is the problem painful enough to act on?

**The Mom Test Questions:**
```
- "Tell me about the last time you faced [problem]"
- "What did you do about it?"
- "How much time/money did you spend?"
- "What happens if you don't solve it?"
- "Have you tried any solutions?"
```

**Severity Scale:**

| Level | Description | Willingness to Solve |
|-------|-------------|---------------------|
| 5 | Hair on fire | Will pay anything now |
| 4 | Serious pain | Actively looking for solution |
| 3 | Annoying | Would use if easy |
| 2 | Minor | Might use if free |
| 1 | Not really | Won't bother |

**Target:** Average severity > 3.5

### Level 3: Willingness to Pay

**Question:** Will people exchange money for a solution?

**Validation Methods:**

1. **Pre-orders:** "Pay $49 now, get it when ready"
2. **Landing page:** Sign up for waitlist (email = interest)
3. **Price anchoring:** "Would you pay $X?" followed by "What about $Y?"
4. **Competitor pricing:** If people pay competitors, they'll pay you

**Strong signals:**
- Credit card submitted (pre-order)
- 10%+ waitlist conversion
- "I'd pay more than $X" responses
- Active subscriptions to alternatives

### The Validation Interview Process

#### Step 1: Find Interview Subjects (10-20 people)

| Source | How |
|--------|-----|
| Reddit | DM active posters in niche |
| LinkedIn | Connect with target titles |
| Twitter/X | Reply to relevant discussions |
| Communities | Slack, Discord, Facebook groups |
| Cold email | Find company emails |

**Script:**
```
"Hi [Name], I'm researching [topic]. Would you spare 15 minutes
to share your experience with [problem]? No selling, just learning."
```

#### Step 2: Conduct the Interview

**Do:**
- Ask about past behavior, not future intentions
- Listen more than talk (80/20 rule)
- Dig into specifics ("Tell me more about...")
- Note emotions and frustrations
- Ask about current solutions

**Don't:**
- Pitch your solution
- Ask leading questions
- Accept "I would" answers (ask about "I did")
- Interview friends and family

#### Step 3: Analyze Results

Categorize responses:

| Signal | Type | Meaning |
|--------|------|---------|
| "I tried X to solve it" | Past action | Problem real |
| "I spent $X on..." | Money spent | WTP exists |
| "It costs me X hours" | Time cost | Quantified pain |
| "I wish there was..." | Desire | Nice to have |
| "I might use..." | Hypothetical | Weak signal |

**Go/No-Go Decision:**

| Criterion | Go | No-Go |
|-----------|-----|-------|
| Problem exists | 8+ of 10 confirm | <5 confirm |
| Severity | Avg > 3.5 | Avg < 3 |
| Active seeking | 5+ tried solutions | <3 tried |
| WTP signals | 3+ price validation | 0 concrete |

---

## Templates

### Problem Validation Report

```markdown
## Problem Validation Report

### Problem Statement
[Specific audience] struggles with [specific problem] because [root cause].

### Validation Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Interviews conducted | 10+ | X | OK/Not |
| Problem confirmed | 80%+ | X% | OK/Not |
| Severity avg | >3.5 | X | OK/Not |
| Active solution seekers | 50%+ | X% | OK/Not |
| WTP signals | 3+ | X | OK/Not |

### Level 1: Problem Existence

**Evidence collected:**
1. [Source] - [Quote/observation]
2. [Source] - [Quote/observation]
...

**Conclusion:** Problem [exists/doesn't exist]

### Level 2: Problem Severity

**Interview findings:**

| Person | Title | Severity (1-5) | Key Quote |
|--------|-------|----------------|-----------|
| P1 | [X] | X | "..." |
| P2 | [X] | X | "..." |
...

**Average Severity:** X

**Current Solutions Tried:**
- [Solution 1] - Used by X people
- [Solution 2] - Used by X people

**Conclusion:** Problem is [severe enough/not severe enough]

### Level 3: Willingness to Pay

**Price validation:**

| Person | "Would pay" | "Too expensive at" | Notes |
|--------|------------|-------------------|-------|
| P1 | $X | $Y | |
| P2 | $X | $Y | |

**Competitor pricing:** $X-$Y range

**Conclusion:** WTP [validated/not validated]

### Final Decision

[ ] GO - Proceed to specification
[ ] PIVOT - Adjust problem/audience
[ ] STOP - Problem not viable

### Key Insights
1. [Insight]
2. [Insight]

### Next Steps
- [ ] [Action]
- [ ] [Action]
```

### Interview Script Template

```markdown
## Interview: [Person Name]
**Date:** [X]
**Duration:** [X] min
**Source:** [How found]

### Warm-up (2 min)
"Thanks for your time. I'm researching [topic]. Tell me about your role."

### Problem Exploration (8 min)
1. "Walk me through how you currently [task related to problem]"
2. "What's the most frustrating part?"
3. "Tell me about the last time you faced [problem]"
4. "What did you do about it?"
5. "What solutions have you tried?"
6. "What happened with those solutions?"

### Severity Assessment (3 min)
7. "How much time do you spend on this weekly?"
8. "What does this problem cost you?"
9. "What happens if you don't solve it?"

### WTP Exploration (2 min)
10. "Have you paid for solutions to this?"
11. "What would a perfect solution look like?"
12. "What would that be worth to you?"

### Notes
[Raw notes during interview]

### Summary
- **Severity:** [1-5]
- **WTP:** [Y/N with amount]
- **Key insight:** [X]
```

---

## Examples

### Example 1: Validating "Freelancers Struggle with Invoicing"

**Interviews:** 12 freelancers

**Results:**
- 11/12 confirmed problem
- Average severity: 4.2
- 8/12 tried solutions (Wave, FreshBooks)
- Main pain: Chasing payments, not creating invoices
- WTP: $10-30/month for better solution

**Decision:** PIVOT - Focus on "payment collection" not "invoicing"

### Example 2: Validating "Developers Need Better Documentation Tools"

**Interviews:** 15 developers

**Results:**
- 14/15 confirmed problem
- Average severity: 2.8 (annoying but manageable)
- 6/15 tried solutions (Notion, GitBook)
- Main pain: Keeping docs updated
- WTP: "Would use if free" (5), "$10/mo" (3), "Company should pay" (7)

**Decision:** STOP - Severity too low, WTP weak for individual developers

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Asking "Would you use...?" | Ask about past behavior instead |
| Interviewing friends | Find strangers in target audience |
| Leading questions | Use open-ended Mom Test questions |
| Too few interviews | Minimum 10 for patterns |
| Ignoring negative signals | Document and act on red flags |
| Skipping WTP validation | Always test payment willingness |

---

## Related Methodologies

- **idea-generation:** Idea Generation
- **niche-evaluation:** Niche Evaluation
- **pain-point-research:** Pain Point Research
- **user-interviews:** User Interviews
- **jobs-to-be-done:** Jobs to Be Done

---

## Agent

**faion-problem-validator-agent** helps validate problem existence. Invoke with:
- "Create validation interview script for [problem]"
- "Analyze these interview results: [data]"
- "Should I proceed with [problem]?"
- "Rate problem severity from these responses: [list]"

---

*Methodology | Research | Version 1.0*
