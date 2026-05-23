# Voice Agents

## Summary

**One-sentence:** Designs production voice agents on real-time STT→LLM→TTS pipelines with ≤800ms end-to-end latency, 1-3-sentence responses, stripped markdown, barge-in, and filler phrases during tool calls.

**One-paragraph:** Voice agents replace IVR menus and phone-support touchpoints with conversational AI. The hard problems are real-time media (WebRTC), VAD turn detection, barge-in, and telephony integration — best absorbed by managed platforms (Retell, Vapi, ElevenLabs CAI). This methodology fixes the system-prompt discipline (1-3 sentences, no markdown), tool-call patterns (filler phrases while tools execute), and observability (per-component p95 latency, transcripts, escalation rate). Build on LiveKit only when self-hosting is required.

**Ефективно для:**

- Phone-support automation: inbound triage, order lookup, appointment changes.
- Outbound campaigns under TCPA / GDPR consent workflows.
- Web/mobile in-app voice replacing complex form flows.
- Live translation agents over WebRTC.

## Applies If (ALL must hold)

- Building a phone or web voice agent for production use.
- End-to-end latency target ≤800ms is feasible (not <300ms).
- Tool calls (CRM lookup, calendar) are required within turns.

## Skip If (ANY kills it)

- Text chat is sufficient — voice adds latency, cost, infra without UX gain.
- Latency budget < 300ms end-to-end — no 2026 stack delivers reliably.
- Use case requires precise multi-step legal/medical consent — voice ambiguity is risky.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Conversation flows | markdown | Product / UX design |
| Tool inventory | YAML | Backend API list |
| Telephony number | phone# | Provider provisioning |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `flow_design` | sonnet | Conversation tree + tool wiring. |
| `system_prompt_author` | sonnet | Voice-specific discipline. |
| `metrics_setup` | haiku | Latency + transcript logging. |

## Templates

| File | Purpose |
|------|---------|
| `templates/system-prompt.txt` | Voice agent system prompt skeleton |
| `templates/retell-webhook.py` | Minimal Retell AI webhook handler (FastAPI) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-voice-agents.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[vision-agentic-pipeline]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is the deployment phone-based? Branches route to a rule id from `content/01-core-rules.xml` (latency-budget-800, tcpa-gdpr-consent, filler-phrase-on-tool, ...) so every leaf is traceable to a testable statement.
