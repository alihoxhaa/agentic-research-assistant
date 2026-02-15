from agents.state import AgentState, AgentTrace

def planner_node(state: AgentState) -> AgentState:
    state.plan = [
        "Clarify deliverable(s) requested",
        "Retrieve relevant evidence from docs",
        "Draft deliverable using only evidence",
        "Verify grounding + citations; mark unknowns",
    ]
    state.trace.append(AgentTrace(
        step="1",
        agent="Planner",
        action="Create execution plan",
        outcome=f"Plan created with {len(state.plan)} steps"
    ))
    return state
