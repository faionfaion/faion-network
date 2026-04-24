# Code Review Examples

Good and bad examples of code review practices, including AI-assisted patterns.

## Comment Prefix System

Use consistent prefixes to signal comment intent:

| Prefix | Meaning | Requires Action |
|--------|---------|-----------------|
| `[Required]` | Must fix before merge | Yes |
| `[Suggestion]` | Consider this improvement | Optional |
| `[Question]` | Need clarification | Yes (answer) |
| `[Nitpick]` | Minor style preference | No |
| `[Nice]` | Good pattern worth noting | No |
| `[FYI]` | Educational, no action needed | No |
| `[Security]` | Security-related concern | Usually yes |
| `[Performance]` | Performance consideration | Context-dependent |

---

## Good Review Comments

### Required Change with Solution

```markdown
[Required] This query is vulnerable to SQL injection. The user input
is concatenated directly into the query string.

Current code:
query = f"SELECT * FROM users WHERE name = '{name}'"

Suggested fix:
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))

See: https://owasp.org/www-community/attacks/SQL_Injection
```

**Why it's good:**
- Clear about the problem
- Shows the vulnerable code
- Provides a concrete fix
- Links to reference

### Suggestion with Explanation

```markdown
[Suggestion] Consider using early return here to reduce nesting.

Current:
if user:
    if user.is_active:
        if user.has_permission('edit'):
            do_something()

Could be:
if not user:
    return
if not user.is_active:
    return
if not user.has_permission('edit'):
    return
do_something()

This makes the happy path clearer and reduces cognitive load.
```

**Why it's good:**
- Shows before/after
- Explains the benefit
- Non-blocking (author can disagree)

### Question That Helps Understanding

```markdown
[Question] I see you're using a 60-second timeout here instead of
our standard 30 seconds. Is this intentional for this specific
endpoint? If so, could you add a comment explaining why?

Context: Our API gateway has a 45-second limit, so this might cause
issues in production.
```

**Why it's good:**
- Asks rather than assumes
- Provides context
- Suggests documentation if intentional

### Praise That Reinforces Patterns

```markdown
[Nice] Great use of the Repository pattern here. This makes the
code much easier to test since we can mock the repository.

I'll reference this in our patterns doc for others to learn from.
```

**Why it's good:**
- Specific about what's good
- Explains why
- Plans to share knowledge

### Educational Comment

```markdown
[FYI] There's a utility function in `utils/string.ts` that does
this exact thing: `truncateWithEllipsis(text, maxLength)`.

Not blocking since your implementation works, but using shared
utilities keeps things consistent and easier to maintain.
```

**Why it's good:**
- Points to existing solution
- Non-blocking
- Explains the benefit

---

## Bad Review Comments

### Vague Criticism

```markdown
BAD: "This is wrong."
BAD: "I don't like this approach."
BAD: "This needs to be better."
```

**Why it's bad:** No actionable feedback. Author doesn't know what to fix.

**Better:**
```markdown
[Required] This function returns null on error, but callers expect
it to throw. This mismatch could cause null pointer exceptions.

Consider throwing an exception or updating the callers to handle null.
```

### Aggressive Tone

```markdown
BAD: "Why would you do it this way?"
BAD: "This is obviously inefficient."
BAD: "Did you even test this?"
```

**Why it's bad:** Puts author on defensive, damages team dynamics.

**Better:**
```markdown
[Question] I see you chose a linear search here. Was there a specific
reason, like the array being small? If the array can grow large,
a binary search or hash lookup might be more efficient.
```

### Bikeshedding

```markdown
BAD: (on a complex PR with real issues)
"Can you rename `userData` to `userInfo`? I think it reads better."
```

**Why it's bad:** Focuses on trivial issues while missing important ones.

**Better:** Address critical issues first. Use `[Nitpick]` sparingly and only after important feedback.

### Unclear Severity

```markdown
BAD: "You should probably handle the null case here."
```

**Why it's bad:** Is this blocking? Optional? Critical?

**Better:**
```markdown
[Required] This will throw NullPointerException if user is null,
which happens when the session expires.

Add a null check:
if (user == null) {
    return redirectToLogin();
}
```

---

## AI-Assisted Review Examples

### Good: Using AI Feedback Wisely

