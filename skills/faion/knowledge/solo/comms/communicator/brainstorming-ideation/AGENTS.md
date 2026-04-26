# Brainstorming Ideation (Agentic Pipeline)

## Summary

Brainstorming-ideation covers using brainstorming techniques as a generative input for automated pipelines — where the output is a scored shortlist, not a facilitated group session. The agent receives a problem statement, runs a structured generation pass (Classic, Reverse, or Brainwriting-simulated), deduplicates semantically, clusters by theme, and scores against an impact/effort rubric. For facilitated group sessions, see `brainstorming-techniques/` which covers the human-facilitation angle.

## Why

Agent-generated idea lists plateau in novelty around 30-40 ideas without persona switching or domain constraint injection. The critical failure points are: (1) mixing generation and evaluation in the same prompt — causes premature convergence; (2) using the generating agent to also score ideas — circular bias toward first-pass outputs; (3) semantic clustering silently merging two distinct viable ideas — human review at the cluster stage is mandatory before scoring.

## When To Use

- Product feature generation: given a persona + pain point, produce candidate features to evaluate against backlog
- Content ideation: bulk-generating article topics, campaign angles, or ad copy variants for human selection
- Risk surfacing: Reverse Brainstorming to enumerate failure modes before a launch or deployment
- Feeding a scored shortlist into a downstream pipeline (Linear backlog, Notion idea database)

## When NOT To Use

- When human group dynamic is the point (team alignment, buy-in, psychological safety) — agentic bulk generation skips the relational work
- When the problem is too narrow for divergent thinking; use direct prompting or SCAMPER instead
- When ideas require domain-expert validation that an LLM cannot reliably provide (medical, legal, engineering safety)
- When you need the dot-voting or scoring to be done by the same agent that generated the ideas — circular bias invalidates the prioritization

## Content

| File | What's inside |
|------|---------------|
| `content/01-agentic-workflow.xml` | Generation → dedup → cluster → score pipeline; persona injection; Reverse Brainstorm variant |
| `content/02-antipatterns.xml` | Circular scoring bias, premature convergence, semantic clustering failures, positional bias in large lists |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-diverge.txt` | Diverge-pass prompt (generation only, no evaluation) |
| `templates/prompt-reverse.txt` | Reverse Brainstorm prompt with inversion step |
| `templates/semantic-dedup.py` | Sentence-transformers semantic deduplication for idea lists |
