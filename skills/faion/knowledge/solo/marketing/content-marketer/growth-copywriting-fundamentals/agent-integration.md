# Agent Integration — Copywriting Fundamentals

## When to use
- Writing or rewriting landing page copy (hero, benefits, CTA, objection handling)
- Drafting email subject lines, ad copy, or social media posts at scale
- Converting feature lists into benefit-oriented messaging
- Conducting VoC (Voice of Customer) analysis to extract language patterns for copy
- Training junior team members or briefing freelancers on copy standards

## When NOT to use
- Brand voice is undefined — copy frameworks produce generic output without a documented tone
- Copy is for highly regulated content (pharmaceuticals, legal, financial advice) — legal review is required before any agent produces messaging
- Target audience research is incomplete — copywriting formulas applied to wrong ICP produce polished but ineffective copy
- The goal is long-form editorial content — copywriting frameworks are for persuasion, not journalism or documentation

## Where it fails / limitations
- LLMs trained on generic copy data default to clichéd power words ("revolutionary," "game-changing") — explicit style instructions are required to suppress them
- VoC synthesis requires real customer data input; agents cannot gather primary research without tool integrations
- Readability scores (Hemingway, Flesch-Kincaid) require the text to be run through an external tool; agents self-assess readability poorly
- A/B test results are never available to the agent — it can propose variants but cannot determine the winner
- Benefit translation from features is only as good as the product knowledge provided in the prompt; hallucinated benefits are a real risk

## Agentic workflow
Claude agents are highly effective at generating copy variants, applying specific formulas (AIDA, PAS, BAB), converting feature lists to benefit copy, and writing 10+ headline variants for testing. Haiku is appropriate for mechanical tasks (formatting, applying a template, extracting phrases from reviews); Sonnet for full copy drafting with brand voice; Opus for VoC synthesis and messaging strategy. Agents should never produce final copy without human review — every deliverable is a draft. For production copy, the agent produces 3-5 variants; a human selects and edits one.

### Recommended subagents
- `faion-sdd-executor-agent` — for running a structured copy audit against an existing landing page
- General Claude Sonnet subagent — for benefit translation, headline variants, email copy drafts
- General Claude Haiku subagent — for mechanical tasks: applying templates, reformatting, extracting VoC phrases

### Prompt pattern
```
Convert the following feature list to benefit-oriented copy.
Product: [name]. ICP: [description]. Tone: [X].
Feature list:
- [feature 1]
- [feature 2]
For each feature, write: Feature → So what → Benefit (one sentence, active voice, ≤15 words).
```

```
Write 10 headline variants for a landing page.
Product: [X]. ICP: [Y]. Primary outcome: [Z].
Use these formulas: How-to, Number list, Question, Result-without-pain, Contrarian.
2 variants per formula.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `hemingway-cli` (unofficial) | Readability scoring in terminal | github.com/nicholasess/hemingwayapp-cli |
| `textstat` (Python) | Flesch-Kincaid, Gunning Fog, SMOG scores | `pip install textstat` |
| `coschedule-headline` | CoSchedule headline score via API (unofficial wrappers exist) | coschedule.com/headline-analyzer |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Hemingway Editor | SaaS/desktop | No API | Manual readability check; use before final review |
| CoSchedule Headline Analyzer | SaaS | No official API | Headline scoring; manual workflow |
| Copy.ai | SaaS | Yes — API | Bulk copy variant generation; lower quality than Claude |
| Jasper | SaaS | Yes — API | Template library; mostly redundant if using Claude directly |
| Grammarly | SaaS | Partial — browser ext | Grammar and tone; no batch API for copy review |
| Readable | SaaS | Partial — API | Readability scoring API; integrable in CI pipelines |
| Wynter | SaaS | No | Message testing with real ICP panel; human-validated copy research |

## Templates & scripts
See `templates.md` for landing page copy structure and email copy structure.

Minimal Python readability check using textstat:
```python
import textstat

copy = """
Stop guessing which marketing works.
Get clear answers in 60 seconds.
No spreadsheets. No analyst needed.
"""

print(f"Flesch reading ease: {textstat.flesch_reading_ease(copy):.1f}  (target: 60-70)")
print(f"Gunning Fog index: {textstat.gunning_fog(copy):.1f}  (target: <10)")
print(f"Avg sentence length: {textstat.avg_sentence_length(copy):.1f} words  (target: <20)")
```

## Best practices
- Start every copy session with VoC data — paste real customer phrases into the prompt so the agent mirrors authentic language
- Specify reading level explicitly in the prompt ("6th-grade reading level, active voice, no jargon") — agents default to formal prose
- Headlines: always request 10 variants minimum, then score by specificity and benefit clarity — never use the first suggestion
- The P.S. line in emails disproportionately affects conversion; treat it as a second CTA and draft it with as much care as the main CTA
- Objection handling copy should map to specific customer objections documented in support tickets or sales calls — agent-hallucinated objections are generic
- Review all copy for passive voice ratio and "we/our" vs "you/your" ratio; target 2:1 in favor of "you"
- For landing pages, write the CTA button text before the body copy — it forces clarity about what action you're driving

## AI-agent gotchas
- Agents reproduce copywriting clichés ("unlock your potential," "take your business to the next level") — explicitly ban these in the prompt system message
- Benefit copy from agents often retains the feature framing in disguise ("our AI helps you...") — ask specifically for customer-outcome-first sentences
- VoC phrase extraction from reviews requires the agent to receive the raw review text as input; agents cannot browse G2 or Trustpilot autonomously
- Copy produced for ads must be checked against platform policies (Meta, Google) before use — agents are unaware of current ad policy restrictions
- Length constraints must be specified per context: email subject (≤50 chars), meta description (≤160 chars), ad headline (≤30 chars) — agents ignore these without explicit instruction

## References
- https://copyblogger.com/copywriting-101/
- https://copyhackers.com/blog/
- https://cxl.com/blog/copywriting/
- https://blog.hubspot.com/marketing/copywriting
- https://www.awai.com/copywriting/
