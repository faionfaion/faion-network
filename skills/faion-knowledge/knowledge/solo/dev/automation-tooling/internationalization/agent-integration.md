# Agent Integration — Internationalization

## When to use
- Externalizing hardcoded strings in an existing single-locale codebase (Python/FastAPI, Django, React/Next, Vue, mobile).
- Adding a second/third locale (especially RTL) and needing to scan layouts for physical CSS properties, fixed widths, hardcoded date/number formats.
- Generating ICU MessageFormat plural/select rules for a target locale (Slavic/Arabic plurals are agent-trap territory).
- Extracting messages, syncing with a TMS (Lokalise/Crowdin/Phrase/Tolgee), and merging back into the repo.
- Bootstrapping `pybabel`, `i18next`, `react-intl`, or `next-intl` configuration end-to-end.

## When NOT to use
- True one-locale-forever apps (internal admin tools, regulated single-market products) — the i18n tax outweighs the value.
- For copywriting/localization quality. Agents extract and wire keys; native human translators decide tone, register, dialect.
- For legal/medical/financial copy in regulated markets — those need certified translators, not LLM output.
- For RTL bidirectional text rendering bugs in libraries — agents can flag them but fixing requires Unicode BIDI expertise.
- When the project uses a proprietary framework with no public message-extraction tooling.

## Where it fails / limitations
- LLM translation quality is non-uniform: strong on EN/ES/DE/FR/UK, weak on low-resource locales (Hausa, Tagalog, Khmer).
- Plural rules: LLMs often emit only `one`/`other` and miss `few`/`many`/`two` for Slavic, Arabic, Welsh.
- Context loss: same EN string ("Open") reused as verb and adjective will be mistranslated without screenshots / `@context` comments.
- Concatenation refactors: agents may turn `"Hello " + name` into `f"Hello {name}"` instead of an ICU template — they must use `{name}` placeholders inside the message string.
- RTL: agents tend to flip layouts globally instead of relying on logical CSS properties; can break LTR rendering.
- Date/number formatting: agents fall back to `toLocaleString()` without specifying calendar, numbering system, or `hourCycle`.
- Key collisions across modules when no namespace convention exists.

## Agentic workflow
Run a two-pass agent: pass 1 extracts strings into messages with stable, dotted keys (e.g. `checkout.cta.pay_now`) and inserts placeholders/ICU; pass 2 validates that no placeholders were dropped, plural rules cover the target locales, and dates/numbers route through `Intl`/Babel formatters. Sync to a TMS via its CLI/API, let humans translate, then pull back and run a build that fails on missing keys. Always check a snapshot of the rendered UI in each locale (Storybook, Percy, Playwright screenshots) — agents cannot judge truncation.

### Recommended subagents
- `general-purpose` — repo-wide string extraction and key-naming refactor.
- `faion-sdd-executor-agent` — when i18n rollout is captured as a multi-task SDD feature.
- A small `i18n-extract` task agent — narrow scope: only edits source files to wrap strings; no other changes. Easier to review.
- A separate `i18n-pluralize` task agent — only fixes plural categories per CLDR rules; output diff over message catalogues.

### Prompt pattern
```
Scan <path> for user-facing strings. For each, replace with t('<dotted.key>')
or <FormattedMessage id="<dotted.key>"/>. Append the EN entry to
locales/en/common.json. Do not translate — leave EN as source of truth.
Skip log lines, exceptions, and admin-only debug strings.
```
```
Given locales/en/messages.json, generate uk/ar/ja entries using ICU
MessageFormat. Preserve all {placeholders}. For plurals, emit all CLDR
categories required by the locale (uk: one/few/many/other; ar: zero/one/two/few/many/other).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pybabel` | Extract / init / update / compile .po/.mo for Python (Babel) | `pip install babel` · babel.pocoo.org |
| `xgettext` / `msgmerge` / `msgfmt` | GNU gettext toolchain | `apt install gettext` |
| `i18next-parser` | Static extraction for i18next/react-i18next | `npm i -D i18next-parser` |
| `formatjs` CLI | Extract + compile for react-intl/FormatJS | `npm i -D @formatjs/cli` |
| `lingui extract` / `lingui compile` | LinguiJS pipeline | lingui.dev |
| `next-intl` | App-Router i18n for Next.js | next-intl.dev |
| `lokalise2` CLI | Push/pull translations to Lokalise | github.com/lokalise/lokalise-cli-2-go |
| `crowdin` CLI | Crowdin sync | crowdin.github.io/crowdin-cli/ |
| `phrase` CLI | Phrase.com sync | phrase.com/cli/ |
| `tolgee-cli` | Tolgee in-context translation sync | tolgee.io |
| `icu-message-format-for-translators` | Lint ICU strings for placeholder/plural drift | npm |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Lokalise | SaaS | Yes | REST + CLI; supports JSON/PO/XLIFF; webhook on translation completion. |
| Crowdin | SaaS | Yes | CLI + REST; in-context proofreading; OSS plan free for public repos. |
| Phrase | SaaS | Yes | Strong CLI, branching, key glossary. |
| Tolgee | OSS + SaaS | Yes | Self-host friendly; in-context editor; ML pre-translate. |
| Weblate | OSS | Yes | Self-host; integrates over Git directly. |
| POEditor | SaaS | Partial | API exists but coarse-grained. |
| Transifex | SaaS | Yes | Standard for OSS. |
| DeepL API | SaaS | Yes | Best raw MT for EN↔EU languages; agents can pre-translate before human review. |
| Google Translate API / Cloud Translation v3 | SaaS | Yes | Wide locale coverage including low-resource. |
| Smartling | SaaS | Partial | Enterprise; complex auth. |

