# __faion_header_v1__
# purpose: Structured JSON logger with request_id correlation
# consumes: see content/02-output-contract.xml
# produces: rubric; depends-on: content/01-core-rules.xml#indexed-foreign-keys
# faion_header_json: {"__faion_header__":{"purpose":"Structured JSON logger with request_id correlation","consumes":"see content/02-output-contract.xml","produces":"rubric","depends_on":"content/01-core-rules.xml#indexed-foreign-keys","token_budget_impact":"~150 tokens when loaded"}}
import json
import logging
import sys


def get_logger(name: str) -> logging.Logger:
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter('%(message)s'))
    l = logging.getLogger(name)
    l.handlers.clear()
    l.addHandler(h)
    l.setLevel(logging.INFO)
    return l


def log(logger: logging.Logger, level: str, event: str, **fields) -> None:
    payload = {"event": event, "level": level, **fields}
    getattr(logger, level)(json.dumps(payload, default=str))
