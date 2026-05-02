---
name: mom-test-customer-interview
description: Run a Mom Test customer interview to learn whether your idea solves a real problem, without pitching or leading the witness.
tier: free
group: business-discovery
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have completed at least one recorded Mom Test interview, produced a set of specific past-behaviour quotes that confirm or deny your core assumption, and written a one-paragraph learning note that tells you whether to keep your current direction or change it.

## Prerequisites

- A problem hypothesis written down in one sentence, e.g. "Freelance designers lose track of client revision feedback spread across email, Slack, and PDFs."
- A target persona in mind — a real category of person who would suffer this problem, e.g. "freelance graphic designers who take on 3+ clients at once".
- Access to at least one person who fits that persona (LinkedIn, Slack community, Indie Hackers, a friend, a former colleague).
- A note-taking method ready: pen + paper, a plain text file, or a voice recorder app.
- 20–30 minutes blocked on your calendar.
- No slide deck, no demo, no product name mentioned during the interview. This is non-negotiable.

## Steps

1. Write your riskiest assumption as a single sentence before the call. Example: "Freelance designers currently spend more than 30 minutes per project consolidating revision notes from multiple channels." Pin it somewhere visible. This is the thing you are trying to falsify — not to confirm.

2. Find your first interviewee. Search LinkedIn for "freelance graphic designer", post in a relevant Slack community such as Design Friends or Indie Hackers with "I'm researching how designers manage client feedback — happy to pay $20 for 20 minutes of your time", or reach out directly to someone you already know who matches the persona. Text or DM works fine. Do not explain what your product idea is.

3. Prepare exactly three seed questions using the Mom Test rules — talk about their life (not your idea), ask for past specifics (not future hypotheticals), and never pitch:
   - "Walk me through the last time you handed off a round of revisions to a client. What did that look like?"
   - "What tools do you actually use today when a client sends you feedback?"
   - "Tell me about the most frustrating project you had in the last 6 months."

4. Open the call by framing it correctly: "I'm trying to understand how designers work — not selling anything, just researching. Totally fine to say 'I don't know' or 'that doesn't apply to me'. Can you walk me through your day when a project is in revision rounds?"

5. Listen for 80% of the call. When your interviewee says anything interesting, follow up with "Tell me more about that" or "What happened next?" or "How often does that happen?". Never say "Would you use a tool that did X?". That question is useless — everyone says yes and no one buys.

6. Avoid these common pitfalls mid-interview:
   - Do not say "We're building something that..." — end the call if you accidentally slip into pitch mode; write it down and restart next time.
   - Do not ask "Would you pay for that?" — instead ask "How are you handling that cost today?" or "What have you already tried to fix it?"
   - Do not validate a compliment. If they say "That sounds cool!", redirect: "Thanks — what are you doing right now when that comes up?"

7. Close the interview by asking for two things: a referral ("Who else do you know who deals with this? Could you introduce me?") and permission to follow up ("If I have a quick follow-up question next week, is it OK to message you?"). Do not pitch the product.

8. Within 10 minutes of ending the call, write your notes in three buckets:
   - **Facts** — concrete things they said they do today. Example: "Uses a shared Google Doc labelled 'Revision Round 2' for every project."
   - **Pain signals** — moments of visible frustration or workarounds. Example: "Spends Sunday evening re-reading Slack threads before Monday client calls."
   - **Non-problems** — things you expected to be painful that they did not mention or dismissed. Example: "Did not mention version tracking as a problem at all."

9. After three interviews, read your notes side by side. If two or more interviewees independently described the same workaround or the same pain signal without you prompting it, that is a real signal. If no one mentioned your assumed problem unprompted, your hypothesis is probably wrong — update it and run three more interviews.

## Verify

Open your notes file after the interview. You have passed the Mom Test standard if:

- You can quote at least two specific past-behaviour statements (e.g. "Last Tuesday I sent three separate emails because the client kept replying to the wrong thread") — not predictions or hypotheticals.
- None of your notes contain the phrase "they said they would use it" or "they liked the idea" — those are not evidence.
- Your notes have at least one entry in the "Non-problems" bucket — if everything was a problem, you were leading the witness.

If your notes contain only opinions ("it would be great if...") and no observed behaviour, the interview did not pass the Mom Test standard. Run another one.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Interviewee keeps asking "what are you building?" | Natural curiosity; they sense you have an agenda | Deflect honestly: "I'm still at research stage — I want to understand the problem before assuming there's a solution. What's your current workflow for X?" |
| Nobody agrees to be interviewed | Request is too vague or asks for too much time | Shorten to "15 minutes, no pitch, I'll send a $15 Amazon gift card after." One specific time offer beats an open-ended "whenever works." |
| Every interviewee says the problem is real | You are asking leading or hypothetical questions | Re-read Step 5. Replace any "Would you..." questions with "Tell me about the last time..." |
| Conversation stays surface-level | You are accepting first-level answers | Follow every short answer with "Can you walk me through a specific example?" or "When did that last happen?" |
| Interviewee pitches you their own solution | They have thought about this problem too | Great signal. Ask "Have you tried to build or buy anything for this?" and "Why did that not work?" |
| You forgot to take notes and can't remember the conversation | No note-taking setup before the call | Reschedule and next time open a plain text file before dialling. Voice recording with permission is also acceptable. |

## Next

- [idea-validation-landing-page](../idea-validation-landing-page/playbook.md) — once two or more interviews confirm a real problem, test demand with a landing page before writing a line of code.
- Run three more interviews with a refined hypothesis — the goal is pattern-finding across five to eight conversations, not a single confirmation.
- [niche-selection-framework](../niche-selection-framework/playbook.md) — if interviews reveal that the problem exists but across very different personas, use the niche-selection framework to pick the one segment to serve first.

## References

- [knowledge/free/dev/code-quality/pair-programming](../../../knowledge/free/dev/code-quality/pair-programming) — the driver-navigator role split directly maps to Mom Test interview structure: one person speaks (driver), the other suppresses their urge to respond and instead observes and records (navigator). Applying the navigator discipline — no interrupting, no explaining, defer judgment until the session ends — is the single most effective way to stop a founder from accidentally pitching during a discovery call.
