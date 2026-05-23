# Agent Integration — Help Users Recognize, Diagnose, and Recover from Errors

## When to use
- When auditing a product against Nielsen Heuristic #9 as part of a broader heuristic evaluation
- When reviewing any new feature before launch — every error state must have a corresponding recovery message
- When support tickets contain phrases like "I got an error" or "it said something went wrong" — generic messages are the root cause
- When engineering has written validation error messages without UX involvement — technical messages need rewriting
- After any API integration is added — server-side errors must be translated to user-facing messages

## When NOT to use
- As a substitute for error prevention (Heuristic #5) — writing good recovery messages does not eliminate the underlying error
- For success states, loading states, or empty states — this methodology is specific to error conditions
- When error conditions are so rare (infrastructure failures affecting <0.01% of sessions) that bespoke messages have negligible ROI

## Where it fails / limitations
- Generic recovery actions ("Try again later", "Contact support") are useless when users do not know what caused the error or when to retry
- Error messages that are accurate but too long are not read — users skim to the action button and retry without understanding the problem
- Mobile UI constrains error message length and placement — messages designed for desktop do not translate directly to small screens
- Error recovery flows that require leaving the current context (redirecting to a support page) cause task abandonment; inline recovery is almost always better
- Accessibility is consistently overlooked: errors that rely on color alone (red border with no text) are invisible to colorblind users and screen readers

## Agentic workflow
A Claude subagent excels at two tasks: (1) auditing a list of existing error messages against the three-component framework (what happened / why / how to fix) and producing improved versions, and (2) generating error message copy for a new feature given a list of error conditions and their technical causes. The agent receives structured error data and returns improved copy; a UX writer or product manager must review and approve before implementation. Accessibility requirements (ARIA, focus management) must be specified to the agent explicitly or they will be omitted.

### Recommended subagents
- Any general-purpose Claude subagent (Sonnet) — audit existing messages, generate improved copy, classify errors by type
- `faion-sdd-executor-agent` — implement error message updates in code after copy is approved

### Prompt pattern
```
You are a UX writer specializing in error message design. For each error condition below, write an improved user-facing error message following this structure:
- Title: 5–8 words, plain language, no technical terms
- Body: 1–2 sentences explaining what happened and why (if known), in second person
- Suggested action: specific step the user can take now
- Primary button label: action verb + object (e.g., "Try Again", "Go to Home", "Update Payment Method")
- Secondary button label (optional): alternative path

Rules:
- Never use error codes in the user-facing message (log them separately)
- Never blame the user
- Always suggest a concrete next step
- If the cause is a server error outside user control, acknowledge uncertainty ("Something went wrong on our end")

Error conditions: [list with technical cause and context]
Platform: [web | iOS | Android]
Product tone: [formal | conversational | playful]
```

```
You are auditing error messages for UX quality. For each message below, score it on:
- clarity: 1–5 (is the problem understandable to a non-technical user?)
- specificity: 1–5 (does it identify the exact problem, not just "something went wrong"?)
- actionability: 1–5 (does it tell the user what to do next?)
- tone: 1–5 (is it non-blaming and helpful?)

Then provide an improved version for any message scoring below 4 in any category.

Messages: [list]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` | Automated accessibility audit including error state accessibility (ARIA, color contrast) | `npm i axe-core` / [deque.com/axe](https://www.deque.com/axe/) |
| `pa11y` | CLI accessibility checker; run against error state URLs | `npm i -g pa11y` / [pa11y.org](https://pa11y.org) |
| `storybook` | Build and review all error states in isolation across the component library | `npx storybook@latest init` / [storybook.js.org](https://storybook.js.org) |
| `i18next` | Manage error message strings across locales; ensures translations are maintained | `npm i i18next` / [i18next.com](https://www.i18next.com) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | Yes — REST API | Error tracking; agents can query Sentry for most frequent error events to prioritize which messages to fix first |
| Datadog | SaaS | Yes — REST API | Error rate monitoring; correlate error spikes with user experience impact |
| Lokalise | SaaS | Yes — API | Translation management for error messages across locales |
| Contentful | SaaS | Yes — API | Store error messages as content entries for non-developer management |
| BugSnag | SaaS | Yes — REST API | Error monitoring; prioritization by user impact |

## Templates & scripts
See `README.md` for the Error Message Template and Error Handling Audit template.

Script — extract all user-facing error strings from a TypeScript/React codebase for audit:
```bash
#!/usr/bin/env bash
# Finds string literals passed to common error display components
# Usage: bash extract-errors.sh ./src/
# Adjust grep pattern to match your error component names
grep -r --include="*.tsx" --include="*.ts" \
  -h -E "(ErrorMessage|Toast\.error|showError|alert\(|errorMessage|errorText)\s*[=(]" \
  "${1:-.}" \
  | grep -oP '["'"'"'][^"'"'"']{5,200}["'"'"']' \
  | sort -u \
  | head -100
```

## Best practices
- Design error states in Storybook alongside the happy path — error states that are not in the component library will be implemented inconsistently in production
- Use Sentry (or equivalent) to rank errors by frequency and user impact before writing new messages — fix the errors that affect the most users first
- Write the error message before writing the error handling code — if you cannot write a plain-language message, the error condition is not well-understood
- Every error message that requires user action must have a button, not just text — links are less discoverable, especially on mobile
- Maintain an error message registry (a spreadsheet or content management entry) listing every error condition, its technical cause, and its approved user-facing text — prevents drift between environments and locales
- For network and server errors, implement exponential backoff with a visible retry countdown rather than an instant retry that hammers a failing server

## AI-agent gotchas
- Agents writing error copy default to overly formal or corporate tone; specify the product's voice explicitly (conversational, concise, action-oriented)
- Agents will suggest "Contact support" as a recovery action for nearly every error — instruct the agent to reserve this only for errors the user genuinely cannot resolve themselves
- Accessibility requirements (ARIA live regions, focus management to error location, color + icon redundancy) are omitted unless explicitly included in the prompt
- Generated error messages for API-level errors often expose technical details (status codes, field names in snake_case) — instruct the agent to translate all technical terms to plain language
- When auditing large codebases, agents cannot determine which error strings are user-facing vs. internal logging — provide a filtered list (from the script above) rather than raw code

## References
- [Error Message Guidelines — NNG](https://www.nngroup.com/articles/error-message-guidelines/)
- [Writing Helpful Error Messages — UX Collective](https://uxdesign.cc/how-to-write-better-error-messages-b0fdc07e60dc)
- [Microcopy: The Complete Guide — Kinneret Yifrah](https://www.microcopybook.com/)
- [Material Design Error Patterns](https://m3.material.io/components/dialogs/guidelines)
- [Axe Accessibility Rules](https://dequeuniversity.com/rules/axe/4.9)
