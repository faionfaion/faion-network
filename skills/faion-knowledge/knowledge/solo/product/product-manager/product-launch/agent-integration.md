# Agent Integration — Product Launch

## When to use
- Public release with a coordinated marketing moment (Product Hunt, press, partner amplification).
- Major version bump where existing users need migration messaging plus net-new acquisition push.
- Beta-to-GA transition where pricing, positioning, or the audience changes.
- Geographic / segment expansion of an existing product into a new market.

## When NOT to use
- Bug-fix releases or quiet shipping behind a feature flag — use a release-notes template, not a launch playbook.
- Solo founder shipping iteratively to <100 users — the playbook overhead drowns the work; ship to a Discord and write a tweet.
- Internal tools — coordinate with stakeholders, but the GTM machinery is theatre.
- Markets where "loud launch" backfires (regulated industries, B2B enterprise where field sales owns timing).

## Where it fails / limitations
- The 8-week timeline assumes a marketing function exists; for a solo PM the same checklist takes 12-16 weeks of part-time work.
- Product Hunt mechanics change roughly yearly (hunter rules, comment weighting, "ship" vs "launch"); a stale playbook will rank #14, not #3.
- Coordinating across timezones for a 12:01 AM PT launch with a global team breaks family/sleep — burnout factor is real and rarely tracked.
- "All-channels-same-day" maximizes spike but tanks long-tail; some products do better with a 2-week drip launch.
- Press pickup is unpredictable — counting on it as a launch pillar means 60% of launches fall flat.

## Agentic workflow
Spin up a launch-planner agent that takes (product, audience, launch type, target date) and produces the timeline + asset checklist + channel matrix. Hand each asset row to a copy agent that drafts variants per channel (tweet thread, LinkedIn post, PH tagline, email subject lines), and a checklist agent that converts the timeline into dated GitHub issues or Linear tasks. On launch day, run a monitor agent that tails analytics and a social-listening agent that flags negative sentiment > threshold for human triage. After T+1 week, a retrospective agent diffs target metrics vs actuals.

### Recommended subagents
- `faion-mlp-impl-planner-agent` — drafts the launch plan timeline and owner assignments (named in the README).
- A copy-variant agent (Sonnet) — generates 5-10 variants per channel from a single positioning brief.
- A monitor agent — polls PH ranking, Twitter mentions, signup metrics on launch day; pings human on anomalies.
- `faion-sdd-executor-agent` — handles last-mile shipping tasks (final deploys, feature flags) as SDD tasks.

### Prompt pattern
```
Given product=<name>, audience=<persona>, launch_type=<soft|beta|full>, date=<YYYY-MM-DD>:
Produce the T-8 to T+2 timeline as a markdown table with columns
[week, date, deliverable, owner, blocker_signal].
For each deliverable add 1-line "definition of done".
Cross-reference the asset checklist so no row is orphaned.
```

```
Given the launch plan in <plan.md> and channel=<twitter|linkedin|product_hunt|email>:
Generate 5 copy variants per channel.
Each variant: hook (max 12 words) + body + CTA. No emojis unless brand uses them.
Tag each variant with the angle: {pain, outcome, social_proof, contrarian, builder_story}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh release create` | Tag the launch artifact, attach assets, generate changelog | https://cli.github.com/manual/gh_release_create |
| `producthunt-cli` (community) | Check launch ranking via PH GraphQL | https://api.producthunt.com/v2/docs |
| `tweepy` / `twitter-api-v2` | Schedule and publish thread on launch day | https://docs.tweepy.org |
| `mailgun` / `resend` CLI | Send announcement blast with idempotency | https://resend.com/docs |
| `umami-cli` / `plausible` API | Pull launch-day traffic spikes from privacy-first analytics | https://plausible.io/docs |
| `slack` / `discord` webhooks | Push live launch metrics to team channel every 15 min | https://api.slack.com/messaging/webhooks |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Product Hunt | SaaS | Partial (read-only API; submission is web UI) | Schedule submission manually; agent can monitor ranking. |
| Beehiiv / ConvertKit / Resend | SaaS | Yes (REST APIs) | Agent drafts and schedules announcement email. |
| Buffer / Hypefury | SaaS | Yes (API) | Schedule cross-channel social blast. |
| Notion / Linear | SaaS | Yes | Track launch checklist with status webhooks. |
| Sentry / Highlight.io | SaaS | Yes | Agent watches launch-day error rate; auto-pages on regression. |
| LaunchList / Tally | SaaS | Yes | Pre-launch waitlist building with API for export. |
| Plausible / Fathom | SaaS | Yes | Privacy-first analytics; clean API for launch-day tracking. |