## Templates & scripts
See `templates.md` and `examples.md` for the Babel + FastAPI + react-intl scaffolds. Minimal CI guard against missing keys:

```bash
#!/usr/bin/env bash
# scripts/check-i18n.sh — fail build on missing/extra keys
set -euo pipefail
SRC=locales/en
for L in uk de fr ja ar; do
  diff <(jq -r 'paths(scalars) | join(".")' "$SRC/common.json" | sort) \
       <(jq -r 'paths(scalars) | join(".")' "locales/$L/common.json" | sort) \
    || { echo "Key drift in $L"; exit 1; }
done
echo "i18n keys aligned across locales."
```

```bash
# Extract → push → pull cycle for a typical TS/React project
npx i18next-parser --config i18next-parser.config.js
lokalise2 file upload --token "$LOKALISE_TOKEN" --project-id "$PROJ" \
  --file 'locales/en/*.json' --lang-iso en --replace-modified
lokalise2 file download --token "$LOKALISE_TOKEN" --project-id "$PROJ" \
  --format json --unzip-to ./locales --original-filenames=true
```

## Best practices
- Use ICU MessageFormat from day one — gettext-style `_n` cannot express gender/select cleanly.
- Stable dotted keys (`feature.surface.intent`) survive copy edits; auto-generated hash keys do not.
- Provide translator context: `description`/`@context` comments + screenshots; without them, ambiguous EN strings break.
- Always pseudo-localize during dev (`Ḫèĺĺō`) to surface unwrapped strings, fixed widths, RTL-bleeds before real translation.
- Reserve 30-50% layout headroom — DE/RU/UK strings expand significantly vs EN.
- Use logical CSS properties (`margin-inline-start`, `padding-block`) and `dir="auto"` on neutral content; gate manual overrides behind `[dir="rtl"]`.
- Format dates/numbers/currency through `Intl` (JS) or Babel (Python), never manual string concat — locale-specific separators differ.
- Treat the EN catalogue as source of truth, version it in Git, and make the TMS a one-way sync target except for translations.
- Validate on every PR: every key in EN exists in every shipped locale; ICU placeholders match across locales.

## AI-agent gotchas
- LLMs hallucinate plural categories — verify against CLDR (`Intl.PluralRules`) for each locale.
- Agents may "translate" placeholder names (`{userName}` → `{ім'яКористувача}`); pin placeholders as inviolable.
- Context-free strings cause polysemy errors: a single agent prompt for "translate 'Open' to JA" yields wrong word in 50%+ cases. Provide UI context.
- Auto-extraction often misses dynamic strings built via interpolation, JSX expressions, or template tags. Run a `grep` for likely plain-text patterns post-extraction.
- For RTL, agents over-rotate: they will flip phone numbers, code blocks, and LTR-only content. Mark such regions with `<bdi>` or `dir="ltr"`.
- Date/time agents tend to ignore time zones and calendars. Locale ≠ timezone; pass both explicitly.
- TMS sync: agents can clobber human-reviewed translations on push. Always push EN-only or use `--keep-translations` flags.
- Numeric formatting: 1,000 (US) vs 1.000 (DE) vs 1 000 (FR) vs ١٬٠٠٠ (Arabic) — always go through `Intl.NumberFormat`.

## References
- Unicode CLDR plural rules: https://cldr.unicode.org/index/cldr-spec/plural-rules
- ICU Message Format: https://unicode-org.github.io/icu/userguide/format_parse/messages/
- Babel (Python): https://babel.pocoo.org/
- FormatJS / react-intl: https://formatjs.io/docs/react-intl/
- i18next: https://www.i18next.com/
- next-intl: https://next-intl.dev/
- W3C Internationalization checker: https://www.w3.org/International/
- Mozilla Project Fluent (alternative to ICU): https://projectfluent.org/
