# Agent Integration — Cognitive Inclusion Design

## When to use
- Designing or auditing forms, dashboards, learning tools, gov services, or healthcare apps used by non-expert public.
- Working in EU (EAA) where WCAG 2.2 AA + cognitive guidance now expected.
- Reducing form abandonment / support load on complex multi-step flows.
- Accommodating ADHD/autism/dyslexia/anxiety/learning-disability users (≈15-20% of population).
- Auditing copy, error messages, microcopy for plain-language / non-blaming tone.

## When NOT to use
- Pure visual/motor a11y audit — use `a11y-testing` + `wcag-22-compliance`.
- Performance-driven, expert-only tooling (CLI dashboards for SREs) — minimalism trumps scaffolding.
- Marketing landing page where brand voice is intentionally playful (idioms OK in moderation).
- Game design where challenge is the point — apply selectively (settings menu, onboarding only).

## Where it fails / limitations
- WCAG 2.1 covered cognitive only thinly; WCAG 2.2 added some (e.g., 3.2.6 Consistent Help, 3.3.7 Redundant Entry) but cognitive remains under-specified.
- "Plain language" is subjective — Flesch/Flesch-Kincaid scores miss domain jargon.
- Auto-save can leak draft data to other users on shared devices — check session model.
- "OpenDyslexic" / "Comic Sans" claims are weakly evidenced; some studies show no benefit, some show preference. Offer choice rather than imposing.
- Sensory-friendly palettes can clash with brand identity; needs design-system buy-in.

## Agentic workflow
Agents are strong at: copy rewrites (plain language, non-blaming tone), error-message audits, form-flow analysis (counting steps, fields, time-on-task estimates), checklist conformance, generating predictable interaction patterns. Weak at: real cognitive testing (need humans with relevant disabilities), judging "sensory-friendly" palettes, validating reduced-motion alternatives feel right. Use agent for first pass, then schedule moderated user testing with neurodiverse panel (Fable, UserTesting + recruit).

### Recommended subagents
- `faion-sdd-executor-agent` — track each cognitive criterion as a task with completion evidence (screenshot, copy snippet).
- Plain-language rewriter subagent — rewrite UI copy to ≤Grade 8, non-blaming, no idioms, check Flesch ≥ 60.
- Form-flow analyzer subagent — given a form spec, count fields, identify time pressure, suggest chunking + auto-save.
- See also: `accessibility-first-design`, `vui-accessibility-inclusivity`.

### Prompt pattern
```
Rewrite this error message for cognitive inclusion:
- Plain language, Flesch reading ease ≥ 60, no jargon, no idioms.
- Non-blaming tone (no "you failed", "invalid").
- Suggest concrete next action.
- Keep under 25 words.
ORIGINAL: "{{copy}}"
```

