# Ukrainian (uk) translation rules

Source language: English. Translator + reviewer follow this. **V4 doctrine — translate by default; tight English whitelist; cultural adaptation licence for body + headings; English-idiom accuracy; reading-register tilt to native target-language tech-writing. See `phase2-translate.md` and `style-guide.md` for the full v4 contract.**

## Reading register (CRITICAL for v4+)

UA prose targets indie-tech readers, not literary fiction readers. Default tilt:

- **Average sentence length**: ~15-25 words. Max ~40 words. If a sentence runs >40, split.
- **Parentheticals**: limit to 1-2 per sentence. The English source often stacks 3-4 — UA should break them out into separate sentences.
- **Active voice over passive**: "рамка ламає правило" beats "правило ламається рамкою".
- **Direct verb choice over Victorian-essay nominalisation**: "Це коштує голос" beats "Це біт, що вбиває статті, коли його пропускати".
- **Conversational over literary**: "Слухай" / "Дивись" / "Чесно кажу" are fine when they earn their place. "Зверни увагу, що" is corporate-UA filler.

NERO sharpness STAYS. What goes is twistiness — the long compound clauses that translate-literally from English Patio11-relentless register. Sharpness is "Скриншоти оцінюють у нуль розподіл виживання." Twistiness is splitting a single thought across 5 commas, 2 dashes, and a subordinate clause. If you can't read the UA paragraph aloud without running out of breath, split it.

The translator's report includes a READING REGISTER section: average sentence length sampled across 3 random paragraphs, longest sentence in the article (word count), and a one-sentence judgement on native-vs-translated feel.

## Voice (NERO persona transferred)

- Гострий, іронічний, no-fluff. Як IT-блог дорослої аудиторії (DOU.ua, dev.ua), не пресреліз.
- Власна думка завжди. Hedging ("можливо", "ймовірно", "потенційно") різати, якщо це не точне модальне значення.
- Іронія/сарказм де вони підкреслюють реальну точку, не самозамилування.
- "ти" для індивідуальних звернень (читачу, indie-розробнику), "ви" для plural або формального контексту. За замовчуванням: "ти" для solopreneur-audience.
- Питання до читача дозволені й вітаються — створюють діалог.

## Address register

Default: **ти** для одиничного solopreneur-читача. "ви" тільки якщо контекст явно plural (команда, agency) або brief вимагає формального тону.

## Banned: russisms (zero tolerance)

Виправляти ВСІ. Reviewer обов'язково шукає кожен. Скорочений перелік найчастіших (повний список нижче):

| Russism | UA correct |
|---------|-----------|
| приймати участь | брати участь |
| вирішувати проблему | розв'язувати / долати проблему |
| відноситися до | стосуватися / ставитися до |
| на даний момент / у даний час | зараз / наразі |
| у відповідності з | відповідно до |
| так як | оскільки / тому що |
| дякуючи (тому що) | завдяки |
| представляти із себе | являти собою |
| наступити (час, подія) | настати |
| у мене відсутній | у мене немає |
| прийняти рішення | ухвалити рішення |
| на протязі | протягом |
| більше всього | найбільше |
| головним чином | здебільшого / переважно |
| у даному випадку | у цьому випадку |
| знаходитися | бути / перебувати |
| виключно (= лише) | винятково |
| незважаючи на | попри |
| мова йде про | йдеться про |
| виглядіти | виглядати |
| розповсюджувати | поширювати |
| опит | опитування |
| участок | ділянка |

Reviewer звітує точну кількість русизмів знайдено + виправлено.

## Banned: calques from English

| Калька з англ. | UA |
|----------------|-----|
| робити сенс | мати сенс |
| взяти до уваги | врахувати |
| беручи до уваги | з огляду на / враховуючи |
| зробити різницю | стати в нагоді / змінити ситуацію |
| отримати точку | зрозуміти / усвідомити |
| у будь-якому випадку | у будь-якому разі |
| тримати в умі | тримати в голові / пам'ятати |
| глянути з іншої точки зору | поглянути з іншого боку |
| на одній сторінці | в одному руслі / порозумілися |
| в кінці дня (= at the end of the day) | зрештою / врешті |

## V2 anglicism policy — translate by default

Список того, що зберігати англійською, ТІСНИЙ. Все інше — перекладати.

### KEEP English (whitelist)

