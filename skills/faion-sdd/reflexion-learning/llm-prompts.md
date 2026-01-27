# LLM Prompts for Reflexion

Prompts to guide LLM agents through the Reflexion cycle.

## System Prompt Additions

Add to your base system prompt for Reflexion-enabled tasks:

```
## Memory-Enabled Execution

You have access to project memory in `.aidocs/memory/`:
- `patterns.md` - Successful approaches to reuse
- `mistakes.md` - Failures to avoid
- `decisions.md` - Architectural context
- `session.md` - Current session state

Before executing any task:
1. Load relevant patterns by domain
2. Load relevant mistakes by domain
3. Apply patterns consciously
4. Watch for mistake triggers

After completing any task:
1. Evaluate outcome against criteria
2. Generate structured reflection
3. Extract new patterns (if success)
4. Document mistakes (if failure)
5. Update memory files
```

## Pre-Task: Memory Loading Prompt

Use before starting a task:

```
## Task Context Loading

I'm about to work on: [TASK DESCRIPTION]
Domain: [DOMAIN - e.g., database, frontend, API, deployment]

Please load relevant context from memory:

1. **Patterns to Apply**
   - Search patterns.md for domain-related patterns
   - Select top 3-5 by confidence score
   - Note how each might apply to this task

2. **Mistakes to Avoid**
   - Search mistakes.md for domain-related warnings
   - Prioritize by severity
   - Identify specific watch points for this task

3. **Relevant Decisions**
   - Check decisions.md for applicable constraints
   - Note any that affect implementation choices

4. **Session Context**
   - Check session.md for any carry-forward items
   - Note any open questions from previous work

Format output as:
---
## Loaded Context for [TASK ID]

### Patterns (apply these)
- PAT-XXX: [name] - [how to apply]
- PAT-XXX: [name] - [how to apply]

### Mistakes (avoid these)
- MIS-XXX: [name] - [watch for this]
- MIS-XXX: [name] - [watch for this]

### Decisions (respect these)
- DEC-XXX: [constraint to follow]

### Session Items
- [Any carry-forward items]
---
```

## During Task: Pattern Application Prompt

Use when applying a specific pattern:

```
I'm applying pattern PAT-XXX: [PATTERN NAME]

Context from memory:
[PASTE PATTERN DETAILS]

Current situation:
[DESCRIBE CURRENT CODE/SITUATION]

Please:
1. Confirm this pattern applies to the current situation
2. Adapt the pattern to my specific context
3. Show me the implementation
4. Note any deviations from the standard pattern

If the pattern doesn't fully apply, explain why and suggest alternatives.
```

## Post-Task: Reflection Generation Prompt

Use after completing a task:

```
## Task Completion Reflection

Task: [TASK ID] - [TITLE]
Outcome: [SUCCESS / PARTIAL / FAILURE]

### Execution Summary
[Brief description of what was done]

### Acceptance Criteria Check
- [ ] AC-1: [Status and notes]
- [ ] AC-2: [Status and notes]

Please generate a structured reflection:

1. **What Worked Well**
   - Specific actions that led to success
   - Patterns that were effective
   - Decisions that paid off

2. **What Could Improve**
   - Challenges encountered
   - Time spent on unexpected issues
   - Things that were harder than expected

3. **Root Cause Analysis** (if partial/failure)
   Use 5 Whys to find root cause:
   - Why 1:
   - Why 2:
   - Why 3:
   - Why 4:
   - Why 5:
   - Root Cause:

4. **Pattern Extraction**
   If successful approach is reusable:
   - Pattern name:
   - Context where it applies:
   - Solution summary:
   - Initial confidence: 0.5

5. **Mistake Documentation**
   If failure occurred:
   - Mistake name:
   - Severity (High/Medium/Low):
   - Prevention strategy:
   - Detection improvement:

6. **Memory Updates**
   List specific updates to make:
   - patterns.md: [add/update pattern]
   - mistakes.md: [add/update mistake]
   - decisions.md: [record decision if any]
   - session.md: [clear or update]
```

## Pattern Extraction Prompt

Use when a successful approach should become a pattern:

