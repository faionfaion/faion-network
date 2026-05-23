# Agent Integration — Error Prevention

## When to use
- When designing any form with more than 3 fields — review every field for constraint, default, and validation opportunities
- When analytics or support data shows a high rate of form submission failures or abandonment
- Before launching a flow that involves irreversible actions (delete, cancel subscription, bulk operations)
- When auditing an existing product for heuristic compliance (Nielsen Heuristic #5)
- When input data quality downstream is poor (corrupted records, broken emails, invalid dates) — trace back to missing front-end constraints

## When NOT to use
- As a substitute for error recovery design — prevention reduces errors but cannot eliminate them; both heuristics (#5 and #9) must be addressed
- For read-only interfaces with no user input — prevention patterns are irrelevant
- When confirmation dialogs are the default response to every action — overuse trains users to dismiss without reading

## Where it fails / limitations
- Inline validation with aggressive feedback (triggering on every keystroke) creates anxiety and interrupts the user before they finish typing; timing matters
- Smart defaults derived from location or profile data may be wrong for edge cases (VPN users, shared devices, corporate accounts) and cannot be treated as ground truth
- Dropdown constraints prevent invalid input but also prevent valid inputs not on the list — internationalization of phone numbers, addresses, and names breaks many constraint assumptions
- Confirmation dialogs are frequently bypassed by experienced users who have habituated to clicking "OK" on everything; they protect against slips, not deliberate mistakes
- Pattern matching for validation (email, phone, URL) via regex is notoriously imperfect; validating existence (DNS lookup for email, API call for address) is more reliable but adds latency

## Agentic workflow
A Claude subagent can audit form specifications or HTML source code to identify missing error prevention patterns: fields without type constraints, text inputs where structured pickers should be used, absence of real-time validation, and destructive actions without confirmation. Given a list of actions in a product and their consequences, the agent can also classify which require confirmation dialogs and suggest appropriate dialog copy. Implementation of specific validation logic is mechanical and can be delegated to a code-generation agent.

### Recommended subagents
- Any general-purpose Claude subagent (Sonnet) — audit form specs, classify actions by risk, draft confirmation dialog copy
- `faion-sdd-executor-agent` — implement validation logic, add constraints to form fields, write inline validation components

### Prompt pattern
```
You are a UX engineer auditing a form for error prevention. For each field below, identify:
1. Appropriate input type (text, email, tel, number, date, select, etc.)
2. Constraints to apply (min, max, pattern, required, maxlength)
3. Smart default if applicable
4. Validation timing (on blur, on change, on submit)
5. Whether a structured input (date picker, phone mask, dropdown) should replace free text

Return JSON: [{ field_name, current_type, recommended_type, constraints, default, validation_timing, structured_input_recommended, notes }]

Form fields: [list with current type and purpose]
Platform: [web | iOS | Android]
```

```
You are reviewing a list of product actions for confirmation dialog requirements.
For each action, determine:
- risk_level: low | medium | high | critical
- requires_confirmation: bool
- reversible: bool
- suggested_confirmation_copy: { title, body, confirm_label, cancel_label } (only if requires_confirmation)

Criteria: confirm only irreversible actions with significant consequences. Do NOT recommend confirmation for routine or easily reversible actions.

Actions: [list with description and consequences]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `zod` | Runtime schema validation for TypeScript forms and APIs | `npm i zod` / [zod.dev](https://zod.dev) |
| `yup` | Schema-based form validation (React ecosystem, Formik) | `npm i yup` / [github.com/jquense/yup](https://github.com/jquense/yup) |
| `vee-validate` | Vue form validation library with built-in error prevention | `npm i vee-validate` / [vee-validate.logaretm.com](https://vee-validate.logaretm.com) |
| `react-hook-form` | Performant form library with built-in validation and constraint support | `npm i react-hook-form` / [react-hook-form.com](https://react-hook-form.com) |
| `libphonenumber-js` | Phone number parsing, validation, and formatting | `npm i libphonenumber-js` / [npmjs](https://www.npmjs.com/package/libphonenumber-js) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Elements | SaaS | Yes — JS SDK | Built-in card validation, formatting, and error prevention; card number, expiry, CVC |
| Google Places Autocomplete | SaaS | Yes — REST/JS API | Address auto-complete with format validation |
| Mailgun Email Validation API | SaaS | Yes — REST API | Validate email existence beyond format; DNS MX lookup |
| Numverify | SaaS | Yes — REST API | Phone number validation and formatting by country |
| Addressy (Loqate) | SaaS | Yes — REST API | Address validation and enrichment |

## Templates & scripts
See `README.md` for the Error Prevention Audit template.

Minimal Zod schema for a common registration form with constraints:
```typescript
import { z } from "zod";

export const registrationSchema = z.object({
  email: z.string().email("Enter a valid email address"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
    .regex(/[0-9]/, "Password must contain at least one number"),
  phone: z
    .string()
    .regex(/^\+?[1-9]\d{6,14}$/, "Enter a valid phone number with country code")
    .optional(),
  birthDate: z
    .string()
    .refine((d) => !isNaN(Date.parse(d)), "Enter a valid date")
    .refine((d) => new Date(d) < new Date(), "Birth date must be in the past"),
  country: z.string().min(2).max(2, "Select a country from the list"),
  quantity: z.number().int().min(1).max(99),
});
```

## Best practices
- Apply validation on blur (when the field loses focus), not on every keystroke — keystroke validation for email or password triggers errors before the user has finished typing
- Show format examples inside the field (placeholder or hint text) before the user starts typing; do not wait for an error to explain the expected format
- When using dropdowns to constrain input, ensure the list is complete enough to not frustrate valid edge cases (e.g., include all 249 ISO countries, not just the 20 most common)
- Log validation errors server-side (which fields fail, how often) — this is the fastest way to identify which prevention measures are missing or broken in production
- Never disable the submit button as the primary prevention strategy — it leaves users confused about what is wrong; use it only after a first failed submission attempt
- For destructive confirmation dialogs, make the confirm button label describe the action ("Delete 47 Items"), not just "OK" or "Confirm" — specificity reduces accidental confirmations

## AI-agent gotchas
- Agents generating validation schemas tend to use overly strict regex for email and phone — prefer library validators (zod `.email()`, libphonenumber) over agent-written patterns
- When auditing existing forms, agents need the actual HTML or component code, not a description — descriptions omit the specific missing constraints that matter
- Agents often recommend confirmation dialogs for too many actions; explicitly tell the agent to reserve dialogs for irreversible actions with significant consequences only
- Smart default recommendations from agents are theoretical — implementation requires access to user context (geolocation, profile data) that the agent does not have; flag these as "requires runtime data"
- Inline validation timing is a UX decision that agents cannot make correctly without knowing the form's interaction pattern; always review timing recommendations with a UX designer

## References
- [Error Prevention Heuristic — NNG](https://www.nngroup.com/articles/slips/)
- [Preventing User Errors — NNG](https://www.nngroup.com/articles/user-errors/)
- [Forms That Work — Caroline Jarrett](https://formsthatwork.com/)
- [Zod Schema Validation Docs](https://zod.dev)
- [React Hook Form Docs](https://react-hook-form.com)
