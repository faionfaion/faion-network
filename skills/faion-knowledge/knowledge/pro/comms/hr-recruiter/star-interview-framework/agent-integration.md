# Agent Integration — STAR Interview Framework

## Status

This methodology directory has README content **byte-identical** to its sibling `star-interview-method` (same id, name, framework tables, templates, sources). The two are an alias pair retained for backward-compatible discoverability.

Rather than duplicating the integration guide, the canonical agentic guidance for the STAR framework lives at:

- `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/star-interview-method/agent-integration.md`

## What to do

When invoking agents to design, run, or analyze STAR-based behavioral interviews, route to `star-interview-method/agent-integration.md`. That file covers:

- When to use / when NOT to use STAR-based behavioral interviewing.
- Where it fails (rehearsed answers, "we → I" attribution drift, R inflation, cross-cultural narrative bias, leadership/communication clustering in LLM-generated banks).
- The four-stage agentic pipeline (question generation, live-interview probe support, transcript STAR extraction, cross-candidate calibration) owned by `faion-recruiter-agent` with `general-purpose` reviewer for adversarial bias passes.
- Prompt patterns for question generation, transcript STAR extraction, and the deterministic STAR-completeness Python helper.
- CLI tools (whisper / pyannote-audio / ATS APIs / interview-intelligence APIs) and SaaS rows (BrightHire, Metaview, Pillar, Greenhouse, Lever, Ashby, Calendly, GoodTime).
- AI-agent gotchas: hallucinated quantified Results, pre-diarization requirement, "we" pronoun mis-attribution, ban on agent-assigned scores, ban on candidate-side live coaching during real interviews.
- Mandatory human-in-loop checkpoints for question approval, scoring, and hire decisions.

## Cross-references

- Sibling: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/star-interview-method/agent-integration.md` (canonical).
- Parent process: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/structured-interview-design/agent-integration.md`.
- Bundle index: `skills/faion-knowledge/knowledge/pro/comms/hr-recruiter/interview-methods/agent-integration.md`.

## Open question

The duplication should be resolved upstream — either deprecate one of the two slugs or differentiate the content (e.g., `star-interview-method` = practitioner how-to, `star-interview-framework` = research / theory). Until then, treat both directories as referring to one body of practice.
