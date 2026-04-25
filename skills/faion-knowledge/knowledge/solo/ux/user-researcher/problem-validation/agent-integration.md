# Agent Integration — Problem Validation

## When to use
- Before committing engineering resources to build a solution
- After pain point research has identified candidate problems — need to assess which are worth solving
- Quarterly review of assumed problems in an existing product backlog
- Pre-pivot: assessing whether a proposed direction has enough validated demand
- When a founder or PM has a strong hypothesis and needs structured pushback

## When NOT to use
- When real users have already been paying for the solution — you have validation, move to retention
- As a substitute for usability testing (problem validation answers "does this problem exist?", not "does this UI work?")
- When n < 5 data points; a single frustrated user is anecdote, not signal
- When all evidence is compliments and hypotheticals — that is negative validation, stop and pivot

## Where it fails / limitations
- Validation hierarchy (paid > committed > engaged > stated) requires time and user access that agents cannot provide
- LLMs cannot interview real users; they can only help prepare for interviews and analyze transcripts afterward
- Commitment signals (LOI, pre-order) require human negotiation and trust-building
- Agents will not catch when a user says what they think the researcher wants to hear (social desirability bias)
- Search volume proxies (Google Trends, Ahrefs) can mislead — high search volume does not equal willingness to pay

## Agentic workflow
An agent is useful for designing the validation protocol (which signals to collect, from which sources, and how to interpret them) and for synthesizing collected evidence against the validation hierarchy. The agent cannot collect evidence itself without tool access, but given a brief summary of collected interviews, forum posts, and behavioral signals, it can score evidence quality and recommend proceed/pivot/kill. A lightweight human-in-loop checkpoint is required after every evidence collection phase.

### Recommended subagents
- `faion-sdd-executor-agent` — run validation tasks within a structured SDD plan
- Any general Claude subagent — draft validation protocol, score evidence, generate problem statement variants

### Prompt pattern
```
You are a lean startup advisor. Given the following problem hypothesis and evidence, evaluate:
1. Where does each piece of evidence sit in the validation hierarchy (paid/committed/engaged/stated/anecdote)?
2. What is missing from the evidence set?
3. Recommend: PROCEED, PIVOT (with direction), or KILL.

Hypothesis: <paste hypothesis>
Evidence collected: <paste evidence>
```

```
Using the Mom Test framework, rewrite these questions to avoid leading or hypothetical framing:
Original questions: <paste questions>
Rules: ask about past behavior, not future intent; never pitch the idea; ask about their life not your solution.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Ahrefs / Semrush CLI | Search volume proxy for problem frequency | ahrefs.com (API); semrush.com (API) |
| Google Trends (pytrends) | Free search interest data | `pip install pytrends` / github.com/GeneralMills/pytrends |
| SurveyMonkey API | Quantitative survey delivery | developer.surveymonkey.com |
| Typeform API | Survey + interview scheduling | developer.typeform.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Typeform | SaaS | Yes (REST API) | Create validation surveys, retrieve responses programmatically |
| SurveyMonkey | SaaS | Yes (REST API) | Design + send surveys; read aggregate results |
| Airtable | SaaS | Yes (REST API) | Track evidence rows: type, source, signal strength |
| Notion | SaaS | Yes (API) | Store problem hypothesis docs; update status |
| Google Trends (pytrends) | OSS wrapper | Yes | Query interest-over-time for problem keywords |
| Gong.io | SaaS | Partial (read API) | Surface call transcripts where problem was mentioned |

## Templates & scripts
See `templates.md` for Problem Validation Report template.

Inline script — evidence scorer:
```python
# evidence_scorer.py — score validation evidence by hierarchy level
HIERARCHY = {
    "paid": 5,
    "committed": 4,  # LOI, signed up, pre-order
    "engaged": 3,    # used prototype, returned 3x
    "stated": 2,     # expressed interest in interview
    "anecdote": 1,   # single mention, no follow-up
}

evidence = [
    {"type": "stated", "source": "Interview #1", "note": "Would pay $50/mo"},
    {"type": "engaged", "source": "Landing page", "note": "47% email signup rate"},
    {"type": "stated", "source": "Reddit", "note": "Upvoted complaint thread"},
    {"type": "anecdote", "source": "Friend", "note": 'Said "sounds interesting"'},
]

total = sum(HIERARCHY[e["type"]] for e in evidence)
max_possible = len(evidence) * 5
print(f"Validation score: {total}/{max_possible} ({100*total//max_possible}%)")
for e in sorted(evidence, key=lambda x: -HIERARCHY[x["type"]]):
    print(f"  [{HIERARCHY[e['type']]}] {e['type']:10} | {e['source']} — {e['note']}")
```

## Best practices
- Define your kill threshold before collecting evidence ("if fewer than 3/10 interviewees confirm the pain, we stop")
- Distinguish between problem frequency (how often) and problem intensity (how much it hurts) — both must exceed threshold
- Use the validation hierarchy explicitly: label each piece of evidence with its tier before synthesizing
- A competitor existing is weak evidence (someone thinks the problem is real); a competitor churning customers is strong evidence (the problem persists unsolved)
- Pre-order is the gold standard for solopreneurs — even 10 real pre-orders at $1 outweigh 100 "I would use this" statements
- Revisit validation when target segment or pricing changes significantly

## AI-agent gotchas
- Do not ask an agent to judge whether a problem is "real" from a brief summary — it will sound convincing regardless
- LLMs exhibit availability bias toward problems that are common in training data (developer pain > niche B2B pain)
- Agents should generate questions to ask, not answers to conclusions; the human must conduct the validation
- Human checkpoint: after agent synthesizes evidence, the founder must read all raw sources, not just the summary
- If an agent recommends PROCEED based on stated interest only, treat it as PIVOT — stated interest is insufficient

## References
- Rob Fitzpatrick, "The Mom Test" (momtestbook.com) — the canonical resource on problem validation interviews
- Eric Ries, "The Lean Startup" — build-measure-learn loop applied to problem validation
- https://leanstack.com/running-lean — Ash Maurya's running lean framework
- https://www.ycombinator.com/library/6e-how-to-talk-to-users
- Justin Wilcox, "How to Get Your First Customers" (customerdevlabs.com)
