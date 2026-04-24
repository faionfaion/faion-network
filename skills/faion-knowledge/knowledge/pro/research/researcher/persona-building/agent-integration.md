# Agent Integration — Persona Building

## When to use
- You have raw transcripts/notes from 8+ customer interviews and need to cluster them into 1–3 buyer archetypes before writing positioning, landing copy, or onboarding flows.
- A landing page exists but bounce/conversion is poor and the team disagrees on "who this is for" — persona synthesis from analytics + support tickets resolves it.
- Sales is closing one segment 3x faster than others; codify that segment as the primary persona to focus marketing spend.
- Pivoting a product into an adjacent market and need a new primary persona before rewriting the home page and pricing tiers.
- A multi-agent pipeline (`faion-research-agent` → `faion-marketing-manager` → `faion-content-marketer`) needs a persona file as a shared input artifact.

## When NOT to use
- Pre-PMF / pre-interview: you have zero customer conversations. Run `user-interviews` and `pain-point-research` first — building personas from imagination is the failure mode this methodology exists to prevent.
- B2B enterprise with named-account selling and < 20 logos. Use account profiles + buying-committee maps instead; personas across 5 accounts are over-fit caricatures.
- Highly heterogeneous marketplaces (e.g. classifieds) where the segmentation axis is transactional behavior, not demography. Use `audience-segmentation` (cluster on behavior) instead.
- Single-feature internal tools where the user is unambiguous (e.g. "the on-call SRE"). A 1-line role description beats a 2-page persona doc.

## Where it fails / limitations
- "Demographic theatre": age/income/photo-stock fields filled in to look complete but never used in any real product/marketing decision. If the persona doesn't change a decision, it's dead weight.
- LLM hallucination of quotes: a model asked to "write a persona for indie SaaS founders" will invent plausible-sounding frustrations. Always ground in transcript citations.
- Persona drift: shipped once, never updated. By month 6 the actual ICP has shifted but the doc still drives copy. Quarterly review or kill the artifact.
- Over-segmentation: 5+ personas across a 3-person team means nobody is the focus. Cap at 1 primary + 1 negative until ARR justifies more.
- Confusing personas with segments: a persona is a representative individual; a segment is a group. Don't use persona docs to set ad targeting — use `audience-segmentation` for that.

## Agentic workflow
Drive persona building as a 4-step pipeline. (1) `faion-research-agent` (mode: `personas`) ingests interview transcripts from `.aidocs/research/interviews/*.md` and produces a clustered patterns file. (2) A synthesis pass writes a draft `user-personas.md` using the lean template. (3) `faion-domain-checker-agent` is irrelevant here; instead route the draft through `faion-marketing-manager` for messaging-fit review. (4) Validate by replaying the persona to 3 real customers (human-in-the-loop, do not automate this step).

### Recommended subagents
- `faion-research-agent` — orchestrator with `personas` mode; reads interviews, clusters, drafts persona doc into `.aidocs/product_docs/user-personas.md`.
- `faion-sdd-executor-agent` — when the persona output is a deliverable in an SDD task (e.g. "F-047: Define primary persona before pricing redesign"), wraps the run with quality gates and CHANGELOG entry.
- `password-scrubber-agent` — run before committing transcripts: interview notes often contain emails/Slack handles. Scrub PII before any artifact lands in a repo.

### Prompt pattern
Synthesis prompt (sub-agent input):
```
Input: 12 interview transcripts at .aidocs/research/interviews/*.md
Task: Cluster on (role, primary goal, blocking frustration). Quote-cite every
trait — format `[T07:L142]` referencing transcript file:line. If a trait has
fewer than 3 supporting quotes across transcripts, mark it [WEAK] and keep it
out of the primary persona. Produce one primary + one negative persona using
the lean template in templates.md. No demographics unless 5+ transcripts agree.
```

Validation prompt (after synthesis):
```
Read .aidocs/product_docs/user-personas.md. For each trait, list the citation.
Flag any trait with no citation as HALLUCINATION. Output a diff that removes
unsupported claims.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dovetail` API | Tag and cluster interview highlights, export persona-ready themes | https://developers.dovetail.com |
| `notably` API | AI-assisted theme synthesis from transcripts | https://www.notably.ai/api |
| `delve` (qual coding) | Manual code-and-cluster for small N (< 20 interviews) | https://delvetool.com |
| `condens` API | Tag, cluster, export | https://condens.io/api |
| `marvin` API | Auto-tagging of qualitative data | https://heymarvin.com |
| `whisper` (OpenAI) | Cheap transcription of recorded interviews → markdown for the pipeline | `pip install openai-whisper` |
| `pyannote` | Speaker diarization (essential for multi-participant transcripts) | `pip install pyannote.audio` |
| `jq` + `yq` | Parse persona JSON/YAML artifacts in CI | system package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes — REST API for highlights, tags, insights | Strongest qual-research API; pricing scales by seat |
| Notably | SaaS | Yes — API + AI synthesis | Built-in LLM theme generation, useful as a second opinion |
| Condens | SaaS | Yes — REST API | EU-hosted, GDPR-friendly for European interviewees |
| Marvin (HeyMarvin) | SaaS | Yes — API | Auto-tag + transcript search |
| Aytm | SaaS | Partial — API-driven panels | Recruit + survey; agent can pull responses but persona synthesis stays in your stack |
| User Interviews | SaaS | Recruit-only API | Source participants; not a synthesis tool |
| Maze | SaaS | API for unmoderated tests | Validate persona predictions, not build them |
| Reduct.video | SaaS | API + transcript export | Video-first; pulls clips into persona docs |
| Delve | SaaS | No public API | Use only for small-N manual coding |
| HubSpot Make My Persona | Free web tool | No | Output is a marketing-shaped doc, not a research artifact; ignore |

