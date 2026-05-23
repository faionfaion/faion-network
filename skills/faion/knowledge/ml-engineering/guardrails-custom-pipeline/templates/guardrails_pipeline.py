"""guardrails_pipeline.py.
purpose: working skeleton of custom guardrails pipeline
consumes: user input string + optional retrieval context
produces: code (importable module + GuardrailResult)
depends-on: openai >= 1.0; python >= 3.11
token-budget-impact: +1200t when loaded as content/05-examples expansion.
"""
from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass, field
from typing import Optional

from openai import AsyncOpenAI


@dataclass
class GuardrailConfig:
    max_input_length: int = 4000
    max_output_length: int = 8000
    enable_pii_detection: bool = True
    enable_injection_detection: bool = True
    enable_content_moderation: bool = True
    enable_hallucination_detection: bool = False


@dataclass
class GuardrailResult:
    is_safe: bool
    input_modified: bool
    output_modified: bool
    original_input: str
    sanitized_input: Optional[str]
    original_output: Optional[str]
    filtered_output: Optional[str]
    violations: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class PIIDetector:
    PATTERNS = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "phone": r"\b(?:\+?1[-.]?)?\(?[0-9]{3}\)?[-.]?[0-9]{3}[-.]?[0-9]{4}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    }
    COMPILED = {k: re.compile(v, re.IGNORECASE) for k, v in PATTERNS.items()}

    def mask(self, text: str) -> tuple[str, list[dict]]:
        findings: list[dict] = []
        out = text
        for kind, rx in self.COMPILED.items():
            out, n = rx.subn(f"[{kind.upper()}]", out)
            if n:
                findings.append({"type": kind, "count": n})
        return out, findings


class PromptInjectionDetector:
    PATTERNS = [
        r"ignore\s+(?:all\s+)?(?:previous|above|prior)\s+(?:instructions?|prompts?)",
        r"forget\s+(?:everything|all|your)\s+(?:instructions?|training)",
        r"you\s+are\s+now\s+(?:in\s+)?(?:developer|debug|admin)\s+mode",
        r"system\s*:\s*",
        r"<\|im_start\|>|<\|im_end\|>",
    ]
    COMPILED = [re.compile(p, re.IGNORECASE) for p in PATTERNS]

    def detect(self, text: str) -> tuple[bool, list[str]]:
        hits: list[str] = []
        for rx in self.COMPILED:
            m = rx.findall(text)
            if m:
                hits.extend(m if isinstance(m[0], str) else [x[0] for x in m])
        return bool(hits), hits


class ContentModerator:
    def __init__(self, client: AsyncOpenAI) -> None:
        self.client = client

    async def acheck(self, text: str) -> tuple[bool, dict]:
        r = await self.client.moderations.create(input=text)
        res = r.results[0]
        return bool(res.flagged), dict(res.categories)


class HallucinationDetector:
    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4o") -> None:
        self.client = client
        self.model = model

    async def acheck(self, response: str, context: str) -> dict:
        prompt = (
            "Decide if RESPONSE is fully supported by CONTEXT. "
            f"CONTEXT:\n<ctx>{context}</ctx>\n"
            f"RESPONSE:\n<resp>{response}</resp>\n"
            'Return JSON {"is_grounded": bool, "unsupported_claims": [str], "confidence": float}.'
        )
        r = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        return json.loads(r.choices[0].message.content)


class GuardrailsPipeline:
    def __init__(self, client: AsyncOpenAI, model: str = "gpt-4o", config: Optional[GuardrailConfig] = None) -> None:
        self.client = client
        self.model = model
        self.config = config or GuardrailConfig()
        self.pii = PIIDetector()
        self.injection = PromptInjectionDetector()
        self.moderator = ContentModerator(client)
        self.judge = HallucinationDetector(client, model)

    async def process_input(self, text: str) -> tuple[Optional[str], list[dict]]:
        cfg = self.config
        violations: list[dict] = []
        sanitised = text[: cfg.max_input_length]
        if len(text) > cfg.max_input_length:
            violations.append({"type": "length", "detail": "input truncated"})

        if cfg.enable_pii_detection:
            sanitised, found = self.pii.mask(sanitised)
            if found:
                violations.append({"type": "pii", "detail": "masked", "findings": found})

        if cfg.enable_injection_detection:
            hit, dets = self.injection.detect(sanitised)
            if hit:
                violations.append({"type": "injection", "detail": "blocked", "detections": dets})
                return None, violations

        if cfg.enable_content_moderation:
            flagged, _ = await self.moderator.acheck(sanitised)
            if flagged:
                violations.append({"type": "moderation", "detail": "input flagged"})
                return None, violations

        return sanitised, violations

    async def process_output(self, output: str, context: Optional[str] = None) -> tuple[str, list[dict]]:
        cfg = self.config
        violations: list[dict] = []
        filtered = output[: cfg.max_output_length]
        if len(output) > cfg.max_output_length:
            violations.append({"type": "length", "detail": "output truncated"})
        if cfg.enable_content_moderation:
            flagged, _ = await self.moderator.acheck(filtered)
            if flagged:
                violations.append({"type": "moderation", "detail": "output flagged"})
                filtered = "[Response filtered due to content policy]"
        if cfg.enable_hallucination_detection and context:
            judged = await self.judge.acheck(filtered, context)
            if not judged.get("is_grounded", True):
                violations.append(
                    {"type": "hallucination", "detail": "ungrounded", "claims": judged.get("unsupported_claims", [])}
                )
        return filtered, violations

    async def arun(self, text: str, system_prompt: str = "", context: Optional[str] = None) -> GuardrailResult:
        sanitised, in_v = await self.process_input(text)
        if sanitised is None:
            return GuardrailResult(
                is_safe=False, input_modified=True, output_modified=False,
                original_input=text, sanitized_input=None,
                original_output=None, filtered_output=None,
                violations=in_v, metadata={"model": self.model, "stage": "input_blocked"},
            )
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": sanitised})
        completion = await self.client.chat.completions.create(model=self.model, messages=msgs)
        raw = completion.choices[0].message.content or ""
        filtered, out_v = await self.process_output(raw, context)
        all_v = in_v + out_v
        is_safe = not any(v["type"] in {"injection", "moderation"} for v in all_v)
        return GuardrailResult(
            is_safe=is_safe,
            input_modified=sanitised != text,
            output_modified=filtered != raw,
            original_input=text, sanitized_input=sanitised,
            original_output=raw, filtered_output=filtered,
            violations=all_v, metadata={"model": self.model, "stage": "complete"},
        )
