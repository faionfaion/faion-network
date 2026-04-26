# Agent Integration — Twitter/X Ads

## When to use
- Targeting tech-savvy / dev audiences for SaaS, dev tools, newsletters, podcasts.
- Building a follower base on a specific niche topic (e.g. AI, crypto, indie hacking).
- Real-time event activation (conferences, product launches, news cycles) where conversation targeting matters.
- Reaching followers of named accounts (competitors, complementary brands, influencers) — Twitter is one of the few platforms where this works directly.

## When NOT to use
- B2C e-commerce with broad consumer audience — Meta and TikTok are 5-10x more efficient on cost per conversion.
- Highly visual / lifestyle products — Twitter creative carries less weight than IG/TikTok.
- Strict brand-safety requirements — post-Musk policy changes mean less control over adjacency.
- Account in a region where X has very low ad inventory (most of EMEA outside the US/UK).

## Where it fails / limitations
- X Ads API access has been gated since 2023; many community SDKs broke. Confirm API tier and price before promising automation.
- Conversion attribution on X is weaker than Meta/Google — pixel coverage drops when users open links in the in-app browser.
- Audience sizes are smaller than reported; "follower lookalikes" of an account with 100K followers may yield a usable pool of only 10-30K active users in a region.
- Disapproval reasons are vague ("violates policy"); appeals are slow and largely manual.
- Engagement metrics (likes, retweets) inflate reported "engagement rate" but rarely correlate with conversions.

## Agentic workflow
A marketing agent picks angles + competitor follower lists; a content agent drafts native-style tweets (no "ad voice"); a publishing agent uploads via X Ads API or n8n. Because attribution is weak, the post-launch agent's main job is to compare on-platform CTR/CPC against landing-page conversion logs from the site's own analytics — never trust X-reported conversions alone. Iterate weekly: refresh creative every 14 days, kill anything below 0.5% CTR after $30 spend.

### Recommended subagents
- `faion-ads-agent` — runs X Ads API mutations, pulls insights.
- `faion-content-marketer` (knowledge tier) — drafts tweet-native copy; doesn't sound like an ad.
- `faion-improver` — weekly diff: on-platform CTR vs site-side conversions vs spend.

### Prompt pattern
```
Write 5 ad tweets for {product} targeting followers of @{competitor1},
@{competitor2}. Each ≤270 chars (leave room for link). Native voice — sounds
like a real account, not a banner. Use one of: problem/solution, social proof,
direct value, contrarian take. No emojis. End with one CTA + link placeholder.
```

```
Audit the last 14 days of campaign {id}. List ad sets with CTR < 0.5% and
spend > $30 (kill list). For survivors, propose 3 variation tweets that keep
the winning hook but rotate the proof point. Cross-check with {analytics}
revenue per click — flag any ad with CTR > 1% but no downstream conversions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| X Ads API (v12+) | Official campaign management | https://developer.x.com/en/docs/x-ads-api |
| `twurl` | Authenticated cURL for X API | `gem install twurl` |
| `python-twitter-ads` (community fork) | Python SDK; check for v12 fork status | https://github.com/xdevplatform/twitter-python-ads-sdk |
| n8n | Glue workflow → X Ads API for non-coders | https://n8n.io |
| `tweepy` | Read-side organic data (to validate audience) | `pip install tweepy` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| X Ads Manager | SaaS | Limited | Official UI; API access tier-gated and pricier than Meta/Google |
| Buffer / Hootsuite | SaaS | Yes | Schedule promoted posts via API, manage paid + organic together |
| Sprout Social | SaaS | Yes | Reporting + paid management, decent API |
| Audiense | SaaS | Yes | Builds custom audiences (TwitterIDs lists) — agent-importable |
| Followerwonk | SaaS | Limited | Audience research; export CSV, agent reads |
| Brandwatch | SaaS | Yes | Conversation/keyword listening — feeds keyword targeting |

## Templates & scripts
See `templates.md` for hook formulas. Inline tailored-audience uploader (the highest-ROI move on X — bring your own list):

```python
import hashlib, requests, os

def upload_tailored_audience(audience_id, emails, bearer):
    """Upload a hashed-email list as a Tailored Audience for retargeting."""
    items = []
    for e in emails:
        h = hashlib.sha256(e.strip().lower().encode()).hexdigest()
        items.append({"operation_type": "Update",
                      "params": {"effective_at": None,
                                 "expires_at": None,
                                 "user_identifier_type": "EMAIL",
                                 "user_identifier": h}})
    url = f"https://ads-api.x.com/12/accounts/{os.environ['X_ACCT']}/custom_audiences/{audience_id}/users"
    r = requests.post(url,
                      headers={"Authorization": f"Bearer {bearer}",
                               "Content-Type": "application/json"},
                      json=items)
    r.raise_for_status()
    return r.json()
```

## Best practices
- Lead with a tailored audience (your email list) for retargeting before any prospecting — X's pixel coverage is too thin for cold scaling.
- "Follower lookalikes" of a competitor is X's killer feature — use it, but pick competitors with > 50K followers for usable pool.
- Never use boosted-tweet style ad creative — make it look like an organic post from a real account, not a banner.
- Cap frequency at ~2 impressions per user per week; X audiences fatigue fast and start replying with hostility.
- Always include a Twitter pixel + UTMs and verify with site-side analytics — don't optimize against X-reported conversions only.
- Test 5+ creatives at launch; expect to kill 4 of them. X creative has a steeper drop-off curve than Meta.

## AI-agent gotchas
- LLM-written tweets sound like LLM-written tweets — humans + reviewers feel it instantly. Always lint for "as a", "in today's fast-paced world", em-dashes pattern.
- The X Ads API is unstable; expect breaking changes between v11/v12/v13. Pin your SDK version and re-test on every minor bump.
- Auto-posting agents can trigger X's spam classifier (especially on new accounts) — warm up the account organically for 30 days first.
- Replies to ads are public and visible to other users — an agent ignoring negative replies leaves them as social proof against you. Either disable replies or have a moderation agent.
- Human-in-loop checkpoint: first ad on a new product, any politically-adjacent topic, any copy that mentions a public figure or competitor by handle.
- Conversion event names matter: X expects exact strings (`Purchase`, `SignUp`, `SiteVisit`) — agents that emit GA4-style names silently fail to optimize.

## References
- https://developer.x.com/en/docs/x-ads-api/campaign-management
- https://business.x.com/en/help/campaign-setup/campaign-targeting.html
- https://business.x.com/en/help/campaign-setup/creative-ad-specifications.html
- https://github.com/xdevplatform/twitter-python-ads-sdk
- https://help.twitter.com/en/business/x-ads-policies
