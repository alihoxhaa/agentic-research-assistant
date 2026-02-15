import json
from pathlib import Path
from typing import Dict, Any, List

from agents.graph import build_graph
from agents.state import AgentState


REQ_SECTIONS = ["Executive Summary", "Client Email Draft", "Action Items"]


def basic_checks(result: AgentState) -> Dict[str, Any]:
    text = (result.final_output or "").lower()
    feedback = (result.verifier_feedback or "").upper()

    has_verdict = "VERDICT:" in feedback
    passed = "VERDICT: PASS" in feedback

    # section checks (soft: only require if writer is designed to always output package)
    section_hits = {s: (s.lower() in text) for s in REQ_SECTIONS}

    # note reference heuristic
    text_for_refs = (result.draft or result.final_output or "")
    has_note_refs = "(see note [" in text_for_refs

    # "not found" behavior heuristic
    has_not_found = "not found in sources" in text

    return {
        "has_verdict": has_verdict,
        "passed": passed,
        "section_hits": section_hits,
        "has_note_refs": has_note_refs,
        "has_not_found": has_not_found,
        "trace_len": len(result.trace or []),
        "citations_len": len(result.citations or []),
    }


def main():
    qs_path = Path("eval/questions.jsonl")
    out_path = Path("eval/results.jsonl")

    graph = build_graph()
    results: List[Dict[str, Any]] = []

    for line in qs_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        q = json.loads(line)
        qid = q["id"]
        task = q["task"]

        state = AgentState(task=task)
        out = graph.invoke(state)
        if isinstance(out, dict):
            out = AgentState(**out)

        checks = basic_checks(out)

        row = {
            "id": qid,
            "task": task,
            "verifier_feedback": out.verifier_feedback,
            "passed": checks["passed"],
            "checks": checks,
            "citations": out.citations,
            "trace": [t.model_dump() for t in (out.trace or [])],
        }
        results.append(row)

        print(f"{qid}: {'PASS' if checks['passed'] else 'FAIL'} | citations={checks['citations_len']} | note_refs={checks['has_note_refs']}")

    out_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in results), encoding="utf-8")
    print(f"\nWrote {len(results)} results to {out_path}")


if __name__ == "__main__":
    main()