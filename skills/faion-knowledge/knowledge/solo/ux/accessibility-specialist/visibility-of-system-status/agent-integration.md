# Agent Integration — Visibility of System Status

## When to use
- Any user action that triggers a server request: form submissions, file uploads, payments, deletions
- Long-running operations (>1 second): imports, exports, report generation, AI completions
- Asynchronous operations where the result arrives later: email send, background job, webhook
- Multi-step forms where users need to know which step they are on and how many remain
- Real-time status changes: connection health, sync state, auto-save confirmation

## When NOT to use
- Instantaneous operations (<100ms) where a loading indicator would flash and disappear distractingly
- Background telemetry or logging operations the user has no reason to know about
- Internal system operations that do not affect the user's current task

## Where it fails / limitations
- Progress bars for indeterminate-length operations are misleading; they can only be accurate for operations with known total work units
- Over-notification: showing a success toast for every auto-save event creates notification fatigue and users stop noticing actual errors
- Skeleton screens require designing the exact expected layout in advance; they break when the content structure differs from expectations
- ARIA live regions for screen readers require careful implementation — `aria-live="assertive"` for errors, `aria-live="polite"` for non-critical updates; mixing them causes accessibility regressions
- Offline/online status detection via `navigator.onLine` is unreliable; it detects network adapter state, not actual internet connectivity

## Agentic workflow
Claude subagents can audit component code or UI descriptions for missing feedback states and generate implementation specs for loading, success, error, and progress patterns. Agents can also write the specific component code (React spinner, toast notification, ARIA live region) given a component spec. The audit step is fully automatable; implementation requires human review for timing decisions (when to show, when to dismiss) that depend on UX context.

### Recommended subagents
- `faion-usability-agent` — audits UI for missing system status feedback; generates Status Feedback Audit template
- `faion-sdd-executor-agent` — implements loading states, toast notifications, and ARIA live regions in code

### Prompt pattern
```
Audit the following UI actions for missing system status feedback.
For each action, check: loading state, success state, error state, progress (if long operation).
Output a Status Feedback Audit table with columns: Action | Missing States | Severity | Fix.

Severity: High = user cannot tell if action succeeded | Medium = confusing delay | Low = minor friction

Actions to audit:
{action_list}
```

```
Generate a React component for a toast notification system.
Requirements:
- Types: success, error, warning, info
- Auto-dismiss: 4s for success, never for error (requires user dismissal)
- Stack up to 3 toasts; older ones scroll off
- ARIA: role="alert" for errors, role="status" for success
- No external library dependency

Framework: {React/Vue/Svelte}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` CLI | Detects missing ARIA live regions and role violations | `npm i -g axe-cli`; deque.com/axe |
| `pa11y` | Automated scan including ARIA status violations | `npm i -g pa11y`; pa11y.org |
| `playwright` | Test loading states and state transitions in CI | playwright.dev |
| `storybook` | Visualize all status states (loading/error/success) in isolation | storybook.js.org |
| `lighthouse` CI | Measures perceived performance including loading feedback quality | `npm i -g lighthouse` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sentry | SaaS | Yes | Error monitoring; surfaces missing error state coverage |
| FullStory | SaaS | Partial | Rage-click detection → identifies missing feedback (duplicate clicks) |
| Datadog RUM | SaaS | Yes | Real user monitoring; tracks long tasks and loading times |
| LogRocket | SaaS | Partial | Session replay; reveals where users click twice (no feedback) |
| Radix UI | OSS | Yes | Headless components with built-in loading/error state patterns |
| shadcn/ui | OSS | Yes | Pre-built components including Button with loading state |

## Templates & scripts
See `templates.md` for Status Feedback Audit template.

Inline script — scan React component files for buttons missing loading state:
```python
import re, glob

def find_buttons_without_loading(src_dir: str) -> list[dict]:
    """Find <Button> or <button> elements without a loading/disabled prop."""
    violations = []
    for filepath in glob.glob(f"{src_dir}/**/*.{'{tsx,jsx}'}", recursive=True):
        with open(filepath) as f:
            content = f.read()
        # Find button elements that trigger async actions (onClick with await or fetch)
        async_buttons = re.findall(
            r'(<[Bb]utton[^>]*onClick=\{[^}]*(?:async|fetch|await|submit)[^}]*\}[^>]*>)',
            content
        )
        for btn in async_buttons:
            has_loading = "loading" in btn.lower() or "disabled" in btn.lower() or "isLoading" in btn
            if not has_loading:
                violations.append({
                    "file": filepath,
                    "element": btn[:100],
                    "issue": "Async button missing loading/disabled state",
                    "severity": "High",
                })
    return violations

for v in find_buttons_without_loading("src/"):
    print(v)
```

## Best practices
- Disable the submit button immediately on click and show a spinner inline in the button — prevents double submission and gives instant feedback within the same element the user just interacted with
- For operations lasting 1-3 seconds, use an indeterminate spinner; for operations where progress can be measured (file upload, batch import), use a determinate progress bar with percentage
- Distinguish error states from loading states with color and icon — a spinner that changes to a red X with "Failed — try again" is clearer than making the spinner disappear
- Auto-save confirmation ("All changes saved") should appear for 2 seconds maximum and not reappear on every keystroke — debounce to show only after a pause in editing
- Connection status indicators should only become visible when the connection is degraded — showing a permanent "Online" indicator trains users to ignore it
- Always provide a recovery action in error states: "Retry", "Contact support", or "Go back" — a bare error message with no path forward causes abandonment

## AI-agent gotchas
- Agents implementing loading states often use `setTimeout` with hardcoded delays to simulate status — this will always be wrong in production; require real async state management
- Toast notification implementations by agents frequently omit the ARIA live region, making them invisible to screen readers; always require `role="alert"` for errors in the prompt
- Progress bar percentage calculations by agents may use naive linear interpolation that produces inaccurate estimates for variable-speed operations; require explicit "indeterminate vs. determinate" decision in the spec
- Agents auditing for status violations from code alone will miss runtime states (a button that becomes a spinner via JS); require dynamic testing with Playwright rather than static analysis alone
- Human checkpoint required before shipping timing decisions (how long to show success, when to auto-dismiss errors) — these are UX judgment calls that depend on content context and user attention patterns

## References
- Nielsen Norman Group: Visibility of System Status — https://www.nngroup.com/articles/visibility-system-status/
- Material Design: Progress Indicators — https://m3.material.io/components/progress-indicators/overview
- Apple HIG: Progress Indicators — https://developer.apple.com/design/human-interface-guidelines/progress-indicators
- WebAIM: ARIA Live Regions — https://webaim.org/techniques/aria/#live
- Radix UI Accessible Components: https://www.radix-ui.com
- Sentry Error Monitoring: https://docs.sentry.io
