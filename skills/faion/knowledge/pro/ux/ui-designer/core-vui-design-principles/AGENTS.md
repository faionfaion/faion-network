# Core VUI Design Principles

## Summary

Three testable principles for voice user interface design: (1) Simplicity — one idea per turn, no redundant phrasing; (2) Natural conversation — sound human, offer one helpful follow-up; (3) Context awareness — use prior turns implicitly, never restate what the user just said. Voice interfaces fail when designed like visual interfaces: dense information, no follow-up offers, and ignoring conversation history all break the spoken medium.

## Why

Voice is ephemeral — users cannot re-read. Dense responses cause cognitive overload and abandonment. LLMs default to verbose and polite; without explicit constraints every system utterance violates principle 1. Encoding the three principles as evaluator rubrics (not free-form review) enables reliable automated checking and measurable improvement across iterations.

## When To Use

- Designing voice-first features (Alexa/Google Assistant skills, IVR, in-car voice, accessibility voice nav).
- Adding spoken output to multimodal agents where the LLM both listens and speaks.
- Auditing existing voice flows for verbosity, missing context tracking, or unnatural phrasing.
- Generating TTS-layer prompt/response copy where SSML, pacing, and turn-taking matter.

## When NOT To Use

- Pure GUI/keyboard apps where voice is not a modality.
- Backend-only agents with no spoken output (text-chat agents need conversation design, not VUI principles).
- One-shot transactional bots where users never have a follow-up turn — those need scripts, not principles.

## Content

| File | What's inside |
|------|---------------|
| `content/01-three-principles.xml` | Definitions, concrete do/don't examples, and evaluator rubric for each principle. |
| `content/02-agent-application.xml` | Agentic workflow, recommended subagents, prompt patterns, and gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vui-utterance-lint.py` | Linter flagging utterances over character limit, with too many clauses, or with filler phrases. |
| `templates/vui-copywriter-prompt.txt` | System prompt for a VUI copywriter subagent that rewrites utterances against the three principles. |

## Scripts

none
