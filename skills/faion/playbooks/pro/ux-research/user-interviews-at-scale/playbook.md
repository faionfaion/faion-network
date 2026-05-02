---
name: user-interviews-at-scale
description: Recruit 12 users via UserInterviews.com or Respondent, run 45-min Zoom sessions, transcribe with Otter.ai, tag in Dovetail, and synthesize 5 actionable insights.
tier: pro
group: ux-research
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have 12 completed user interviews with screen recordings, Otter.ai transcripts tagged by theme in Dovetail, and 5 synthesized insights with direct quote citations — ready to share with your client or feed into a design sprint.

## Prerequisites

- A UserInterviews.com or Respondent account (both offer pay-per-participant; no subscription required).
- A Calendly account (free tier works; individual event type).
- A Zoom account with cloud recording enabled (Zoom Pro, $15/mo minimum).
- An Otter.ai account (Business plan, $20/mo, needed for bulk import + speaker ID).
- A Dovetail account (Starter plan, $29/mo, needed for tagging + insight synthesis).
- A screener brief: target user profile (role, company size, behavior) written before you start.
- A $600–$1,200 budget for incentives ($50–$100 per participant × 12).
- An interview guide: 6–8 open-ended questions drafted and reviewed by a stakeholder.

## Steps

### Phase 1: Recruit

1. Log in to https://app.userinterviews.com (or https://www.respondent.io for B2B audiences with tighter targeting).
2. Click **Create a project** → choose **Remote Interviews** → set session length to **45 minutes**.
3. In the screener, add the demographic and behavioral filters matching your target profile. For a SaaS agency audience, typical filters are: job title contains "founder" or "head of", company size 10–200, uses project management software daily.
4. Set incentive to **$75 USD** (sweet spot for 45 min; raise to $100 for senior titles). UserInterviews handles payments; Respondent deducts from a pre-funded wallet.
5. Set **recruiting target: 15** (aim for 15 to account for no-shows; cancel 3 once you hit 12 confirmed).
6. In the **Scheduling** step, paste your Calendly link (see Phase 2). UserInterviews sends it to screened participants automatically.
7. Launch the project. Expect 12 confirmed slots within 48–72 hours for US/EU audiences.

### Phase 2: Schedule

1. In Calendly, create an event: **45 min / User Interview / one-on-one**.
2. Set availability to cover your research window (e.g., Mon–Fri, 9am–5pm for 2 weeks).
3. Enable **Google Calendar or Outlook sync** to block already-busy slots automatically.
4. Under **Confirmation email**, add: "You'll receive a Zoom link 15 minutes before the session. Please join from a quiet room."
5. Under **Notifications → Reminders**, set 24h + 1h reminders. Both reduce no-show rates by ~30%.
6. Copy the event link and paste it into the UserInterviews scheduling step (Phase 1, step 6).

### Phase 3: Run sessions

1. Create a dedicated Zoom meeting for all interviews (same link reused; avoids link management overhead). Enable **Record to the cloud** automatically on join.
2. At session start, say: "I'd like to record this session for transcription. The recording stays within our team and won't be shared externally. Is that OK?" Wait for explicit verbal consent before proceeding.
3. Share your screen to show the interview guide as a reference — not to the participant, just for yourself via a second monitor or printed sheet.
4. Follow the guide but use follow-up probes: "Can you tell me more about that?", "What happened next?", "Why was that important to you?"
5. At 40 minutes, transition: "We have about 5 minutes left — is there anything you wanted to mention that we haven't covered?"
6. After the call, add a 2-sentence note to a shared doc while memory is fresh: what surprised you, what confirmed existing assumptions. Do this before the next session.
7. After all 12 sessions, download the Zoom cloud recordings from https://zoom.us/recording (MP4 + M4A).

### Phase 4: Transcribe

1. In Otter.ai, go to **Import** → drag all 12 audio files (M4A is faster to process than MP4).
2. Otter auto-generates transcripts within 5–15 minutes per file.
3. Open each transcript, click **Speakers**, and assign correct names (Interviewer / Participant). This enables speaker-filtered exports later.
4. For each transcript, skim for obvious errors in proper nouns (product names, tools). Correct inline — no need for full proofread at this stage.
5. Export all 12 transcripts: **Export → TXT** (plain text is faster to import into Dovetail than DOCX).

