---
id: cognitive-walkthrough-basics
name: "Cognitive Walkthrough: Basics"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
parent: cognitive-walkthrough
---

# Cognitive Walkthrough: Basics

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #cognitive-walkthrough #usability-inspection
- **Agent:** faion-usability-agent
- **Related:** cog-walk-process.md

## Problem

New users struggle with products but teams can't pinpoint why. Onboarding is complex and first-time user issues remain hidden. Need to evaluate learnability before user testing.

## Framework

### What is Cognitive Walkthrough?

A usability inspection method where evaluators step through a task from first-time user's perspective, assessing whether users can figure out how to complete tasks without prior training.

### Focus Areas

| Area | Questions |
|------|-----------|
| **Learnability** | Can new users figure it out? |
| **Action visibility** | Is the next step obvious? |
| **Understanding** | Will users know what to do? |
| **Feedback** | Will users know they did right? |

### Cognitive Walkthrough vs. Heuristic Evaluation

| Aspect | Cognitive Walkthrough | Heuristic Evaluation |
|--------|----------------------|----------------------|
| Focus | Task completion by new user | Broad usability principles |
| Method | Step-by-step task analysis | Expert review against heuristics |
| Questions | 4 specific questions per step | 10 general heuristics |
| Best for | Learnability, onboarding | General usability issues |

## The Four Questions

### Q1: Will user try to achieve right effect?

**Checks:**
- Is the goal clear?
- Does user know action is needed?
- Is motivation present?

**Common failures:**
- User doesn't know something is required
- User thinks they're done when they're not

### Q2: Will user notice correct action available?

**Checks:**
- Is control visible?
- Is it in expected location?
- Does it stand out?

**Common failures:**
- Action is below the fold
- Control doesn't look clickable
- Too many competing options

### Q3: Will user associate action with effect?

**Checks:**
- Is the label clear?
- Is the icon recognizable?
- Does it match user's mental model?

**Common failures:**
- Jargon in labels
- Ambiguous icons
- Unexpected location

### Q4: Will user see progress is being made?

**Checks:**
- Is there feedback?
- Does UI change appropriately?
- Is success communicated?

**Common failures:**
- No loading indicator
- Page looks the same after action
- Error not displayed

## Examples

### Example 1: Sign-Up Flow

**Step:** Click "Get Started" button

| Question | Answer | Notes |
|----------|--------|-------|
| Q1: Will try? | Yes | Clear value proposition above button |
| Q2: Will notice? | Partial | Button visible but competes with "Sign In" |
| Q3: Will associate? | No | "Get Started" unclear if it means sign up or demo |
| Q4: Progress visible? | Yes | Takes user to registration form |

**Issue:** "Get Started" is ambiguous
**Fix:** Change to "Create Free Account"

### Example 2: File Upload

**Step:** Drag file to upload zone

| Question | Answer | Notes |
|----------|--------|-------|
| Q1: Will try? | Partial | Users might look for browse button first |
| Q2: Will notice? | Yes | Large drop zone visible |
| Q3: Will associate? | Yes | Icon and text suggest drag-drop |
| Q4: Progress visible? | No | No indication file is uploading |

**Issue:** Missing upload progress indicator
**Fix:** Add progress bar and file name during upload

## When to Use

| Situation | Cognitive Walkthrough Appropriate |
|-----------|-----------------------------------|
| Early prototypes | Yes |
| Before user testing | Yes |
| Onboarding flows | Yes |
| New feature launch | Yes |
| Complex workflows | Yes |
| Frequent tasks | No, use heuristic evaluation |
| Expert users | No, focus on efficiency instead |

## Common Mistakes

1. **Using power users** - Should evaluate for first-time users
2. **Skipping steps** - Must evaluate every action
3. **Not documenting "Yes"** - Record positive findings too
4. **Vague issues** - Be specific about what's wrong
5. **No recommendations** - Always suggest a fix

## Best Practices

### Before the Walkthrough

- Have working interface ready
- Print evaluation forms
- Define realistic user persona
- Identify complete action sequence
- Brief evaluators on method

### During the Walkthrough

- Go step by step, don't skip ahead
- Answer all four questions for every step
- Take notes on the spot
- Capture screenshots
- Discuss disagreements

### After the Walkthrough

- Compile findings immediately
- Prioritize issues
- Share with team
- Track fixes
- Consider re-evaluation

## Sources

- [Usability Inspection Methods](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/) - Nielsen Norman Group comprehensive guide
- [Cognitive Walkthroughs](https://www.interaction-design.org/literature/article/how-to-conduct-a-cognitive-walkthrough) - Interaction Design Foundation tutorial
- [The Cognitive Walkthrough Method: A Practitioner's Guide](https://dl.acm.org/doi/10.5555/180171.180189) - Original paper by Wharton et al.
- [UX Booth: Cognitive Walkthroughs](https://www.uxbooth.com/articles/complete-beginners-guide-to-design-research/) - Practical implementation guide
- [Usability.gov: Cognitive Walkthrough](https://www.usability.gov/how-to-and-tools/methods/cognitive-walkthroughs.html) - Federal government resource