| English | Reason |
|---------|--------|
| CLI, SDD, MRR, ARR, CAC, LTV, PMF, MVP, SaaS, API, SDK, JWT, KPI, OKR, JTBD, GTM, BDD, TDD, OSS, ICP, NPS, ROI, OOM, CRM, ERP, OTP, MFA, P/E, EV, AOV | Industry acronyms — no UA equivalent |
| runway, churn, burn rate | SaaS metrics — встановлені англіцизми у спільноті |
| faion, faion-cli, faion-network | Brand |
| Stripe, Paddle, Polar, LemonSqueezy, Creem, Mercury, Brex, Wise, Quaderno, Lago, ChartMogul, Baremetrics, ProfitWell, GitHub, Vercel, AWS, GCP, Cloudflare, Gumroad, AppSumo, Indie Hackers, Hacker News | Brand / product names |
| W2, 1099, W-9, LLC, S-Corp, Sole Prop, COBRA, ACA, 401(k), RSU, FEIE | US tax/legal — no UA equivalent |
| slug-format strings, file paths, command names, code blocks | Verbatim from system |

### TRANSLATE (V2 — old practice was too English)

| English | UA target |
|---------|-----------|
| feature | функція (за контекстом — можливість) |
| workflow | процес / робочий потік |
| pattern | патерн (OK — прижилося) АБО шаблон |
| ship (verb) | випустити / відвантажити / релізнути |
| deploy (verb) | розгорнути / задеплоїти (slang OK у voice) |
| burnout | вигорання |
| pivot (noun/verb) | поворот / зміна напряму / переорієнтуватися |
| brokerage | брокерський рахунок |
| moonshot | амбітний експеримент / великий замах |
| sanity check | перевірка здоровим глуздом / здорова перевірка |
| handoff | передача |
| half-step | напівкрок |
| trigger | тригер (OK — прижилося) АБО запуск |
| dashboard | панель / дашборд (OK — прижилося) |
| optics | вигляд / враження |
| haircut (= discount) | дисконт / зріз |
| bookings | замовлення / законтрактовано |
| framework | фреймворк (OK — прижилося в IT) |
| stack | стек (OK — прижилося) |
| onboarding | онбординг (OK — прижилося) АБО введення |
| post-mortem | post-mortem (OK — industry term) АБО розбір |

**Правило**: якщо є точне українське слово — використовуй його. v1 articles err'или в бік English; reset to err у бік української.

## Ambiguous calques — ADAPT to the reader (CRITICAL)

Translation — це не дослівність. Це **доставка змісту читачеві у його мовній моделі**. Якщо UA-слово зберігає форму англійського джерела, але змінює (або ламає) його значення в голові українського читача — це **провал**, не точність.

**Першочерговий критерій: чи розуміє читач без додаткового контексту?** Якщо UA-слово має домінантне інше значення в українському узусі — це слово ламається у голові читача в перші ж секунди. Переписати.

### Класичні пастки (zero tolerance — обов'язково адаптувати)

