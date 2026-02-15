from agents.state import AgentState, AgentTrace
from tools.retrieval import query_vectorstore
from tools.safety import strip_prompt_injection


def research_node(state: AgentState) -> AgentState:
    docs = query_vectorstore(state.task, k=6)

    notes = []
    citations = []

    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown")
        raw = (d.page_content or "").strip()
        safe_text = strip_prompt_injection(raw)

        snippet = " ".join(safe_text.split())
        snippet = snippet[:450] + ("..." if len(snippet) > 450 else "")

        notes.append(f"[{i}] {snippet}")
        citations.append({"id": str(i), "source": src})

    state.notes = notes
    state.citations = citations

    state.trace.append(
        AgentTrace(
            step="2",
            agent="Research",
            action="Vector search (Chroma) + prompt-injection filtering",
            outcome=f"Retrieved {len(docs)} chunks with citations",
        )
    )
    return state