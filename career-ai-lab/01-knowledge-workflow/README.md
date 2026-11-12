# 01 — Permission-aware Knowledge Workflow

**Inspired by:** FERI Junior AI Developer (AI agents, APIs, business-process automation, authorization, monitoring).

## Current MVP
A **deterministic retrieval proof of concept**, NOT a deployed LLM chatbot or autonomous agent. It selects approved short synthetic policy documents based on keyword overlap, enforces allowed roles **before retrieval**, cites document IDs, and abstains when no evidence exists.

Run: python career-ai-lab/01-knowledge-workflow/agent.py

## Next milestones
1. Add ingestion from structured synthetic documents and a simple REST API.
2. Add embedding retrieval and compare against keyword baseline.
3. Integrate an optional LLM with evidence-only output and refusal tests.
4. Introduce configurable role permissions, prompt-injection tests, monitoring and human approval for sensitive actions.
5. Report a measured retrieval benchmark and record failure cases.

No real customer, bank, or user data. No guarantee of security or production readiness.