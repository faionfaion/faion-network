# LLM Prompts for Spec Writing

Prompts to use with LLMs for generating and reviewing specifications.

---

## When to Use LLMs for Specs

| Task | LLM Usefulness | Notes |
|------|----------------|-------|
| Generate initial draft | High | From brief or idea |
| Expand requirements | High | Add detail to outline |
| Write acceptance criteria | High | Convert FR to AC |
| Review for gaps | High | Find missing pieces |
| Check SMART criteria | Medium | Validate specificity |
| Prioritize features | Low | Requires business context |
| Validate feasibility | Low | Requires technical context |

---

## Spec Generation Prompts

### From Brief to Full Spec

Use when you have a high-level idea and need a complete specification.

```markdown
## Task
Generate a specification document for the following feature.

## Feature Brief
[Paste your 2-5 sentence feature description]

## Project Context
- Tech stack: [e.g., Next.js, PostgreSQL, Tailwind]
- Existing patterns: [e.g., "Auth uses JWT, forms use react-hook-form"]
- Constraints: [e.g., "Must work offline, no external services"]

## Requirements
1. Use the following spec structure:
   - Problem Statement (Who, Problem, Impact, Solution, Success Metric)
   - User Personas (at least 1)
   - User Stories (with INVEST criteria)
   - Functional Requirements (FR-XXX format, SMART)
   - Non-Functional Requirements (performance, security)
   - Acceptance Criteria (Given-When-Then)
   - Out of Scope (with reasoning)
   - Boundaries (Always/Ask First/Never)

2. Make all requirements:
   - Specific: One interpretation only
   - Measurable: Testable pass/fail
   - With concrete values (not "should be fast" but "< 500ms")

3. Include acceptance criteria for:
   - Happy path
   - Error cases
   - Edge cases

## Output Format
Return as markdown following the structure above.
```

---

### From User Stories to Requirements

Use when you have user stories and need detailed requirements.

```markdown
## Task
Expand these user stories into detailed functional requirements.

## User Stories
[Paste user stories]

## Requirements for Output
For each user story, generate:

1. Functional Requirements (FR-XXX format):
   - Use "System SHALL" for must-haves
   - Use "System SHOULD" for should-haves
   - Include validation rules with specific values
   - Link back to user story (Traces to: US-XXX)

2. Each requirement must be SMART:
   - Specific: Single interpretation
   - Measurable: Can verify pass/fail
   - Achievable: Technically possible
   - Relevant: Delivers user value
   - Time-bound: Has priority (Must/Should/Could)

## Example Format
### FR-001: [Title]
**Requirement:** System SHALL [specific action].
**Rationale:** [Why needed]
**Traces to:** US-001
**Priority:** Must
**Validation Rules:**
- [Rule with specific value]
- [Rule with specific value]
```

---

### From Requirements to Acceptance Criteria

Use when you have requirements and need testable acceptance criteria.

```markdown
## Task
Generate acceptance criteria for these requirements using Given-When-Then format.

## Requirements
[Paste requirements]

## Requirements for Output
For each requirement, generate:

1. Happy path scenario (main success)
2. At least one error scenario
3. Relevant edge cases

Each acceptance criterion must:
- Use Given-When-Then format
- Include specific test values (not "valid input" but "test@example.com")
- Be independently testable
- Have a clear pass/fail determination

## Example Format
### AC-001: [Scenario Title]

**Scenario:** [Brief description]

**Given:** [Specific precondition]
**And:** [Additional precondition with values]
**When:** [Specific action with values]
**Then:** [Expected result with values]
**And:** [Additional expected result]
```

---

### Generate API Specification

Use when defining REST API endpoints.

```markdown
## Task
Generate an API specification for the following endpoint.

## Endpoint Description
[Describe what the endpoint does]

## Context
- Auth method: [JWT / API Key / None]
- Response format: JSON
- Error format: { error: { code, message, details? } }

## Requirements for Output
Generate specification including:

1. Endpoint details (method, path, auth, rate limit)
2. Request format:
   - Headers (with required flag)
   - Path parameters (with types)
   - Query parameters (with types, defaults)
   - Request body (with validation rules)
3. Response format:
   - Success response (200/201) with example
   - Error responses (400, 401, 403, 404, 500) with examples
4. Acceptance criteria (Given-When-Then) for:
   - Successful request
   - Validation error
   - Auth error
   - Rate limiting

Use specific example values throughout.
```

---

### Generate UI Component Spec

Use when specifying reusable UI components.

```markdown
## Task
Generate a component specification for the following UI component.

## Component Description
[Describe the component's purpose and variants]

## Design System Context
- Color tokens: [List primary colors]
- Spacing scale: [e.g., 4px base]
- Typography: [Font family, sizes]

## Requirements for Output
Generate specification including:

1. Props interface (TypeScript):
   - Required vs optional props
   - Prop types and allowed values
   - Default values
   - Callback signatures

2. Visual specifications:
   - Variants table (colors, borders)
   - Sizes table (height, padding, font)
   - States (default, hover, focus, active, disabled, loading, error)

3. Accessibility requirements:
   - Semantic HTML element
   - ARIA attributes
   - Keyboard interactions
   - Focus management
   - Touch target size

4. Acceptance criteria for:
   - Default rendering
   - Each state (hover, focus, disabled, loading)
   - Keyboard navigation
```