```
## Extract New Pattern

I successfully solved this problem:
[DESCRIBE PROBLEM]

Using this approach:
[DESCRIBE SOLUTION]

Please help me formalize this as a reusable pattern:

1. **Pattern Naming**
   - Suggest a clear, descriptive name
   - Should describe what it does, not how

2. **Context Definition**
   - When does this pattern apply?
   - What conditions must be true?
   - What domains is it relevant to?

3. **Problem Statement**
   - What specific problem does it solve?
   - What are the symptoms of the problem?

4. **Solution Description**
   - Step-by-step solution
   - Code examples if applicable
   - Key decisions in the solution

5. **Trade-offs**
   - Benefits of using this pattern
   - Costs or downsides
   - When NOT to use it

6. **Confidence Assessment**
   - How confident are you in this pattern?
   - What would increase confidence?
   - What edge cases might exist?

Output as pattern entry for patterns.md.
```

## Mistake Analysis Prompt

Use when a failure should be documented:

```
## Document Mistake

Something went wrong:
[DESCRIBE WHAT HAPPENED]

The impact was:
[DESCRIBE IMPACT - time lost, bugs, user complaints, etc.]

Please help me analyze and document this:

1. **5 Whys Analysis**
   Guide me through 5 Whys to find root cause:
   - Start with: "Why did [the failure] happen?"
   - Keep asking "Why?" until we reach root cause

2. **Categorization**
   What type of mistake is this?
   - Estimation / Implementation / Testing / Communication / Process

3. **Severity Assessment**
   - High: Production impact, data loss, security issue
   - Medium: Deployment delay, significant rework
   - Low: Minor rework, no user impact

4. **Prevention Strategy**
   - What specific action would prevent this?
   - Is it a checklist item? A validation? A test?
   - Can it be automated?

5. **Detection Improvement**
   - How could this be caught earlier?
   - In requirements? In design? In code review? In testing?

6. **Warning Signs**
   - What early indicators might predict this?
   - Add these to "watch for" list

Output as mistake entry for mistakes.md.
```

## Memory Query Prompt

Use to find relevant memory items:

```
## Memory Query

I need to find relevant patterns and mistakes for:
Task type: [TYPE - e.g., "API integration"]
Domain: [DOMAIN - e.g., "payments", "authentication"]
Technologies: [TECH - e.g., "Stripe", "OAuth"]

Search criteria:
1. Domain match (highest priority)
2. Technology match
3. Problem similarity
4. Recent usage (recency bonus)

Please search memory and return:

### Top 5 Patterns
Sorted by: confidence * relevance

| Rank | ID | Name | Confidence | Relevance |
|------|-----|------|------------|-----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Top 3 Mistakes to Avoid
Sorted by: severity * relevance

| Rank | ID | Name | Severity | Relevance |
|------|-----|------|----------|-----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Relevant Decisions
Any decisions that constrain this task:

| ID | Decision | Impact |
|----|----------|--------|
| | | |
```

## Confidence Update Prompt

Use after applying a pattern to update confidence:

```
## Update Pattern Confidence

Pattern: PAT-XXX - [NAME]
Previous confidence: [X.XX]
Usage count: [N]

This usage:
- Outcome: [success/partial/failure]
- Notes: [any observations]

Calculate new confidence:

If success:
  new_confidence = min(0.95, old_confidence + 0.05)
  usage_count += 1

If partial:
  new_confidence = old_confidence * 0.95

If failure:
  new_confidence = max(0.3, old_confidence - 0.15)

Also check:
- Days since last use > 90? Apply 0.9 decay

New values:
- Confidence: [calculate]
- Usage count: [update]
- Last used: [today's date]

Please update the pattern entry in patterns.md.
```

## Sprint Reflection Prompt

Use at end of sprint/iteration:

```
## Sprint Reflection

Sprint: [NUMBER/NAME]
Period: [START DATE] to [END DATE]

### Tasks Completed
[List of completed tasks]

### Tasks Incomplete
[List of incomplete tasks with reasons]

Please analyze this sprint:

1. **Pattern Usage Summary**
   - Which patterns were used most?
   - Which had highest success rate?
   - Any patterns that should be deprecated?

2. **Mistake Occurrence Summary**
   - Which mistakes were avoided?
   - Which mistakes occurred?
   - Any new mistake patterns?

3. **Estimation Accuracy**
   - Compare estimated vs actual complexity
   - Identify systematic over/under estimation
   - Suggest calibration adjustments

4. **Memory Maintenance**
   - Patterns to promote (confidence boost)
   - Patterns to demote (confidence decay)
   - Mistakes to archive (no longer relevant)
   - Patterns to merge (similar solutions)

5. **Action Items**
   - Process improvements
   - Documentation updates
   - Knowledge sharing needs

6. **Next Sprint Focus**
   - Key patterns to load
   - Key mistakes to watch for
   - Skills to develop
```

