# User Interview Methods

## Summary

Two structured interview frameworks — basic user-interview and customer-interview-framework — for extracting validated problem signal from real users. Both share a core rule: ask about past behavior, not future intent; talk less than 20% of the time; never pitch. The interview flows in 4–5 timed stages ending with willingness-to-pay and referral asks.

## Why

Unstructured interviews generate polite agreement and hypotheticals, not signal. Timed, staged interview scripts force the researcher to listen rather than pitch and surface emotional intensity (frustration, excitement) that predicts actual behavior. The Mom Test principle — asking about their life, not your idea — is the concrete mechanism that separates usable data from vanity feedback.

## When To Use

- Before committing to build: validating a problem hypothesis with 5–15 real users
- Designing a discovery sprint: need a structured guide to run consistently across interviewees
- Synthesizing transcripts: extracting themes, quotes, and patterns after interviews complete
- Practicing interview technique: simulating an interviewee to refine question phrasing

## When NOT To Use

- When n < 5 — a single frustrated user is anecdote, not signal
- When you need statistical confidence — use surveys; interviews give direction, not significance
- When the decision has already been made — interviews at that stage are rationalization theatre
- Replacing usability testing — interviews surface beliefs, not behaviors; watch users act instead
- When speed is the only constraint and even 3 interviews are not feasible — use a fake door test

## Content

| File | What's inside |
|------|---------------|
| `content/01-interview-frameworks.xml` | Interview types, 45-min structure, golden rules, question patterns |
| `content/02-examples-and-antipatterns.xml` | Worked insight examples, antipatterns (leading questions, pitching, hypotheticals) |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-script.md` | 45-min warm-up/current-state/pain/solution/wrap-up script |
| `templates/interview-guide.md` | Typed guide with hypothesis, script sections, and notes table |
| `templates/prompt-draft-guide.txt` | LLM prompt to draft an interview guide from a problem hypothesis |
| `templates/prompt-synthesize.txt` | LLM prompt to extract themes, surprising findings, and non-segments from transcripts |
| `templates/theme-extractor.py` | Batch transcript theme counter (keyword frequency across .txt files) |
