"""
PromptTemplate — reusable prompt with system, user template, and few-shot examples.

Usage:
    template = PromptTemplate(
        system="You are a sentiment classifier. Respond with: positive, negative, or neutral.",
        user_template="Classify: {text}",
        examples=[
            {"input": "Classify: I love this!", "output": "positive"},
            {"input": "Classify: This is terrible.", "output": "negative"},
        ]
    )
    messages = template.render(text="This exceeded my expectations!")
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
