# LLM Prompts for Pattern Extraction

Prompts for extracting and managing patterns using LLM agents.

## Pattern Discovery Prompts

### After Task Completion

```
Analyze the completed task and identify potential patterns:

TASK: {task_id}
CHANGES: {files_changed}
APPROACH: {implementation_summary}

Questions to answer:
1. What problem did this task solve?
2. Is this problem likely to recur in other contexts?
3. What was non-obvious about the solution?
4. Could this solution be generalized?

If a pattern exists, output:
- Pattern name
- Category (code/architecture/workflow)
- Subcategory
- Problem statement (1-2 sentences)
- Solution summary (1-2 sentences)
- Key code snippet (if applicable)
- Contexts where this applies
```

### Retrospective Pattern Mining

```
Review the following completed tasks and identify recurring patterns:

TASKS: {list_of_task_ids}
PERIOD: {date_range}

For each potential pattern, assess:
1. How many tasks exhibited this pattern? (minimum 2)
2. What is the common problem being solved?
3. What is the consistent approach used?
4. Are there variations that should be noted?

Output format:
- Pattern candidates with evidence
- Confidence score based on frequency and consistency
- Recommendation: capture / investigate / skip
```

---

## Pattern Validation Prompts

### Pre-Application Check

```
Before applying this pattern, validate its applicability:

PATTERN: {pattern_id}
CURRENT_CONTEXT: {task_description}
CODEBASE: {relevant_file_paths}

Check:
1. Does the current problem match the pattern's problem statement?
2. Does the context match the pattern's "When to Use" criteria?
3. Are there any "When NOT to Use" criteria that apply?
4. Are there project-specific constraints that affect applicability?

Output:
- Applicability score (0-100%)
- Specific concerns if any
- Recommended adaptations if needed
- Alternative patterns to consider
```

### Post-Application Review

```
Evaluate how well the pattern worked in this application:

PATTERN: {pattern_id}
TASK: {task_id}
OUTCOME: {success|partial|failure}
NOTES: {implementation_notes}

Analyze:
1. Did the pattern solve the problem as expected?
2. Were there unexpected complications?
3. Should the pattern be updated based on this experience?
4. Should confidence score change?

Output:
- Updated confidence score recommendation
- Suggested pattern updates (if any)
- New contexts to add to "When to Use"
- New anti-contexts to add to "When NOT to Use"
```

---

## Pattern Merging Prompts

### Duplicate Detection

```
Analyze these patterns for potential overlap:

PATTERN_A: {pattern_a_summary}
PATTERN_B: {pattern_b_summary}

Determine:
1. Do they solve the same fundamental problem?
2. Are they variations of the same approach?
3. Can they be merged without losing information?
4. Should they remain separate with cross-references?

Output:
- Relationship: duplicate / variant / related / distinct
- If merge recommended: proposed merged pattern
- If variant: differentiating criteria
- If related: cross-reference recommendations
```

### Pattern Consolidation

```
Consolidate these related patterns into a unified pattern:

PATTERNS: {list_of_pattern_ids}
USAGE_DATA: {usage_statistics}

Create:
1. Unified problem statement covering all cases
2. Core solution that applies to all
3. Variations section for context-specific adaptations
4. Combined "When to Use" and "When NOT to Use"
5. Merged validation data

Output:
- Consolidated pattern in full template format
- List of deprecated pattern IDs
- Migration notes for existing references
```

---

## Pattern Maintenance Prompts

### Confidence Recalculation

```
Recalculate confidence score for this pattern:

PATTERN: {pattern_id}
CURRENT_CONFIDENCE: {score}
USAGE_HISTORY:
  - Total uses: {count}
  - Successful: {success_count}
  - Failed: {failure_count}
  - Last used: {date}

Formula:
confidence = base_score * usage_factor * success_factor * recency_factor

Where:
- base_score: 0.5
- usage_factor: min(usage_count / 10, 1.5)
- success_factor: success_rate ^ 0.5
- recency_factor: 1.0 - (days_since_last_use / 365) * 0.3

Output:
- New confidence score
- Score breakdown by factor
- Recommendation: maintain / promote / demote / archive
```

