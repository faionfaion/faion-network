# Pattern and Mistake Memory Templates

Standard formats for Reflexion memory files in SDD projects.

## Memory File Structure

```
.aidocs/memory/
├── patterns.md       # Successful approaches
├── mistakes.md       # Failures to avoid
├── decisions.md      # Architectural decisions
└── session.md        # Current session state
```

## Pattern Memory Template

### File: `.aidocs/memory/patterns.md`

```markdown
# Pattern Memory

Successful patterns learned from project execution.

## Index

| ID | Name | Domain | Confidence |
|----|------|--------|------------|
| PAT-001 | Error Boundary | React | 0.90 |
| PAT-002 | Batched Migration | Database | 0.85 |
| PAT-003 | API Response Validation | Integration | 0.75 |

---

## PAT-001: Error Boundary Pattern

**Domain:** React, Frontend
**Context:** Async components with data fetching
**Problem:** Unhandled promise rejections crash entire app

**Solution:**
```tsx
function AsyncComponent() {
  const [error, setError] = useState<Error | null>(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData()
      .then(setData)
      .catch(setError);
  }, []);

  if (error) return <ErrorFallback error={error} />;
  if (!data) return <Loading />;
  return <DataView data={data} />;
}
```

**Benefits:**
- Graceful degradation
- Better user experience
- Easier debugging

**Trade-offs:**
- More boilerplate code
- Need to design error states

**Metadata:**
| Field | Value |
|-------|-------|
| Confidence | 0.90 |
| Usage Count | 8 |
| Last Used | 2024-01-15 |
| Source | TASK-042 |

---

## PAT-002: Batched Migration

**Domain:** Database, DevOps
**Context:** Schema changes on tables with >100k rows
**Problem:** Single-transaction migrations timeout or lock

**Solution:**
1. Check row count: `SELECT COUNT(*) FROM table`
2. If >100k rows, use batched approach:
   - Add column as nullable
   - Update in batches of 50-100k
   - Add NOT NULL constraint after

```sql
-- Step 1: Add nullable
ALTER TABLE users ADD COLUMN status VARCHAR(20);

-- Step 2: Batch update
UPDATE users SET status = 'active'
WHERE id IN (SELECT id FROM users WHERE status IS NULL LIMIT 100000);
-- Repeat until done

-- Step 3: Add constraint
ALTER TABLE users ALTER COLUMN status SET NOT NULL;
```

**Benefits:**
- No table locks
- Resumable if interrupted
- Zero downtime

**Trade-offs:**
- More complex migration
- Longer total time

**Metadata:**
| Field | Value |
|-------|-------|
| Confidence | 0.85 |
| Usage Count | 4 |
| Last Used | 2024-01-10 |
| Source | TASK-055 |

---

## Pattern Entry Template

Copy this template for new patterns:

```markdown
## PAT-XXX: [Name]

**Domain:** [Area of application]
**Context:** [When this pattern applies]
**Problem:** [What problem it solves]

**Solution:**
[Step-by-step or code example]

**Benefits:**
- [Benefit 1]
- [Benefit 2]

**Trade-offs:**
- [Trade-off 1]
- [Trade-off 2]

**Metadata:**
| Field | Value |
|-------|-------|
| Confidence | 0.50 |
| Usage Count | 0 |
| Last Used | [date] |
| Source | [task-id] |
```
```

## Mistake Memory Template

### File: `.aidocs/memory/mistakes.md`

```markdown
# Mistake Memory

Failures and errors to avoid in future tasks.

## Index

| ID | Name | Severity | Occurrences |
|----|------|----------|-------------|
| MIS-001 | Migration Data Ignorance | High | 2 |
| MIS-002 | API Format Assumption | Medium | 3 |
| MIS-003 | Happy Path Testing | Medium | 5 |

---

## MIS-001: Migration Data Ignorance

**Severity:** High
**Domain:** Database, DevOps

**What Happened:**
Migration timed out after 30 minutes on production.
Table had 2.8M rows, migration tried single transaction.

**Root Cause:**
Didn't check data volume before planning migration approach.
Assumed table was small based on development database.

**Impact:**
- 45 minutes wasted
- Deployment blocked
- Rollback required

**Prevention Strategy:**
1. Always run `SELECT COUNT(*)` before migration planning
2. For >100k rows, use batched migration pattern (PAT-002)
3. Test migrations against production-scale data

**Detection Improvement:**
Add pre-migration check to CI pipeline:
```bash
# Check affected tables before migration
for table in $(get_migration_tables); do
  count=$(psql -c "SELECT COUNT(*) FROM $table")
  if [ $count -gt 100000 ]; then
    echo "WARNING: $table has $count rows"
  fi
