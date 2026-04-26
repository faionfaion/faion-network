"""
LangGraph Corrective RAG workflow skeleton.
Nodes: retrieve → grade_documents → [rewrite_query | web_search | generate]
"""
from typing import Literal
from langgraph.graph import StateGraph, END
from templates.state_schemas import CorrectiveRAGState


def retrieve(state: CorrectiveRAGState) -> dict:
    docs = vector_store.similarity_search(state["question"], k=4)
    return {"documents": [d.page_content for d in docs]}


def grade_documents(state: CorrectiveRAGState) -> dict:
    filtered, web_needed = [], False
    for doc in state["documents"]:
        if document_grader.grade(state["question"], doc).binary_score == "yes":
            filtered.append(doc)
    if len(filtered) < 2:
        web_needed = True
    return {"documents": filtered, "web_search_needed": web_needed}


def rewrite_query(state: CorrectiveRAGState) -> dict:
    rewritten = query_rewriter.rewrite(state["question"], state["current_query"])
    retries = state.get("retries", 0) + 1
    return {"current_query": rewritten.rewritten_query, "retries": retries}


def web_search(state: CorrectiveRAGState) -> dict:
    results = tavily_search.search(state["question"], max_results=3)
    extra = [r["content"] for r in results]
    return {"documents": state["documents"] + extra, "web_search_needed": False}


def generate(state: CorrectiveRAGState) -> dict:
    context = "\n\n".join(state["documents"])
    answer = rag_chain.invoke({"question": state["question"], "context": context})
    return {"generation": answer}


def decide_after_grading(state: CorrectiveRAGState) -> Literal["web_search", "rewrite_query", "generate"]:
    if state["web_search_needed"]:
        if state.get("retries", 0) < state.get("max_retries", 2):
            return "rewrite_query"
        return "web_search"
    return "generate"


def build_crag():
    wf = StateGraph(CorrectiveRAGState)
    wf.add_node("retrieve", retrieve)
    wf.add_node("grade_documents", grade_documents)
    wf.add_node("rewrite_query", rewrite_query)
    wf.add_node("web_search", web_search)
    wf.add_node("generate", generate)
    wf.set_entry_point("retrieve")
    wf.add_edge("retrieve", "grade_documents")
    wf.add_conditional_edges("grade_documents", decide_after_grading,
                             {"rewrite_query": "rewrite_query",
                              "web_search": "web_search",
                              "generate": "generate"})
    wf.add_edge("rewrite_query", "retrieve")
    wf.add_edge("web_search", "generate")
    wf.add_edge("generate", END)
    return wf.compile()
