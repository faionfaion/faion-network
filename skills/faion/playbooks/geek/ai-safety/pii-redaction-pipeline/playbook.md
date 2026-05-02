---
name: pii-redaction-pipeline
description: Redact PII before sending to an LLM and restore original values in the response using Microsoft Presidio and the Anthropic SDK.
tier: geek
group: ai-safety
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a Python pipeline that detects and tokenizes `PERSON`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `CREDIT_CARD`, and custom `CLIENT_ID` entities in user input before sending it to `claude-sonnet-4-6`, then restores the original values in the model's response — so no raw PII ever leaves your application boundary.

## Prerequisites

- Python 3.11+.
- `pip install presidio-analyzer presidio-anonymizer anthropic>=0.51 spacy`.
- spaCy English model: `python -m spacy download en_core_web_lg`.
- An `ANTHROPIC_API_KEY` exported in the environment.
- Familiarity with Presidio's `AnalyzerEngine` / `AnonymizerEngine` API — see [Microsoft Presidio docs](https://microsoft.github.io/presidio/).
- Understanding of guardrail pipeline patterns — see `knowledge/geek/ai/llm-integration/guardrails-implementation` before proceeding if you need broader input/output validation beyond PII.

## Steps

1. **Install dependencies** and verify Presidio loads the NLP engine.

   ```bash
   pip install presidio-analyzer presidio-anonymizer anthropic>=0.51 spacy
   python -m spacy download en_core_web_lg
   python -c "from presidio_analyzer import AnalyzerEngine; AnalyzerEngine(); print('Presidio OK')"
   ```

2. **Implement the custom `CLIENT_ID` recognizer** using a regex pattern that matches your internal ID format (e.g. `CLT-` followed by 8 alphanumeric characters).

   ```python
   # recognizers.py
   from presidio_analyzer import Pattern, PatternRecognizer

   def build_client_id_recognizer() -> PatternRecognizer:
       """Recognize CLIENT_ID tokens like CLT-A1B2C3D4."""
       pattern = Pattern(
           name="client_id_pattern",
           regex=r"\bCLT-[A-Z0-9]{8}\b",
           score=0.9,
       )
       return PatternRecognizer(
           supported_entity="CLIENT_ID",
           patterns=[pattern],
           context=["client", "account", "id"],
       )
   ```

3. **Build the redaction engine** — a class that wraps `AnalyzerEngine` + `AnonymizerEngine` and maintains a per-request token map for reversal.

   ```python
   # redactor.py
   import re
   import logging
   from dataclasses import dataclass, field
   from presidio_analyzer import AnalyzerEngine
   from presidio_anonymizer import AnonymizerEngine
   from presidio_anonymizer.entities import OperatorConfig
   from recognizers import build_client_id_recognizer

   log = logging.getLogger("pii.redactor")

   ENTITIES = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "CLIENT_ID"]

   # Counters per entity type within a single request
   _COUNTER_PATTERN = re.compile(r"<([A-Z_]+)_(\d+)>")


   @dataclass
   class RedactionResult:
       redacted_text: str
       token_map: dict[str, str]  # "<PERSON_1>" -> "Alice Johnson"


   class PIIRedactor:
       def __init__(self) -> None:
           self._analyzer = AnalyzerEngine()
           self._analyzer.registry.add_recognizer(build_client_id_recognizer())
           self._anonymizer = AnonymizerEngine()

       def redact(self, text: str) -> RedactionResult:
           """Analyze + anonymize text; return redacted version + reverse map."""
           results = self._analyzer.analyze(
               text=text,
               entities=ENTITIES,
               language="en",
           )
           if not results:
               return RedactionResult(redacted_text=text, token_map={})

           # Sort by start position descending for safe in-place replacement
           results.sort(key=lambda r: r.start, reverse=True)

           counters: dict[str, int] = {}
           token_map: dict[str, str] = {}
           redacted = text

           for result in results:
               entity = result.entity_type
               counters[entity] = counters.get(entity, 0) + 1
               placeholder = f"<{entity}_{counters[entity]}>"
               original = text[result.start:result.end]
               token_map[placeholder] = original
               redacted = redacted[: result.start] + placeholder + redacted[result.end :]

           log.info(
               "redacted %d PII entities: %s",
               len(results),
               {k: v[:4] + "***" for k, v in token_map.items()},
           )
           return RedactionResult(redacted_text=redacted, token_map=token_map)

       @staticmethod
       def restore(text: str, token_map: dict[str, str]) -> str:
           """Replace all placeholders in LLM response with original PII values."""
           for placeholder, original in token_map.items():
               text = text.replace(placeholder, original)
           return text
   ```

