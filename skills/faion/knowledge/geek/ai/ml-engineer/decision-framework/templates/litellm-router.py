# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

# LiteLLM complexity-based router: simple→DeepSeek, balanced→Sonnet, complex→Opus
from litellm import Router

router = Router(
    model_list=[
        {"model_name": "fast", "litellm_params": {"model": "deepseek/deepseek-chat"}},
        {"model_name": "balanced", "litellm_params": {"model": "anthropic/claude-sonnet-4-20250514"}},
        {"model_name": "powerful", "litellm_params": {"model": "anthropic/claude-opus-4-5-20251101"}},
    ]
)

def route_by_complexity(task: str, complexity: str) -> str:
    """
    complexity: "simple" | "medium" | "complex"
    - simple: extraction, classification, FAQ-like (<500 tokens)
    - medium: standard generation, code, analysis
    - complex: deep reasoning, contract analysis, research synthesis
    """
    model_map = {"simple": "fast", "medium": "balanced", "complex": "powerful"}
    model = model_map.get(complexity, "balanced")
    response = router.completion(
        model=model,
        messages=[{"role": "user", "content": task}],
    )
    return response.choices[0].message.content