## Templates & scripts
See `templates.md` for the full and lean persona shapes. The repo also ships an empty `templates.md` for this methodology — if you need a quick agent-callable cluster pass, the script below produces a first-draft persona from a directory of transcripts.

```python
# cluster_personas.py — first-draft persona synthesis from transcripts
# Usage: python cluster_personas.py .aidocs/research/interviews/ > draft-persona.md
import sys, pathlib, re, collections, json

interviews = pathlib.Path(sys.argv[1]).glob("*.md")
traits = collections.defaultdict(list)  # (axis, value) -> [citations]

AXES = {
    "role":        re.compile(r"(?im)^.*?(role|title|job)\s*[:\-]\s*(.+)$"),
    "goal":        re.compile(r"(?im)^.*?(goal|wants?|trying to)\s*[:\-]\s*(.+)$"),
    "frustration": re.compile(r"(?im)^.*?(frustration|pain|blocker|stuck)\s*[:\-]\s*(.+)$"),
    "trigger":     re.compile(r"(?im)^.*?(buy|signed up|started using)\s+(?:when|after)\s+(.+)$"),
}

for f in interviews:
    text = f.read_text(encoding="utf-8", errors="ignore")
    for axis, rx in AXES.items():
        for m in rx.finditer(text):
            value = m.group(2).strip().lower()[:80]
            line = text[: m.start()].count("\n") + 1
            traits[(axis, value)].append(f"[{f.stem}:L{line}]")

print("# Draft persona (auto-generated, requires human review)\n")
for axis in ("role", "goal", "frustration", "trigger"):
    print(f"## {axis.title()}")
    rows = sorted(((k[1], v) for k, v in traits.items() if k[0] == axis),
                  key=lambda r: -len(r[1]))
    for value, cites in rows[:5]:
        flag = " [WEAK]" if len(cites) < 3 else ""
        print(f"- {value}{flag} — {len(cites)} mentions {' '.join(cites[:5])}")
    print()
```

## Best practices
- Cite every trait. A persona without `[transcript:line]` citations is fiction. Treat uncited traits as hypotheses, not facts.
- Co-locate persona doc with messaging tests. Each persona's "Headline" field gets an open A/B ticket — if the headline never wins a test, the persona is wrong.
- Keep one primary persona until $X ARR threshold (team-defined). Splitting attention between 3 personas at seed-stage is the fastest path to muddled positioning.
- Define the negative persona early and link it to your sales-disqualification SOP. "Who do we say no to?" is more decision-shaping than the primary persona.
- Use lean template for working personas; only expand to full template when handing off to a marketing or design team that needs context you internalized.
- Re-validate every quarter by showing the doc to 3 real customers and asking "does this sound like you?" If two say "no", rebuild.
- Pair with `jobs-to-be-done`. Persona = who, JTBD = why-they-hire-the-product. Both required for a non-trivial product.

## AI-agent gotchas
- LLMs invent plausible quotes. Always require transcript citations in synthesis prompts; reject any persona output that lacks them.
- Models over-anchor on the first transcript fed in (recency/primacy bias). Shuffle transcript order between runs; if persona output changes drastically, the data is too thin.
- Demographic stereotypes leak through pre-trained priors ("32-year-old freelance designer in Brooklyn"). Strip demographics from the prompt unless the data actually supports them — instruct the model: "no demographic field unless 5+ transcripts agree."
- Synthesis at temperature > 0.3 fabricates. Use temperature 0 for clustering; reserve creative phrasing only for the optional "characteristic quote" field, and even then mark it as paraphrase.
- Long-context dump of 30 transcripts in one call → model collapses to averages and loses outliers. Map-reduce: cluster per-transcript, then merge cluster summaries.
- Human-in-the-loop checkpoints: (a) before committing a persona to repo, a human reviews citations; (b) before using persona to drive ad spend, a human re-interviews 2 customers.
- Don't let an agent autonomously update the persona doc on a schedule. Drift detection ("does the persona still match new interviews?") can be automated; rewrites must not.
- PII: transcripts contain names, emails, employer names. Run `password-scrubber-agent` (or equivalent) before any artifact crosses repo boundaries. The persona doc itself should reference participants by ID (`P07`), never name.

## References
- Adlin, T. & Pruitt, J. — *The Essential Persona Lifecycle* (Morgan Kaufmann, 2010)
- Cooper, A. — *The Inmates Are Running the Asylum* (1999) — origin of design personas
- Nielsen Norman Group — "Personas: Practice and Theory" (https://www.nngroup.com/articles/persona/)
- Christensen et al. — "Know Your Customers' Jobs to Be Done" — HBR 2016 (pair with persona work)
- Dovetail blog — "How to write a research-backed persona" (https://dovetail.com/research/persona-template/)
- Sibling methodologies in this skill: `audience-segmentation`, `user-interviews`, `pain-point-research`, `survey-design`, `continuous-discovery`