4. **Implement the LLM call wrapper** that enforces redact-before-call and restore-after-call.

   ```python
   # llm_client.py
   import anthropic
   from redactor import PIIRedactor

   MODEL = "claude-sonnet-4-6"
   MAX_TOKENS = 2048

   _client = anthropic.Anthropic()
   _redactor = PIIRedactor()


   def chat_with_redaction(user_message: str, system_prompt: str = "") -> str:
       """Send user_message to Claude with PII redacted; restore PII in response.

       The model never receives raw PII. If it echoes a placeholder like
       <PERSON_1> in its reply, it is restored to the original value before
       returning to the caller.
       """
       result = _redactor.redact(user_message)

       kwargs: dict = {
           "model": MODEL,
           "max_tokens": MAX_TOKENS,
           "messages": [{"role": "user", "content": result.redacted_text}],
       }
       if system_prompt:
           kwargs["system"] = system_prompt

       response = _client.messages.create(**kwargs)
       raw_reply = response.content[0].text

       restored_reply = _redactor.restore(raw_reply, result.token_map)
       return restored_reply
   ```

5. **Add a logging safeguard** so the application never writes raw PII to structured logs — only placeholders and truncated originals appear.

   ```python
   # audit_log.py
   import json
   import logging
   import pathlib
   import datetime

   audit_log = logging.getLogger("pii.audit")


   def log_redaction_event(
       request_id: str,
       entity_types: list[str],
       placeholder_count: int,
       log_dir: str = "./audit_logs",
   ) -> None:
       """Write a structured audit record. Never include raw PII values."""
       pathlib.Path(log_dir).mkdir(parents=True, exist_ok=True)
       record = {
           "ts": datetime.datetime.utcnow().isoformat() + "Z",
           "request_id": request_id,
           "entity_types_redacted": entity_types,
           "placeholder_count": placeholder_count,
       }
       audit_path = pathlib.Path(log_dir) / "redaction_audit.jsonl"
       with audit_path.open("a", encoding="utf-8") as fh:
           fh.write(json.dumps(record) + "\n")
       audit_log.info("audit: %s — %d entities", request_id, placeholder_count)
   ```

6. **Wire everything into a runnable script** that demonstrates the full pre/post pipeline.

   ```python
   # pipeline.py
   import uuid
   import logging
   from llm_client import chat_with_redaction, _redactor
   from audit_log import log_redaction_event

   logging.basicConfig(
       level=logging.INFO,
       format="%(levelname)s %(name)s %(message)s",
   )

   SYSTEM_PROMPT = (
       "You are a helpful assistant. "
       "When summarizing requests, always address the person by the name they provide."
   )

   SAMPLE_INPUTS = [
       (
           "Hello, I'm Alice Johnson. My email is alice.johnson@acme-corp.com "
           "and my client ID is CLT-A1B2C3D4. Please summarize my account status."
       ),
       (
           "Transfer $500 from card 4111111111111111. "
           "Call me back at +1-555-867-5309. — Bob Martinez"
       ),
   ]


   def main() -> None:
       for raw_input in SAMPLE_INPUTS:
           request_id = str(uuid.uuid4())[:8]
           redaction = _redactor.redact(raw_input)

           log_redaction_event(
               request_id=request_id,
               entity_types=list({
                   k.split("_")[1] for k in redaction.token_map
               }),
               placeholder_count=len(redaction.token_map),
           )

           reply = chat_with_redaction(raw_input, system_prompt=SYSTEM_PROMPT)
           print(f"--- request {request_id} ---")
           print("ORIGINAL :", raw_input[:80] + "...")
           print("REDACTED :", redaction.redacted_text[:80] + "...")
           print("REPLY    :", reply[:120])
           print()


   if __name__ == "__main__":
       main()
   ```

