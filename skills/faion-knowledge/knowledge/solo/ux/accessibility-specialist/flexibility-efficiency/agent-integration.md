# Agent Integration — Flexibility and Efficiency of Use

## When to use
- Designing or auditing productivity tools, developer tools, admin panels, or any app with repeat-use workflows
- Adding keyboard shortcut coverage to an existing web application
- Auditing whether an interface serves both novice onboarding and power-user acceleration
- Planning customization features (saved layouts, quick actions, pinned items) for SaaS products
- Evaluating CLI tools or APIs for efficiency affordances

## When NOT to use
- One-time-use flows (checkout, onboarding wizard, password reset) where shortcuts add no value
- Consumer apps with mostly casual, infrequent users — shortcut investment is wasted
- Early prototype stages before task flows are validated — optimizing efficiency before correctness is premature
- Accessibility-first flows where additional modalities (shortcuts) must be layered carefully to avoid conflicts with screen readers

## Where it fails / limitations
- Shortcut discoverability gap: adding shortcuts without surfacing them (menus, tooltip, shortcut panel) gives zero efficiency gain
- Platform conflicts: custom shortcuts frequently collide with OS-level, browser-level, or screen-reader shortcuts
- Customization overhead: exposing too many customization options creates its own cognitive load for novice users
- Bulk operations without confirmation introduce irreversible data loss risk
- "Multiple paths" can fragment user mental models if the paths behave subtly differently

## Agentic workflow
An agent receives a feature description or existing UI component list and produces a Flexibility Audit (audit template from `templates.md`): for each key action it checks whether a keyboard shortcut exists, whether it is discoverable, whether bulk operations are available, and whether the default suits a novice. A second pass checks for platform-standard shortcut conflicts. Output is a gap table with remediation priority. Agents can also generate the shortcut-reference panel content (Markdown table of action → shortcut) from a component inventory.

### Recommended subagents
- `faion-sdd-executor-agent` — drives structured flexibility audit from a task file
- General Claude subagent (sonnet) — generates keyboard shortcut tables and checks for platform conflicts given an action list

### Prompt pattern
```
You are a UX engineer auditing [product] for Flexibility and Efficiency of Use (Nielsen Heuristic #7).
Given the following list of user actions: [list], for each action:
1. Does a keyboard shortcut exist? If yes, is it listed in menus/tooltips?
2. Does it conflict with standard OS/browser shortcuts (Ctrl+W, Ctrl+T, Alt+F4, etc.)?
3. Is there a bulk version for operating on multiple items?
4. Does the feature have a "default that works for novices" path?
Output: a markdown table with columns: Action | Shortcut | Discoverable | Conflict Risk | Bulk Op | Novice Path.
```

```
Shortcut panel generator:
Given this list of actions and their keyboard shortcuts, generate a keyboard shortcut reference panel
in Markdown table format grouped by category (Navigation, Editing, File Operations, View).
Flag any shortcut that conflicts with common browser shortcuts.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `hotkeys-js` | Browser keyboard shortcut library with conflict detection | `npm i hotkeys-js` / https://github.com/jaywcjlove/hotkeys-js |
| `tinykeys` | Lightweight shortcut binding with sequence support | `npm i tinykeys` / https://github.com/jamiebuilds/tinykeys |
| `axe-core` | Checks keyboard accessibility (focus traps, tab order) | `npm i -g axe-core` / https://github.com/dequelabs/axe-core |
| `playwright` | Automated keyboard shortcut integration tests | `npm i -D @playwright/test` / https://playwright.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| FullStory | SaaS | No direct API | Reveals shortcut usage rates and click-vs-keyboard ratios per action |
| Heap Analytics | SaaS | No | Event tracking for shortcut usage adoption over time |
| LaunchDarkly | SaaS | Yes (REST API) | Feature-flag new shortcut sets for power-user beta groups |
| Intercom / Pendo | SaaS | Partial | In-app shortcut discovery banners; Pendo has REST API for flow management |

## Templates & scripts
See `templates.md` for the Flexibility Audit template.

Inline script — extract all keyboard shortcut bindings from a JS bundle (grep-based):
```bash
#!/usr/bin/env bash
# find-shortcuts.sh — list all keyboard shortcut strings in a project
# Usage: bash find-shortcuts.sh src/
TARGET=${1:-.}
echo "=== Keyboard shortcut candidates ==="
grep -rE "(Ctrl|Alt|Meta|Shift)\+[A-Za-z0-9]|key(down|up|press)|hotkey|shortcut|keybind" \
  --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
  "$TARGET" \
  | grep -v "node_modules" \
  | grep -v ".test." \
  | awk -F: '{printf "%-60s %s\n", $1":"$2, $3}' \
  | sort -u
```

## Best practices
- Ship shortcuts in menus first (visible), then tooltip (hover), then shortcut panel (? or Ctrl+/) — layered discoverability
- Follow platform conventions before inventing new ones: Ctrl+S = Save, Ctrl+Z = Undo are non-negotiable
- Test shortcuts against NVDA + Chrome and VoiceOver + Safari before shipping — screen readers capture many key combinations
- Implement customizable shortcuts only after default shortcuts are proven insufficient; premature customization multiplies QA surface
- Batch operations should always show a count confirmation ("Delete 14 items?") before executing destructive actions
- Expose a "reset to defaults" option alongside any customization to prevent users from getting permanently lost

## AI-agent gotchas
- Agents generating shortcut tables often produce conflicts with Ctrl+W (close tab), Ctrl+T (new tab), Ctrl+P (print) — always run a conflict check pass
- "Multiple paths" generated by agents may silently diverge in behavior (e.g., double-click edits inline, right-click opens modal) — flag these for human review
- Agents cannot observe actual shortcut adoption; efficiency gains claimed in an audit are hypotheses until measured
- Human checkpoint required for irreversible bulk operations: agent can design the UX pattern, but confirmation dialogs and undo mechanisms must be verified by a developer

## References
- https://www.nngroup.com/articles/flexibility-efficiency-heuristic/
- https://www.smashingmagazine.com/2021/09/keyboard-shortcuts-web-applications/
- https://developer.apple.com/design/human-interface-guidelines/keyboards
- https://m3.material.io/foundations/navigation
- About Face: The Essentials of Interaction Design (4th ed.) — Alan Cooper et al.