---

## Spec Review Prompts

### Check for Gaps

Use to find missing pieces in existing specs.

```markdown
## Task
Review this specification for gaps and missing information.

## Specification
[Paste specification]

## Check For
1. Missing sections:
   - Problem statement
   - User personas
   - Success metrics
   - Non-functional requirements
   - Out of scope
   - Assumptions/constraints
   - Boundaries

2. Incomplete requirements:
   - Requirements without traceability
   - Requirements without priorities
   - Vague language (fast, good, easy, secure, many)
   - Missing validation rules

3. Acceptance criteria gaps:
   - Missing happy path
   - Missing error scenarios
   - Missing edge cases
   - Vague values ("valid input" instead of specific values)

4. LLM execution readiness:
   - Missing boundaries (Always/Ask First/Never)
   - Missing technical context
   - Ambiguous implementation details

## Output Format
List each gap as:
- **Section:** [Where the gap is]
- **Issue:** [What's missing or wrong]
- **Recommendation:** [How to fix]
```

---

### Validate SMART Criteria

Use to check if requirements meet SMART criteria.

```markdown
## Task
Validate these requirements against SMART criteria.

## Requirements
[Paste requirements]

## For Each Requirement, Check

| Criterion | Question | Pass/Fail |
|-----------|----------|-----------|
| Specific | Is there only one possible interpretation? | |
| Measurable | Can you verify this pass/fail with a test? | |
| Achievable | Is this technically possible? | |
| Relevant | Does this deliver user/business value? | |
| Time-bound | Is priority assigned (Must/Should/Could)? | |

## Output Format
For each requirement:
- **ID:** FR-XXX
- **Status:** Pass / Needs Revision
- **Issues:** [List any criteria that fail]
- **Suggested Revision:** [If needs revision]
```

---

### Convert Vague to Specific

Use to transform vague requirements into specific ones.

```markdown
## Task
Convert these vague requirements into specific, measurable requirements.

## Vague Requirements
[Paste vague requirements]

## Transformation Rules
- "Fast" -> Specify response time (e.g., "< 500ms p95")
- "Secure" -> Specify mechanism (e.g., "bcrypt 12 rounds")
- "User-friendly" -> Specify interaction (e.g., "< 3 clicks")
- "Handle errors" -> Specify behavior (e.g., "display message, log to Sentry")
- "Support many users" -> Specify number (e.g., "10,000 concurrent")
- "Mobile-friendly" -> Specify breakpoints (e.g., "responsive at 320px, 768px, 1024px")

## Output Format
For each vague requirement:
- **Original:** [Vague text]
- **Specific:** [Precise replacement with values]
- **Rationale:** [Why this specific value]
```

---

## Iterative Refinement Prompts

### Expand Brief to Outline

Step 1 of iterative spec writing.

```markdown
## Task
Expand this brief into a specification outline.

## Brief
[1-3 sentences describing the feature]

## Output
Create an outline with:
1. Problem statement (fill in Who, Problem, Impact)
2. List of likely user stories (titles only)
3. List of obvious requirements (titles only)
4. List of potential out-of-scope items
5. Questions that need answering before full spec

Do NOT write the full spec yet - just the outline.
```

---

### Expand Outline to Draft

Step 2 of iterative spec writing.

```markdown
## Task
Expand this outline into a full specification draft.

## Outline
[Paste outline from previous step]

## Answers to Questions
[Answer any questions from the outline]

## Output
Full specification following the standard template, including:
- Complete user stories with INVEST criteria
- Detailed functional requirements with SMART criteria
- Acceptance criteria with Given-When-Then
- Non-functional requirements
- Out of scope with reasoning
```

---

### Review and Refine Draft

Step 3 of iterative spec writing.

```markdown
## Task
Review and refine this specification draft.

## Draft Specification
[Paste draft]

## Review Focus
1. Are all requirements specific and measurable?
2. Are acceptance criteria using concrete values?
3. Is anything missing for LLM execution?
4. Are boundaries (Always/Ask First/Never) clear?

## Output
Return the refined specification with:
- Improvements highlighted
- Rationale for changes
- Any remaining questions
```

---

## Best Practices

### Prompt Engineering Tips

1. **Provide context** - Tech stack, existing patterns, constraints
2. **Show examples** - Include example format in prompt
3. **Be specific about output** - Request exact structure
4. **Iterate** - Start with outline, expand gradually
5. **Review critically** - LLM output needs human validation

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| LLM invents requirements | Provide clear scope boundaries |
| Generic acceptance criteria | Request specific test values |
| Missing edge cases | Explicitly ask for error/edge scenarios |
| Over-detailed spec | Request MVP scope first |
| Inconsistent format | Provide template in prompt |

### Quality Checklist

After LLM generates spec, verify:

- [ ] All requirements trace to user stories
- [ ] No vague language remains
- [ ] Acceptance criteria have concrete values
- [ ] Boundaries are defined for LLM execution
- [ ] Out of scope is explicitly stated
- [ ] Technical context matches project

---

*LLM Prompts for Spec Writing | v1.0.0*
