# Agent Integration — Negotiation & Persuasion

## When to use
- Drafting negotiation preparation briefs (BATNA analysis, ZOPA mapping, interest extraction) before a real human negotiation
- Generating counter-argument libraries for price, scope, or contract discussions
- Writing persuasion copy that applies Cialdini principles (sales pages, pitch decks, outreach emails)
- Coaching mode: simulating the other party to help a user rehearse responses to hardball tactics
- Post-negotiation retrospective: analyzing transcripts or notes to identify missed leverage points

## When NOT to use
- Live real-time negotiation — the agent cannot read body language, tone, or emotional state in the room
- Legally binding contract drafting — output needs attorney review before signing
- Hostage or crisis negotiation scenarios — requires licensed human expertise
- When the user has not yet established their walk-away point — agent output will be generic without that anchor

## Where it fails / limitations
- BATNA estimation is only as good as the context provided; agent cannot research the counterparty's real alternatives without a search tool
- Cialdini tactics applied mechanically in copy can read as manipulative if the underlying offer is weak
- Salary negotiation scripts miss cultural context (e.g., collectivist cultures where direct anchoring is offensive)
- Simulated roleplay partners are not adversarial enough — real counterparties surface objections agents do not anticipate

## Agentic workflow
Use a two-subagent pattern: a research subagent gathers market data (comparable salaries, contract precedents, competitor pricing) and a drafting subagent synthesizes that data into a preparation brief using the negotiation template in README.md. For persuasion copy, a single Sonnet call with Cialdini principle selection and copy generation is sufficient. Human review is mandatory before any real negotiation begins.

### Recommended subagents
- `faion-sdd-executor-agent` — execute structured negotiation-prep task sequences from a spec
- `password-scrubber-agent` — sanitize any real counterparty details before logging prep docs

### Prompt pattern
```
You are preparing a negotiation brief. Given:
- My position: <position>
- My interests: <interests>
- My BATNA: <batna>
- Counterparty profile: <profile>

Produce: (1) predicted counterparty interests, (2) ZOPA estimate, (3) three creative options for mutual gain, (4) five Cialdini-based persuasion angles for the opening pitch.
```

```
Roleplay as a tough buyer negotiating price for <product>. Start at 60% of my ask. Use anchoring, the flinch, and silence. I will respond. After 5 exchanges, break character and critique my technique.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `llm` (Simon Willison) | Draft negotiation briefs via CLI piping | `pip install llm` / https://llm.datasette.io |
| `jq` | Parse JSON salary data from APIs (Levels.fyi, Glassdoor) | `apt install jq` / https://jqlang.github.io/jq |
| `pandoc` | Convert negotiation prep docs to PDF for meetings | `apt install pandoc` / https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Levels.fyi API | SaaS (public data) | Yes (scrape/CSV) | Compensation benchmarks for salary negotiation |
| Glassdoor | SaaS | Partial (unofficial API) | Salary ranges; rate-limited |
| Gong.io | SaaS | No (human-centric) | Call analysis; no agent API for live data |
| Contractbook | SaaS | Yes (REST API) | Contract management; can read/write clause data |
| DocuSign | SaaS | Yes (REST API) | Execution step; not negotiation drafting |
| PandaDoc | SaaS | Yes (REST API) | Template-based contract generation |

## Templates & scripts
See `templates.md` for the full Negotiation Preparation Template. The README.md inline template covers: My Position, My Interests, My BATNA, Walk-Away, Their Position (Predicted), Their Interests, Their BATNA, Creative Options, Objective Criteria.

```python
# Minimal ZOPA calculator
def zopa(my_walk_away, their_walk_away, buyer=True):
    """Return overlap range or None."""
    if buyer:
        low, high = my_walk_away, their_walk_away
    else:
        low, high = their_walk_away, my_walk_away
    if low <= high:
        return (low, high)
    return None  # no ZOPA, negotiation cannot close

print(zopa(80_000, 105_000, buyer=False))  # (80000, 105000)
```

## Best practices
- Anchor with a specific number, not a range — ranges anchor on the favorable end for the counterparty
- Send written summaries after verbal negotiations; ambiguity always benefits the more powerful party
- Never reveal your BATNA unless it is genuinely strong — revealing a weak BATNA destroys leverage
- Use the "nibble" only after the main agreement is signed, not before; premature nibbles signal desperation
- When generating Cialdini-based copy, pick at most two principles per message — stacking all six reads as a sales script and triggers skepticism
- For salary negotiations, always name a number first if you have good market data — the anchoring effect outweighs the risk of underselling

## AI-agent gotchas
- **Human-in-loop before sending:** Any agent-drafted offer, counter, or persuasion message must be reviewed by the human before delivery — tone and relationship context cannot be fully captured in a brief
- **Context completeness:** The agent's BATNA and ZOPA analysis is only as accurate as the inputs; garbage in → plausible-sounding but wrong brief out
- **Roleplay calibration:** Simulated counterparties are too rational; real negotiators use emotion, ego, and politics — agent roleplay understates these
- **Legal review gate:** Contract language suggestions from the agent are starting points, not final clauses; flag this explicitly in any output that includes contract terms
- **Overconfidence in Cialdini scoring:** The agent cannot measure which principle will be effective for a specific individual; A/B testing is required for persuasion copy

## References
- Fisher, R. & Ury, W. (1981). *Getting to Yes*. Penguin Books.
- Cialdini, R. (2006). *Influence: The Psychology of Persuasion*. Harper Business.
- Voss, C. (2016). *Never Split the Difference*. Harper Business.
- https://www.pon.harvard.edu/daily/negotiation-skills-daily/ — Harvard Program on Negotiation blog
- https://levels.fyi — compensation benchmarks for salary negotiation prep
