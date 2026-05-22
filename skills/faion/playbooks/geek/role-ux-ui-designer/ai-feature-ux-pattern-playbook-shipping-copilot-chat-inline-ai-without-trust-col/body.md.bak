# AI-feature UX pattern playbook: copilot / chat / inline-AI without trust collapse

## Context

Designer ships an AI feature (chat, copilot side-panel, inline autocomplete, or agentic action). Includes pattern selection, trust + disclosure framing, human-in-the-loop UI, streaming response UX, a11y, and trust metrics. Done when the feature ships with a defined trust dashboard and override paths.

## Outcome

AI feature ask -> vetted UX pattern + trust signals + override + measurable metrics. Designer is asked to add an AI feature; ends with a vetted UX pattern + a11y + trust/disclosure framing + override path + measurable trust metrics.

## Steps

1. **Pick pattern.** Match pattern to job. Tasks: Map job (read / draft / decide / act) to pattern; Document trade-offs per pattern; Get sponsor sign-off on pattern choice.
2. **Trust + disclosure.** Users see what is AI and what is not. Tasks: Add provenance + confidence cues; Disclose data sources + limitations; Surface 'why' explanations on demand.
3. **Human-in-the-loop.** User stays in control. Tasks: Add accept / reject / edit affordances; Add undo + audit log on agentic actions; Document confirmation patterns for irreversible acts.
4. **Streaming UX.** Latency does not break trust. Tasks: Stream tokens vs full-block responses; Add interruptible generation; Surface partial results gracefully.
5. **A11y for AI.** AT users get the same experience. Tasks: Announce streamed updates politely; Make controls keyboard-reachable; Test with NVDA + VoiceOver.
6. **Validate with synthetic + real.** Find failure modes before customers do. Tasks: Run synthetic-user scenarios across edge cases; Run real-user sessions on flagship flows; Adjust patterns to address failure modes.
7. **Trust metrics dashboard.** Measure trust, not just usage. Tasks: Define trust signals (accept rate, undo rate, sentiment); Wire a dashboard with baseline; Schedule monthly review.

## Decision points

- **After Pick pattern:** Advance only when pattern is signed off.
- **After Trust + disclosure:** Advance only when disclosure is visible without effort.
- **After Human-in-the-loop:** Advance only when override path is always available.
- **After Streaming UX:** Advance only when interruption + partials work.
- **After A11y for AI:** Advance only after AT testing passes.
- **After Validate with synthetic + real:** Advance only when criticals are addressed.
- **After Trust metrics dashboard:** Done when dashboard has baseline + review cadence.

## References

- `faion/knowledge/geek/ux/user-researcher/synthetic-users`
- `faion/knowledge/geek/ux/ux-ui-designer/ai-accessibility-automation-2026`
- `faion/knowledge/geek/ux/ux-ui-designer/ai-design-assistant-patterns`
- `faion/knowledge/geek/ux/ux-ui-designer/generative-ui-design`
- Related: `zero-to-one-product-design-brief-to-dev-handoff-8-weeks`, `design-system-as-code-lifecycle-tokens-storybook-figma-library-pr-governance`
