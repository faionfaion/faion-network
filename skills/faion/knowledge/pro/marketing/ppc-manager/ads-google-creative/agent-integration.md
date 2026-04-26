# Agent Integration — Google Ads Creative & Copy

## When to use
- Bulk-generating Responsive Search Ads (RSAs) across many ad groups for an SMB or e-com catalog.
- Refreshing creative for ad groups whose Ad Strength is "Poor" or "Average".
- Localizing winning ads into N languages while preserving the strongest hooks.
- Producing variations for systematic A/B tests (hook vs benefit vs proof).
- Bringing existing ETAs (legacy Expanded Text Ads) into RSA format with full 15 headlines / 4 descriptions.

## When NOT to use
- Highly regulated verticals (medical, finance, gambling) — agent-generated copy almost certainly violates platform policy on claims; route through human compliance.
- Branded campaigns with strict legal-approved copy — the win from variation is small, the legal risk is large.
- Performance Max — copy lives in asset groups, not RSAs; use the pmax methodology instead.
- Account already at "Excellent" Ad Strength with stable CTR — refreshing top performers usually drops CTR before it lifts.

## Where it fails / limitations
- Google's Ad Strength score rewards diversity even when diverse headlines hurt CTR — chasing "Excellent" can lower performance.
- 30-char headline limit cuts most agent output mid-word; agents must validate `len(s) <= 30` per asset, not just trust the LLM.
- Pinning destroys Smart Bidding's ability to combine assets — only pin when legally required (claim, brand mark).
- Disapprovals come 24-48h after upload; agents that publish-and-walk-away leave dead campaigns running on a single approved RSA.
- Google quietly rewrites RSAs via "automatically created assets" — the variant your agent wrote may not be the one that served.

## Agentic workflow
Two-stage pipeline: (1) **strategy agent** picks angles per ad group from keyword intent + competitor scan + brand brief; (2) **copy agent** generates 15 headlines + 4 descriptions per angle, validates char counts, dedupes, scores readability. A reviewer agent (or human) then approves before push to API. After 7-14 days, an analyzer agent reads asset-level performance, kills "low" assets, requests new variations matching what won.

### Recommended subagents
- `faion-ads-agent` — owns Google Ads API, RSA mutations, asset performance pulls.
- `faion-marketing-manager` — picks angles, defines USPs, supplies social proof numbers.
- `faion-improver` — closes the loop: assets labeled "Low" → request replacements; "Best" → request similar-style variations.

### Prompt pattern
```
For ad group "{name}" with keywords {kw_list} and landing page {url}, write
an RSA: 15 headlines (≤30 chars each, all unique, include keyword in 2-3),
4 descriptions (≤90 chars, use full length). Mix benefit/proof/CTA/urgency.
Output as JSON {headlines: [...], descriptions: [...]}. No emojis. No claims
that need disclaimer (best, #1, guaranteed). Do NOT pin.
```

```
Audit RSAs in account {cid}. For each ad with Ad Strength <= Average:
list its assets with PerformanceLabel = LOW or LEARNING. Propose 5
replacement headlines per LOW asset, matched to the angle of the BEST asset.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` SDK | Bulk-create RSAs via API | `pip install google-ads` |
| Google Ads Editor | Desktop bulk-edit, offline preview | https://ads.google.com/home/tools/ads-editor |
| `gaarf` | Pull asset-level performance to CSV | `pip install google-ads-api-report-fetcher` |
| Anyword / Copy.ai / Jasper | Hosted copy generators (API) | Various |
| `pyahocorasick` | Fast keyword-presence checks at scale | `pip install pyahocorasick` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads API | SaaS API | Yes | `AdGroupAdService.mutate_ad_group_ads` for RSA upload |
| Optmyzr Copy Suggestions | SaaS | Partial | UI-driven, has API in Pro tier |
| Anyword | SaaS API | Yes | Predicts performance score per variation |
| SEMrush Ad Builder | SaaS | Limited | Manual workflow, scrape competitors first |
| SpyFu | SaaS | Yes | Pull competitor ad copy via API for inspiration |
| Adalysis | SaaS | Limited | Audit RSAs, manual export |

## Templates & scripts
See `templates.md` for the RSA structure. Inline char-validator + RSA mutation builder — the most error-prone step:

```python
def build_rsa_operation(client, customer_id, ad_group_id, headlines, descriptions, final_url):
    """Build an RSA upload op with strict char-limit checks."""
    assert 3 <= len(headlines) <= 15, "RSA needs 3-15 headlines"
    assert 2 <= len(descriptions) <= 4, "RSA needs 2-4 descriptions"
    bad_h = [h for h in headlines if len(h) > 30]
    bad_d = [d for d in descriptions if len(d) > 90]
    if bad_h or bad_d:
        raise ValueError(f"Over-limit: H={bad_h} D={bad_d}")
    if len(set(headlines)) != len(headlines):
        raise ValueError("Duplicate headlines — Google rejects")

    op = client.get_type("AdGroupAdOperation")
    aga = op.create
    aga.ad_group = client.get_service("AdGroupService").ad_group_path(customer_id, ad_group_id)
    aga.status = client.enums.AdGroupAdStatusEnum.PAUSED  # always upload paused
    ad = aga.ad
    ad.final_urls.append(final_url)
    rsa = ad.responsive_search_ad
    for h in headlines:
        a = client.get_type("AdTextAsset"); a.text = h
        rsa.headlines.append(a)
    for d in descriptions:
        a = client.get_type("AdTextAsset"); a.text = d
        rsa.descriptions.append(a)
    return op
```

## Best practices
- Generate 20+ headline candidates, then dedupe and pick 15 — LLMs repeat themselves on first pass.
- Validate `len(asset) <= 30` after every transform (translation, capitalization, casing) — non-ASCII chars eat budget unpredictably.
- Always upload new RSAs as `PAUSED`, run a manual eyeball, then enable. Disapprovals on enabled ads tank the ad group.
- Run a "competitive scan" once per quarter: Google's Auction Insights + Meta Ad Library for the brand's competitors → feed angles to the copy agent.
- Don't pin unless legally required. Pinning kills the Smart Bidding asset combiner and usually drops CTR 10-20%.
- For multilingual accounts, generate native — never translate. Translated EN→ES headlines clip at 30 chars and read awkwardly.

## AI-agent gotchas
- LLMs love forbidden words: "best", "#1", "guaranteed", "free" (when not free) — Google policy disapproves; lint output for a banned-words list.
- Char count in Python `len()` differs from Google's count for emojis and accented chars — test with the API's `validate_only=True` before bulk publish.
- Agents will write 15 paraphrased versions of the same headline. Run a similarity check (Jaccard or embedding cosine) before upload, drop dupes.
- Google's "automatically created assets" silently adds AI-generated assets to your RSAs. If brand voice matters, disable per campaign — agents miss this setting.
- Human-in-loop checkpoint: first batch on a new account, regulated verticals, any copy mentioning price/discount/offer that requires legal review.
- Performance labels (`Low`/`Good`/`Best`) need 30+ days of data and meaningful spend — don't let an agent kill assets after 3 days.

## References
- https://support.google.com/google-ads/answer/7684791 (RSA best practices)
- https://support.google.com/google-ads/answer/9989981 (Ad Strength)
- https://developers.google.com/google-ads/api/docs/ads/overview
- https://support.google.com/adspolicy/answer/6008942 (policy violations)
