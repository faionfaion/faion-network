# Problem Validation 2026

## Summary

An updated problem validation methodology for 2026 emphasizing continuous evidence-based validation over one-time gates. Core rule: rank all evidence on a 5-level hierarchy (paid > committed > engaged with prototype > expressed interest > stated problem); only declare a problem validated when ≥3 tier-1 or tier-2 signals come from cold, non-network respondents. Validation is an ongoing process, not a checklist to pass once.

## Why

Survey-only validation and warm-contact interviews systematically over-report demand. Behavioral commitments (payment, sign-up, prototype time) are the only reliable signals. LLM-generated "synthetic user" data produces plausible but worthless results. The 2026 update reflects that AI-adjacent markets shift rapidly; re-validation is required every quarter to catch invalidated assumptions before they drive quarter-long sprints.

## When To Use

- Pre-MVP: validate problem is real, painful, and worth paying for before writing code.
- Pivoting: re-validate problem assumptions when retention is low or engagement is sparse.
- Adjacent expansion: testing whether an existing segment has a related underserved problem.
- After a hypothesis breaks (low conversion, no upsell) to confirm the problem still holds.

## When NOT To Use

- PMF is established with a paying user base — switch to feature-discovery and continuous-discovery.
- Incremental funnel optimization where A/B testing answers faster.
- Cannot reach the target segment within a week — you will over-rely on weak proxies.
- Commodity or undifferentiated problems where solution quality matters more than problem existence.

## Content

| File | What's inside |
|------|---------------|
| `content/01-evidence-hierarchy.xml` | 5-level evidence hierarchy, commitment signal types (time/reputation/money), red flags, and how to weight each level. |
| `content/02-interview-protocol.xml` | Mom Test question rules, Vision-Framing-Weakness-Pedestal-Ask opener, 3-agent agentic workflow, and agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/red-flag-scanner.py` | Python script: scans interview transcript for compliment/hypothetical/generic red-flag language patterns. |
| `templates/signal-extractor-prompt.txt` | Prompt for a signal-extractor subagent: extracts commitments and red flags from transcripts as structured JSON. |
