# Internal Confluence Page Notes (Draft Inputs)

Page title: Agentic Research & Action Assistant — Design Overview

Purpose
- Build a multi-agent assistant that produces a deliverable package:
  1) executive summary
  2) client-ready email
  3) action items
- Enforce grounding with citations and “Not found in sources”.

Key components
- Planner: breaks task into steps and deliverables.
- Research: retrieves evidence snippets from the knowledge base and returns citations.
- Writer: drafts outputs using only research notes.
- Verifier: checks for missing evidence, contradictions, and citation coverage.

Non-goals (v1)
- No confidential data in repo.
- No production deployment requirements (optional demo only).
