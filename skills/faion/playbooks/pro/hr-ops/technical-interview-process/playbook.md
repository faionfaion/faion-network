---
name: technical-interview-process
description: Run a structured 4-stage interview loop — phone screen, paid take-home, onsite panel, calibration — with per-stage scorecards and a consistent hiring bar.
tier: pro
group: hr-ops
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a repeatable, bias-reduced technical interview loop: a 30-minute phone screen, a paid 3-hour take-home assignment, a four-stage onsite panel (coding pairing, systems design, behavioral, team match), and a calibration session that produces a written hire/no-hire decision before any offer conversation begins.

## Prerequisites

- A written job description with at least three concrete must-have technical competencies identified (e.g., "designs RESTful APIs", "owns a production service end-to-end", "mentors junior engineers").
- A recruiting coordinator or calendar tool (Calendly, Cal.com) to schedule asynchronously — panel stages are 60 min each, back-to-back scheduling burns interviewers.
- A scorecard template stored in your ATS or a shared doc (Notion, Linear, Google Docs) — one per stage, accessible to every interviewer before the call.
- Budget approved for take-home compensation: $200 flat fee, paid within 7 days regardless of outcome.
- Four interviewers identified and briefed: one per onsite stage. Each interviewer owns their stage; they do not attend other stages to avoid anchoring bias.
- Familiarity with structured interview design principles — see References.

## Steps

1. **Define the hiring bar before opening the role.** Write a one-page rubric: what does "meets bar" look like at each of the four scorecard dimensions (technical depth, communication, problem-solving, culture add)? Post this in your shared hiring doc so every interviewer calibrates to the same expectation before the first candidate enters the loop.

2. **Schedule the 30-minute phone screen.** Send a Calendly link with a 30-minute slot. Before the call, read the candidate's resume and note two open questions. On the call, cover: (a) motivation for the role, (b) one technical deep-dive ("walk me through the hardest production incident you owned"), (c) logistics check (availability, remote/on-site fit, compensation range). Use the phone-screen scorecard row to record your go/no-go immediately after the call — not hours later.

3. **Send the take-home assignment within 24 hours of a phone-screen pass.** The assignment must: (a) take ≤3 hours of focused work, (b) map directly to the role's day-one responsibilities (e.g., add an endpoint to an existing small Django service, not a greenfield app), (c) include a grading rubric in the brief so the candidate knows what you evaluate. Email the assignment with a 5-day deadline and the $200 payment details. Pay via Wise, PayPal, or bank transfer — document the payer's name and amount in your ATS note.

4. **Grade the take-home blind before reading the name.** Have two reviewers score independently using the take-home rubric. Discuss divergences >1 point on any dimension. If both score below "meets bar", send a decline with brief feedback within 24 hours. If both pass, proceed to scheduling the onsite.

5. **Run the four-stage onsite panel.** Schedule all four stages in a single day or across two consecutive mornings. Each stage is independent — interviewers do not share notes until the calibration session.

   - **Stage 1 — Coding pairing (60 min).** Use a shared editor (VS Code Live Share, Replit). Give a problem the candidate is likely to encounter on the job: "extend this existing payment service to support a retry queue." Evaluate how they navigate unfamiliar code, ask clarifying questions, and handle a deliberate edge case you introduce mid-session. No whiteboard algorithm puzzles unrelated to the role.

   - **Stage 2 — Systems design (60 min).** Provide a realistic prompt: "Design the notification delivery system for a SaaS app with 50k daily active users." Use a shared whiteboard (Excalidraw, Miro). Probe trade-offs: "What changes if we need to support 10M users?" Score on breadth of options considered, depth of reasoning, and comfort acknowledging unknowns.

   - **Stage 3 — Behavioral (60 min).** Use STAR-format questions drawn from your must-have competencies. Prepare four questions; you will typically complete two to three in 60 minutes. Example: "Tell me about a time you disagreed with a technical decision your team had already committed to — what did you do?" Take verbatim notes on the Situation and Result — these are the hardest to reconstruct later.

   - **Stage 4 — Team match (30 min).** One of the future teammates (not a hiring manager) runs this stage. Goal: mutual fit check, answer candidate questions, give a realistic job preview. Score on engagement, curiosity, and red flags (e.g., no questions at all, disparaging previous employer unprompted). This stage is a two-way gate — the candidate also decides.