## Self-Correction Prompt

Use when attempting to improve a failed solution:

```
## Self-Correction Attempt

Previous attempt:
[DESCRIBE WHAT WAS TRIED]

Result:
[DESCRIBE FAILURE - error message, test failure, etc.]

External feedback:
[ANY COMPILER ERRORS, TEST RESULTS, LINTER OUTPUT]

Memory context:
[RELEVANT PATTERNS AND MISTAKES]

Please:

1. **Analyze the Failure**
   - What specifically went wrong?
   - Is this a known mistake pattern?

2. **Generate Reflection**
   - Why did the previous approach fail?
   - What assumption was wrong?
   - What was missed?

3. **Plan Correction**
   - What specific changes are needed?
   - Which patterns should be applied?
   - What mistakes should be avoided?

4. **Execute with Verification**
   - Implement the correction
   - Verify with available feedback (tests, types, linter)
   - Confirm the issue is resolved

Note: Focus on external signals (test results, type errors) rather than
pure self-evaluation, as research shows LLMs struggle with intrinsic
self-correction.
```

## Memory Initialization Prompt

Use when starting a new project:

```
## Initialize Project Memory

Project: [PROJECT NAME]
Domain: [PRIMARY DOMAIN]
Tech stack: [TECHNOLOGIES]

Please help me bootstrap the memory system:

1. **Create Memory Structure**
   Initialize these files:
   - .aidocs/memory/patterns.md
   - .aidocs/memory/mistakes.md
   - .aidocs/memory/decisions.md
   - .aidocs/memory/session.md

2. **Seed with Domain Patterns**
   Based on the tech stack, suggest initial patterns:
   - Common [DOMAIN] patterns
   - [TECHNOLOGY]-specific best practices
   - Initial confidence: 0.6 (not yet validated in project)

3. **Seed with Common Mistakes**
   Based on the domain, suggest initial mistakes to watch:
   - Common [DOMAIN] pitfalls
   - [TECHNOLOGY]-specific gotchas
   - Severity based on typical impact

4. **Record Initial Decisions**
   Document the tech stack decisions:
   - Why [TECHNOLOGY A] over alternatives
   - Key configuration choices
   - Architectural direction

This gives us a starting point that we'll refine through actual usage.
```

## Prompt Chaining for Full Cycle

Complete Reflexion cycle as prompt chain:

```
# 1. Pre-Task
[Run Memory Query Prompt]
↓
# 2. During Task
[Run Pattern Application Prompt as needed]
↓
# 3. If Error
[Run Self-Correction Prompt]
↓
# 4. Post-Task
[Run Reflection Generation Prompt]
↓
# 5. If New Pattern
[Run Pattern Extraction Prompt]
↓
# 6. If New Mistake
[Run Mistake Analysis Prompt]
↓
# 7. Update Confidence
[Run Confidence Update Prompt for used patterns]
↓
# 8. End of Sprint
[Run Sprint Reflection Prompt]
```

## Claude Code Integration

For Claude Code specifically, add to your system prompt or CLAUDE.md:

```markdown
## Reflexion Integration

Before each task:
1. Read .aidocs/memory/patterns.md
2. Read .aidocs/memory/mistakes.md
3. Identify relevant entries for task domain
4. Note in your response: "Loaded patterns: PAT-XXX, PAT-YYY"
5. Note in your response: "Watching for: MIS-XXX, MIS-YYY"

After each task:
1. Evaluate success against acceptance criteria
2. If successful: Consider new pattern extraction
3. If failed: Document mistake with root cause
4. Update memory files as needed
5. Report: "Memory updated: [what changed]"

Use Edit tool to update memory files.
Never delete patterns/mistakes - only add or update confidence.
```
