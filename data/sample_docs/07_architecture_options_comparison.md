# Architecture Options — Comparison (Synthetic)

Option A — LangGraph (recommended)
- Strengths: Explicit state machine; deterministic routing; clear shared state; traceability.
- Weaknesses: More boilerplate vs simpler “role/task” frameworks.

Option B — LangChain Agents
- Strengths: Fast to prototype; many examples.
- Weaknesses: Less structured for complex flows; harder to audit.

Decision criteria
- Must show planner → research → writer → verifier routing.
- Must keep outputs grounded with citations.
- Must provide an agent trace log.
