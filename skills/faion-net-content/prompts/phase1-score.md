# Scoring agent prompt — Phase 1.3

You are one of 5 parallel scoring agents evaluating the entire 100-idea pool from Phase 1.2. Each agent runs independently; aggregation is downstream.

## Inputs

- **Raw idea pool**: `{{session_dir}}/brainstorm-*.json` — 5 files, 20 ideas each = 100 total. Read them all.
- **Project context** (memorise before scoring):
  - faion.net sells a CLI tool + SDD methodology stack to solopreneurs.
  - Positioning: SDD-first, CLI-first install, "ship in weeks not months", solopreneur economic reality.
  - Token-pricing is FORBIDDEN copy (memory rule `no-token-pricing`).
  - Methodology bodies are CLI-only (memory rule `methodologies-cli-only`).
  - Landing pages address problems, never name buyer personas (memory rule `landing-no-persona-labels`).
- **Corpus**: ~2615 methodologies + 455 playbooks for "corpus_synergy" scoring.

## Criteria (10-point scale each)

| Criterion | Question | 10 = | 1 = |
|-----------|----------|------|-----|
| `strategic_value` | Does this advance faion's positioning (SDD-first, solopreneur stack, CLI moat)? | Anchors the brand as category-defining authority. | Generic content that any AI blog could publish. |
| `search_demand` | Realistic SEO/distribution potential given current audience signals? | Demonstrable existing search demand + low competition. | Pure invention, no signal anyone wants this. |
| `pain_severity` | How urgent/painful is the problem this solves for the ICP? | Solves a problem that costs the reader money/time today. | Mildly interesting at best. |
| `differentiation` | Do we say something new vs the existing internet on this topic? | Genuinely contrarian or novel framing with evidence. | 100th rehash of well-trodden topic. |
| `corpus_synergy` | How well does this leverage faion-network methodologies/playbooks? | Naturally cites 3+ methodologies, drives `faion get-content` clicks. | Zero corpus alignment; we'd write it from scratch. |

## Process

1. Read ALL 100 ideas before scoring any.
2. For each idea, score all 5 criteria (1-10 integers).
3. Add a 1-2 sentence `rationale` capturing the dominant reason for the lowest scoring criterion.
4. Flag `red_flags` if you see:
   - `token_pricing_copy` — copy that frames faion as token reseller.
   - `methodology_inlining` — would require publishing methodology bodies on web.
   - `persona_labeling` — landing-style "for solopreneurs" labels.
   - `weak_evidence` — pain anchor seems invented.
5. Independent judgement — do NOT try to align with other scoring agents.

## Output

Single JSON file at `{{session_dir}}/scores-agent-{{agent_id}}.json`:

```json
{
  "agent_id": "{{agent_id}}",
  "scored_at": "<ISO-8601 timestamp>",
  "scores": {
    "<idea_id>": {
      "strategic_value": <1-10>,
      "search_demand": <1-10>,
      "pain_severity": <1-10>,
      "differentiation": <1-10>,
      "corpus_synergy": <1-10>,
      "mean": <float>,
      "rationale": "<text>",
      "red_flags": ["<flag>", ...]
    },
    ...
  }
}
```

## Hard rules

- Score ALL 100 ideas; no skipping.
- No tied criterion means within an idea (force distinctions between dimensions).
- Don't pad scores upward to be agreeable. Honest 4/10 beats deceptive 7/10.
- No emojis.

## Final report

One paragraph: distribution summary (how many ideas scored ≥ 7 mean, top 3 by mean, any red-flag triggers).
