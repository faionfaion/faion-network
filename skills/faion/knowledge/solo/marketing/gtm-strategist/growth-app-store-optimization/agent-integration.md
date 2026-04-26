# Agent Integration — App Store Optimization (ASO)

## When to use
- Initial app listing needs keyword research and metadata optimization before launch
- Organic downloads have plateaued; need keyword gap analysis vs. top competitors
- App icon or screenshot set hasn't been refreshed in 6+ months
- New locale/language is being targeted; need localized metadata
- Conducting monthly ASO audit: keyword rankings, review velocity, conversion funnel
- Bulk-drafting review response templates for negative review categories

## When NOT to use
- App has fewer than 100 active users — prioritize product and retention over ASO; ranking signals depend on engagement
- App is in a category where paid UA (Apple Search Ads, Google UAC) dominates — ASO alone will not move the needle
- Seeking A/B test execution — SplitMetrics and StoreMaven require human setup; agents can advise on variants but cannot run store-side tests
- Localization requiring cultural nuance in high-context markets (Japan, Korea, China) — machine translation of ASO copy is insufficient; native review required

## Where it fails / limitations
- Agents cannot query Sensor Tower, AppTweak, or data.ai directly without API credentials — keyword volume data must be provided as input
- iOS keyword field is 100 chars; agents may generate lists that exceed it or include duplicates of name/subtitle — always validate character counts
- Google Play description keyword density recommendations conflict across sources; agent output should be treated as a draft, not a final
- Review sentiment is a ranking signal agents cannot directly influence — response drafts help but review volume requires in-product prompting
- Store ranking algorithms update frequently (Apple's especially); agent knowledge has a training cutoff

## Agentic workflow
ASO benefits from two distinct agent passes: (1) keyword research and metadata drafting — given a seed keyword list and competitor names, an agent generates prioritized keyword candidates and writes optimized metadata within character limits; (2) review management — given a batch of recent reviews exported from App Store Connect or Google Play Console, an agent categorizes them by sentiment and issue type, and drafts responses for each category. The agent should never submit responses or metadata changes directly; all updates go through the developer console after human review.

### Recommended subagents
- `faion-content-agent` (referenced in README) — metadata copywriting, review response drafts, screenshot text overlay copy
- A `aso-audit-agent` could ingest a monthly keyword ranking CSV and produce the ASO audit template output automatically

### Prompt pattern
```
You are an ASO specialist for [App Name] on iOS and Google Play.
App category: [category]
Target audience: [persona]
Seed keywords: [comma-separated list]
Competitors: [App1, App2, App3]

Task:
1. Generate 20 keyword candidates ranked by estimated relevance (high/medium/low volume, low/medium/high difficulty — use qualitative assessment only; no hallucinated numbers).
2. Write an optimized iOS app name (max 30 chars) and subtitle (max 30 chars) incorporating top keywords.
3. Write iOS keywords field (max 100 chars, comma-separated, no spaces, no duplicates of name/subtitle).
4. Write Google Play title (max 50 chars) and short description (max 80 chars).
Output: structured markdown, character count shown for each field.
```

```
Here are 20 recent 1-2 star reviews for [App]: [reviews as JSON array].
Task:
1. Group by root cause (bug / UX confusion / missing feature / performance / pricing).
2. For each group, draft a response template (max 80 words) using an empathetic, solution-focused tone.
Output: JSON array of {group, count, response_template}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `fastlane` | Automate metadata uploads to both stores; screenshot generation | https://fastlane.tools |
| `fastlane deliver` | Push iOS metadata and screenshots from local files | https://docs.fastlane.tools/actions/deliver/ |
| `fastlane supply` | Push Android metadata and APK/AAB to Google Play | https://docs.fastlane.tools/actions/supply/ |
| App Store Connect API | Pull ratings, reviews, keyword data programmatically | https://developer.apple.com/documentation/appstoreconnectapi |
| Google Play Developer API | Reviews, listings, in-app purchases management | https://developers.google.com/android-publisher |
| `app-store-connect-api-python` | Python SDK for App Store Connect API | https://github.com/codinn/applaud |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Sensor Tower | SaaS | Yes — REST API (paid) | Keyword volume, competitor ranking, review data |
| AppTweak | SaaS | Yes — REST API (paid) | ASO intelligence; keyword difficulty scores |
| data.ai (App Annie) | SaaS | Yes — REST API (paid) | Market data, download estimates |
| SplitMetrics | SaaS | Partial — UI-driven | A/B test store page elements; no automation API |
| Appfollow | SaaS | Yes — REST API | Review management, response automation |
| AppBot | SaaS | Yes — REST API | Sentiment analysis on reviews |
| Mobile Action | SaaS | Yes — REST API | Keyword tracking, competitor monitoring |

## Templates & scripts
See templates.md for: App Store listing checklist, ASO audit template.

Inline script — validate iOS metadata character limits before submission:

```python
def validate_ios_metadata(name: str, subtitle: str, keywords: str) -> list[str]:
    """Return list of validation errors for iOS metadata fields."""
    errors = []
    if len(name) > 30:
        errors.append(f"Name too long: {len(name)} chars (max 30)")
    if len(subtitle) > 30:
        errors.append(f"Subtitle too long: {len(subtitle)} chars (max 30)")
    if len(keywords) > 100:
        errors.append(f"Keywords too long: {len(keywords)} chars (max 100)")

    kw_list = [k.strip() for k in keywords.split(",")]
    name_words = name.lower().split()
    dupes = [k for k in kw_list if k.lower() in name_words or k.lower() in subtitle.lower()]
    if dupes:
        errors.append(f"Keywords duplicate name/subtitle: {dupes}")
    if any(" " in k for k in kw_list):
        errors.append("Keywords field must not contain spaces (use commas only)")

    return errors or ["All fields valid"]
```

## Best practices
- Run keyword research before writing metadata, not after — common mistake is writing copy first, then stuffing keywords in awkwardly
- Screenshot slot 1 and 2 carry ~80% of conversion weight; spend design time there first and treat slots 3-6 as secondary
- Respond to negative reviews within 24-48 hours — review response rate and quality are indirect ranking signals on Google Play
- Update app metadata (What's New / changelogs) with every release; stores use update frequency as a freshness signal
- Use fastlane deliver/supply to manage metadata as code (stored in git) rather than editing in the developer console UI — enables version control and agent-generated updates via PR
- Localize screenshots (text overlay) before localizing keywords — visual content has higher conversion impact per locale investment

## AI-agent gotchas
- Agents will generate keyword volume/difficulty numbers without real data if not constrained — explicitly forbid numerical estimates unless real data is provided as context
- iOS keyword field: agents often include spaces after commas or duplicate terms from the app name — validate programmatically before submission (use the script above)
- Google Play description: agents may keyword-stuff in ways that trigger Play Store spam detection — instruct agent to prioritize readability and limit key term repetition to 3-5 occurrences maximum
- Review responses posted via API are public immediately — always queue for human review before submission; Appfollow and AppBot support approval workflows
- Human-in-loop checkpoint: any metadata change submission requires manual review; automated fastlane delivery should never run without a human-initiated trigger
- Localization: agents translating to Japanese, Korean, or Chinese produce acceptable literal translations but miss cultural nuance in app names and CTAs — flag these locales for native speaker review

## References
- https://developer.apple.com/app-store/product-page/ — Official Apple ASO guidance
- https://developer.android.com/distribute/best-practices/launch/store-listing — Official Google Play listing guidelines
- https://developer.apple.com/documentation/appstoreconnectapi — App Store Connect API reference
- https://developers.google.com/android-publisher — Google Play Developer API reference
- https://docs.fastlane.tools — fastlane documentation for automated metadata management
- https://www.apptweak.com/en/aso-blog — Data-driven ASO strategy articles
