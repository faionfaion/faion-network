# TASK_{NNN}: {Concise Title in Imperative Voice}

**Phase:** {N}
**Wave:** {N}

**Description:**
{2-3 sentences: what needs to be done and why it matters}

**Traces to:**
- AD-{N}: {Full architectural decision text — do not require reader to open design.md}
- FR-{N}: {Full requirement text — do not require reader to open spec.md}

**Depends on:** TASK_{NNN} [FS], TASK_{NNN} [SS] (or "None")

**Blocks:** TASK_{NNN}, TASK_{NNN}

**Complexity:** simple | normal | complex
**Context Estimate:** ~{X}k tokens

**Acceptance Criteria:**
- [ ] {Specific, observable outcome — HTTP status code, database state assertion, or measurable value}
- [ ] {Another specific criterion}
- [ ] {At least 3 criteria for normal/complex tasks}

**Files:**
| Action | File | Purpose |
|--------|------|---------|
| CREATE | `{path}` | {what this file does} |
| MODIFY | `{path}` | {what to add or change} |

**Technical Notes:**
{Cite exact file path and pattern to follow, not generic advice. Write after Wave N-1 execution for Wave N+ tasks.}

**Tests:**
- [ ] Unit: {specific test description}
- [ ] Integration: {specific test description}
