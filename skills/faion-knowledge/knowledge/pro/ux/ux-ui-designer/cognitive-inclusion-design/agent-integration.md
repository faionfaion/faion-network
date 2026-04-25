# Agent Integration — Cognitive Inclusion Design

## When to use
- Designing for users with ADHD, autism, dyslexia, dyscalculia, anxiety, low-literacy, or aging cognition.
- Adding plain-language, focus mode, reduced-motion, customizable text/layout, time-extension features.
- Reviewing flows where cognitive load is the dominant friction (forms, taxes, healthcare, legal, government).
- Aligning with WCAG 3.0 working draft cognitive guidelines and W3C COGA Task Force gap analysis.

## When NOT to use
- Pure visual / motor accessibility — handle via WCAG 2.2 AA + assistive-tech testing first.
- Marketing surfaces with single-action goals (CTA + form) — usually does not need cognitive customization.
- Highly regulated technical interfaces (industrial control) where literal labeling is already required.
- As a substitute for plain-language editing — cognitive design assumes content is already plain.

## Where it fails / limitations
- "Dyslexia-friendly fonts" (e.g., OpenDyslexic) have weak empirical support — provide as option, not default.
- Customization (font, color, spacing) only helps if discoverable and persistent across sessions.
- Plain-language and "literal language" can clash with branded voice; product needs a tone-of-voice exception list.
- Reducing motion globally can break critical animations (focus indicators, progress feedback).
- Time-limit removal can collide with security session timeouts — needs UX + security joint review.
- Most automated tools cannot detect cognitive issues; requires structured manual review + user research.

## Agentic workflow
Use a subagent to run a Cognitive Accessibility Checklist (W3C COGA + Hassell Inclusion + Microsoft Inclusive Design) against each screen using DOM + content snapshots. A second agent rewrites flagged copy at a target reading level (Hemingway grade ≤6, Flesch-Kincaid ≥70) and produces alternative shorter versions. A third proposes settings (focus mode, font, motion) and persistence design. Recruitment of cognitive-disabled users for validation is a human responsibility.

### Recommended subagents
- `faion-usability-agent` — runs cognitive checklist, rewrites copy, proposes setting matrix.
- `faion-ux-researcher-agent` — recruits and runs sessions with cognitively diverse users.
- `faion-sdd-executor-agent` — implements settings UI, persists preferences, applies font/spacing tokens.

### Prompt pattern
```
For page <url>, output: (1) Flesch-Kincaid grade level of body
copy, (2) sentences over 20 words, (3) idioms, metaphors, irony,
sarcasm — list each with literal rewrite, (4) jargon — list each
with definition. Output as a fix-list, not narrative.
```

```
Propose a "Focus Mode" for this page: items to hide (decoration,
secondary nav, animations), items to keep (primary task, save
button, exit). Provide CSS class strategy that does not break
keyboard order or screen-reader traversal.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `textlint` + `textlint-rule-write-good` | Plain-language linting in CI | `npm i -D textlint textlint-rule-write-good` |
| `proselint` | Style + clarity linter | `pip install proselint` |
| `readability` (`pip install readability`) | Flesch-Kincaid, SMOG, Coleman-Liau | github.com/andreasvc/readability |
| `vale` | Configurable prose linter (plain-language style guides) | vale.sh |
| `axe-core` `cognitive` rule extension | Limited cognitive checks (focus, blinking, time) | deque.com/axe |
| `motion-prefers-checker` (custom) | Lints CSS for `prefers-reduced-motion` coverage | — |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Hemingway Editor | SaaS | Partial — no API; emulate with `readability` | Useful as design reference. |
| Acrolinx | SaaS | Yes — REST API | Enterprise plain-language enforcement. |
| Readable.com | SaaS | Yes — REST | Bulk readability scoring. |
| Userway / accessiBe | SaaS overlay | No | Avoid; not a substitute for fixes. |
| Recite Me | SaaS | Partial — embed widget | User-side customization toolbar. |
| Texthelp Read&Write | SaaS | Yes — extension | Validate compatibility, not a fix. |
| Microsoft Immersive Reader | SaaS | Yes — embed API | Strong reference for reading customization patterns. |

## Templates & scripts
See `templates.md` and `examples.md`. Inline minimal user-preference token plan (CSS):

```css
:root {
  --reading-font: system-ui, sans-serif;
  --reading-line-height: 1.5;
  --reading-letter-spacing: 0;
  --motion-duration: 0.2s;
}
[data-pref-font="dyslexia-option"] { --reading-font: "OpenDyslexic", sans-serif; }
[data-pref-line-height="loose"]    { --reading-line-height: 1.8; }
[data-pref-letter-spacing="wide"]  { --reading-letter-spacing: 0.05em; }
@media (prefers-reduced-motion: reduce) {
  :root { --motion-duration: 0s; }
}
body {
  font-family: var(--reading-font);
  line-height: var(--reading-line-height);
  letter-spacing: var(--reading-letter-spacing);
}
* { animation-duration: var(--motion-duration) !important; transition-duration: var(--motion-duration) !important; }
```

## Best practices
- Offer an explicit "Reading preferences" panel (font, size, line-height, contrast, motion). Persist to user account.
- Default to system settings: `prefers-reduced-motion`, `prefers-color-scheme`, `forced-colors`, `prefers-contrast`.
- Show progress for any task >2 steps — both numeric ("3 of 5") and visual.
- Auto-save every form field on blur; never lose user input on session expiry.
- Use literal language for instructions; reserve metaphor for marketing copy with literal alt.
- For time limits, offer extend / disable. If security forces a limit, warn at 80% with clear extend control.
- Avoid all-caps for emphasis (some screen readers spell letter-by-letter and dyslexic readers struggle).
- Provide a non-blaming error message format: "Phone needs 10 digits — you entered 9."

## AI-agent gotchas
- Agents add jargon to "sound professional" — enforce a banned-word list (utilize → use, leverage → use, etc.).
- LLMs default to long sentences; require max 20 words/sentence and ≤2 ideas per sentence.
- Agents apply OpenDyslexic globally — keep it opt-in; default font choice is contested.
- "Reduce motion" agent adds `* { animation: none }` blanket rule, breaking focus indicators — scope carefully.
- Time-limit removal vs. security session: agent must surface this as a trade-off, not silently extend.
- Agents recommend overlay widgets — refuse; document fix at source.
- Cognitive needs are heterogeneous; avoid grouping users by diagnosis. Design for needs (focus, time, structure), not labels.

## References
- W3C Cognitive and Learning Disabilities (COGA) Task Force — w3.org/WAI/cognitive/
- W3C "Making Content Usable for People with Cognitive and Learning Disabilities" — w3.org/TR/coga-usable/
- WCAG 3.0 Working Draft — w3.org/TR/wcag-3.0/
- Microsoft Inclusive Design Toolkit — inclusive.microsoft.design
- "Cognitive Accessibility Roadmap and Gap Analysis" (W3C) — w3.org/TR/coga-gap-analysis/
- Hassell Inclusion, "Cognitive Accessibility Patterns" — hassellinclusion.com
- Plain Language Action Network (PLAIN) — plainlanguage.gov
- Centre for Inclusive Design, "The Benefit of Designing for Everyone" — centreforinclusivedesign.org.au