7. **Run the pipeline** and confirm redacted text is sent to the API while the response contains real names.

   ```bash
   ANTHROPIC_API_KEY=sk-ant-... python pipeline.py
   ```

   Expected log lines show `pii.redactor` logging entity placeholders (never raw values) and `pii.audit` recording counts. The printed `REPLY` contains the real name (e.g. `Alice Johnson`), restored from the token map after the model responded with `<PERSON_1>`.

## Verify

Run the pipeline and inspect the audit log:

```bash
ANTHROPIC_API_KEY=sk-ant-... python pipeline.py && \
  python -c "
import json, pathlib
lines = [json.loads(l) for l in pathlib.Path('audit_logs/redaction_audit.jsonl').read_text().splitlines()]
for r in lines:
    print(r['request_id'], r['entity_types_redacted'], r['placeholder_count'])
"
```

Expected output shows two audit records, each listing redacted entity types with `placeholder_count >= 1`. Confirm the `REPLY` output contains the original name (`Alice Johnson` / `Bob Martinez`), not the placeholder, proving restoration worked.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `PERSON` entities not detected | spaCy model not downloaded or wrong model name | Run `python -m spacy download en_core_web_lg`; verify `AnalyzerEngine()` loads without warnings about NLP engine |
| `CLIENT_ID` never matches | Regex does not match your ID format | Adjust the `regex` in `build_client_id_recognizer()` to your format; test with `re.findall(pattern, sample_text)` before wiring into Presidio |
| Placeholders leak into the final reply | Token map is request-scoped but shared across concurrent calls | Create a new `PIIRedactor()` per request, or pass `token_map` explicitly; do not use a module-level `token_map` shared across threads |
| Model output contains `<PERSON_1>` literally (restore failed) | The model wrapped the placeholder in backticks or quotes | Strip surrounding code formatting from the model response before calling `restore()`; add `raw_reply.strip('`"\' ')` around the model text |
| `Credit card` numbers not redacted | Presidio `CREDIT_CARD` requires the Luhn-valid format | Ensure the test card number passes Luhn check (e.g. `4111111111111111`); synthetic non-Luhn numbers are not recognized by default |
| Audit log contains raw PII | `log_redaction_event` called with original text instead of token_map keys | Pass only `entity_types` (extracted from placeholder keys) and counts — never pass `token_map.values()` to the audit function |

## Next

- Add output scanning with `guardrails-implementation` to detect if the model hallucinates new PII that was never in the input.
- Integrate `llm-observability-stack-2026` to emit per-request redaction metrics (entity type distribution, placeholder counts) to your observability backend.
- Extend the custom recognizer set with domain-specific patterns (SSN, IBAN, medical record numbers) by adding additional `PatternRecognizer` or `SpacyRecognizer` subclasses.

## References

- [knowledge/geek/ai/llm-integration/guardrails-implementation](../../../knowledge/geek/ai/llm-integration/guardrails-implementation) — the layered-defense and PII-scrubbing patterns in this methodology back the pre/post pipeline structure in Steps 3–4; specifically, the `GuardrailsPipeline` class shape informed the `PIIRedactor.redact()` / `restore()` split
- [knowledge/geek/ai/llm-integration/guardrails-basics](../../../knowledge/geek/ai/llm-integration/guardrails-basics) — establishes the input-validation vs. output-validation boundary that determines where token substitution must occur relative to the API call in Step 4
- [knowledge/geek/ai/ml-ops/llm-observability-stack-2026](../../../knowledge/geek/ai/ml-ops/llm-observability-stack-2026) — the audit JSONL schema in Step 5 is designed to forward to the observability stack's structured-log ingest endpoint with zero schema changes
