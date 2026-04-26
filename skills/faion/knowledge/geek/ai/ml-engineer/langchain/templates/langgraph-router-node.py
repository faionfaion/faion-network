# LangGraph routing node using structured output
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

class RouteDecision(BaseModel):
    next_node: str  # "executor" | "critic" | "done"
    reasoning: str

def router_node(state: dict) -> dict:
    model = ChatAnthropic(model="claude-sonnet-4-20250514")
    chain = (
        ChatPromptTemplate.from_template(
            "Given state: {state}\nDecide next step. Options: executor, critic, done."
        )
        | model.with_structured_output(RouteDecision)
    )
    decision = chain.invoke({"state": str(state)})
    return {"next": decision.next_node}
