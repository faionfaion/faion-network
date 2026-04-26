# Agent Integration — Business Storytelling

## When to use
- Drafting an executive summary, board update, or investor pitch that must lead with a recommendation, not background
- Rewriting a data-heavy report that lists facts without explaining implications
- Structuring a product launch announcement or case study for a technical or non-technical audience
- Preparing a presentation outline where the hook, problem, and call-to-action need to be clearly separated

## When NOT to use
- Purely operational documents (API docs, runbooks, incident postmortems) where narrative structure adds no value
- Legal or compliance documents where precision and completeness override persuasive flow
- Internal technical specs read by developers who need depth, not narrative arc — pyramid principle still applies but Pixar/hero frameworks do not

## Where it fails / limitations
- Pyramid Principle applied mechanically produces cold, robotic documents — it requires judgment about what the reader already knows
- SCQA generates artificial narrative tension when the situation is genuinely stable; forcing "complication" where none exists undermines credibility
- Data storytelling fails when the underlying metrics are contested — the story becomes a source of skepticism rather than persuasion
- Business storytelling frameworks are culturally specific; high-context cultures (Japan, Korea) resist the "answer first" structure of Pyramid Principle

## Agentic workflow
An agent producing a business narrative should receive the raw facts (data, situation, desired outcome) and apply the SCQA or Pyramid Principle framework in a single generation pass. For executive summaries, the agent leads with the recommendation, then generates supporting arguments that are MECE-checked. For case studies, the Pixar framework is applied: situation → routine → change → consequence chain → resolution. The agent should never pad a section with abstract language — every sentence must pass the "so what" test explicitly before output.

### Recommended subagents
- `faion-sdd-executor-agent` — can be directed to draft, then refine in a second pass where the agent checks each bullet for specificity and eliminates filler phrases

### Prompt pattern
```
Apply the Pyramid Principle to write an executive summary.
Recommendation (1 sentence): <recommendation>
Data/evidence available: <bullet list of facts>
Audience: <role, e.g. C-suite with 5 min to read>
Output format: Recommendation → 3 arguments → evidence under each argument.
MECE check: flag any overlapping arguments before finalizing.
```

```
Write a case study using the Pixar framework.
Situation: <who the customer is and their baseline>
Change event: <what we did / what was implemented>
Consequence chain: <what happened as a result, in sequence>
Resolution: <final outcome with specific metrics>
Add a 1-sentence customer quote at the end.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `marp` | Convert Markdown to presentation slides | `npm i -g @marp-team/marp-cli` / https://marp.app |
| `pandoc` | Convert structured Markdown to DOCX, PDF, or HTML | https://pandoc.org |
| `reveal.js` | HTML presentation framework usable with Markdown | https://revealjs.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Notion | SaaS | Partial | Agent can draft structured content; formatting review needs human for visual polish |
| Google Slides (via API) | SaaS | Partial | Slides can be created via API but slide design/layout still requires human review |
| Canva | SaaS | No | Visual tool with no useful API for structured narrative generation |
| Marp | OSS | Yes | Agent writes Markdown, Marp renders to slides; fully automatable for text-heavy decks |
| Beautiful.ai | SaaS | No | Presentation tool without programmable content API |

## Templates & scripts
See `templates.md` for Executive Summary, Case Study, and Presentation Outline templates.

SCQA template (inline):
```markdown
## Situation
[2-3 sentences: stable context the audience knows or can verify]

## Complication
[1-2 sentences: what changed or what tension exists]

## Question
[1 sentence: the question the audience is now asking]

## Answer
[1-2 sentences: your recommendation or finding]
```

## Best practices
- Write the recommendation first, then gather supporting evidence — do not write background until the conclusion is locked
- Every data point must be paired with an implication statement ("so what"): "uptime is 99.9%" alone is incomplete; "this means fewer than 9 hours of downtime per year, invisible to users" is complete
- Use concrete numbers over percentages when the base is unknown to the reader: "3 of 10 users" is clearer than "30%"
- Analogies must map to concepts the specific audience already understands — test the analogy domain before using it
- The hook (first 30 seconds) must create a question in the reader's mind, not just introduce the speaker or the topic

## AI-agent gotchas
- Agents default to abstract, hedge-heavy language ("leverage synergies", "drive value") — instruct explicitly to use concrete numbers and specific outcomes only
- MECE validation requires domain knowledge the agent may not have; flag arguments for human MECE review before using in board-level documents
- Agents applying Pyramid Principle sometimes bury the recommendation in the third paragraph — always verify the first sentence states the conclusion
- Human checkpoint required before sending any externally-facing narrative document; agents cannot verify factual accuracy of metrics or competitive claims
- For presentations, agents produce slide text that is too dense for actual slides — add a post-processing step: "reduce each slide to one key point, max 20 words"

## References
- https://hbr.org/2014/03/why-storytelling-is-so-powerful-in-the-digital-era
- https://www.khanacademy.org/computing/pixar (Pixar in a Box Storytelling)
- https://www.duarte.com/resources/ (Nancy Duarte presentation frameworks)
- Barbara Minto, "The Pyramid Principle" (McKinsey, 1987)