6. **Run the calibration session within 48 hours of the final onsite stage.** All four interviewers attend a 45-minute synchronous call. Format: each interviewer gives a one-sentence hire/no-hire and their top evidence before anyone else speaks (prevents anchoring). Then discuss. The hiring manager holds a casting vote if the panel splits 2–2. Write the final decision and reasoning in the ATS before anyone contacts the candidate.

7. **Communicate the outcome within 24 hours of calibration.** Hire decision → move to offer stage (compensation, equity, start date). No-hire → send a brief decline with one actionable observation ("strong systems thinking; we needed deeper experience with stateful services at scale"). Keep the feedback factual and role-specific; avoid personality assessments.

## Verify

After the first three candidates complete the full loop, run this audit:

```
Scorecard completion rate: all 4 stages × all 4 dimensions filled → target 100%
Inter-rater delta: avg absolute difference per dimension ≤1.0 (signals calibration health)
Time-to-decision: calibration session held ≤48h after final onsite → target ≥90% of loops
Take-home payment: all $200 fees paid within 7 days → target 100%
```

Run the audit in a spreadsheet (one row per candidate, one column per metric). If inter-rater delta exceeds 1.5 on any dimension, run a 30-minute rubric re-calibration session before the next candidate.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Interviewers give 3–5 scores with no justification | Scorecard treated as checkbox, not evidence log | Add a mandatory "evidence" free-text field per dimension; make it clear a score without evidence is invalid during calibration |
| Panel keeps splitting on "culture add" dimension | "Culture add" is undefined or means different things to different interviewers | Replace "culture add" with a concrete behavioral proxy, e.g. "gives and receives direct feedback without defensiveness" — rewrite the rubric level descriptors |
| Candidates ghost after the take-home brief | Assignment feels like unpaid consulting | Shorten to a clearly bounded sub-problem, include the $200 payment confirmation in the email subject line, and set a 5-day (not 2-day) deadline |
| Phone screens consistently pass but onsites consistently fail | Phone-screen bar is too loose | Add one structured technical question to the phone screen — a two-minute "live coding" sketch or a targeted architecture question; don't rely solely on the behavioral warm-up |
| Hiring decision delayed >1 week after final onsite | Calibration session not scheduled upfront | Book the calibration slot at the same time as the final onsite; cancel it if onsite produces a clear unanimous no-hire |
| Behavioral stage produces thin STAR answers | Candidates give high-level summaries instead of specifics | After the candidate's first answer, probe with "what specifically did you do — not the team" and "what was the measurable outcome?" — document these follow-up questions in the scorecard |

## Next

- Run the `first-hire-developer` playbook to handle JD writing, sourcing, and the offer letter mechanics that precede this loop.
- After the first hire completes 30 days, run a retrospective against the hiring rubric: did the scorecard predict on-the-job performance? Update level descriptors where predictions were wrong.
- Consider promoting the take-home rubric to a shared knowledge artifact so future interviewers can grade independently without a briefing call.

## References

- [knowledge/pro/comms/hr-recruiter/structured-interview-design](../../../knowledge/pro/comms/hr-recruiter/structured-interview-design) — provides the four-dimension scorecard framework and level descriptors (1–5) that each onsite stage uses; the per-stage scoring in Steps 5a–5d maps directly to its rubric structure.
- [knowledge/pro/comms/hr-recruiter/interview-methods](../../../knowledge/pro/comms/hr-recruiter/interview-methods) — grounds the anti-pattern call-out against brain-teasers and whiteboard algorithms: its evidence base shows these have near-zero predictive validity for job performance compared to structured behavioral and work-sample methods.
- [knowledge/pro/comms/hr-recruiter/star-interview-framework](../../../knowledge/pro/comms/hr-recruiter/star-interview-framework) — STAR probe sequence used in Stage 3 behavioral questions; the follow-up probes in Troubleshooting row 6 come directly from its question templates.
- [knowledge/pro/comms/hr-recruiter/recruiting-process](../../../knowledge/pro/comms/hr-recruiter/recruiting-process) — defines the funnel-stage gates (phone screen → take-home → panel → offer) that this playbook operationalizes, and the SLA targets (24h to decline, 48h calibration window) used in the Verify audit.
