# Agent Integration — Mobile UX Patterns

## When to use
- When reviewing a mobile design against platform conventions (iOS HIG, Material Design) before handoff
- When evaluating a mobile feature for touch target compliance, keyboard behavior, and orientation handling
- When documenting a new mobile pattern for a design system so it's reproducible across teams
- When auditing an existing mobile app for UX debt — map deviations from established patterns
- When making a case to engineering that a non-standard pattern needs custom implementation

## When NOT to use
- As a substitute for testing on real devices with real users — pattern compliance does not equal usability
- When designing for novel form factors (foldables, wearables, AR) where established patterns don't apply
- When the product's core differentiator is a custom interaction model (e.g., gesture-first apps) — force-fitting standard patterns reduces the differentiator

## Where it fails / limitations
- Pattern libraries describe what works on average, not what works for your specific users and tasks
- iOS and Android patterns diverge in non-obvious ways (bottom sheets, navigation drawers, swipe gestures) — a single implementation can feel wrong on one platform
- Mobile UX research data (e.g., "hamburger menu = 50% less discovery") is real but not universal; context matters
- Pattern documentation becomes outdated as OS design languages evolve (iOS 17 → 18 introduced significant navigation changes)
- Agents reviewing static screenshots cannot evaluate animation timing, haptic feedback, or gesture conflict — these require device testing

## Agentic workflow
An agent can conduct a mobile UX pattern audit by reviewing screenshots or design files against the mobile checklist (touch targets, thumb zones, keyboard types, loading states). The agent flags deviations, assigns severity, and suggests which standard pattern to apply. A human reviews flagged items, tests on device, and approves or overrides.

For pattern documentation, an agent can generate a new pattern spec from a brief description and existing examples, following the mobile pattern documentation template.

### Recommended subagents
- `faion-sdd-executor-agent` — run a mobile UX checklist audit on a set of design screenshots and produce a deviation report
- General Claude subagent with vision — analyze mobile screenshots for touch target size, text readability, and navigation pattern compliance

### Prompt pattern
```
You are a mobile UX expert reviewing the attached screenshots of [app / screen name] for iOS.
Apply the following checklist. For each item, mark: Pass / Fail / Cannot determine from screenshot.
If Fail, describe the specific violation and suggest the correct pattern.

Checklist:
- Touch targets: primary buttons >= 44pt
- Thumb reachability: primary CTA in easy zone (bottom third)
- Navigation: clear back/close action visible
- Text: body text >= 16px
- Forms: appropriate keyboard type specified
- Loading: skeleton screen or spinner present
- Errors: error message near the problematic field
```

```
Document this mobile pattern using the pattern spec template:
Pattern name: [name]
Description: [what it does]
Platform: [iOS / Android / Both]
Reference: [existing app using this pattern]

Template to fill: [paste mobile pattern documentation template]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lighthouse` | Automated mobile performance + accessibility audit | `npm i -g lighthouse` / developers.google.com/web/tools/lighthouse |
| `maestro` | Mobile UI testing and screenshot capture | `curl -Ls "https://get.maestro.mobile.dev" \| bash` / maestro.mobile.dev |
| `xcrun simctl` | iOS simulator screenshots via CLI | Xcode CLI tools / developer.apple.com |
| `adb screencap` | Android device/emulator screenshots | Android SDK / developer.android.com/tools/adb |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Mobbin | SaaS | No | Curated mobile UI screenshot library; browse-only |
| Pttrns | SaaS | No | Mobile design pattern library; browse-only |
| BrowserStack | SaaS | Yes (REST API + Automate) | Real device testing with screenshot capture via API |
| Maze | SaaS | Partial (API) | Mobile prototype testing; results via API |
| Figma | SaaS | Partial (REST API) | Design file access; agent can read frames and annotations |

## Templates & scripts
See `templates.md` for mobile design checklist template and mobile pattern documentation template with full iOS/Android spec fields.

Inline: touch target size validator for a list of element dimensions:
```python
MIN_TOUCH_PT = 44  # Apple HIG minimum
MIN_TOUCH_DP = 48  # Material Design minimum

def audit_touch_targets(elements: list[dict], platform: str = "ios") -> list[dict]:
    """
    elements: list of {name, width_pt, height_pt}
    Returns: list of elements that fail the minimum touch target requirement.
    """
    min_size = MIN_TOUCH_PT if platform == "ios" else MIN_TOUCH_DP
    failures = []
    for el in elements:
        w, h = el.get("width_pt", 0), el.get("height_pt", 0)
        if w < min_size or h < min_size:
            failures.append({**el, "min_required": min_size, "issue": f"{w}x{h}pt below {min_size}pt"})
    return failures
```

## Best practices
- Test on the lowest-tier device your users actually use — pattern compliance on a flagship phone does not guarantee usability on a 3-year-old mid-range device
- Validate thumb reachability with the Steven Hoober thumb zone model: easy zone covers bottom ~40% of screen one-handed; never place primary CTAs at top center
- Bottom tab bar is the default for 3-5 sections; switching to a hamburger menu is a deliberate tradeoff that reduces discoverability — quantify this before accepting it
- For forms, always test with the software keyboard open; it typically covers the bottom 40-50% of the viewport and can hide CTAs
- Skeleton screens perform better than spinners on perceived load time — use them for content lists and cards; spinners remain appropriate for brief operations under 1 second
- Pull-to-refresh is now a standard gesture on iOS and Android — implement it for any list view that can have new content

## AI-agent gotchas
- Agents cannot verify touch target sizes from screenshots without knowing the device scale factor and screen density; always provide dimensions in the prompt or design spec
- Animation timing (loading skeleton → content transition, swipe gesture physics) cannot be evaluated from static screenshots — mark these as "requires device testing"
- Platform-specific behaviors (iOS back swipe edge gesture, Android predictive back gesture) require platform-native testing, not screenshot analysis
- Do not trust agent pattern recommendations for accessibility — VoiceOver/TalkBack behavior requires manual testing with assistive technology enabled
- LLMs may recommend Android Material 2 patterns instead of Material 3 (or vice versa); specify the target design system version in the prompt

## References
- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Material Design 3 guidelines: https://m3.material.io/
- Hoober, S. "Touch Design for Mobile Interfaces." Rosenfeld Media, 2017.
- Wroblewski, L. "Mobile First." A Book Apart, 2011.
- Neil, T. "Mobile Design Pattern Gallery." O'Reilly, 2014.
- NNg mobile usability: https://www.nngroup.com/articles/mobile-usability/
