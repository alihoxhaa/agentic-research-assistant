# Agentic Research & Action Assistant (Multi-Agent System)

A multi-agent assistant that takes a business task (e.g., “Summarize competitor positioning from our docs + draft a client-ready email + create action items”) and coordinates specialized agents to produce a grounded, traceable “deliverable package”.

This repository implements the required workflow:
**plan → research/retrieve → draft → verify**  
…and includes a **single corrective retry** (verify → revise → verify) to stabilize quality.

---

## Key capabilities

### Deliverable package output (always structured)
The Writer produces a consistent package with:
1) **Executive Summary**
2) **Client Email Draft**
3) **Action Items**

### Grounded outputs with traceability
- **Citations:** research produces a note list and a `note id → source file` mapping; the Writer uses `(see note [#])`.
- **Agent Trace:** every agent appends a structured log entry (`step, agent, action, outcome`) to the shared state.

### Safety & correctness
- **Prompt injection defense:** document text is treated as untrusted; “instructions inside docs” are ignored.
- **Verifier agent:** checks grounding and citation correctness. If evidence is missing, outputs must say **“Not found in sources.”**

### Quality stabilization (Writer↔Verifier retry loop)
If the Verifier returns `VERDICT: FAIL`, the workflow triggers **one rewrite attempt**:
- The Writer receives `FIX_INSTRUCTIONS` and must correct citations/claims
- The Verifier re-checks
- The loop runs **at most once** (prevents infinite loops)

### Evaluation harness
- Runs a set of tasks from `eval/questions.jsonl`
- Prints PASS/FAIL to terminal
- Writes run results to `eval/results.jsonl`

---

## Architecture (how it works)

### Agents
- **Planner** (`agents/planner.py`)  
  Produces a short execution plan for the task.
- **Research** (`agents/research.py`)  
  Uses vector search to retrieve relevant chunks from the knowledge base; outputs:
  - `notes`: `[1] ... [2] ...`
  - `citations`: `[{id: "1", source: "..."} ...]`
- **Writer** (`agents/writer.py`)  
  Writes the deliverable package using only the research notes. Enforces:
  - every factual bullet must have `(see note [#])` or be labeled **Not found in sources**
  - if Verifier failed, rewrite using `FIX_INSTRUCTIONS`
- **Verifier** (`agents/verifier.py`)  
  Checks grounding; returns strict PASS/FAIL with issues and fix instructions.

### Routing (LangGraph)
Defined in `agents/graph.py`:
- `planner → research → writer → verifier`
- If `verifier` FAIL and `retried=False`: `writer → verifier` once
- Else: END

### Shared state
`agents/state.py` defines a Pydantic `AgentState` shared across all nodes:
- `task, plan, notes, citations, draft, verifier_feedback, final_output, trace, errors, retried`

---

## Nice-to-haves implemented (per assignment)

This project includes multiple optional enhancements beyond the baseline:
- **Prompt injection defense** (treat doc text as untrusted + filtering step)
- **Evaluation set** with automated PASS/FAIL checks (`eval/run_eval.py`)
- **Multi-output mode** (deliverable package: summary + email + action items)
- **Quality stabilization loop** (single retry based on Verifier FIX_INSTRUCTIONS)
- **Traceability** (agent trace + citations)

---


## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows
   source .venv/bin/activate   # Unix/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys

4. run ingestion:
   ```bash
   python -m tools.ingest
   ```

4.1 optional: run eval test programaticaly to test example tasks
   ```bash
   python -m eval.run_eval
   '''

## Running the Application

```bash
streamlit run app/streamlit_app.py
```

## Deployment

following the setup, app is meant to deploy locally
or through link: 

## App tip
on the sidebar you can find 5 demos corresponding to the example tasks