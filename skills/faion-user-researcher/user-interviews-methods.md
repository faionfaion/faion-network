# User Interview Methods

Methods for conducting effective user interviews and extracting actionable insights.

---

## user-interviews

### Problem
Entrepreneurs build based on assumptions rather than validated user needs.

### Framework

**Interview Types:**

| Type | When | Goal | Questions |
|------|------|------|-----------|
| Problem | Early | Validate problem exists | Open-ended exploration |
| Solution | After problem validated | Test solution fit | Prototype feedback |
| Usability | With prototype | Test UX | Task-based |

**Interview Structure (45 min):**
1. Warm-up (5 min): Build rapport
2. Current state (10 min): How do they do it today?
3. Pain exploration (15 min): What's frustrating?
4. Solution probing (10 min): Would X help?
5. Wrap-up (5 min): Would they pay? Referrals?

**Golden Rules:**
- Talk less than 20% of the time
- Never pitch, only probe
- Ask about past behavior, not future intent
- Look for emotion (frustration, excitement)

**Sample Questions:**
- "Tell me about the last time you [problem]..."
- "What did you try? What happened?"
- "On a scale of 1-10, how frustrating is this?"
- "How much time/money does this cost you?"

### Templates

**Interview Script:**
```markdown
## Warm-up
"Thanks for joining. I'm researching [topic]. No sales pitch, just learning."

## Current State
"Walk me through how you currently [task]."
"What tools do you use?"
"How often do you do this?"

## Pain Exploration
"What's the most frustrating part?"
"Tell me about the last time it went wrong."
"What workarounds have you tried?"

## Solution Probing (show concept/prototype)
"Would something like this help?"
"What's missing?"
"Would you pay for this? How much?"

## Wrap-up
"Who else should I talk to?"
"Can I follow up in 2 weeks?"
```

### Examples

**Key Insights from 10 Interviews:**
- 8/10 mentioned same frustration
- Average time wasted: 3 hours/week
- Willingness to pay: $50-100/month
- Quote: "I would kill for this solution"

### Agent
faion-research-agent (mode: validate)

---

## customer-interview-framework

### Problem
Interviews fail to extract actionable insights due to poor questions and structure.

### Framework

**Interview Types:**

| Type | Stage | Goal | Duration |
|------|-------|------|----------|
| Discovery | Problem validation | Understand context | 30 min |
| Problem | Problem validation | Deep dive on pain | 45 min |
| Solution | Solution validation | Test concepts | 45 min |
| Usability | Product development | Test prototype | 60 min |

**Interview Flow:**

```
1. Warm-up (5 min)
   - Build rapport
   - Set expectations

2. Context (10 min)
   - Their role, background
   - Current situation

3. Deep dive (20 min)
   - Pain exploration
   - Past behavior
   - Emotional triggers

4. Concept test (10 min)
   - Show solution
   - Get reaction

5. Wrap-up (5 min)
   - Willingness to pay
   - Referrals
```

**Question Types:**

| Type | Purpose | Example |
|------|---------|---------|
| Open | Explore | "Tell me about..." |
| Probing | Go deeper | "Why is that?" |
| Clarifying | Understand | "Can you give an example?" |
| Summary | Confirm | "So you're saying..." |

**Anti-patterns:**
- Leading questions: "Don't you think X is great?"
- Future hypotheticals: "Would you use...?"
- Pitching: Explaining your solution too early
- Multiple questions: Asking 2+ questions at once

### Templates

**Interview Guide:**
```markdown
## Interview: {Type}

### Preparation
- Hypothesis to test: {hypothesis}
- Key questions: 5 max
- Recording setup: {yes/no}

### Script

#### Warm-up
"Thanks for joining. I'm researching [topic]. No right/wrong answers, just honest feedback."

#### Context
"Tell me about your role."
"Walk me through a typical day."

#### Deep Dive
"Tell me about the last time you [problem]."
"What happened? What did you do?"
"How did that make you feel?"
"What would you change?"

#### Concept Test
[Show prototype/concept]
"What do you think this is?"
"Would this help? How?"
"What's missing?"

#### Wrap-up
"Would you pay for this? How much?"
"Who else should I talk to?"

### Notes Template

| Question | Answer | Insight |
|----------|--------|---------|
| {question} | {verbatim} | {interpretation} |
```

### Examples

**Key Interview Insights:**
- 8/10 mentioned same frustration
- Verbatim: "I would pay $100 to not deal with this"
- Behavior: Currently using 3 tools as workaround
- Insight: Strong problem-solution fit

### Agent
faion-research-agent (mode: validate)

---

*User Interview Methods | 2 methodologies*
*Part of faion-researcher v1.3*
