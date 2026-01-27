# Mistake Templates

## Mistake Record Schema

### Full Mistake Record (JSON)

```json
{
  "id": "MIS_YYYY_NNN",
  "version": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z",

  "metadata": {
    "category": "hallucination | context | implementation | data | security | deployment | estimation | process",
    "subcategory": "specific-type",
    "severity": "critical | high | medium | low",
    "language": "python | javascript | go | etc",
    "domain": "database | api | frontend | infrastructure | etc",
    "tags": ["tag1", "tag2"],
    "llm_related": true
  },

  "mistake": {
    "title": "Brief descriptive title",
    "summary": "One paragraph summary",

    "what_happened": {
      "description": "Detailed description of the incident",
      "timeline": [
        "HH:MM - Event 1",
        "HH:MM - Event 2"
      ],
      "impact": {
        "data_loss": "description or null",
        "downtime": "duration or null",
        "cost": "developer hours or money",
        "user_impact": "number of users affected"
      }
    },

    "root_cause_analysis": {
      "immediate_cause": "What directly caused the issue",
      "contributing_factors": [
        "Factor 1",
        "Factor 2"
      ],
      "root_cause": "The fundamental cause",
      "five_whys": [
        "Why 1? -> Answer 1",
        "Why 2? -> Answer 2",
        "Why 3? -> Answer 3",
        "Why 4? -> Answer 4",
        "Why 5? -> Root cause"
      ]
    },

    "prevention": {
      "immediate_actions": [
        "Fix 1",
        "Fix 2"
      ],
      "process_changes": [
        "Process change 1"
      ],
      "automation": [
        "Automated check 1"
      ],
      "checklist_items": [
        {
          "checklist": "checklist-name",
          "item": "New checklist item text",
          "position": "first | before-execution | after-completion"
        }
      ]
    }
  },

  "validation": {
    "occurrence_count": 1,
    "last_occurrence": "2024-01-15T10:00:00Z",
    "prevention_effectiveness": {
      "prevented": 0,
      "total": 0
    },
    "related_incidents": []
  },

  "provenance": {
    "discovered_in": "TASK_XXX | INC_XXX",
    "reported_by": "claude-agent | human",
    "verified_by": "human-review",
    "post_mortem_url": "https://..."
  }
}
```

---

## Quick Capture Template (Markdown)

For fast documentation during incident response:

```markdown
## Mistake: [Brief Title]

**ID:** MIS_YYYY_NNN
**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low
**Category:** [hallucination / context / implementation / data / security / deployment / estimation / process]

### What Happened
[1-3 sentences describing the incident]

### Impact
- Time lost: X hours
- Users affected: N
- Data loss: Yes/No
- Cost: $X or N developer hours

### Root Cause
[Brief root cause - one sentence]

### Five Whys
1. Why? → [Answer 1]
2. Why? → [Answer 2]
3. Why? → [Answer 3]
4. Why? → [Answer 4]
5. Why? → [Root Cause]

### Prevention
- [ ] [Immediate action 1]
- [ ] [Immediate action 2]
- [ ] [Process change]

### Source
Discovered in: TASK_XXX / INC_XXX
```

---

## LLM-Specific Mistake Template

For errors specifically caused by LLM behavior:

```markdown
## LLM Mistake: [Brief Title]

**ID:** MIS_YYYY_NNN
**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low
**Category:** Hallucination / Context Loss / Instruction Drift / Scope Creep

### LLM Context
- Model used: [Claude / GPT-4 / etc]
- Task type: [Code generation / Refactoring / Bug fix / etc]
- Context size: [Approximate tokens or lines]

### What Happened
[Description of the LLM error]

### LLM Output Analysis
**What LLM generated:**
```
[Problematic code or text]
```

**What was expected:**
```
[Correct code or text]
```

**Warning signs missed:**
- [Sign 1 - e.g., unusually confident about new feature]
- [Sign 2 - e.g., no documentation reference]

### Root Cause Analysis

**Context issues:**
- [ ] Insufficient documentation in context
- [ ] Context window exceeded
- [ ] Instructions unclear
- [ ] Examples missing

**Prompt issues:**
- [ ] Task too broad
- [ ] Ambiguous requirements
- [ ] Missing constraints

**Verification issues:**
- [ ] Output not tested
- [ ] No type checking
- [ ] No code review
- [ ] Trusted LLM too much

### Correction
**What feedback fixed it:**
[The prompt or feedback that produced correct output]

**Iterations needed:** N

### Prevention

**Context improvements:**
- [ ] [Add specific documentation to standard context]
- [ ] [Include examples for this pattern]

**Prompt improvements:**
- [ ] [More specific instructions]
- [ ] [Add constraints]

**Verification improvements:**
- [ ] [Add automated check]
- [ ] [Add to review checklist]

### Source
Task: TASK_XXX
Conversation: [Link if available]
```

