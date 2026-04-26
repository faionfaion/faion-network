# Agent Integration — Business Storytelling

## When to use
- Drafting executive summaries, project proposals, and strategy presentations using Pyramid Principle structure
- Converting data-heavy reports into SCQA narratives (Situation → Complication → Question → Answer)
- Generating hook variants for presentations (surprising stat, question, bold statement, story, contradiction)
- Producing "So What" annotations for data points: raw metric → implication → audience consequence
- Structuring case studies and success stories using the Pixar framework
- Converting abstract benefit language ("improved efficiency") into concrete, quantified statements

## When NOT to use
- Replacing human delivery — storytelling impact depends on speaker presence, timing, and authenticity; a script is a scaffold, not a performance
- When the data does not exist — agents will invent plausible-sounding numbers to fill the "Concrete vs Abstract" pattern; all quantification must come from real inputs
- Brand storytelling for external audiences without human review — LLM-generated narrative often lacks the distinctive voice that differentiates a brand
- When the "Complication" in SCQA is unclear — forcing narrative tension around a non-problem produces manipulative-feeling content

## Where it fails / limitations
- Pyramid Principle requires MECE (Mutually Exclusive, Collectively Exhaustive) argument structure — agents frequently produce overlapping arguments or miss a category
- Pixar framework applied to business contexts can feel forced ("once upon a time, our team...") without careful tone calibration
- The "Concrete vs Abstract" conversion requires real metrics; agents will generate plausible but false benchmarks if not constrained
- Hook generation tends toward cliche — "Did you know that X% of [category]?" is LLM default; force specificity via prompt constraints
- Long presentations (10+ slides) lose structural coherence because agents optimize locally per slide rather than globally

## Agentic workflow
An agent receives: topic, audience type, key argument, 2-3 supporting data points, desired output format (exec summary / presentation outline / case study). It produces a SCQA narrative scaffold first, then expands into the chosen format using Pyramid Principle structure. A "So What" annotation pass labels each data point with its implication and audience consequence. The hook is generated in 3 variants (stat / question / story) for human selection.

### Recommended subagents
- General Claude Opus call — full narrative drafting; Pyramid Principle structure + SCQA requires reasoning about argument hierarchy
- General Claude Sonnet call — "So What" annotation pass and case study templating; structured conversion task

### Prompt pattern
SCQA + Pyramid Principle:
```
Draft a business narrative for: <TOPIC>.
Audience: <AUDIENCE_TYPE>.
Key recommendation: <ANSWER_FIRST>.
Supporting arguments (3): <ARGUMENT_1>, <ARGUMENT_2>, <ARGUMENT_3>.
Data available: <METRICS>.
Structure: SCQA opening, then Pyramid Principle body (answer → 3 arguments → evidence).
Do not invent metrics. Mark gaps as [DATA NEEDED].
```

"So What" annotation:
```
For each data point below, add two levels of "So What":
Level 1: What does this number mean? (implication)
Level 2: Why does this matter to <AUDIENCE>? (consequence)
Data points: <LIST>
```

Hook generation:
```
Generate 3 opening hooks for a presentation on: <TOPIC>.
Audience: <AUDIENCE>.
Variant 1: Surprising statistic (must use real data from: <SOURCE_DATA>)
Variant 2: Question (creates genuine tension)
Variant 3: 2-sentence story (specific, not generic)
No clichés. No "In today's world..."
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `marp` | Convert markdown narrative to presentation deck | `npm install -g @marp-team/marp-cli` |
| `pandoc` | Export agent-generated docs to PDF / DOCX / PPTX | https://pandoc.org |
| `reveal-md` | Markdown-to-HTML slides for web presentations | `npm install -g reveal-md` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Slides | SaaS | Yes — Google Slides API | Programmatic slide creation from agent markdown output |
| Notion | SaaS | Yes — REST API | Store narrative drafts; version-track story variants |
| Beautiful.ai | SaaS | No public API | Human-paste; good for design-quality output |
| Gamma.app | SaaS | No public API | AI-native deck tool; import markdown |
| Tome | SaaS | No public API | AI storytelling deck; human-in-the-loop required |

## Templates & scripts
See `templates.md` for Executive Summary, Case Study, and Presentation Outline templates.

MECE checker (simple overlap detector for Pyramid Principle arguments):
```python
def check_mece_overlap(arguments: list[str], threshold: float = 0.6) -> list[tuple[str, str]]:
    """
    Flag pairs of arguments that share more than threshold word overlap.
    High overlap = likely not mutually exclusive.
    """
    from itertools import combinations
    def word_overlap(a: str, b: str) -> float:
        wa, wb = set(a.lower().split()), set(b.lower().split())
        return len(wa & wb) / len(wa | wb) if wa | wb else 0.0
    flagged = []
    for a, b in combinations(arguments, 2):
        if word_overlap(a, b) >= threshold:
            flagged.append((a, b))
    return flagged
```

Pixar business narrative template:
```
Once upon a time, [CURRENT_STATE with specific numbers].
Every day, [ROUTINE_PAIN or ROUTINE_PROCESS].
One day, [CHANGE_OR_DECISION].
Because of that, [FIRST_CONSEQUENCE with metric].
Because of that, [SECOND_CONSEQUENCE with metric].
Until finally, [RESOLUTION with outcome].
```

## Best practices
- Write the SCQA Complication before the Answer — if you cannot articulate a genuine tension, the story will not hold; use this as a validity check for the presentation's premise.
- For executive audiences: apply the "So What" test to every data point before finalizing. Executives interpret implications; they do not derive them from raw numbers.
- The "Rule of Three" (three arguments, three supporting facts, three benefits) is not arbitrary — it is the maximum working-memory load for a spoken presentation; enforce it even when more data is available.
- Before/After structure with numbers is the highest-impact single technique in data storytelling; prioritize it over abstract benefit language in every output.
- Use analogies for technical concepts presented to non-technical audiences — the "restaurant kitchen = microservices" example in the README is effective; agents can generate domain-appropriate analogies when given the target audience context.

## AI-agent gotchas
- Agents will produce Pyramid Principle structures where the three arguments overlap significantly (not MECE); run the MECE checker or explicitly prompt "ensure arguments do not overlap."
- The "Burying the Lead" anti-pattern is the LLM default in long-form writing — agents build up to the conclusion; Pyramid Principle requires inverting this. Explicitly state "lead with the recommendation" in every prompt.
- Hook generation defaults to "Did you know?" or "In today's fast-paced world..." which are both forbidden by professional communication standards; add a negative example list to the hook prompt.
- Pixar framework applied to business without tone calibration produces narrative that feels inappropriately casual in formal settings; specify formality level in the prompt.
- Human checkpoint required: the "So What" annotation must be verified against actual audience knowledge level — an agent calibrated to a general audience will produce over-explained implications for domain experts or under-explained ones for senior executives.

## References
- Minto, B. (1987). The Pyramid Principle. FT Prentice Hall.
- Duarte, N. (2010). Resonate. Wiley.
- Harvard Business Review — Why Storytelling Is So Powerful: https://hbr.org/2014/03/why-storytelling-is-so-powerful-in-the-digital-era
- Pixar Story Rules: https://www.pixar.com/careers
- Marp CLI docs: https://marp.app