| EN | UA-калька (TYPICALLY WRONG) | Чому ламається | UA target |
|----|------------------------------|-----------------|-----------|
| `bet` (поставити, ризикнути) | "ставка" | Домінантне значення в UA — процентна ставка / зарплатна ставка / ставка у грі. У контексті "five small bets" читач думає про % або про азартну гру, а не про ризиковані ділові кроки. | "малий ризик" / "обережний крок" / "малий експеримент" / "етап" — залежно від контексту |
| `runway` (фін. строк виживання) | "злітна смуга" | Це SaaS-термін, читач знає EN-форму. Зберігати англ. `runway` + перший раз із поясненням. | EN: `runway` (фінансовий строк виживання — скільки місяців пройде до нуля при поточних витратах) |
| `burn` / `burn rate` | "пропалювати" / "пропалювання" | Домінантне значення — буквальне "пекти". У SaaS-контексті — швидкість витрат. | EN: `burn rate` (швидкість витрат) АБО "темп спалювання" з контекстом |
| `pipeline` (sales pipeline / deal pipeline) | "трубопровід" | Буквальне фіз. значення в UA. У бізнес-контексті — потік угод / sales-воронка. | "потік угод" / "воронка продажів" / `sales pipeline` як термін |
| `bandwidth` (особистий ресурс часу) | "пропускна здатність" | Технічний термін, у контексті "I don't have bandwidth" про людину — ламається. | "ресурс / резерв часу" / "не маю сил" / "не витягну" |
| `low-hanging fruit` | "низько висячий плід" | Буквальний калькований образ — звучить як рослинництво. | "легкі очки" / "найпростіше" / "що лежить під ногами" |
| `move the needle` | "зрушити стрілку" | UA-читач не має цього образу (з вимірювача). | "зробити різницю" / "реально вплинути" / "зрушити з місця" |
| `play` (a long game) | "гра" | OK у game-контексті, але "long game" → не "довга гра", а "грати у далеку перспективу" / "довгий горизонт". | "далекий горизонт" / "довга стратегія" |
| `default` (= за замовчуванням, прийняти стандартну поведінку) | "за замовчуванням" як дієслово | UA-калька "задефолтитися" не існує у живій мові. | "піти за стандартом" / "автоматично обрати" |
| `compound` (capital, audience) | "компаундити" | OK у IT-сленгу, але масовий читач не зрозуміє. Перший раз — з поясненням. | "наростати з % на %" / "накопичуватися експоненційно" / `compound` (накопичення з ефектом складного відсотка) |
| `leverage` (verb) | "леверажити" / "важелити" | Калька не прижилася. | "використовувати як важіль" / "піднімати з опорою на" |
| `hedge` (a position) | "хеджувати" | OK у фінансах для аудиторії, що знає термін. Для масової — пояснити. | "страхувати позицію" / "перестраховуватися" |

### Робоча процедура — як ловити ці пастки

1. **Перед перекладом термін** — спитати себе: **"Яке домінантне значення цього UA-слова без контексту?"** Якщо домінантне значення НЕ збігається з тим, що мав на увазі автор EN — це пастка. Адаптувати.
2. **Прочитати UA-речення вголос без контексту попередніх речень**. Якщо читач, який прийшов з пошуковика на середину статті, зрозуміє слово правильно — OK. Якщо може зрозуміти неправильно — переписати.
3. **Заголовок, лід, перші 2 секції — критично**. Тут читач ще не побудував контекст. Тут не можна допускати двозначних калькованих термінів. У заголовку особливо.
4. **Колонка "що означає у голові читача"** має перевагу над колонкою "що означає в EN-оригіналі". Receipts (числа, імена, дати) — verbatim; **поняття — адаптовано**.

### Заголовок + лід — окреме правило

Заголовок не має містити двозначних UA-слів, які потребують 200 слів контексту для правильного розуміння. Якщо у тебе у заголовку слово, чиє домінантне UA-значення відрізняється від EN-значення джерела — **переписати заголовок або замінити слово**.

Приклад **поганого** UA-заголовка: *"Як піти у соло у 2026-му: Зворотний поворот, п'ять малих ставок без шрамів у CV"* — "ставка" читається масовим читачем як "rate" або "зарплатна ставка"; ризиково-ділове значення не доставляється.

Приклад **доброго** перепису: *"...п'ять обережних кроків без шрамів у CV"* АБО *"...п'ять малих експериментів без шрамів у CV"* АБО *"...п'ять етапів без шрамів у CV"*.

### Reviewer обов'язково перевіряє

Перекладач звітує у "READER-ADAPTATION AUDIT" секції:
- Список усіх термінів, для яких була зроблена адаптація замість дослівного перекладу (EN термін → який варіант UA обрано → чому).
- Окремий audit заголовка: чи кожне слово у заголовку доставляє правильне значення без контексту?
- Перші 2 абзаци пройдені під тим самим audit.

Reviewer перевіряє цей звіт + sample-checks: відкриває заголовок та лід у голові немедіакомпетентного UA-читача (соломінчий тест: "якби моя мама прочитала тільки заголовок — що вона зрозуміла?"). Якщо хоч одне слово ламається — APPROVE-WITH-FOLLOWUPS з фіксом.

## Anti-AI-tell у UA — banned target-language moves

Перекладач/редактор НЕ дозволяє ці українські формули (UA-еквіваленти 20 forbidden moves):

### Banned openings + meta

- "В даний час" / "На сьогоднішній день" / "У сучасному світі"
- "Давай розглянемо" / "Розгляньмо детально" / "Заглибимося"
- "У цій статті ми..." / "У даній статті розглянемо"
- "Вітаємо у світі X" / "Ласкаво просимо у X"
- "Слід зазначити, що..." / "Варто наголосити, що..."
- "Однак, важливо пам'ятати" / "Проте, не забуваймо"
- "Як ми побачимо далі" / "Як буде показано нижче"

