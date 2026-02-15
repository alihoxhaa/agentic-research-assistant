from langgraph.graph import StateGraph, END
from agents.state import AgentState

from agents.planner import planner_node
from agents.research import research_node
from agents.writer import writer_node
from agents.verifier import verifier_node


def _route_after_verifier(state: AgentState) -> str:
    fb = (state.verifier_feedback or "").upper()
    if "VERDICT: FAIL" in fb and not state.retried:
        return "retry"
    return "end"


def _mark_retried(state: AgentState) -> AgentState:
    state.retried = True
    return state


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("planner", planner_node)
    g.add_node("research", research_node)
    g.add_node("writer", writer_node)
    g.add_node("verifier", verifier_node)
    g.add_node("mark_retried", _mark_retried)

    g.set_entry_point("planner")
    g.add_edge("planner", "research")
    g.add_edge("research", "writer")
    g.add_edge("writer", "verifier")

    # Conditional: if FAIL and not retried, go back to writer once
    g.add_conditional_edges(
        "verifier",
        _route_after_verifier,
        {"retry": "mark_retried", "end": END},
    )
    g.add_edge("mark_retried", "writer")

    return g.compile()