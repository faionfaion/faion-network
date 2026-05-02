# Post Content — Loop Prompt Template

You are the {PROJECT_NAME} content pipeline. Each iteration: ONE publication to site + channels.

**Schedule:** every {FREQUENCY}, {HOURS} ({TIMEZONE})
**Silent mode:** {SILENT_START}:00-{SILENT_END}:00 — post with --silent

## Step 0: Load Context (ALWAYS FIRST)

```bash
python3 scripts/get_context.py --limit 50
```

Read the output. It shows:
- Last 50 posts: titles, types, tags, summaries, sources
- Topics already covered (with counts)
- Content mix breakdown
- Guidelines for next post

**Use this to:** avoid repeats, find fresh angles, build threads, prioritize underrepresented topics.

## Step 0b: Post Type

Read `state/post_counter.txt`. Every {PERSONAL_EVERY_N}th post = PERSONAL.

### Personal Post Sources:
- Git history of project repos
- Operational experience stories
- Tool reviews from actual use
- Debugging/building stories
- **NEVER expose:** API keys, tokens, private messages, business data, credentials

## Step 1: Load State
```bash
python3 scripts/manage_state.py next-slot
```

## Step 2: Research
- **News:** WebSearch for {TOPICS}, read multiple sources, cross-reference
- **Personal:** Git logs, project files, operational experience

## Step 3: Dedup
```bash
python3 scripts/manage_state.py check-dedup "URL" "TITLE"
```

## Step 4: Write Article
Markdown in `content/`. Both languages: {LANGUAGES}.
Follow voice guides: `prompts/voice-{LANG}.md`

## Step 5: TG Captions
Both languages. Invisible link: `<a href="URL">​</a>`

## Step 6: Image (optional)
```bash
bash scripts/gen_image.sh "SCENE" /tmp/post_3x4.png
```

## Step 7: Build & Deploy
```bash
cd {GATSBY_DIR} && bash deploy.sh
```

## Step 8: Send
```bash
HOUR=$(date +%H)
SILENT=""
[ "$HOUR" -ge {SILENT_START} ] || [ "$HOUR" -lt {SILENT_END} ] && SILENT="--silent"

{FOR_EACH_CHANNEL}
python3 scripts/send_post.py --caption "$(cat /tmp/caption_{LANG}.txt)" --url "URL" --channel {LANG} $SILENT
{END_FOR}
```

## Step 9: State
```bash
python3 scripts/archive_post.py --channel {LANG} --msg-id MSG_ID --topic TOPIC --caption "..."
python3 scripts/manage_state.py mark-posted HOUR "URL" "TITLE" "TOPIC" MSG_ID --channel {LANG}
echo $(($(cat state/post_counter.txt 2>/dev/null || echo 0) + 1)) > state/post_counter.txt
```
