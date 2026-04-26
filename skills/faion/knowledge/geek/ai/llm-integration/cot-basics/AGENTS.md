# Chain-of-Thought Basics

## Summary

Chain-of-Thought (CoT) prompting instructs an LLM to emit intermediate reasoning steps before producing a final answer. Three main variants: zero-shot CoT (append "Let's think step by step." to the user turn), few-shot CoT (provide 2–3 worked reasoning examples), and self-consistency (run N=3–7 parallel paths and vote on the majority answer). For Claude, native extended thinking (`budget_tokens`) replaces manual CoT when maximum accuracy is required.

## Why

LLMs produce higher accuracy on multi-step reasoning tasks when forced to write out intermediate steps. The reasoning chain acts as a working scratchpad: the model commits to sub-answers before reaching the final answer, which reduces drift on long problems. Self-consistency further improves accuracy by aggregating diverse reasoning paths — the majority vote reduces the impact of any single flawed chain.

## When To Use

- Task requires multi-step reasoning: math, logic, code debugging, root cause analysis.
- Agent must explain reasoning to a downstream consumer or auditor.
- Accuracy matters more than latency (self-consistency requires N calls).
- Structured decomposition is needed before calling external tools (plan before act).

## When NOT To Use

- Simple lookup or classification tasks — CoT adds tokens with no accuracy gain.
- Latency-critical paths where a single-token answer suffices.
- Tasks whose steps cannot be verified (pure creative generation) — overhead without benefit.
- High-volume pipelines where cost dominates; use zero-shot direct answering instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cot-techniques.xml` | Zero-shot, few-shot, and self-consistency rules; answer marker requirement; trigger phrase placement. |
| `content/02-cot-antipatterns.xml` | Failure modes: wrong extraction, temp=0 collapse, bad examples, blind trust in reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/self-consistency.py` | Self-consistency loop: N parallel calls, majority vote, confidence score. |
| `templates/cot-prompt.txt` | System prompt for a reasoner subagent with XML-structured output. |
