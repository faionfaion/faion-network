# Agent Integration — Internationalization

## When to use
- Product is shipping into a second locale or already has user demand from non-English speakers.
- Legal / contractual obligation (EU CRA, French Toubon law, Quebec Bill 96, accessibility regs).
- Externalising hardcoded strings before translation work begins (any subsequent edits cost 5–10× more in translated apps).
- Adding RTL support (Arabic, Hebrew, Persian) — must be designed in, not retrofitted.
- Standardising date/number/currency formatting across services (e.g., backend → email → mobile must agree).

## When NOT to use
- Single-locale internal tool with no plan to expand — i18n adds extraction, build-time, and reviewer overhead.
- Marketing landing pages best handled by a translation CMS (Phrase, Lokalise, Crowdin) rather than code.
- Domain-specific jargon that doesn't translate (e.g., crypto trading lingo) — keep English; localise only the chrome.
- "We'll just use Google Translate at runtime" — fluency is too low for product UI; only acceptable for user-generated content snippets.

## Where it fails / limitations
- String concatenation: `"Hello, " + name + "!"` doesn't translate; word order varies (Japanese "name-さん, hello"). Use ICU MessageFormat with placeholders.
- Plural rules differ wildly (English: 2 forms; Russian/Ukrainian: 3; Arabic: 6). Naive `if n == 1 ... else` breaks in 90% of locales.
- Date/number formats: `1,234.56` (en) vs `1.234,56` (de) vs `1 234,56` (fr); `MM/DD/YYYY` is local to the US. Use ICU / `Intl` not `strftime`.
- Hardcoded widths: 30%+ longer German strings overflow buttons; 200%+ on Arabic/Hebrew with diacritics.
- Bidirectional text (LTR + RTL mixed) needs `dir="auto"`/Unicode bidi controls; CSS `text-align: left` becomes wrong on RTL — use `start`/`end`.
- Locale detection from `Accept-Language` alone is insecure for user prefs (changes per device); persist a chosen `locale` per user in DB.
- Translator return: missing keys, broken placeholders (`{name}` typed `{Name}`), HTML re-escaped wrong. Need lint on `.po`/`.json` import.

## Agentic workflow
Externalise first: agent runs an extraction pass over the codebase (`pybabel extract`, `i18next-parser`, `formatjs extract`) and inserts `t("...")` calls; PR is reviewed for missed strings via grep for hardcoded text. CI lints message catalogues for ICU validity (`gettext-lint`, `i18n-ally`, `formatjs lint`). Pseudo-localisation in CI to surface truncation early. Translation memory (Crowdin/Lokalise/Phrase) connected via API; agent uploads new keys, downloads completed translations, and commits the JSON/PO files back. Agent should NEVER auto-translate user-facing strings via LLM into production without human review for tone and terminology.

### Recommended subagents
- `faion-sdd-executor-agent` — drives extraction → key naming → ICU rewrite → catalogue upload sequentially.
- A custom `i18n-extraction-reviewer` agent that scans the diff for any literal user-visible string and flags it.
- `simplify` skill — collapse duplicate keys after extraction.