## Templates & scripts
See `templates.md` for the launch plan and launch-day checklist. Inline launch-day status poller:

```bash
#!/usr/bin/env bash
# launch-pulse.sh — every 5 min, post current metrics to Slack
set -euo pipefail
SLACK_WEBHOOK="${SLACK_WEBHOOK:?set SLACK_WEBHOOK}"
PLAUSIBLE_TOKEN="${PLAUSIBLE_TOKEN:?}"
SITE="${SITE:?your-domain.com}"

while true; do
  signups=$(curl -s "https://api.your-app/metrics/signups/today" | jq -r .count)
  visitors=$(curl -s -H "Authorization: Bearer $PLAUSIBLE_TOKEN" \
    "https://plausible.io/api/v1/stats/aggregate?site_id=$SITE&period=day&metrics=visitors" \
    | jq -r .results.visitors.value)
  msg="Launch pulse — visitors: $visitors, signups: $signups, $(date -u +%H:%MZ)"
  curl -s -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"$msg\"}" "$SLACK_WEBHOOK" >/dev/null
  sleep 300
done
```

## Best practices
- Lock the launch date 2 weeks out and treat it as immovable; sliding once erodes team trust and breaks partner commitments.
- Tuesday or Wednesday, mid-month, avoid US holidays and major industry events (re:Invent, Google I/O, WWDC weeks).
- Pre-build a "rollback narrative" — a 200-word post explaining why the launch was paused; if you never publish it, fine.
- Have one launch DRI who can say no to feature creep in the last 72 hours; everyone else is in support mode.
- Capture testimonials in the 48 hours after launch — that is when goodwill is highest and converts to permission to quote.
- Run a 30-min postmortem within 7 days; otherwise lessons evaporate as the team moves on.
- For Product Hunt: warm hunters 4 weeks out, never beg for upvotes publicly, comment within first hour.

## AI-agent gotchas
- LLMs over-promise the launch outcome ("100K signups, top of PH"). Force them to use historical baselines from comparable launches as anchors, not aspirational numbers.
- Copy agents inflate adjectives ("revolutionary", "game-changing"). Add a banned-words list to the prompt: revolutionary, game-changing, leverage, paradigm, seamless, robust, cutting-edge.
- Auto-publishing to social on launch day is a reputational landmine — always require a human approval gate between agent draft and `POST` to the network.
- Agents will happily write 50 social posts; the diminishing return is brutal after 5-8 per channel. Cap output explicitly.
- Human-in-loop checkpoint: T-7 days, a human reads the full asset bundle out loud — typos, broken links, wrong screenshot. LLMs miss visual issues.
- Human-in-loop checkpoint: T-Day morning, kill switch is held by a human, not the agent. Agents that auto-roll-back on noise (Twitter snark) will rollback unnecessarily.
- Do not let the agent draft the post-launch retrospective from metrics alone — it will produce a self-congratulatory artifact. Force it to interview 3 customers first.

## References
- April Dunford, "Obviously Awesome" — positioning before launch.
- Lenny Rachitsky — Product Hunt launch playbook: https://www.lennysnewsletter.com/p/how-to-launch-on-product-hunt
- Product Hunt official launch guide: https://www.producthunt.com/launch
- Atlassian launch checklist template: https://www.atlassian.com/team-playbook/plays/launch-plan
- Reforge "GTM for product launches": https://www.reforge.com/blog
