# purpose: RouteLLM-style router client emitted by preference-trained-router
# consumes: trained classifier + weak/strong model handles + uncertainty_band
# produces: route() that picks model with uncertainty fallback
# depends-on: r4-uncertainty-fallback
# token-budget-impact: ~250 tokens
"""Minimal RouteLLM wrapper.

Input  → user prompt
Output → completion, plus the route taken (weak | strong).

Threshold (`mf_threshold`) is the operating point you tuned on the
validation set — see content/01-router-architecture.xml.
"""

from dataclasses import dataclass

from routellm.controller import Controller


@dataclass
class RouteResult:
    text: str
    route: str  # "weak" | "strong"


class PreferenceRouter:
    def __init__(
        self,
        strong_model: str = "claude-opus-4",
        weak_model: str = "claude-haiku-4-5",
        mf_threshold: float = 0.11593,
    ) -> None:
        self.threshold = mf_threshold
        self.controller = Controller(
            routers=["mf"],
            strong_model=strong_model,
            weak_model=weak_model,
        )

    def chat(self, prompt: str) -> RouteResult:
        score = self.controller.route(prompt)            # 0..1
        route = "strong" if score >= self.threshold else "weak"
        resp = self.controller.chat.completions.create(
            model=f"router-mf-{self.threshold}",
            messages=[{"role": "user", "content": prompt}],
        )
        return RouteResult(text=resp.choices[0].message.content, route=route)
