# Agent Integration — Diary Study (Basics)

## When to use
- Studying behavior over time: onboarding journey, habit formation, multi-device usage, long-term feature adoption.
- Capturing in-the-moment context (location, mood, environment) that lab studies erase.
- Pre-purchase consideration journeys for high-consideration products (cars, software platforms, B2B tools).
- Validating retention drop-off hypotheses by tracking individual usage trajectories.

## When NOT to use
- Need answer in <2 weeks — minimum useful diary period is 7-14 days.
- Single isolated event with no context dependency — a post-event interview is faster.
- Sensitive personal contexts where continuous self-documentation would feel surveillance-like (mental health, finances) without ethics review.
- Tightly observable behaviors already covered by product analytics — diary adds noise, not signal.

## Where it fails / limitations
- Participant fatigue: dropoff after day 7-10 unless re-engaged. Studies >3 weeks lose 30-50% of entries.
- Selection bias: people willing to journal twice daily for a month are not your average user.
- Self-report drift: entries early in the study are detailed; late entries become "same as yesterday".
- Recall bias on event-contingent prompts: "log every time you used the app" → users batch-log at end of day, losing in-the-moment context.
- Data is messy: photos, voice notes, free-text, ratings — synthesis is expensive without tooling.

## Agentic workflow
Agents run the operational backbone: scheduled prompts, reminder cadence, multimodal entry intake (text + image + audio), per-participant compliance dashboards, and rolling theme synthesis. Humans do recruitment screening, exit interviews, and final interpretation. A coordinator agent manages each cohort: it schedules prompts, ingests entries, transcribes audio/video locally, classifies entry quality (usable / vague / off-topic), nudges low-compliance participants, and produces weekly synthesis snapshots for the researcher.

### Recommended subagents
- `faion-ux-researcher-agent` — owns the protocol, designs entry templates, performs final synthesis.
- `faion-product-manager` — converts diary themes into opportunity statements + roadmap signals.
- `faion-content-marketer` — extracts user-language vocabulary surfacing in entries.
- `faion-llm-integration` (geek) — operationalizes multimodal ingestion (Whisper transcription, image captioning).
- `faion-data-analyst` style subagent — computes compliance and engagement metrics per participant.

### Prompt pattern
Per-entry classification:
```
Entry: {text}
Attached media: {image_caption_if_any}
Classify: usable | vague | off-topic. If usable, extract: trigger, context (location/time/mood), task, outcome (success/failure/partial), notable quote. Return JSON.
```
Weekly synthesis:
```
Entries from week {n}, segment {seg}: {entries_json}
Identify 3-5 emergent themes. For each: theme, count of entries supporting, representative quote with participant_id, change vs week {n-1}. Flag any themes weakening (was strong, now absent).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Twilio CLI | SMS reminders + entry collection | `npm i -g twilio-cli` |
| Telegram Bot API | Multimodal entry intake (text/photo/voice) | https://core.telegram.org/bots/api |
| WhatsApp Business API | Higher-engagement intake in many markets | https://developers.facebook.com/docs/whatsapp |
| OpenAI Whisper | Local transcription of voice diary entries | `pip install openai-whisper` |
| Anthropic SDK + vision | Image-entry captioning + theme extraction | `pip install anthropic` |
| `cron` / systemd timers | Schedule daily prompt jobs | builtin |
| `pandas` | Compliance + engagement metrics per participant | `pip install pandas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| dscout | SaaS | Yes — REST API | Mobile-native, multimedia diary; gold standard |
| Indeemo | SaaS | Yes — API | Video diaries; mobile app |
| Revelation | SaaS | Partial | Enterprise; multi-method (diary + community + survey) |
| Recollective | SaaS | Yes — API | Async + live blend; tagging tools |
| Lookback | SaaS | Partial | Video-heavy; diary + live combo |
| Ethnio | SaaS | Yes | Recruitment + intercept tied to diary entries |
| Telegram + custom bot | OSS | Yes | DIY; cheap; works in many emerging markets |
| Airtable + automations | SaaS | Yes — API | Lightweight DIY, good for small N |
| Dovetail | SaaS | Yes — API | Tagging + theme synthesis workspace |
| Marvin / Condens | SaaS | Yes | Research repository; agents post entries + tags |

