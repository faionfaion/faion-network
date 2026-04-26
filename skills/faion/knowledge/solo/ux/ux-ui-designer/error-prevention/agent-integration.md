# Agent Integration — Error Prevention

## When to use
- Auditing form specs or component designs for missing input constraints, absent real-time validation, and unguarded destructive actions
- Generating an error prevention checklist tailored to a specific form or workflow from a spec document
- Reviewing API endpoint contracts to flag inputs accepted without server-side constraints that also lack client-side prevention
- Drafting confirmation dialog copy for destructive actions (delete, cancel subscription, bulk operations)
- Reviewing code PRs for validation gaps: fields that accept any string where a constrained type or enum is appropriate

## When NOT to use
- Replacing QA — error prevention is a design heuristic, not a test suite; it complements but does not substitute testing
- Over-adding confirmations to routine, easily reversible actions — dialog fatigue degrades prevention effectiveness for genuinely dangerous actions
- Very early concept stages where form fields are not yet defined

## Where it fails / limitations
- Agents auditing from specs or wireframes cannot detect runtime validation gaps — a field may look constrained in the spec but accept any input in the actual implementation
- "Smart defaults" recommendations require understanding user behavior data (most common selections, geographic distribution) that agents rarely have access to
- Inline validation timing (on blur vs. on change vs. on submit) is a context-sensitive judgment; agents will suggest on-change but this creates noise for fields like passwords
- Confirmation dialog wording must be precise enough to convey the consequence; generic agent-generated copy ("Are you sure?") is worse than no dialog at all
- Error prevention for complex multi-step workflows (wizard-style flows) requires understanding the full state machine, not just individual fields

## Agentic workflow
A Claude agent reads a form spec or component definition and applies the Error Prevention Audit template: for each field it identifies the input type, constraints that should be applied, appropriate validation timing, smart default opportunities, and whether any associated action is destructive enough to require confirmation. The output is a prioritized remediation list. For code reviews, the agent scans form handler code for missing server-side validation and unguarded mutation endpoints.

### Recommended subagents
- `faion-sdd-executor-agent` — checks that each form field in a spec has a defined validation rule in the acceptance criteria before the feature moves to implementation

### Prompt pattern
```
You are a UX error prevention auditor applying Nielsen's Heuristic #5.
Review the form specification below. For each field, analyze:
1. Input type — is it constrained (picker, select, numeric stepper) or open (text)?
2. Validation — is there real-time validation? What triggers it? What is the rule?
3. Default — is a smart default appropriate? What would it be?
4. Format guidance — does the user know what format is expected?

For each field with a gap: describe the gap, classify severity (High if blocks task, Medium if causes errors, Low if cosmetic), and propose the specific prevention fix.
Also list any destructive actions in this flow and assess whether the current confirmation (if any) is adequate.
```

```
Review this form validation code. Find:
- Fields that accept any string type where an enum, regex, or numeric constraint is appropriate
- Validation that only runs on submit (not real-time for high-stakes fields)
- Destructive mutation endpoints with no confirmation step in the frontend
Report as a list with file:line references.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `zod` (TypeScript) | Runtime schema validation; enforce field constraints at the boundary | `npm i zod` / zod.dev |
| `yup` | Alternative schema validation for forms; integrates with Formik/React Hook Form | `npm i yup` |
| `pydantic` (Python) | Server-side input validation with type enforcement | `pip install pydantic` / docs.pydantic.dev |
| `axe-cli` | Catch missing required field indicators and unlabeled inputs | `npm i -g axe-cli` / github.com/dequelabs/axe-cli |
| `htmlhint` | Check HTML forms for missing `required`, `type`, `autocomplete` attributes | `npm i -g htmlhint` / htmlhint.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog / Sentry | SaaS | Yes — API | Query real form error rates and error types to identify highest-impact prevention targets |
| FullStory | SaaS | Partial | Rage-click and dead-click data reveals where users hit unexpected errors |
| LogRocket | SaaS | Yes — API | Session replay + console errors correlated; surfaces validation failures at scale |
| Formspree / Typeform | SaaS | Partial | Built-in validation; limited custom constraint configuration |

## Templates & scripts
See `templates.md` for the Error Prevention Audit template.

```python
# Zod schema generator stub — agent produces this from a form spec
# Example output for an email + phone form
import textwrap

def generate_zod_schema(fields: list[dict]) -> str:
    lines = ["import { z } from 'zod';", "", "export const formSchema = z.object({"]
    for f in fields:
        name = f["name"]
        ftype = f.get("type", "string")
        required = f.get("required", True)
        if ftype == "email":
            rule = "z.string().email('Invalid email format')"
        elif ftype == "phone":
            rule = "z.string().regex(/^[+]?[\\d\\s\\-().]{7,15}$/, 'Invalid phone format')"
        elif ftype == "integer":
            mn, mx = f.get("min", 1), f.get("max", 999)
            rule = f"z.number().int().min({mn}).max({mx})"
        else:
            rule = "z.string().min(1)"
        if not required:
            rule += ".optional()"
        lines.append(f"  {name}: {rule},")
    lines.append("});")
    return "\n".join(lines)
```

## Best practices
- Prefer constrained input types (date pickers, select dropdowns, numeric steppers) over open text fields whenever the valid value set is finite or format-bound
- Validate on blur for most fields, on change for password strength indicators only — on-change validation for other fields triggers error states before users finish typing
- For destructive actions: make the confirmation button label specific to the action ("Delete 47 files" not "OK") and position Cancel as the default focus
- Apply `autocomplete` attributes to all personal data fields — browser autofill is the cheapest recognition/recall aid for repeat data entry
- Surface format hints before the user enters data (placeholder or helper text), not only after they make an error

## AI-agent gotchas
- Agents reviewing code will miss client-side-only validation gaps unless they also review the corresponding API handler — always audit both layers in the same pass
- Generated confirmation dialog copy tends to be vague ("This action cannot be undone") — require the agent to include the specific object count or name in the button label
- Agents will recommend real-time validation for every field; over-application causes form rage interactions — specify that on-blur is the default and on-change is reserved for complex fields (passwords, search)
- Human review required before deploying any agent-generated change that removes or modifies an existing confirmation dialog — accidental removal of a confirmation is a data loss risk
- Zod/Pydantic schemas generated from specs will not account for cross-field validation rules (e.g., end date must be after start date); flag these as needing manual implementation

## References
- https://www.nngroup.com/articles/slips/
- https://www.nngroup.com/articles/user-errors/
- https://formsthatwork.com/
- https://zod.dev/
- https://docs.pydantic.dev/