done
```

**Metadata:**
| Field | Value |
|-------|-------|
| Occurrences | 2 |
| Last Seen | 2024-01-15 |
| Source | TASK-055, TASK-089 |

---

## MIS-002: API Format Assumption

**Severity:** Medium
**Domain:** Integration, Backend

**What Happened:**
Code crashed on null value in API response.
Assumed field would always be present based on documentation.

**Root Cause:**
API documentation was outdated or incomplete.
Didn't validate response structure before accessing fields.

**Impact:**
- Runtime errors in production
- User-facing error messages

**Prevention Strategy:**
1. Always validate API response structure
2. Use TypeScript/Zod for response typing
3. Test with various response scenarios
4. Don't trust documentation blindly

**Detection Improvement:**
```typescript
// Add response validation
const ResponseSchema = z.object({
  data: z.object({
    id: z.string(),
    value: z.string().optional(), // Mark optional fields
  }),
});

const validated = ResponseSchema.parse(response);
```

**Metadata:**
| Field | Value |
|-------|-------|
| Occurrences | 3 |
| Last Seen | 2024-01-12 |
| Source | TASK-078, TASK-092, TASK-103 |

---

## Mistake Entry Template

Copy this template for new mistakes:

```markdown
## MIS-XXX: [Name]

**Severity:** [High/Medium/Low]
**Domain:** [Area where mistake occurred]

**What Happened:**
[Specific description of the failure]

**Root Cause:**
[The underlying reason, not symptoms]

**Impact:**
- [Impact 1]
- [Impact 2]

**Prevention Strategy:**
1. [Prevention step 1]
2. [Prevention step 2]

**Detection Improvement:**
[How to catch this earlier next time]

**Metadata:**
| Field | Value |
|-------|-------|
| Occurrences | 1 |
| Last Seen | [date] |
| Source | [task-id] |
```
```

## Session Memory Template

### File: `.aidocs/memory/session.md`

```markdown
# Session Memory

Current execution context for task continuity.

## Active Task

| Field | Value |
|-------|-------|
| Task ID | TASK-XXX |
| Title | [Task title] |
| Status | in_progress |
| Started | 2024-01-15T10:00:00Z |

## Loaded Patterns

Selected for this task based on domain matching:

| ID | Name | Confidence | Notes |
|----|------|------------|-------|
| PAT-001 | Error Boundary | 0.90 | Apply to async components |
| PAT-015 | Form Validation | 0.85 | Use for email field |

## Loaded Mistakes

Warnings relevant to this task:

| ID | Name | Severity | Watch For |
|----|------|----------|-----------|
| MIS-002 | API Assumption | Medium | Validate Stripe responses |
| MIS-003 | Happy Path Testing | Medium | Add edge case tests |

## Decisions Made

Choices during this session:

| Decision | Rationale | Reversible |
|----------|-----------|------------|
| Use Zod for validation | Type-safe, good errors | Yes |
| PostgreSQL not MySQL | Team familiarity | No |

## Progress Notes

Chronological execution notes:

### 10:00 - Started
- Read spec and design docs
- Loaded relevant patterns

### 10:30 - Implementation
- Created base component structure
- Applied PAT-001 for error handling

### 11:15 - Testing
- Unit tests passing
- Found edge case: empty array response

## Open Questions

Unresolved items needing clarification:

- [ ] Error message wording for rate limits
- [ ] Retry policy for failed webhooks

## Carry Forward

Items for next session:

- Complete integration tests
- Update API documentation
- Deploy to staging

---

## Session Template

Clear and restart with:

```markdown
# Session Memory

## Active Task

| Field | Value |
|-------|-------|
| Task ID | |
| Title | |
| Status | |
| Started | |

## Loaded Patterns

| ID | Name | Confidence | Notes |
|----|------|------------|-------|

## Loaded Mistakes

| ID | Name | Severity | Watch For |
|----|------|----------|-----------|

## Decisions Made

| Decision | Rationale | Reversible |
|----------|-----------|------------|

## Progress Notes

## Open Questions

## Carry Forward
```
```

## Decision Memory Template

### File: `.aidocs/memory/decisions.md`

```markdown
# Decision Memory

Key technical and architectural decisions.

## Index

| ID | Decision | Date | Status |
|----|----------|------|--------|
| DEC-001 | Use PostgreSQL | 2024-01-01 | Active |
| DEC-002 | TypeScript strict mode | 2024-01-01 | Active |
| DEC-003 | Monorepo with Nx | 2024-01-05 | Active |

---

## DEC-001: Use PostgreSQL

**Date:** 2024-01-01
**Status:** Active
**Context:** Database selection for new project

**Decision:**
Use PostgreSQL as primary database.

**Rationale:**
- Team has strong PostgreSQL experience
- JSON/JSONB support for flexible data
- Strong ecosystem (PostGIS, pg_trgm)
- Better for complex queries than MySQL

**Alternatives Considered:**
| Option | Pros | Cons |
|--------|------|------|
| MySQL | Simpler, widespread | Less feature-rich |
| MongoDB | Flexible schema | Team unfamiliar |
| SQLite | Zero config | Not suitable for prod |

**Consequences:**
- Need PostgreSQL-compatible hosting
- Can use advanced features (CTEs, window functions)
- Migration path to other SQL DBs possible

**References:**
- ADR-001 in /docs/adr/

---

## DEC-002: TypeScript Strict Mode

**Date:** 2024-01-01
**Status:** Active
**Context:** TypeScript configuration

**Decision:**
Enable strict mode in tsconfig.json:
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

**Rationale:**
- Catches more bugs at compile time
- Better IDE support
- Forces explicit typing

**Consequences:**
- More verbose code initially
- Some third-party types need fixes
- Learning curve for team

---

## Decision Entry Template

```markdown
## DEC-XXX: [Decision Title]

