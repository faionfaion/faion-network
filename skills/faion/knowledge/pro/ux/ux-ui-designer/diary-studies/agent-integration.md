# Agent Integration — Diary Studies

## When to use
- Understanding longitudinal behavior change: onboarding, habit formation, churn precursors.
- Studying multi-device or context-switching usage where moments are scattered across days.
- Pre-redesign discovery for products with usage that lab studies can't reproduce (sleep apps, journaling, fitness, medication).
- Validating retention drivers — identifying what triggers re-engagement vs. abandonment.
- B2B "day-in-the-life" research where workflows span weeks (procurement, hiring, project planning).

## When NOT to use
- Quick directional input on a feature — too slow; use intercept survey or unmoderated test.
- One-time / rare events that won't surface within reasonable study duration.
- Audiences with low literacy or self-reporting reliability without significant scaffolding.
- Fully synchronous tasks where in-the-moment observation is more valuable (use contextual inquiry).
- Highly regulated domains where ongoing self-reporting risks PII/PHI leak.

## Where it fails / limitations
- Self-report bias: participants under-report negative or embarrassing moments.
- Diary fatigue starts around day 7 in interval-contingent studies; entries collapse to "same as yesterday."
- Participant attrition is high (20–40% over 4 weeks); recruit 30% over target.
- Signal-contingent prompts at random times annoy people in meetings; entries get skipped or dashed off.
- Cross-cultural and translation issues compound across longitudinal entries.
- Ethics review can stall studies for weeks — not a fast research method.

## Agentic workflow
Agents shine in scaffolding (study plan, screener, prompts, reminder cadence), automating follow-ups, and analyzing the corpus of entries (clustering, theme extraction, attrition tracking). Avoid letting an agent generate "synthetic insights" before human-coded baseline; over-fitting to LLM clustering is a known trap. Schedule check-ins via cron / queue, not chat — diary studies live or die on logistics consistency.

### Recommended subagents
- `faion-ux-researcher-agent` — drafts study plan, screener, entry templates, exit-interview script.
- `faion-usability-agent` — secondary pass on coded entries to flag breakdowns and behavioral shifts.
- `password-scrubber-agent` — redact PII before any LLM-side analysis (entries often contain location, names, photos with metadata).
- A scheduled prompt agent (cron + queue) — sends reminder pings, monitors entry rate, escalates inactive participants to the researcher.

### Prompt pattern
```
Generate a diary-study plan from brief.
Inputs: {research_questions, audience, duration_days, capture_method, incentive}
Output:
  type: interval|event|signal-contingent
  prompt_cadence: [...]
  entry_template: structured fields ≤5 questions, each ≤15 words
  reminder_schedule
  attrition_safeguards
  ethics_notes
Cap completion-time-per-entry at 5 min. Flag fields that exceed cap.
```

```
You are coding diary entries.
Schema per entry: {timestamp, location_context, trigger, outcome, sentiment[-2..+2],
                   feature_used[], breakdown_reported (bool), quote (verbatim or null)}.
Never invent quote text. Mark uncertain fields as null.
Output JSONL.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cron` / `systemd timer` | Scheduled prompt dispatch (SMS, email, push) | OS-native |
| `n8n` / `temporal` | Workflow orchestration for reminders + escalations | https://n8n.io / https://temporal.io |
| `pandoc` | Normalize entries (md/docx/csv) for LLM ingestion | https://pandoc.org |
| `whisperx` | Transcribe audio/video diary entries | https://github.com/m-bain/whisperX |
| `taguette` | Free OSS qualitative coding | https://www.taguette.org |
| `jq` / `csvkit` | Wrangle exported entry corpora | https://stedolan.github.io/jq/ |
| `python-twilio` | SMS prompt + ingest for low-friction studies | https://www.twilio.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| dscout | SaaS | Yes (REST + export) | Mobile-native, multimedia, gold standard. |
| Indeemo | SaaS | Partial | Strong video diary; webhook-based export. |
| Revelation | SaaS | Yes | Enterprise multi-method; tagging API. |
| Lookback | SaaS | Limited | Better for moderated; diary as add-on. |
| Userbrain / Userlytics | SaaS | Partial | Lightweight; less ideal for true longitudinal. |
| Typeform / Google Forms + Twilio | DIY | Yes | Cheapest route; fragile for media-rich entries. |
| Telegram / WhatsApp Business API | Messaging | Yes | High response rates in regions where SMS is dead. |
| Notion / Airtable | DIY data store | Yes (REST) | Lightweight backend for collected entries. |

## Templates & scripts
See `templates.md` for study plan + entry templates. Inline reminder cadence helper:

```python
# diary_reminders.py — emit per-participant reminder schedule
import json, datetime as dt, sys
study_start = dt.date.fromisoformat(sys.argv[1])
days = int(sys.argv[2])
participants = json.load(open(sys.argv[3]))  # [{id, channel, tz}]

schedule = []
for p in participants:
    for d in range(days):
        date = study_start + dt.timedelta(days=d)
        # heavier reminders early (build habit), lighter mid-study, check-in near end
        send = d < 3 or d % 3 == 0 or d == days - 1
        if send:
            schedule.append({"pid": p["id"], "channel": p["channel"], "tz": p["tz"],
                             "date": date.isoformat(), "type": "prompt"})
print(json.dumps(schedule, indent=2))
```

## Best practices
- Pilot with 2 participants for 3 days before launch — every logistic bug surfaces here.
- Cap entry time at 5 minutes; over that, attrition spikes.
- Vary the prompt — repeated identical prompts degrade response quality after day 4.
- Use mixed media (text + photo + voice) selectively; photo-only studies miss context, voice-only studies hide breakdowns.
- Run a weekly micro-interview (15 min) per participant to clarify ambiguous entries while context is fresh.
- Pay incentives in tranches (signup, mid-study, exit-interview) — flat one-shot payment increases drop-off.
- Plan analysis incrementally — don't accumulate 4 weeks of entries before starting to code.

## AI-agent gotchas
- LLMs synthesize patterns that don't exist in sparse longitudinal data; force per-entry citation when reporting themes.
- Sentiment scoring of self-report drift is noisy; treat as directional signal, not metric.
- Photo entries often contain inadvertent PII (faces, addresses). Redact before any cloud upload.
- Reminder dispatch via LLM-orchestrator can hallucinate participant phone numbers; pin to a verified participant table, never free-form.
- "Signal-contingent" implementations need true random schedule with per-participant tz; agents default to UTC and disrespect local norms.
- Cross-language studies: never auto-translate during analysis; quote in source language, translate at reporting time only.

## References
- Nielsen Norman Group, *Diary Studies*. https://www.nngroup.com/articles/diary-studies/
- Bolger, Davis, Rafaeli, *Diary Methods: Capturing Life as it is Lived* (Annual Review of Psychology, 2003).
- Csikszentmihalyi & Larson, *Validity and Reliability of the Experience-Sampling Method* (1987).
- dscout, *Practical Guide to Running Diary Studies*. https://dscout.com/people-nerds/diary-studies
- Interaction Design Foundation, *How to Conduct Diary Studies*. https://www.interaction-design.org/literature/article/how-to-conduct-diary-studies
- Smashing Magazine, *Longitudinal UX Research with Diary Studies* (2019).
