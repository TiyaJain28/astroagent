from langgraph.graph import StateGraph, END

from app.state.astro_state import AstroState
from app.graph.nodes import (
    router_node,
    reasoning_node,
    tool_node,transit_node,
    interpretation_node
)

def route_decision(state):
    return state["next_step"]

def build_graph():
    workflow = StateGraph(AstroState)

    workflow.add_node("router", router_node)
    workflow.add_node("reasoning", reasoning_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("interpretation", interpretation_node)
    workflow.add_node(
    "transit",
    transit_node
)
    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "birth_chart": "reasoning",
        "daily_transit": "transit",
        "general": "interpretation"
    }
)
    workflow.add_edge("reasoning", "tool")
    workflow.add_edge("tool", "interpretation")
    workflow.add_edge("interpretation", END)
    workflow.add_edge(
    "transit",
    "interpretation"
)
    return workflow.compile()