```markdown
AI Comment:
"Consider using Optional instead of null returns."

Human Response:
[Suggestion] (Expanding on AI feedback) The AI flagged null returns
here. In Java 11+, using Optional makes the API clearer:

Old: public User findUser(id)     // returns null if not found
New: public Optional<User> findUser(id)  // intent is clear

This prevents callers from forgetting null checks. Thoughts?
```

**Why it's good:** Human adds context and judgment to AI suggestion.

### Good: Dismissing AI False Positive

```markdown
AI Comment:
"Potential infinite loop detected in while(true) loop."

Human Response:
Dismissing AI suggestion - this is intentional. This is an event
loop that processes messages until shutdown. The break condition
is in the message handler on line 45 when receiving SHUTDOWN message.

Added a comment to clarify:
// Main event loop - exits on SHUTDOWN message (see handler line 45)
```

**Why it's good:** Explains why AI is wrong, improves code clarity.

### Good: Multi-Model Validation

```markdown
Reviewed with:
- CodeRabbit: Style and patterns [PASSED]
- Claude: Logic review [1 issue - fixed]
- Semgrep: Security scan [PASSED]

Claude caught a race condition in the cache update that CodeRabbit
missed. Added mutex lock as suggested.
```

**Why it's good:** Uses different AI tools for different strengths.

### Bad: Blindly Accepting AI

```markdown
AI suggested refactoring to functional style.
Applied all suggestions.
```

**Why it's bad:** AI doesn't understand your performance requirements or team's familiarity with functional patterns.

### Bad: Ignoring All AI Feedback

```markdown
AI flagged 12 issues.
Response: "These are all false positives."
(No explanation provided)
```

**Why it's bad:** AI is often right. Dismissing without explanation misses real issues and doesn't help improve AI rules.

---

## PR Description Examples

### Good PR Description

```markdown
## Summary

Adds rate limiting to the /api/login endpoint to prevent brute
force attacks. Implements token bucket algorithm with configurable
limits per IP.

## SDD References

| Document | Link |
|----------|------|
| Spec | [SPEC-042 Security Hardening](link) |
| Design | [DESIGN-042 Rate Limiting](link) |
| Task | [TASK-042-03 Implement Rate Limiter](link) |

## Changes

- Added RateLimiter class with token bucket algorithm
- Integrated with login endpoint via middleware
- Added configuration for limits (default: 5 attempts/minute)
- Added Redis backend for distributed deployments

## Acceptance Criteria

| AC | Status | Evidence |
|----|--------|----------|
| AC-1: Block after 5 failed attempts | Verified | [Test link] |
| AC-2: Reset after 1 minute | Verified | [Test link] |
| AC-3: Works across servers | Verified | [Integration test] |

## Testing

- Unit tests: 12 new tests, all passing
- Integration: Tested with Redis cluster
- Manual: Verified in staging environment

## Security Considerations

- Rate limit state stored in Redis (not in-memory) for multi-server
- IP extraction handles X-Forwarded-For (configurable)
- Limits configurable via environment variables

## Notes for Reviewer

Please pay special attention to:
1. Redis connection handling (lines 45-60) - first time using async Redis
2. IP extraction logic - want to make sure it's correct for our proxy setup
```

**Why it's good:**
- Clear summary of what and why
- Links to SDD documents
- Shows verification evidence
- Highlights areas needing attention

### Bad PR Description

```markdown
Fixed login bug
```

**Why it's bad:** No context, no traceability, reviewer has no idea what to focus on.

---

## Review Thread Examples

### Good: Collaborative Discussion

```markdown
REVIEWER:
[Question] Why fetch all users and filter in memory instead of
using a database query?

AUTHOR:
Good question! The filter conditions are dynamic and can be complex
(user-defined). Building the query dynamically was getting messy.
The user count is capped at 100 per org, so performance is acceptable.

REVIEWER:
Makes sense for current scale. [Suggestion] Consider adding a comment
about the 100-user assumption and maybe a TODO to revisit if we
increase that limit?

AUTHOR:
Done! Added comment on line 34 with link to the limit config.

REVIEWER:
Perfect, approved!
```

### Bad: Adversarial Discussion

```markdown
REVIEWER:
This is inefficient.

AUTHOR:
It works.

REVIEWER:
It's still inefficient.

AUTHOR:
Can you be more specific?

REVIEWER:
You should know this.
```

**Problem:** No learning happens, relationship damaged.

---

## AI Review Prompt Examples

See [llm-prompts.md](llm-prompts.md) for comprehensive prompts to use with AI code review tools.
