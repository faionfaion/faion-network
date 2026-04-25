# Agent Integration — Error Recovery (Nielsen Heuristic #9)

## When to use
- Auditing existing UI error messages for clarity and actionability
- Writing or reviewing microcopy for form validation, network errors, 404s, and payment failures
- Before a launch: systematic sweep of all error states in a feature
- When support tickets show users confused by a specific error message
- Code review: checking that error strings returned by the API are user-presentable before they surface in UI

## When NOT to use
- Preventing errors in the first place (use Heuristic #5 — Error Prevention instead)
- Designing empty states or onboarding flows — different UX domain
- Performance or reliability issues causing errors — fix the root cause, not the message
- When the error is silent by design (background sync failures that auto-retry)

## Where it fails / limitations
- Good error messages alone cannot fix bad information architecture — if users reach the wrong place, clarity of the error message is irrelevant
- Agents can generate grammatically correct error messages that still fail comprehension testing because they assume user knowledge the agent does not have
- Localization: plain-language messages in English may not translate well — every locale needs native-speaker review
- Dynamic error messages (showing field-specific server validation) require backend contract alignment; agent cannot infer server error schema without API docs
- Accessibility compliance (ARIA live regions, focus management) requires front-end implementation, not just message copy

## Agentic workflow
An agent can systematically audit a codebase or design file for error strings, classify them by type (validation, network, auth, 404, generic), and score each against the three-component framework (what happened / why / how to fix). It then outputs a prioritized rewrite list. The agent needs a structured input — either extracted strings from codebase search or a design file export. Human review of rewrites is needed before shipping, especially for payment errors and auth failures where tone matters legally and commercially.

### Recommended subagents
- `faion-usability-agent` — applies heuristic scoring to existing error messages and classifies severity
- general code-search agent — extracts all error strings from codebase using grep/AST patterns before audit

### Prompt pattern
```
Review the following error messages. For each, score it 1-3 on three dimensions:
1. What happened (1=vague, 3=specific)
2. Why it happened (1=missing, 3=contextual)
3. How to fix (1=no action, 3=specific actionable step)
Then provide a rewritten version that scores 3/3/3. Do not use technical jargon or error codes.
Format: | Original | Scores | Rewrite |
```

```
Given this API error response schema (JSON), write user-facing error messages for each error_code.
Rules: plain English, no codes in UI, include at least one recovery action per message,
blame the system not the user.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ripgrep` (`rg`) | Extract all error string literals from codebase for audit | `apt install ripgrep` / github.com/BurntSushi/ripgrep |
| `jq` | Parse API error response schemas to map codes → messages | `apt install jq` / jq.org |
| `vale` | Prose linting — can enforce plain language rules on error copy | `brew install vale` / docs.errata.ai/vale |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | Yes — REST API | Query most frequent errors in production; agent can prioritize which to rewrite based on occurrence count |
| LogRocket | SaaS | Yes — API | Session replay + error tracking; identifies which error messages cause abandonment |
| Phrase / Lokalise | SaaS | Yes — API | Translation management; agent can push rewritten strings and flag for locale review |
| Lingo | SaaS | Partial | Shared copy library; useful for centralizing error string standards |
| Zeplin / Figma | SaaS | Partial — plugin API | Agent can annotate error states in design files via plugin |

## Templates & scripts
See `templates.md` for the Error Message Design and Error Handling Audit templates.

Inline script — extract all error string candidates from a Python/JS codebase:
```bash
#!/usr/bin/env bash
# Usage: ./extract_errors.sh ./src
# Outputs: error_strings.txt with file:line:match

TARGET=${1:-.}

echo "=== Python error strings ==="
rg --type py -n \
  '(raise|messages\.|error\s*=|detail\s*=)\s*["\x27]' \
  "$TARGET" | head -100

echo "=== JavaScript error strings ==="
rg --type js --type ts -n \
  '(throw new Error|message:\s*["\x27]|errorMessage\s*=)' \
  "$TARGET" | head -100

echo "=== Template strings ==="
rg -n 'Error|error|failed|invalid|not found|denied|unauthorized' \
  --glob '*.html' --glob '*.jsx' --glob '*.tsx' \
  "$TARGET" | grep -v '^\s*//' | head -100
```

## Best practices
- The three-part structure (what / why / how) is non-negotiable for severity-3+ errors; severity-1 cosmetic issues can use shorter copy.
- Inline placement (next to the field) is always better than a top-of-form summary for single-field errors; use both for multi-field forms.
- Recovery actions should be buttons or links, not instructions. "Try again" as a `<button>` beats "Please try again" as text.
- Payment and auth errors have legal implications — avoid language that implies the user's card is fraudulent; use neutral phrasing ("card not accepted").
- Blank-state vs. error-state: distinguish between "no results" (not an error) and "search failed" (an error). Different message, different design.
- Test error messages with users who have no product knowledge — comprehension failures are invisible to the team.
- Standardize error message style in a shared copy library (Notion table, Lokalise) to prevent team members from writing ad-hoc variations.

## AI-agent gotchas
- Agents often improve grammar but keep the error code in parentheses — explicitly prohibit codes in the system prompt.
- Agents struggle with domain-specific errors (payment declines, GDPR consent failures) unless given full business context.
- "Do not blame the user" is easy to violate subtly — "you entered" is still blame; prompt for second-person only when the user had a genuine choice.
- Agents generate long rewrites; real UI has character limits. Include max-character constraints in prompts.
- An agent sweep of error strings will miss errors generated dynamically by third-party SDKs (Stripe, Auth0) that are passed through unchanged — these need separate handling.
- ARIA live region implementation cannot be verified by a text-only agent — always flag for front-end developer review.

## References
- https://www.nngroup.com/articles/error-message-guidelines/
- https://uxdesign.cc/how-to-write-better-error-messages-b0fdc07e60dc
- Microcopy: The Complete Guide — Kinneret Yifrah
- https://material.io/design/communication/confirmation-acknowledgement.html
- https://www.uxmatters.com/mt/archives/2010/08/avoiding-catastrophe-design-for-prevention-and-recovery.php