### Banned closers

- "На завершення" / "Підбиваючи підсумки" / "Підсумовуючи"
- "Отже, можна зробити висновок"
- "Сподіваємося, ця стаття була корисною"

### Banned filler verbs/nouns (UA equivalents of delve/tapestry/landscape/realm/navigate/robust/leverage)

| EN forbidden | UA equivalent — теж banned |
|--------------|---------------------------|
| delve | заглиблюватися (як риторика) / занурюватися (як риторика) |
| tapestry | гобелен / полотно (метафора) / мозаїка |
| landscape | ландшафт (= "current landscape") / царина |
| realm | царина / сфера (як filler) |
| navigate (challenges) | навігувати / орієнтуватися (як filler) |
| robust | надійний (як empty intensifier) / потужний |
| leverage (verb) | використовувати по-максимуму / задіяти (як filler) |

### Banned intensifiers

- "глибоко" / "неймовірно" / "абсолютно" / "безумовно" / "однозначно" (empty)
- "по-справжньому" / "дійсно" (як filler before adjective)

### Banned structural moves

- Тріади "X, Y та Z" в кожному реченні
- "Це не просто X — це Y" pivot
- Em-dash більше 2 на абзац
- Підсумкове речення в кінці кожної секції
- Підзаголовок кожні 200 слів
- Симетричні абзаци по 3-4 рядки кожен

## Prompt-callout translation policy

Стаття містить `<PromptCallout>` блоки. Правила перекладу:

- **`/faion` префікс ЗАЛИШАЄТЬСЯ англійською** — це команда.
- Все ПІСЛЯ `/faion` перекладається українською як природний запит.
- Зберігай конкретні числа, валюту, slug-схожі терміни (MRR, burn, runway) дослівно.

Приклад:

- EN source: `/faion let's calculate my runway: $50K savings, $4K/mo burn, $800 MRR`
- UA: `/faion давай прорахуємо мій runway: $50K заощаджень, $4K/міс burn, MRR $800`

Інші приклади:

- EN: `/faion check PMF for solo SaaS against 5-criterion rubric`
- UA: `/faion перевір PMF мого соло-SaaS за 5-критерієвим rubric`

- EN: `/faion build me a 30-60-90 day plan`
- UA: `/faion збудуй мені 30-60-90-денний план`

## Receipt preservation (CORRECT-SIDED — V4 update)

Receipts мають ДВІ категорії; правила різні:

### Категорія A — verbatim (числа / дати / місця / URLs)

- **Долари**: "$250K TC", "$4K/mo burn", "$800 MRR" — verbatim. Не "приблизно 250 тисяч".
- **Дати**: "March 2014", "Q2 2023" — транслітерувати числами "березень 2014" / "Q2 2023" (числа однакові, місяць перекладається).
- **Місця**: Bay Area → "Bay Area" (бренд) АБО "район Затоки Сан-Франциско" з контекстом; San Francisco → "Сан-Франциско" (стандартна транслітерація — місто має українську форму); Lisbon → "Лісабон"; Saigon → "Сайгон". Якщо місто має закріплену UA-форму — використовуй її; якщо ні (мала локація) — зберігай EN.
- **HN handles, Twitter handles, URLs, slug-схожі**: verbatim.
- **Бренди / продукти**: Stripe, GitHub, Vercel, AWS, Indie Hackers, Hacker News — verbatim (це назви компаній / платформ, не слова).

### Категорія B — TRANSLATED (імена людей + назви статей + цитати з форумів)

**Імена справжніх людей у тілі статті — ТРАНСЛІТЕРУЮТЬСЯ.** Це principle of receipts ≠ збереження англійського написання у тілі. Транслітерація + латинське оригінальне у дужках при першій згадці у КОЖНІЙ H2-секції:

