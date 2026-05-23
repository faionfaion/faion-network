# purpose: Reusable Playwright extractors + normalizers for the daily scrape.
# consumes: Playwright Page handle, field schema.
# produces: per-row dict with normalizers_applied[] populated.
# depends-on: playwright (sync API), stdlib datetime, locale-aware Decimal.
# token-budget-impact: ~300 tokens when loaded as context.

from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any


def normalize_text(s: str | None) -> tuple[str | None, list[str]]:
    if s is None:
        return None, []
    v = re.sub(r"[\x00-\x1f\x7f]", "", s)
    v = re.sub(r"\s+", " ", v).strip()
    return (v or None), ["text-trim", "text-collapse-ws", "text-strip-nonprintable"]


def parse_price(raw: str, locale: str = "en-US") -> tuple[float | None, str | None]:
    # Locale-aware: detect group + decimal separators.
    group_sep, dec_sep = (",", ".") if locale.lower().startswith("en") else (".", ",")
    cleaned = re.sub(r"[^\d\-+.,\s]", "", raw)
    cleaned = cleaned.replace(group_sep, "").replace(" ", "").replace(dec_sep, ".")
    try:
        return float(Decimal(cleaned)), None
    except (InvalidOperation, ValueError):
        return None, f"unparseable price: {raw}"


def parse_date_iso(raw: str) -> tuple[str | None, str | None]:
    for fmt in ("%Y-%m-%d", "%d %b %Y", "%B %d, %Y", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).date().isoformat(), None
        except ValueError:
            continue
    return None, f"unparseable date: {raw}"


def extract_text(locator) -> str | None:
    try:
        return locator.first.text_content()
    except Exception:
        return None


def extract_many(locator) -> list[str]:
    try:
        return locator.all_text_contents()
    except Exception:
        return []


def build_row(
    fields_raw: dict[str, Any],
    schema_kinds: dict[str, str],
) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    applied: set[str] = set()
    failures: list[dict[str, str]] = []
    for k, raw in fields_raw.items():
        kind = schema_kinds.get(k, "text")
        if raw is None:
            fields[k] = None
            continue
        if kind == "text":
            v, used = normalize_text(str(raw))
            fields[k] = v
            applied.update(used)
        elif kind == "price":
            v, reason = parse_price(str(raw))
            fields[k] = v
            applied.add("price-to-float")
            if reason:
                failures.append({"field": k, "reason": reason})
        elif kind == "date":
            v, reason = parse_date_iso(str(raw))
            fields[k] = v
            applied.add("date-to-iso")
            if reason:
                failures.append({"field": k, "reason": reason})
        else:
            fields[k] = raw
    return {"fields": fields, "normalizers_applied": sorted(applied), "parse_failures": failures}
