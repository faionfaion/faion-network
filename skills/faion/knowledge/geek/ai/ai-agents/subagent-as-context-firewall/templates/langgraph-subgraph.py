# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

from langgraph.graph import StateGraph

def investigator_subgraph():
    sg = StateGraph(SubgraphState)
    sg.add_node("scan", scan_files)
    sg.add_node("extract", extract_refs)
    sg.set_entry_point("scan")
    return sg.compile()

# Parent graph
parent = StateGraph(MainState)
parent.add_node("investigate", investigator_subgraph().invoke)
# parent.state only sees the subgraph's RETURN, not its internal scan_state