| EN | UA (перша згадка в секції) | UA (наступні в тій самій секції) |
|----|---------------------------|---------------------------------|
| Patrick McKenzie | Патрік МакКензі (Patrick McKenzie — засновник Stripe Atlas, автор есеїв Kalzumeus, перейшов на стратегічне консультування Stripe на початку 2023-го) | МакКензі |
| Sahil Lavingia | Сахіл Лавінгія (Sahil Lavingia — засновник Gumroad, автор *«Минималіст-підприємець»*) | Лавінгія |
| Pieter Levels | Пітер Левелс (Pieter Levels — засновник Nomad List, Photo AI, Remote OK; портфоліо ~$3.1-$3.5M ARR станом на травень 2026-го) | Левелс |
| Tony Dinh | Тоні Дінь (Tony Dinh — індiе-розробник у Сайгоні, автор DevUtils + TypingMind + BlackMagic, $1M+ ARR як соло) | Дінь |
| Marc Lou | Марк Лу (Marc Lou — засновник ShipFast, CodeFast, DataFast; $1M доходу 2025-го через три продукти як соло з 50K X-аудиторією) | Лу |
| Karri Saarinen | Каррі Сааринен (Karri Saarinen — засновник Linear, ex-Airbnb, фінська lineage) | Сааринен |
| Tuomas Artman | Туомас Артман (Tuomas Artman — співзасновник Linear, ex-Uber) | Артман |
| Paul Graham | Пол Грем (Paul Graham — співзасновник Y Combinator, автор есеїв) | Грем |
| Jason Cohen | Джейсон Коен (Jason Cohen — засновник WP Engine, автор bootstrapping-есеїв) | Коен |

**Назви статей / есеїв / постів — ТРАНСЛАТУЮТЬСЯ + лінкуються на оригінал у новій вкладці**:

| EN | UA |
|----|-----|
| *"Reflecting on My Failure to Build a Billion-Dollar Company"* (есе Lavingia 2019) | `<a href="https://sahillavingia.com/reflecting" target="_blank" rel="noopener">*«Розмірковуючи над моїм провалом збудувати компанію на мільярд»*</a>` (есе Лавінгії, лютий 2019) |
| *"What Working At Stripe Has Been Like"* (есе McKenzie 2019) | `<a href="..." target="_blank" rel="noopener">*«Як було працювати в Stripe»*</a>` (есе МакКензі, 2019) |
| *"I'm Joining Stripe to Work on Atlas"* (пост McKenzie 2016) | `<a href="..." target="_blank" rel="noopener">*«Йду в Stripe працювати над Atlas»*</a>` (пост МакКензі, 2016) |
| *"The Minimalist Entrepreneur"* (книга Lavingia 2021) | *«Минималіст-підприємець»* (книга Лавінгії, Penguin Portfolio 2021) |
| *"State of Independent SaaS"* (звіт MicroConf) | *«Стан незалежного SaaS»* (звіт MicroConf) |

**Цитати з форумів / AMA / Twitter — ТРАНСЛАТУЮТЬСЯ + лінкуються**:

| EN | UA |
|----|-----|
| *"I did it, I quit my job. I am officially an indie hacker"* (IH-пост січня 2026) | `<a href="..." target="_blank" rel="noopener">*«Зробив це. Звільнився. Тепер офіційно indie hacker»*</a> (пост на Indie Hackers, січень 2026)` |
| *"I left my high-paying job, bootstrapped, burned, joined back after three years"* (IH AMA, hash 95e7afbbfc) | `<a href="..." target="_blank" rel="noopener">*«Я звільнився з добре оплачуваної роботи, бутстрапнув, прогорів і повернувся через три роки»*</a> (AMA на Indie Hackers, hash 95e7afbbfc)` |
| *"buying a $5 latte would fill me with guilt"* (IH-пост d02afe5b80) | `<a href="..." target="_blank" rel="noopener">*«купівля $5 латте викликала почуття провини»*</a> (пост на Indie Hackers, hash d02afe5b80)` |
| *"founded and operated $X-revenue SaaS for Y months"* (приклад рядка резюме) | *«заснував і вів SaaS з оборотом $X протягом Y місяців»* (приклад рядка в резюме) |

**Hash-IDs (d02afe5b80, 95e7afbbfc, item 25104578) — verbatim**, бо це ідентифікатори. Але сама цитата перекладається + лінкується на оригінал.

### Чому це правильно

Receipt-preservation principle = специфіка робить anecdote unfalsifiable. Збереження $-сум і дат це робить; збереження *англійського написання* імені — НІ. Транслітероване ім'я + Latin parenthetical = специфічно + читабельно для UA-читача. Англійська цитата в тілі UA-статті = читач НЕ парсить її, навіть якщо знає англійську — це когнітивне навантаження посеред речення. Переклад зберігає смисл, лінк на оригінал — це і є receipt-trail.

