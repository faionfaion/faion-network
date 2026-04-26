# Agent Integration — Spatial Computing Overview

## When to use
- Quick exec briefing on AR/VR/MR landscape and platform tradeoffs.
- Choosing a target platform (Vision Pro vs. Quest vs. Android XR vs. HoloLens) for a new product.
- Roadmap planning: gauging market growth, install base, and platform momentum for a 12–24 month bet.
- Onboarding a new designer/PM into the spatial space.

## When NOT to use
- Already past platform-selection — switch to platform-specific skills (visionOS HIG, Quest design, etc).
- Detailed UX patterns work — use spatial-ui-patterns / spatial-interaction-patterns instead.
- Hardware purchasing decisions for a fleet — needs procurement + IT-management depth this overview doesn't cover.

## Where it fails / limitations
- Market data dates fast; the 87% growth and 40% adoption numbers must be re-validated quarterly.
- Platform comparisons gloss over SDK-level differences (OpenXR, ARKit, ARCore, Mixed Reality Toolkit).
- Says nothing about content distribution / store policies, which are decisive for consumer apps.
- "Spatial computing" as a term is contested — Apple uses it differently from Microsoft and Meta.

## Agentic workflow
Use a Claude subagent to keep the platform comparison fresh: every 2–3 months it re-pulls vendor docs, install base estimates, and developer-program changes, then emits a delta against the prior snapshot. Humans approve the new comparison table before it lands in the methodology doc.

### Recommended subagents
- `faion-ux-researcher-agent` — surveys design-system maturity per platform.
- General Claude subagent — refreshes the platform-landscape table from current vendor docs (WebSearch + WebFetch).
- `faion-pm-agent` — produces a platform-selection ADR using this overview as context.

### Prompt pattern
```
Refresh the platform table for AR/VR/MR. For each row output:
platform, OS, install base estimate (with citation+date), SDK,
content distribution, dominant use cases, 1 strength, 1 weakness.
Mark any cell whose source is older than 6 months as STALE.
```

```
Given product idea <X>, target audience <Y>, distribution
constraints <Z>, recommend ONE primary platform and ONE fallback.
Output as ADR: context, decision, alternatives, risks, review date.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `xcrun simctl` | visionOS simulator from CLI | Xcode |
| `adb` | Quest sideload + logs | Android SDK Platform-Tools |
| OpenXR Explorer | Inspect runtime capabilities | https://github.com/maluoi/openxr-explorer |
| `ar-cli` (ARCore) | Validate AR scenes | Google ARCore SDK |
| `realitykit-tool` | Convert USDZ for Vision Pro | Xcode 15+ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apple Vision Pro Dev Tools | SaaS | Limited | RealityKit + visionOS toolchain |
| Meta Horizon OS | SaaS | API | App lab, store, telemetry |
| Google ARCore / Android XR | SaaS | API | ARCore Cloud Anchors, Geospatial API |
| Microsoft Mesh / HoloLens | SaaS | API | Enterprise spatial collaboration |
| Magic Leap 2 SDK | SaaS | API | Industrial AR, narrow consumer reach |
| Niantic Lightship | SaaS | API | Outdoor AR, world-mapping |
| Snap AR Studio | SaaS | API | Reach via Snapchat install base |
| 8th Wall (Niantic) | SaaS | API | WebXR for browser-based AR |

## Templates & scripts
See `templates.md` if present; otherwise this overview is reference-only. Inline platform-selection table generator:

```python
#!/usr/bin/env python3
# platform-pick.py — score platforms against weighted criteria.
import yaml, sys
cfg = yaml.safe_load(open(sys.argv[1]))
for p, scores in cfg["platforms"].items():
    weighted = sum(scores[k] * cfg["weights"][k] for k in scores)
    print(f"{p}\t{weighted:.2f}")
```

## Best practices
- Refresh the landscape table at least quarterly — install base and SDK feature gaps shift fast.
- Always cite the publication date of every market figure; un-dated numbers are noise.
- Pick the platform from the audience's existing device, not the most exciting platform.
- Plan for cross-platform via OpenXR; avoid SDK lock-in unless one platform is dominant for your audience.
- Track 2 KPIs per platform pick: time-to-first-ship + cost-per-active-user-minute. Reassess yearly.
- Treat WebXR as the lowest-friction reach channel for marketing/demo, not for production training.

## AI-agent gotchas
- Vendor marketing pages exaggerate install base; require third-party citations (IDC, Counterpoint, Statista).
- Agents conflate "Apple Vision Pro" and "visionOS" — keep hardware vs. OS terminology strict.
- Platform comparisons drift to feature lists; force agents to reduce to the 1 strength / 1 weakness pair.
- "Mixed reality" terminology overlaps with "spatial computing"; require precise definitions per vendor.
- Don't let agents answer "which platform should I pick" without stated audience + budget + region.
- WebXR support is uneven — do not let an agent claim "supported" without testing on the target browser.

## References
- Apple visionOS HIG — https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos.
- Meta Quest Developer Center — https://developer.oculus.com/.
- Google ARCore + Android XR — https://developers.google.com/ar.
- Microsoft Mixed Reality Documentation — https://learn.microsoft.com/windows/mixed-reality/.
- Khronos OpenXR Specification — https://www.khronos.org/openxr/.
- IDC Spatial Computing Market Reports (annual).
- Counterpoint XR Tracker (quarterly install-base updates).
