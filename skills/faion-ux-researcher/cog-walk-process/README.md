---
id: cognitive-walkthrough-process
name: "Cognitive Walkthrough: Process"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
parent: cognitive-walkthrough
---

# Cognitive Walkthrough: Process

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #cognitive-walkthrough #usability-inspection
- **Agent:** faion-usability-agent
- **Related:** cog-walk-basics.md

---

## Process

### Step 1: Define Prerequisites

**Identify:**
- Target user persona
- Task to evaluate
- Correct action sequence
- Interface to evaluate (prototype or live)

```
Example:
Persona: First-time user, no prior experience
Task: Create a new account and set up profile
Correct sequence:
1. Click "Sign Up"
2. Enter email
3. Enter password
4. Click "Create Account"
5. Enter profile name
6. Upload photo (optional)
7. Click "Complete Setup"
```

### Step 2: Assemble Evaluators

**Who should participate:**
- UX designers
- Product managers
- Developers
- Anyone who understands users

**Group size:** 2-4 evaluators

### Step 3: Walk Through Each Step

For each action in the sequence, ask:

**Question 1: Will the user try to achieve the right effect?**
- Does the user know they need to do something?
- Does the user understand the goal?

**Question 2: Will the user notice that the correct action is available?**
- Is the action visible?
- Is it in an expected location?

**Question 3: Will the user associate the correct action with the desired effect?**
- Does the label make sense?
- Is the purpose clear?

**Question 4: If the correct action is performed, will the user see that progress is being made?**
- Is there feedback?
- Does the user know it worked?

### Step 4: Document Issues

For any "No" answer:
- Describe the problem
- Explain why it's an issue
- Suggest a solution

### Step 5: Summarize Findings

- List all issues found
- Prioritize by severity
- Recommend fixes

---

## Templates

### Walkthrough Planning Template

```markdown
# Cognitive Walkthrough Plan

**Date:** [Date]
**Facilitator:** [Name]
**Evaluators:** [Names]

## User Profile

**Persona:** [Name or description]
**Experience level:** [First-time user / Occasional / etc.]
**Prior knowledge:** [What they already know]
**Goal:** [What they're trying to achieve]

## Task Definition

**Task:** [Clear task statement]

**Success criteria:** [What counts as completion]

## Correct Action Sequence

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | [Action] | [Result] |
| 2 | [Action] | [Result] |
| 3 | [Action] | [Result] |

## Interface

**Type:** Prototype / Staging / Production
**Link:** [URL or file location]

## Scope

- Pages/screens included: [List]
- What's out of scope: [List]
```

### Walkthrough Evaluation Form

```markdown
# Cognitive Walkthrough Evaluation

**Task:** [Task name]
**Step:** [Step number and description]

## Question 1: Will user try to achieve the right effect?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Question 2: Will user notice correct action is available?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Question 3: Will user associate action with desired effect?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Question 4: Will user see progress is being made?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Issues Found

| Issue | Question | Severity | Suggestion |
|-------|----------|----------|------------|
| [Issue] | Q1/Q2/Q3/Q4 | H/M/L | [Fix] |

## Screenshot

[Annotated screenshot if applicable]
```

### Summary Report Template

```markdown
# Cognitive Walkthrough Report

**Date:** [Date]
**Task:** [Task evaluated]
**Evaluators:** [Names]

## Executive Summary

**Steps evaluated:** [Number]
**Issues found:** [Number]
**Critical issues:** [Number]

**Key finding:** [Most important takeaway]

## Task Overview

**Persona:** [User description]
**Goal:** [What user is trying to do]
**Optimal path:** [Number of steps]

## Findings by Step

### Step 1: [Action description]

**Issues found:**
- [Issue 1]: [Description]
  - Question affected: [Q1/Q2/Q3/Q4]
  - Impact: [Description]
  - Recommendation: [Fix]

### Step 2: [Action description]

[Same structure]

## Issues Summary

| Step | Issue | Question | Severity | Status |
|------|-------|----------|----------|--------|
| 1 | [Issue] | Q2 | High | Open |
| 2 | [Issue] | Q4 | Medium | Open |

## Priority Recommendations

### Critical (Fix before launch)
1. [Recommendation]
2. [Recommendation]

### Important (Fix soon)
1. [Recommendation]

### Nice to have
1. [Recommendation]

## Positive Findings

[What worked well - don't change these]

## Appendix

- Detailed evaluation forms
- Screenshots
- Prototype links
```

---

## Checklist

Before walkthrough:
- [ ] User persona defined
- [ ] Task clearly stated
- [ ] Correct sequence documented
- [ ] Interface accessible
- [ ] Evaluators briefed
- [ ] Forms prepared

During walkthrough:
- [ ] Each step evaluated
- [ ] All four questions answered
- [ ] Issues documented with details
- [ ] Recommendations captured
- [ ] Screenshots taken

After walkthrough:
- [ ] Report compiled
- [ ] Issues prioritized
- [ ] Findings shared
- [ ] Fixes assigned
- [ ] Re-evaluation scheduled

## Sources

- [Cognitive Walkthrough Process](https://www.nngroup.com/articles/cognitive-walkthrough-workshop/) - NNG workshop guide
- [How to Run a Cognitive Walkthrough](https://www.usability.gov/how-to-and-tools/methods/cognitive-walkthroughs.html) - Usability.gov tutorial
- [The Cognitive Walkthrough: A Practitioner's Guide](https://dl.acm.org/doi/10.5555/180171.180189) - Original research paper
- [Conducting Effective Cognitive Walkthroughs](https://www.interaction-design.org/literature/article/how-to-conduct-a-cognitive-walkthrough) - IDF detailed process
- [Microsoft Cognitive Walkthrough Template](https://www.microsoft.com/en-us/research/publication/cognitive-walkthrough-method-practitioners-guide/) - Industry templates
