# SDD Workflow Overview

## Summary

Specification-Driven Development: intent is the source of truth. The complete phase sequence is CONSTITUTION → SPEC → DESIGN → TEST-PLAN → IMPL-PLAN → TASKS → EXECUTE → REVIEW → DONE. Spec answers WHAT to build, design answers HOW, test-plan answers HOW to verify (written before impl-plan). Each phase transition requires a confidence threshold (90%+ for spec→design, 95%+ for plan→execute). The "15-minute waterfall" variant covers medium tasks: 5min spec, 5min design, 5min task list.

## Why

Developers and AI agents start coding immediately without planning, leading to scope creep, wrong implementations, and untestable results. SDD provides the specification as an anti-hallucination anchor: a machine-readable contract that grounds LLM code generation, makes "done" objective (tests from test-plan pass), and creates an audit trail for decisions. Research shows developers confident in AI-generated code are 2.5x more likely to have used specs.

## When To Use

- Multi-day features or anything requiring cross-module coordination
- AI-assisted development where reducing hallucinations is critical
- Production systems requiring quality assurance and audit trail
- Team collaboration requiring shared understanding of requirements

## When NOT To Use

- Tasks under 2 hours with a clear implementation path — direct implementation
- Exploratory prototypes where code is discarded — spike with throwaway code
- Bug fixes with clear root cause — fix + test
- Project has no .aidocs/ structure and no bandwidth to set it up — use 15-minute waterfall

## Content

| File | What's inside |
|------|---------------|
| `content/01-phases.xml` | Phase sequence, artifacts per phase, confidence thresholds, transition gates |
| `content/02-sdd-levels.xml` | Three SDD levels (Spec-First, Spec-Anchored, Spec-as-Source), 15-minute waterfall, level selection |

## Templates

| File | Purpose |
|------|---------|
| `templates/quick-spec.md` | 15-minute waterfall quick spec template |
