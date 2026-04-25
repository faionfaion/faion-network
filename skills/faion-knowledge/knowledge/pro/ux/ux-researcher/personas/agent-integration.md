# Agent Integration — Personas

## When to use
- Synthesizing research data (interviews, surveys, support tickets, analytics) into 3-5 representative user types.
- Aligning a team that disagrees about who the user is — produce a shared reference artifact.
- Re-validating outdated personas when the product, market, or user base has shifted.
- Bootstrapping proto-personas before research, with explicit assumptions to validate.

## When NOT to use
- Marketing-only segmentation (psychographics, ad targeting) — those need separate marketing-persona models.
- Single-user products (internal tools with one stakeholder) where a persona adds zero signal.
- Teams with no plan to use personas in design reviews — building them as posters is a waste.
- High-stakes regulated domains (medical devices, aerospace) where formal user-task analysis supersedes lightweight personas.

## Where it fails / limitations
- Research-based personas decay. Methodology recommends update but does not specify a cadence; in practice, every product pivot or new market warrants revisit.
- Personas are reductive by design — outliers and accessibility-edge users disappear. Pair with inclusive-design personas (e.g., extreme users) to compensate.
- Cultural assumptions baked into a persona (US tech-comfortable manager) do not transfer across markets without re-research.
- Quote authenticity is hard: AI-generated quotes feel synthetic and reduce team trust in the artifact.
- "3-5 primary personas" is a rule of thumb — real complex products may need a primary set plus a secondary set with explicit deprioritization rules.

## Agentic workflow
LLMs are excellent at clustering qualitative data and drafting persona prose; they are weak at deciding which clusters matter. Use an analysis agent to read tagged interview transcripts and propose 6-10 clusters with evidence; a curation agent (with human review) selects the 3-5 personas to keep; a drafting agent fills the persona template citing source quotes verbatim. Persist evidence links — every claim in the persona should map to a transcript span.

### Recommended subagents
- `interview-clusterer` — sonnet; ingests tagged transcripts, returns clusters with goal/behavior/pain themes and evidence quotes.
- `persona-drafter` — haiku; fills persona template from a cluster definition + evidence pack.
- `persona-validator` — sonnet; reviews a persona for evidence coverage, anti-pattern detection (just-demographics, made-up quotes), and JTBD linkage.
- `proto-persona-author` — haiku; produces lightweight proto-personas with explicit "assumption" tags.

### Prompt pattern
```
You are persona-drafter. Inputs: <cluster_summary>, <evidence_quotes_with_source_ids>.
Produce a persona using the template. Every Goal, Frustration, and Behavior MUST cite
at least one evidence_id. Mark inferences with [INFERENCE]. Do NOT invent quotes — pick
the most representative quote_id for the Quote field.
Output: markdown + JSON {evidence_map: {field -> [evidence_ids]}}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dovetail` CLI / API | Tag and cluster interview transcripts | dovetail.com/api |
| `condens` API | Research repo with thematic tagging | condens.io |
| `marvinapp` (Marvin) | Qualitative analysis with API | heymarvin.com |
| `whisperx` | Transcribe interviews locally | github.com/m-bain/whisperX |
| `openai-whisper` | OSS transcription | github.com/openai/whisper |
| `airtable-cli` / `notion-cli` | Persona library storage and updates | airtable.com / notion.so |
| `pandoc` | Convert persona markdown to slides/PDF for stakeholders | pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Dovetail | SaaS | Yes — REST + Insights API | Industry standard for research repos |
| Condens | SaaS | Yes — REST | Smaller player, strong tagging |
| Marvin | SaaS | Yes — REST | AI-assisted theming |
| Notably | SaaS | Yes — REST | AI-native research repo |
| UserTesting | SaaS | Yes — REST | Source of recorded sessions |
| Maze | SaaS | Yes — REST | Survey + tree test data into personas |
| Airtable / Notion | SaaS | Yes — REST | Lightweight persona library hosting |

## Templates & scripts
See `templates.md` for full persona and proto-persona templates. Evidence-coverage check:

```python
# persona_evidence_check.py — fail if any claim lacks evidence id
import yaml, sys, re

REQUIRED = ("goals", "frustrations", "behaviors")

def check(path):
    p = yaml.safe_load(open(path))
    issues = []
    for section in REQUIRED:
        for i, item in enumerate(p.get(section, [])):
            text = item if isinstance(item, str) else item.get("text", "")
            ids = item.get("evidence_ids", []) if isinstance(item, dict) else re.findall(r"\[E-\d+\]", text)
            if not ids:
                issues.append(f"{section}[{i}]: no evidence")
    if p.get("quote", {}).get("source_id") is None:
        issues.append("quote: no source_id")
    for line in issues:
        print(line)
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(check(sys.argv[1]))
```

## Best practices
- Cap evidence-free inferences at 20 % per persona and tag them explicitly. Anything more, the persona is fiction.
- Pair every persona with a "non-persona" (someone the product is explicitly NOT for). Saying no in design reviews requires negative space.
- Keep personas as living markdown in a research repo, not as PDFs. Diff history shows when assumptions change.
- Use the same persona in user stories, A/B test hypotheses, and onboarding flows. If it never re-appears, you built a poster.
- Cite real quotes verbatim with attribution to anonymous IDs. Synthesized "voicey" quotes tank credibility on first audit.
- Refresh research-based personas at least once per major release; refresh proto-personas the moment the first 5 user interviews close.

## AI-agent gotchas
- LLMs hallucinate plausible quotes and demographics. Lock the drafter to evidence-only mode and reject outputs with quotes not present in the source corpus.
- Cluster quality depends on tagging consistency. Run an inter-rater check on tags before clustering — agents amplify tag noise.
- Persona "names + photos" risk encoding stereotypes (always-female-marketer, always-male-CTO). Audit the set for diversity and rotate per-update.
- Proto-personas drift toward team biases. Force the author agent to surface 3+ assumptions per proto and link each to a planned validation method.
- Beware the "synthetic users" pitch — generating personas purely from LLM imagination yields fluent fiction with no signal. Real research is required.
- Never let the agent merge research data from different markets/locales into a single persona without explicit instruction; segment first, persona-fy second.
- Persona files referenced in prompt context can balloon. Keep a one-paragraph persona summary for prompt injection and link to the full doc by URL/ID.

## References
- Alan Cooper, "About Face" (4th ed.) and "The Inmates Are Running the Asylum".
- Mulder & Yaar, "The User Is Always Right".
- Kim Goodwin, "Designing for the Digital Age" (research-based persona method).
- Nielsen Norman Group — "Personas: Practice and Theory" (nngroup.com/articles/persona/).
- Interaction Design Foundation — Personas guide.
- Lean UX (Gothelf & Seiden) for proto-persona practice.