### Prompt pattern
```
Externalize all user-visible strings in <path>.
Constraints:
- Use ICU MessageFormat: plurals via {n, plural, one{...} other{...}}, gender via select.
- Key naming: <component>.<element>.<purpose> (e.g., checkout.button.submit).
- Never concatenate translated parts; one message = one full sentence with placeholders.
- For dates/numbers/currency, use Intl.DateTimeFormat / Intl.NumberFormat (or babel.numbers) — no strftime.
- Output: code patch + new entries appended to en.json (others empty).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Babel (Python) | Locale data, `pybabel extract/init/update/compile` | `pip install babel` |
| GNU gettext (`xgettext`, `msgfmt`, `msgmerge`) | Universal i18n toolchain | system pkg |
| i18next + i18next-parser | JS/TS string extraction + i18next runtime | `npm i -D i18next-parser` |
| FormatJS (`@formatjs/cli`) | ICU compiler, lint, extract | `npm i -D @formatjs/cli` |
| react-intl / next-intl / vue-i18n | Framework runtimes | npm |
| Polyglot.js / LinguiJS | Lightweight runtime alternatives | npm |
| ICU4C / icu4j | Reference ICU implementations | system |
| Pseudoloc / `psh` | Pseudo-localisation generator | `npm i -D pseudoloc` |
| crowdin-cli / lokalise-cli2 / phrase-cli | TMS sync | npm / brew |
| ftl (Fluent) tools | Mozilla Fluent format | github.com/projectfluent |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Crowdin | SaaS | Yes — REST + CLI | Branching, glossary, machine-translation suggestions; popular for OSS. |
| Lokalise | SaaS | Yes — REST + CLI | Strong API, key-namespacing, screenshot context. |
| Phrase (formerly PhraseApp) | SaaS | Yes — REST + CLI | Enterprise-grade workflow + Memsource integration. |
| Tolgee | OSS + SaaS | Yes — REST + CLI | In-context editing; great for solo / small team. |
| Weblate | OSS | Yes — REST | Self-host translation platform; OSS-friendly licence. |
| Transifex | SaaS | Yes — REST | Long-standing TMS. |
| DeepL API | SaaS | Yes — REST | High-quality MT; use as draft, not final. |
| Google Cloud Translation / Azure Translator | SaaS | Yes | Lower-cost MT for bulk drafts; QA still needed. |
| Locize | SaaS | Yes — REST | Tight i18next integration. |

## Templates & scripts
See `templates.md` and `examples.md` for Babel + i18next setup. Pseudo-localisation pre-commit guard:

```python
# scripts/pseudo_loc.py — generate test catalogue with [Ⱡǿřȅḿ] padding to surface truncation
import json, sys, pathlib
EN = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
data = json.loads(EN.read_text())
def pseudo(s: str) -> str:
    pad = "~~" * max(1, len(s) // 3)  # 30% longer
    return f"[!!{s}{pad}!!]"
def walk(obj):
    if isinstance(obj, dict): return {k: walk(v) for k, v in obj.items()}
    if isinstance(obj, str):  return pseudo(obj)
    return obj
OUT.write_text(json.dumps(walk(data), ensure_ascii=False, indent=2))
```

## Best practices
- One message = one complete sentence; never compose from fragments.
- Use ICU MessageFormat for plurals, gender, select; do not invent your own placeholder syntax.
- Key naming: hierarchical and stable (`checkout.button.submit`), never the English text as the key — refactors break translations.
- Locale priority: explicit user setting > account default > `Accept-Language` > geo-IP > app default. Persist user choice in DB.
- Keep one source-of-truth catalogue (English / source) in git; everything else flows through TMS.
- Run pseudo-loc in staging permanently — surfaces hardcoded strings, truncation, RTL bugs before translators get involved.
- Test RTL: `dir="rtl"` on `<html>` flips layout; use `start`/`end` (CSS logical properties), not `left`/`right`.
- Number/currency/date through `Intl.*` (JS) / `babel.numbers` / `babel.dates` (Python) / `ICU` (Java/Go/Rust) — never `strftime` and never string-concat currency symbols.
- Don't translate technical strings (API errors, log messages); translate only user-visible UI.

## AI-agent gotchas
- Agents extract strings but use English as the key (`t("Submit order")`); breaks when copy is changed slightly. Force hierarchical keys.
- LLMs concatenate: `t("greeting") + " " + name + "!"` — fails translation. Force single-string ICU placeholders.
- "Plural" handling: agents write `if (n === 1) ... else ...` — wrong for Slavic, Arabic, Welsh. Force ICU `{n, plural, ...}`.
- `Accept-Language` parsing in agent code often picks the first tag without weighting `q` values; users on multilingual systems get the wrong locale.
- Currency formatting: `f"${amount:.2f}"` is wrong for everyone outside USD. Force `Intl.NumberFormat("xx-XX", {style:"currency", currency: code})`.
- Auto-translation via LLM: agents will offer to "translate everything to UK" — do NOT ship without human review; tone, formality, false friends.
- Right-to-left: agents flip `text-align: right` instead of using logical `text-align: end`; bidirectional embed tags get lost on copy-paste through the LLM.
- HTML inside translations: agents allow free-form HTML; translators inject XSS or mangle tags. Use placeholders (`<0>...</0>`) and re-render.
- Human-in-loop checkpoint: every catalogue release goes through a native-speaker reviewer; agent's role is to extract, lint, and sync — never to ship strings unreviewed.

## References
- ICU User Guide — https://unicode-org.github.io/icu/userguide/
- ICU MessageFormat — https://unicode-org.github.io/icu/userguide/format_parse/messages/
- CLDR — https://cldr.unicode.org/
- W3C Internationalization — https://www.w3.org/International/
- MDN Intl — https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
- Mozilla Fluent — https://projectfluent.org/
- i18next — https://www.i18next.com/
- FormatJS — https://formatjs.io/
- Babel (Python) — https://babel.pocoo.org/
