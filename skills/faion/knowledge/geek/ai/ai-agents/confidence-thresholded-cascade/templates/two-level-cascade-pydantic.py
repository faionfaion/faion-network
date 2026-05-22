# purpose: two-level cascade (Haiku -> Opus) with Pydantic schema and explicit IDK
# consumes: task string + Anthropic API key
# produces: answer string (from cheap leg if confident, strong leg otherwise)
# depends-on: anthropic SDK, pydantic v2
# token-budget-impact: cheap ~400 tokens, escalated cases ~2k tokens
"""Two-level cascade with Pydantic-validated cheap-model schema."""
from pydantic import BaseModel, Field
from anthropic import Anthropic

client = Anthropic()
THRESHOLD = 0.85


class CheapAnswer(BaseModel):
    reasoning: str
    answer: str
    confidence_0_to_1: float = Field(ge=0.0, le=1.0)
    requires_escalation: bool


class StrongAnswer(BaseModel):
    reasoning: str
    answer: str


def cascade(task: str) -> str:
    cheap = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Task: {task}\nReturn STRICT JSON matching the CheapAnswer schema."}],
    )
    parsed = CheapAnswer.model_validate_json(cheap.content[0].text)
    if not parsed.requires_escalation and parsed.confidence_0_to_1 >= THRESHOLD:
        return parsed.answer
    strong = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{"role": "user", "content": f"Task: {task}\nReturn STRICT JSON matching the StrongAnswer schema."}],
    )
    return StrongAnswer.model_validate_json(strong.content[0].text).answer
