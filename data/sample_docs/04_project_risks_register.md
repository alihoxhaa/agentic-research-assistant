# Project Risks Register (Synthetic)

R1 — Ungrounded claims in generated drafts
- Impact: High
- Likelihood: Medium
- Signals: Draft includes numbers/dates/names not present in sources
- Mitigation: Verifier blocks unsupported claims; require citations for factual statements; show “Not found in sources”.

R2 — Prompt injection via documents
- Impact: High
- Likelihood: Medium
- Signals: Documents contain instructions like “ignore previous rules”
- Mitigation: Research agent treats docs as untrusted data; strip/flag instruction-like text; tool allowlist.

R3 — Unclear deliverables and inconsistent formats
- Impact: Medium
- Likelihood: High
- Signals: User asks for summary + email + action list; output mixes formats
- Mitigation: Planner outputs explicit deliverable checklist; writer produces separate sections.

R4 — Retrieval misses relevant context (chunking issues)
- Impact: Medium
- Likelihood: Medium
- Signals: Important details not retrieved; incomplete citations
- Mitigation: Tune chunk size/overlap; include metadata (source, section); increase k for recall.