### Staleness Check

```
Evaluate pattern freshness and relevance:

PATTERN: {pattern_id}
LAST_USED: {date}
TECHNOLOGY_CONTEXT: {language, framework, versions}

Check:
1. Has the technology evolved since pattern creation?
2. Are there newer best practices that supersede this?
3. Is the code example still valid?
4. Are the trade-offs still accurate?

Output:
- Freshness status: current / needs_update / obsolete
- Specific updates needed
- Alternative modern approaches if applicable
- Recommendation: update / archive / deprecate
```

### Gap Analysis

```
Identify missing patterns in the knowledge base:

EXISTING_PATTERNS: {pattern_index}
RECENT_TASKS: {list_of_completed_tasks}
COMMON_TECHNOLOGIES: {tech_stack}

Analyze:
1. What problems were solved that have no matching pattern?
2. What patterns do similar projects typically have?
3. What anti-patterns have been encountered but not documented?
4. What categories are underrepresented?

Output:
- Prioritized list of missing patterns
- Suggested pattern outlines
- Anti-patterns to document
- Category balance recommendations
```

---

## CLAUDE.md Sync Prompts

### Pattern Selection for CLAUDE.md

```
Select patterns to sync to CLAUDE.md:

ALL_PATTERNS: {pattern_index}
CURRENT_CLAUDE_MD: {current_patterns_section}
PROJECT_CONTEXT: {tech_stack, common_tasks}

Criteria:
- Confidence >= 0.8
- Usage count >= 5
- Relevant to project tech stack
- Not already in CLAUDE.md

Output:
- Patterns to add
- Patterns to update
- Patterns to remove (if obsolete)
- Formatted markdown section
```

### Pattern Summary Generation

```
Generate concise pattern summary for CLAUDE.md:

PATTERN: {full_pattern_details}
MAX_LENGTH: 3 lines

Requirements:
- Pattern name and confidence
- One-line problem/solution
- Reference to full documentation

Output:
Formatted markdown entry for CLAUDE.md patterns section
```

---

## Session Memory Prompts

### Session Pattern Loading

```
Load relevant patterns for this session:

CURRENT_TASK: {task_description}
FEATURE_CONTEXT: {feature_spec_summary}
TECHNOLOGY: {relevant_tech}

Query patterns by:
1. Matching category to task type
2. Matching technology to task tech
3. Matching problem keywords
4. High confidence (0.7+)

Output:
- List of 3-5 most relevant patterns
- Brief explanation of why each is relevant
- Any anti-patterns to avoid
```

### Session Observation Capture

```
Capture observations from this session for later review:

SESSION_WORK: {summary_of_actions}
ISSUES_ENCOUNTERED: {problems_and_solutions}
APPROACHES_USED: {implementation_approaches}

Identify:
1. Potential new patterns (worth capturing)
2. Potential anti-patterns (mistakes made)
3. Existing patterns that worked well
4. Existing patterns that need updates

Output:
- Observations structured for session.md
- Recommended actions for pattern maintenance
- Priority: high / medium / low for each
```

---

## Reflexion Prompts

### Post-Task Reflexion

```
Reflect on task execution and extract learnings:

TASK: {task_id}
PLAN: {original_plan}
EXECUTION: {what_actually_happened}
OUTCOME: {success|partial|failure}

Analyze:
1. What worked well? (potential patterns)
2. What went wrong? (potential anti-patterns)
3. What was unexpected? (knowledge gaps)
4. What would you do differently? (improvements)

Output:
- Patterns to capture
- Mistakes to document
- Knowledge to add to CLAUDE.md
- Recommendations for similar future tasks
```

### PDCA Cycle Analysis

```
Apply PDCA (Plan-Do-Check-Act) analysis:

PLAN: {what_was_planned}
DO: {what_was_executed}
CHECK: {results_and_observations}

Act phase - determine:
1. What patterns emerged that should be standardized?
2. What deviations from plan should become standard?
3. What failed approaches should be documented as anti-patterns?
4. What updates to existing knowledge are needed?

Output:
- Standardization recommendations
- Pattern updates
- Anti-pattern documentation
- CLAUDE.md sync candidates
```