## Framework stages — translate the coinage to UA

5-етапний фреймворк Reversible Pivot. Канонічні UA-форми:

| EN stage | UA coinage |
|----------|-----------|
| Stealth-Validation | Прихована Валідація |
| Transition-Runway | Перехідний Runway (зберегти `runway` як SaaS-термін) |
| Half-Step | Напівкрок |
| Full-Solo | Повне Соло |
| Defensive-Retreat | Оборонний Відступ |

Перша згадка кожного етапу у статті: `Етап 1 — Прихована Валідація (Stealth-Validation): повний W2 (American federal tax form W-2 — статус найманого працівника), продукт як side-project`. Наступні згадки: `Етап 1 — Прихована Валідація` без EN.

У списках етапів у TLDR / нав-блоці — обов'язково обидві форми пар, бо це найкритичніший discovery-момент.

## Survivor bias + cognitive-bias terms

- `survivor bias` / `survivorship bias` → перша згадка: "ефект виживших (survivor bias — статистичний bias, де ми бачимо лише тих, хто пройшов селекцію, і ігноруємо тих, хто не пройшов)"; наступні: "ефект виживших".
- `survivor-bias-receipt` як hyphen chain — заборонено. Перепиши: "квитанція ефекту виживших" або "квитанція, що ілюструє ефект виживших".
- `confirmation bias` → "ефект підтвердження" (UA-стандарт).
- `selection bias` → "ефект селекції".
- `hindsight bias` → "ефект після-знання" / "ретроспективна упередженість".

## US tax / W2 / COBRA / RSU / 401(k) — gloss in same breath at first mention IN EACH SECTION

UA-читач не знає, що таке W2 / COBRA / RSU / 401(k) без пояснення. Доктрина:

- **Перша згадка у статті**: повний gloss. Напр.: `повний W2 (American federal tax form W-2 — статус найманого працівника з повною зарплатою, медичним пакетом і pre-tax-пенсійним планом)`.
- **Перша згадка у НОВІЙ H2-секції**: коротший gloss або хоча б плейн-мова коло. Напр.: `на W2 (статус найманого)`.
- **Наступні згадки у тій самій секції**: bare `W2`.

Це окремий випадок multicultural-English-doctrine — gloss завжди є, бо UA-читач не парсить цю термінологію.

## Tone calibration

- Іронія/сарказм як у NERO:
  - "Linkedin тобі скаже, що це leverage. Я скажу — це втеча від реального продукту."
  - "Витрачати $200 на A/B-тести pricing-сторінки коли в тебе ще нема 100 платних — це не оптимізація, це театр."
- Уникати "ми віримо", "ми переконані" — пишемо особисту думку.

## Cultural adaptation

- Долари — зберігати $ (це SaaS-benchmark валюта). Не конвертувати в гривню.
- Дати — формат "2026-05-25" (ISO) або "травень 2026" (текстом).
- Hacker News, Reddit, Twitter, Indie Hackers — бренди, оригінал.

## Title rules

- UA title не транслітерує EN. Адаптується.
- EN: "Stop A/B Testing Your Pricing Page" → UA: "Кинь A/B-тестувати свою pricing-сторінку" АБО "A/B-тести pricing-сторінки нічого тобі не дають" (теза як заголовок).
- Заголовки не закінчуються знаком оклику. Двокрапка `:` для розділення — OK.

## Reviewer checklist

- [ ] Зéро русизмів зі списку вище.
- [ ] Англіцизми-кальки прибрано.
- [ ] V2: усі слова з TRANSLATE-списку перекладено (feature, workflow, ship, deploy, burnout, pivot, brokerage, moonshot, sanity check, handoff, half-step, dashboard, optics, haircut, bookings).
- [ ] Whitelist English терміни (CLI, MRR, runway, churn, brand names, US tax) збережено.
- [ ] Anti-AI-tell: жодного "у даний час / розгляньмо / слід зазначити / на завершення".
- [ ] Receipts (імена, дати, $, місця) — verbatim.
- [ ] Prompt-callouts: `/faion` префікс EN, тіло перекладено природно.
- [ ] "ти/ви" consistent на всю статтю.
- [ ] No emojis.
- [ ] Word count ±15% від EN source.
