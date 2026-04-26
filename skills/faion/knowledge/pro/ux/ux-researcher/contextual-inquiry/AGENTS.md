# Contextual Inquiry

## Summary

Contextual inquiry is a semi-structured field research method conducted in the user's actual work environment while tasks unfold. The researcher observes, asks questions, and shares interpretations for immediate correction using the master-apprentice model: user is the expert, researcher is the learner.

## Why

Lab interviews capture what people think they do; contextual inquiry captures what they actually do. Workarounds, tacit knowledge, physical artifacts, and environmental constraints only surface in context. The master-apprentice framing and shared-interpretation principle produce richer, more accurate data than recall-based methods while reducing observer-effect distortion.

## When To Use

- Discovery research where workflows, tools, and physical environment matter (clinical, factory, financial back-office, field ops).
- Mapping current-state tasks before redesign — capturing workarounds, shadow IT, and tacit knowledge.
- Validating that a new product fits real work, not idealized work, before spec freeze.
- Investigating incidents where reported procedure diverges from actual practice.

## When NOT To Use

- Quick usability feedback on a finished design — usability testing is faster and cheaper.
- Pure attitudinal or preference questions — surveys are sufficient.
- High-secrecy environments (defense, M&A) where observation is restricted — fall back to artifact analysis.
- Remote-only access where physical artifacts cannot be observed — use diary studies instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Four principles (context, partnership, interpretation, focus), observation rules, what to capture. |
| `content/02-process.xml` | Six-step process: prepare, intro, observe-interview, capture, debrief, cross-session analysis. |
| `content/03-analysis.xml` | Affinity diagram, sequence model, cultural model; remote adaptations and limitations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observation-guide.md` | Pre-session guide: focus areas, opening script, observation checklist, notes table. |
| `templates/session-notes.md` | Structured post-session notes: environment, workflow sequences, workarounds, insights. |
| `templates/ci-row-schema.py` | Dataclass for a single tagged observation row used in cross-session analysis. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/observation_tagger_prompt.txt` | LLM prompt for extracting structured observation rows from transcripts. |
