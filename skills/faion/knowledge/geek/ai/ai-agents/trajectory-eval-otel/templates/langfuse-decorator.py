from langfuse.decorators import observe

@observe()
def agent_step(input):
    # inputs/outputs auto-captured to Langfuse
    return llm_call(input)
