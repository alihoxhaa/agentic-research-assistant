import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import uuid
from datetime import datetime

import streamlit as st

from agents.graph import build_graph
from agents.state import AgentState


DEMO_TASKS = [
    "Summarize the top 5 risks mentioned across these project docs and propose mitigations.",
    "Create a client update email from the latest weekly report doc.",
    "Compare two approaches described in docs and recommend one with justification.",
    "Extract all deadlines + owners from docs and format them into an action list.",
    "Draft an internal Confluence page from a set of markdown notes.",
]


def _format_citations(citations: list[dict] | None) -> list[str]:
    if not citations:
        return []
    lines = []
    for c in citations:
        nid = c.get("id", "?")
        src = c.get("source", "unknown")
        # show filename only (cleaner), keep full path in tooltip-style by showing both if different
        fname = src.replace("\\", "/").split("/")[-1]
        if fname and fname != src:
            lines.append(f"[{nid}] {fname} — {src}")
        else:
            lines.append(f"[{nid}] {src}")
    return lines


def _trace_rows(trace) -> list[dict]:
    rows = []
    for t in trace or []:
        # t may be pydantic model or dict
        if hasattr(t, "model_dump"):
            rows.append(t.model_dump())
        elif isinstance(t, dict):
            rows.append(t)
        else:
            rows.append(
                {
                    "step": getattr(t, "step", ""),
                    "agent": getattr(t, "agent", ""),
                    "action": getattr(t, "action", ""),
                    "outcome": getattr(t, "outcome", ""),
                }
            )
    return rows


def main():
    st.set_page_config(page_title="Agentic Research & Action Assistant", layout="wide", initial_sidebar_state="expanded")
    st.title("Agentic Research & Action Assistant")
    st.caption("Planner → Research → Writer → Verifier (single retry on FAIL). Grounded outputs with citations + trace.")

    # Build graph once per session
    if "graph" not in st.session_state:
        st.session_state.graph = build_graph()

    # Demo buttons
    with st.sidebar:
        st.header("Demo tasks")
        st.write("Click to load a demo prompt into the textbox.")
        for i, task in enumerate(DEMO_TASKS, start=1):
            if st.button(f"Demo {i}", use_container_width=True):
                st.session_state["task_text"] = task

        st.divider()
        st.caption("Tip: If you changed docs, rerun ingestion:\n`python -m tools.ingest`")

    task = st.text_area(
        "Task",
        key="task_text",
        height=130,
        placeholder="Write a business task… (e.g., summarize, draft email, extract owners/dates).",
    )

    col_run, col_clear = st.columns([1, 1])
    run_btn = col_run.button("Run", type="primary", use_container_width=True)
    clear_btn = col_clear.button("Clear", use_container_width=True)

    if clear_btn:
        st.session_state["task_text"] = ""
        st.rerun()

    if run_btn:
        if not task or not task.strip():
            st.warning("Please enter a task.")
            st.stop()

        run_id = uuid.uuid4().hex[:8]
        started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with st.spinner("Running agents…"):
            state = AgentState(task=task.strip())
            out = st.session_state.graph.invoke(state)

            # LangGraph may return dict
            if isinstance(out, dict):
                out = AgentState(**out)

        st.success(f"Done. Run ID: `{run_id}` • Started: {started}")

        left, right = st.columns([2, 1], gap="large")

        with left:
            st.subheader("Final Deliverable")
            st.write(out.final_output or "(empty)")

        with right:
            st.subheader("Citations")
            citations_lines = _format_citations(out.citations)
            if citations_lines:
                for ln in citations_lines:
                    st.markdown(f"- {ln}")
            else:
                st.write("(none)")

            st.subheader("Agent Trace")
            rows = _trace_rows(out.trace)
            if rows:
                st.dataframe(rows, use_container_width=True, hide_index=True)
            else:
                st.write("(no trace)")

            with st.expander("Verifier Feedback (raw)"):
                st.code(out.verifier_feedback or "(none)", language="text")


if __name__ == "__main__":
    main()