**Date:** [YYYY-MM-DD]
**Status:** [Active/Superseded/Deprecated]
**Context:** [What prompted this decision]

**Decision:**
[What was decided]

**Rationale:**
[Why this option was chosen]

**Alternatives Considered:**
| Option | Pros | Cons |
|--------|------|------|

**Consequences:**
[Impacts of this decision]

**References:**
- [Links to ADRs, docs, discussions]
```
```

## Quick Reflection Template

### File: `.aidocs/memory/reflections/TASK-XXX.md`

For archiving individual task reflections:

```markdown
# Reflection: TASK-XXX

**Task:** [Title]
**Date:** [YYYY-MM-DD]
**Outcome:** [Success/Partial/Failure]

## Summary

[2-3 sentences summarizing the task execution]

## What Worked

- [Specific thing 1]
- [Specific thing 2]

## What Didn't Work

- [Specific thing 1]
- [Specific thing 2]

## Patterns Extracted

| ID | Name | Confidence |
|----|------|------------|
| PAT-XXX | [Name] | [0.XX] |

## Mistakes Documented

| ID | Name | Severity |
|----|------|----------|
| MIS-XXX | [Name] | [Severity] |

## Action Items

- [ ] [Action 1]
- [ ] [Action 2]

## Notes

[Any additional context or observations]
```

## Memory Initialization Script

Create a new project's memory structure:

```bash
#!/bin/bash
# init-memory.sh

mkdir -p .aidocs/memory
mkdir -p .aidocs/memory/reflections

cat > .aidocs/memory/patterns.md << 'EOF'
# Pattern Memory

Successful patterns learned from project execution.

## Index

| ID | Name | Domain | Confidence |
|----|------|--------|------------|

---

<!-- Add patterns below -->
EOF

cat > .aidocs/memory/mistakes.md << 'EOF'
# Mistake Memory

Failures and errors to avoid in future tasks.

## Index

| ID | Name | Severity | Occurrences |
|----|------|----------|-------------|

---

<!-- Add mistakes below -->
EOF

cat > .aidocs/memory/decisions.md << 'EOF'
# Decision Memory

Key technical and architectural decisions.

## Index

| ID | Decision | Date | Status |
|----|----------|------|--------|

---

<!-- Add decisions below -->
EOF

cat > .aidocs/memory/session.md << 'EOF'
# Session Memory

No active session.
EOF

echo "Memory structure initialized in .aidocs/memory/"
```

## JSONL Alternative Format

For programmatic access, patterns and mistakes can also be stored as JSONL:

### `.aidocs/memory/patterns.jsonl`

```jsonl
{"id":"PAT-001","name":"Error Boundary Pattern","domain":"React","context":"Async components","problem":"Unhandled rejections","solution":"Wrap in try-catch with error state","confidence":0.9,"usage_count":8,"last_used":"2024-01-15","source":"TASK-042"}
{"id":"PAT-002","name":"Batched Migration","domain":"Database","context":"Large table changes","problem":"Migration timeouts","solution":"Add nullable, batch update, add constraint","confidence":0.85,"usage_count":4,"last_used":"2024-01-10","source":"TASK-055"}
```

### `.aidocs/memory/mistakes.jsonl`

```jsonl
{"id":"MIS-001","name":"Migration Data Ignorance","severity":"high","domain":"Database","description":"Didn't check row count before migration","root_cause":"Assumed small table","prevention":"Always COUNT(*) first","occurrences":2,"last_seen":"2024-01-15","source":"TASK-055"}
{"id":"MIS-002","name":"API Format Assumption","severity":"medium","domain":"Integration","description":"Assumed field always present","root_cause":"Trusted docs blindly","prevention":"Validate response structure","occurrences":3,"last_seen":"2024-01-12","source":"TASK-078"}
```

## ID Generation

Pattern for generating IDs:

| Type | Format | Example |
|------|--------|---------|
| Pattern | PAT-NNN | PAT-001, PAT-042 |
| Mistake | MIS-NNN | MIS-001, MIS-015 |
| Decision | DEC-NNN | DEC-001, DEC-008 |

Increment within project scope. Reset for new projects.
