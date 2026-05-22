"""
purpose: PromptTemplate dataclass + render() — pin prompts as code constants for diff and CI snapshot tests.
consumes: system string, user_template with `{var}` placeholders, optional few-shot examples list.
produces: rendered messages array (list[dict]) for OpenAI-compatible chat completions.
depends-on: stdlib only (dataclasses, typing).
token-budget-impact: zero overhead beyond the literal token count; examples capped at 3–5.
"""
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class PromptTemplate:
    system: str
    user_template: str
    examples: List[Dict[str, str]] = field(default_factory=list)
    version: str = "v1"

    def render(self, **kwargs) -> List[Dict[str, str]]:
        """Render the template into a messages array ready for any OpenAI-compatible API."""
        msgs: List[Dict[str, str]] = [{"role": "system", "content": self.system}]
        for ex in self.examples:
            msgs.append({"role": "user", "content": ex["input"]})
            msgs.append({"role": "assistant", "content": ex["output"]})
        msgs.append({"role": "user", "content": self.user_template.format(**kwargs)})
        return msgs


# Example: zero-shot extraction
EXTRACT_JSON = PromptTemplate(
    system="Extract the requested fields. Return only valid JSON, no prose.",
    user_template='Text: {text}\n\nReturn: {{"sentiment": str, "topics": [str]}}',
    version="extract-v1",
)