## Templates & scripts
See `templates.md` for daily and event-based entry templates. Minimal Telegram-bot intake skeleton:

```python
# diary_bot.py — text + photo + voice intake → JSONL + Whisper transcript
import json, os, datetime, pathlib
from telegram.ext import Application, MessageHandler, filters

LOG = pathlib.Path("entries.jsonl")
app = Application.builder().token(os.environ["TG_TOKEN"]).build()

async def on_msg(update, ctx):
    msg = update.message
    entry = {
        "ts": datetime.datetime.utcnow().isoformat(),
        "participant_id": msg.from_user.id,
        "text": msg.text or msg.caption or "",
    }
    if msg.photo:
        f = await msg.photo[-1].get_file()
        path = f"media/{msg.message_id}.jpg"
        await f.download_to_drive(path)
        entry["photo"] = path
    if msg.voice:
        f = await msg.voice.get_file()
        path = f"media/{msg.message_id}.ogg"
        await f.download_to_drive(path)
        entry["voice"] = path
        # transcribe locally with whisper after-the-fact
    with LOG.open("a") as fp:
        fp.write(json.dumps(entry) + "\n")
    await msg.reply_text("Got it — thanks!")

app.add_handler(MessageHandler(filters.ALL, on_msg))
app.run_polling()
```

## Best practices
- Cap the study at 10-21 days for most products; 28+ days only for true habit-formation research.
- Each entry should take <3 minutes for participants. If the form is longer, split into "quick log" + weekly deep-dive.
- Send mid-study check-in calls (15 min) to catch confusion and rebuild commitment. This single intervention lifts compliance noticeably.
- Pay in tranches: e.g. 30% on completion of week 1, 70% at study end. Pre-paid full incentive correlates with mid-study dropout.
- Mix entry formats: text + photo + 30-sec voice. Different participants engage with different modalities; mixed corpora are richer for synthesis.
- Run rolling synthesis from day 3 — late synthesis loses the chance to add probing follow-ups while the study is still live.
- Always conclude with an exit interview (30-45 min) per participant; the diary entries become the *interview script*.

## AI-agent gotchas
- Voice entries with PII (addresses, names, financial info) must be transcribed locally (Whisper) before any cloud LLM step. dscout and similar SaaS hold raw audio — verify data residency before uploading.
- LLM theme synthesis over-clusters early entries; force per-week themes and require the model to surface "themes that emerged this week vs prior weeks" so evolution isn't flattened.
- Image entries: vision models often miss the actual subject (caption a "kitchen counter with phone" as "domestic interior"). Pair vision caption with the participant's text caption — never rely on the vision model alone.
- Reminder fatigue: automated nudges feel spammy after the third unanswered prompt. Switch to a single human-style check-in DM after two missed days.
- Compliance metrics ("X entries received") hide entry quality. Run a quality classifier and report "usable entries" separately.
- Do not let an agent autonomously decide to extend the study or ask additional questions — protocol changes mid-study invalidate cross-participant comparison and need researcher approval.
- Prompt caching: when batch-classifying entries, cache the rubric + study context as a system prompt to cut cost ~80% across a cohort.

## References
- Nielsen Norman Group — Diary Studies: https://www.nngroup.com/articles/diary-studies/
- dscout — People Nerds Diary Study Guide: https://dscout.com/people-nerds/diary-studies
- Csikszentmihalyi & Larson — Experience Sampling Method (academic foundation)
- Smashing Magazine — Diary Studies in UX: https://www.smashingmagazine.com/2019/05/diary-study-ux-research/
- Whisper repo: https://github.com/openai/whisper