### Phase 5: Tag in Dovetail

1. Create a new Dovetail **Project** named after the research study (e.g., "Agency Owner Onboarding — May 2026").
2. Import all 12 transcripts: **Data → Import → Text files**. Each becomes a separate note.
3. Create a tag group called **Themes** with 6–10 initial tags derived from your interview guide topics (e.g., `onboarding-friction`, `tool-switching`, `pricing-concern`, `workflow-integration`, `success-moment`).
4. Work through each transcript: highlight a quote, click **Tag**, assign one or more theme tags. Aim for 15–25 highlights per transcript (180–300 highlights total).
5. Add a second tag group **Sentiment** with three tags: `positive`, `neutral`, `negative`. Apply to every highlight.
6. After tagging all 12, open **Insights** → click **Charts** → group by Theme. Identify the 5 themes with the most highlights — those become your 5 insights.

### Phase 6: Synthesize 5 insights

1. In Dovetail, create an **Insight** for each of the 5 top themes.
2. For each insight, write a one-sentence finding in the format: **"[User type] [struggle/achieve] [outcome] when [condition]."** Example: "Agency owners lose 2–3 hours per week reconciling client feedback because they lack a single source of truth."
3. Pull 2–3 supporting quotes from the tagged highlights directly into the insight (Dovetail link button → **Add evidence**).
4. Add a **Recommendation** field: one concrete design or product action that addresses the finding.
5. Export the full insight report: **Insights → Share → Export PDF**. This is the deliverable for the client or stakeholder review.

## Verify

Open the exported PDF. Confirm:

- 5 insight cards are present, each with a one-sentence finding.
- Each insight links to ≥2 quote citations.
- All quotes are attributable (Participant 1–12, no personally identifiable information).

Cross-check participant count in Dovetail: **Data → Notes** should list exactly 12 transcripts with ≥15 highlights each.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| UserInterviews returns <5 screened participants after 48h | Screener too narrow | Loosen one filter (e.g., raise company size cap from 50 to 200) and relaunch |
| Participant no-shows >3 of 12 | Reminder gap or wrong time zone | Check Calendly timezone setting; manually confirm via email day-before for remaining slots |
| Zoom cloud recording missing for a session | Recording failed to upload | Check Zoom Recording settings; as fallback, use local recording from the Zoom app (saved to Desktop) |
| Otter.ai speaker assignment wrong throughout transcript | Audio mixed channels | Re-import with M4A audio only (not MP4); Otter separates channels more reliably from audio-only files |
| Dovetail highlights feel scattered; no clear themes | Interview guide was too broad | Run an affinity sort: move all highlights to a whiteboard view, group physically by similarity, then name the groups → these become your tags |
| Client rejects insight because it lacks data | Quotes without counts | Add "N=X of 12 participants mentioned this" to each insight card in Dovetail |

## Next

- Run a follow-up survey to quantify findings from qualitative themes — see `solo/ux-research/` for lean survey playbooks.
- Schedule a design sprint using insights as How-Might-We inputs.
- Upgrade to Dovetail's **Team plan** ($99/mo) if multiple researchers tag simultaneously — avoids tag naming conflicts.

## References

- [knowledge/pro/ux/user-researcher/user-research-at-scale](../../../knowledge/pro/ux/user-researcher/user-research-at-scale) — provides the participant count rationale (12 interviews for saturation) and panel recruitment trade-offs between UserInterviews.com and Respondent that back Phase 1 platform choice
- [knowledge/pro/ux/ux-researcher/surveys](../../../knowledge/pro/ux/ux-researcher/surveys) — informs the screener design in Phase 1 steps 3–4, particularly question type selection and demographic filter logic
- [knowledge/pro/ux/user-researcher/audience-segmentation](../../../knowledge/pro/ux/user-researcher/audience-segmentation) — underpins the screener criteria construction for agency-owner targeting and the "senior title → higher incentive" rule in Phase 1 step 4
- [knowledge/pro/ux/ux-researcher/focus-groups](../../../knowledge/pro/ux/ux-researcher/focus-groups) — contrasts focus-group synthesis patterns with one-on-one interview synthesis; informs the Dovetail tagging cadence and 5-insight limit in Phase 5–6
