# Voice UI Patterns

## Summary

Practical patterns for designing voice user interfaces: prompt writing rules, progressive error recovery (3-step ladder), multimodal voice+screen coordination, platform-specific constraints (Alexa, Google Actions, Siri), and key performance metrics. The core discipline is designing for the ear, not the eye — one idea per turn, concise confirmations only for high-stakes actions, and always providing an escape hatch.

## Why

VUI fails when designed like a GUI: long prompts cause users to forget the start; identical error messages frustrate; missing escape hatches trap users. Empirical VUI research (NNG, Google, Amazon design guides) shows task completion drops sharply after 15 seconds of speech and more than 3-4 options per turn. Progressive error ladders and implicit confirmations for low-risk actions reduce abandonment.

## When To Use

- Designing a new voice skill (Alexa, Google Action, Siri Shortcut, or custom voice bot).
- Producing prompt copy, error ladders, and confirmation patterns from a feature spec.
- Auditing an existing voice flow against NNG / Google / Amazon design guidelines.
- Designing multimodal (voice + screen) flows for display devices.

## When NOT To Use

- Pure text chatbots with no audio — use chatbot conversation-design playbooks instead.
- IVR with regulatory script requirements (banking, healthcare) — legal-mandated wording overrides UX guidance.
- Pre-product validation phase — design utterances on real user data, not imagined scripts.
- Languages with limited TTS quality where prosody coaching is futile.

## Content

| File | What's inside |
|------|---------------|
| `content/01-prompt-rules.xml` | Prompt writing do/don't rules, error recovery ladder, multimodal coordination patterns. |
| `content/02-platform-and-metrics.xml` | Platform constraints (Alexa/Google/Siri), performance metrics targets, testing checklist. |

## Templates

| File | Purpose |
|------|---------|
| `templates/vui-lint.py` | Linter that scores voice copy against length (8 s) and blame-free framing rules. |
| `templates/conversation-graph-prompt.txt` | Prompt template for generating a full conversation graph from an intent spec. |

## Scripts

none
