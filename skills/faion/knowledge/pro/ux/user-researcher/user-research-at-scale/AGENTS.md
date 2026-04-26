# User Research at Scale

## Summary

An operating model for running research in parallel with product velocity using AI-augmented pipelines: automated transcription, agent-driven tagging and clustering, human verification on a sampled 10%, and a repository as the single source of truth. Humans own study design, ethics, interpretation, and stakeholder framing; agents own transcription, tagging, clustering, and report drafting.

## Why

Traditional one-researcher-at-a-time cadence cannot keep up with multi-squad product velocity. AI tools (transcription, sentiment tagging, affinity clustering) compress the mechanical work by 5-10x, but only when paired with human quality gates — auto-tagging errors compound silently without them. The bottleneck shifts from "who do we talk to" to "what do we do with insights," which requires a repository strategy and a decisions-ledger to prove ROI.

## When To Use

- Multiple squads need research findings same-week, not month-later.
- Continuous-discovery model where every PM/designer runs small studies and researchers are enablers.
- High-volume unmoderated testing (1k+ recordings/quarter) where AI analysis is a force multiplier.
- Multinational rollouts requiring parallel sessions across regions/locales.
- Mature ResearchOps with repository, intake, and recruitment infrastructure already in place.

## When NOT To Use

- Pre-PMF startups with fewer than 50 paying users — qualitative depth beats scale.
- Studies requiring sensitive populations (children, healthcare, accessibility) where ethics review must dominate throughput.
- Strategic generative research (problem framing) — small samples with senior researcher synthesis still win.
- Regulated environments (HIPAA, GDPR special-category data) where AI auto-tagging is restricted.

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline.xml` | Assembly-line model: recruit → transcribe → tag → cluster → report; platform capabilities |
| `content/02-agentic-workflow.xml` | Subagent patterns, prompt templates, gotchas, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/tag-session.py` | Whisper + Anthropic pipeline for transcription and taxonomy tagging at scale |
