from agents.state import AgentState, AgentTrace
from langchain_openai import ChatOpenAI


VERIFIER_SYSTEM = """You are the Verifier/QA agent.
Goal: Prevent unsupported claims while allowing conservative answers.

Rules:
- The draft must be grounded ONLY in the research notes.
- Non-trivial factual claims should include a reference like (see note [#]).
- Paraphrasing is allowed as long as the meaning matches the notes (do NOT require exact phrasing).
- If the draft explicitly states "Not found in sources" for a requested detail, that is acceptable and should not be penalized.
- If a bullet/action item has "(Not found in sources.)", treat it as a conservative placeholder and do not fail solely because of it.
- FAIL only when the draft asserts a specific fact that contradicts the notes or clearly goes beyond them without "Not found in sources".

Return EXACTLY this format:

VERDICT: PASS or FAIL
ISSUES:
- ...
FIX_INSTRUCTIONS:
- ...
"""


def verifier_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

    notes_text = "\n".join(state.notes or [])
    draft_text = state.draft or ""

    user_prompt = f"""Research Notes:
{notes_text}

Draft:
{draft_text}

Check grounding and note-references. If unsupported claims exist or references are missing, FAIL.
"""

    resp = llm.invoke(
        [
            {"role": "system", "content": VERIFIER_SYSTEM},
            {"role": "user", "content": user_prompt},
        ]
    )

    feedback = resp.content.strip()
    state.verifier_feedback = feedback

    verdict_line = next((ln for ln in feedback.splitlines() if ln.startswith("VERDICT:")), "")
    passed = "PASS" in verdict_line

    if passed:
        state.final_output = state.draft
        outcome = "PASS: grounded"
    else:
        state.final_output = (
            "VERIFIER FAILED — Output not fully grounded in sources.\n\n"
            f"{feedback}\n\n"
            "Policy: If sources don’t support it, the assistant must say: Not found in sources."
        )
        outcome = "FAIL: ungrounded or missing note refs"

    state.trace.append(
        AgentTrace(
            step="4",
            agent="Verifier",
            action="LLM grounding + evidence-reference enforcement",
            outcome=outcome,
        )
    )
    return state