---

## Prevention Rule Template

For automated detection rules:

```json
{
  "id": "PREV_NNN",
  "source_mistake": "MIS_YYYY_NNN",
  "name": "Descriptive rule name",
  "description": "What this rule prevents",

  "trigger": {
    "type": "file_pattern | task_keyword | file_size | code_pattern",
    "config": {
      "pattern": "regex or glob pattern",
      "file_types": ["*.py", "*.ts"],
      "keywords": ["word1", "word2"],
      "threshold": 500
    }
  },

  "action": {
    "type": "warn | require_checklist | block | suggest",
    "message": "Warning message with MIS reference",
    "checklist": "checklist-name-if-applicable"
  },

  "metadata": {
    "created_at": "2024-01-15",
    "enabled": true,
    "triggered_count": 0,
    "prevented_count": 0
  }
}
```

---

## Incident Report Template

For detailed post-mortem documentation:

```markdown
# Incident Report: INC_YYYY_NNN

## Summary
- **Date:** YYYY-MM-DD
- **Duration:** X hours
- **Severity:** Critical / High / Medium / Low
- **Status:** Resolved / Ongoing / Monitoring

## Impact
| Metric | Value |
|--------|-------|
| Users affected | N |
| Data loss | Yes/No |
| Downtime | X hours |
| Financial impact | $X |

## Timeline

| Time | Event |
|------|-------|
| HH:MM | First indication of issue |
| HH:MM | Issue confirmed |
| HH:MM | Investigation started |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Issue resolved |

## Root Cause Analysis

### Immediate Cause
[What directly caused the incident]

### Contributing Factors
1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

### Five Whys
1. Why [symptom]? → [Answer]
2. Why [answer 1]? → [Answer]
3. Why [answer 2]? → [Answer]
4. Why [answer 3]? → [Answer]
5. Why [answer 4]? → [Root cause]

### Root Cause
[Final root cause statement]

## Resolution

### Immediate Actions Taken
1. [Action 1]
2. [Action 2]

### Long-term Fixes
1. [Fix 1] - Status: Done/In Progress/Planned
2. [Fix 2] - Status: Done/In Progress/Planned

## Prevention

### Process Changes
- [ ] [Change 1]
- [ ] [Change 2]

### Automation
- [ ] [Automated check 1]
- [ ] [Monitoring addition]

### Documentation Updates
- [ ] [Doc 1 updated]
- [ ] [Runbook created]

## Lessons Learned

### What Went Well
- [Positive 1]
- [Positive 2]

### What Went Poorly
- [Issue 1]
- [Issue 2]

### Where We Got Lucky
- [Lucky break 1]

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action 1] | [Name] | YYYY-MM-DD | Open |
| [Action 2] | [Name] | YYYY-MM-DD | Open |

## Related

- Mistake Record: MIS_YYYY_NNN
- Related Incidents: [INC_XXX, INC_YYY]
- Documentation: [Links]
```

---

## Monthly Review Template

```markdown
# Mistake Review: [Month Year]

## Summary
| Metric | Count |
|--------|-------|
| New mistakes documented | N |
| Recurring mistakes | N |
| Successfully prevented | N |
| Critical/High severity | N |

## Mistakes by Category
| Category | Count | Trend |
|----------|-------|-------|
| Hallucination | N | up/down/stable |
| Context Loss | N | up/down/stable |
| Implementation | N | up/down/stable |
| Security | N | up/down/stable |
| Data Handling | N | up/down/stable |

## Top Issues This Month
1. **[Category]:** [Brief description] (MIS_XXX)
2. **[Category]:** [Brief description] (MIS_XXX)
3. **[Category]:** [Brief description] (MIS_XXX)

## Prevention Effectiveness
| Prevention Rule | Triggered | Prevented | Effectiveness |
|-----------------|-----------|-----------|---------------|
| PREV_001: [Name] | N | N | N% |
| PREV_002: [Name] | N | N | N% |

## Recurring Mistakes
Mistakes that occurred multiple times:
- MIS_XXX: [Title] - N occurrences
- MIS_YYY: [Title] - N occurrences

## Action Items
- [ ] Review PREV_XXX (not effective)
- [ ] Add automation for MIS_YYY
- [ ] Update checklist for [category]
- [ ] Share learnings: [specific topic]

## Trends Analysis
[Are we improving? What patterns are emerging? Areas of concern?]

## Next Month Focus
- [ ] [Priority 1]
- [ ] [Priority 2]
```