```
Audit this multi-step form for cognitive load. Output:
1) Step count, fields per step, total fields.
2) Time-pressure elements (timeouts, countdowns).
3) Auto-save and resume gaps.
4) Recommendations against the cognitive-inclusion checklist.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `textstat` | Flesch, Gunning Fog, Dale-Chall readability | `pip install textstat` |
| `vale` (Microsoft Writing Style) | Linter for plain-language rules | https://vale.sh; styles: Microsoft, write-good |
| `alex` | Catches insensitive/blame language | `npm i -g alex` |
| `write-good` | English prose linter | `npm i -g write-good` |
| `hemingway-cli` | Readability + complex sentence flagging | https://github.com/btford/write-good |
| `prefers-reduced-motion` test | Playwright `page.emulateMedia({reducedMotion:'reduce'})` | https://playwright.dev |
| `eslint-plugin-jsx-a11y` | Catches some cognitive-related issues (autoplay, focus) | `npm i -D eslint-plugin-jsx-a11y` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Immersive Reader | SaaS | API | Drop-in for read-aloud + dyslexia formatting. |
| Speechify / NaturalReader | SaaS | API | Text-to-speech voices; embed for cognitive aid. |
| Stark | SaaS / Figma plugin | plugin | Has cognitive-load checks (focus, motion, contrast). |
| Hemingway / ProWritingAid | SaaS | API (paid) | Readability scoring inline. |
| GrackleDocs / Allyant | SaaS | manual | Document remediation (PDF/Word) with plain-language pass. |
| Fable | SaaS | human-in-loop | Recruits neurodiverse testers — irreplaceable for usability. |
| UserTesting + recruiter screeners | SaaS | semi-automated | Filter for ADHD, dyslexia, autism. |
| Kingsfund / GDS Plain English | gov resource | n/a | Standards reference. |

## Templates & scripts
See README "Implementation Checklist". Inline copy-readability gate for CI:

```bash
#!/usr/bin/env python3
# readability_gate.py - fail CI if any UI string drops below Flesch 60.
import json, sys, textstat, pathlib
THRESHOLD = 60.0
errors = []
for path in pathlib.Path("locales").glob("**/en.json"):
    data = json.loads(path.read_text())
    def walk(d, key=""):
        if isinstance(d, dict):
            for k, v in d.items(): walk(v, f"{key}.{k}" if key else k)
        elif isinstance(d, str) and len(d.split()) >= 6:
            score = textstat.flesch_reading_ease(d)
            if score < THRESHOLD:
                errors.append(f"{path}:{key} score={score:.1f} < {THRESHOLD}: {d[:60]!r}")
    walk(data)
for e in errors: print(e)
sys.exit(1 if errors else 0)
```

## Best practices
- Default to `prefers-reduced-motion: reduce` for any non-essential animation; only animate on explicit user opt-in.
- Auto-save every 15-30 s with explicit "All changes saved" indicator; never rely on browser memory.
- Inline validation > submit-time validation for cognitive load (immediate feedback reduces anxiety).
- Allow "save and continue later" with email magic link on every form > 3 steps.
- Provide a "simple mode" toggle that hides non-essential UI for users who get overwhelmed.
- Pair iconography with text labels — icons alone are ambiguous for autism / aphasia users.
- Use predictable layouts (same nav location, same primary action position) across pages.
- Test copy with `vale` + `alex` in pre-commit; CI gate with `textstat` Flesch ≥ 60.

## AI-agent gotchas
- LLMs default to verbose, hedging copy ("might want to consider", "perhaps could") — explicit instruction needed for direct, plain language.
- Agent-rewritten error messages may strip technical detail needed for support — keep error CODE for support, soften the user-facing message only.
- "Reduced motion" detection in CSS `@media` doesn't catch JS-driven animations (GSAP, Lottie) — agent must check JS too.
- Agents tend to over-add ARIA live regions for "feedback" — too many announcements overwhelm screen-reader users.
- Auto-save naively serialized to localStorage may leak data on shared devices — agent must scope to authenticated session.
- Don't let the agent "translate" copy across locales for cognitive load — Flesch only works for English; per-language metrics needed (LIX for Swedish, Kandel-Moles for Spanish, etc.).
- Empathy-claims drift: an agent may add "We're so sorry!" — over-apologetic copy is itself anxiety-inducing for many users; aim for calm-neutral.
- "Dyslexia-friendly" font swap should be opt-in, not forced — typographic preferences vary.

## References
- W3C Cognitive Accessibility Task Force — https://www.w3.org/WAI/cognitive/
- Making Content Usable for People with Cognitive and Learning Disabilities — https://www.w3.org/TR/coga-usable/
- WebAIM cognitive disabilities — https://webaim.org/articles/cognitive/
- BDA dyslexia style guide — https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-style-guide
- GOV.UK content design guidelines — https://www.gov.uk/guidance/content-design
- Microsoft inclusive design toolkit — https://www.microsoft.com/design/inclusive/
- Plain Language Action and Information Network — https://www.plainlanguage.gov
