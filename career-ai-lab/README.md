# Career AI Lab — independent portfolio projects

**Status: starter implementations (in progress), 12 November 2026.**

Three small, reproducible Python projects inspired by skills mentioned in publicly advertised AI/ML/Data roles in Hessen, Germany. They are **independent learning projects**, not work done for FERI, statworx, DB Systel or their customers. **Only synthetic demonstration data** is used; no confidential, personal, licensed or employer data belongs here.

| Project | Skill demonstrated | Role inspiration | Current scope |
| --- | --- | --- | --- |
| [01 Knowledge Workflow](01-knowledge-workflow/README.md) | Retrieval with role-based document access, sources, abstention | Junior AI Developer (FERI) | Deterministic proof of concept, **not yet an LLM agent** |
| [02 Demand Forecast](02-demand-forecast/README.md) | Chronological split, time-series features, baseline vs. ML | (Junior) ML Engineer (statworx) | Synthetic one-step-ahead backtest |
| [03 Data Quality Pipeline](03-data-quality-pipeline/README.md) | Ingestion, validation, deduplication, provenance | Data Engineer (DB Systel) | Local batch ETL demonstration |

## Quick start

Requires Python 3.11+:

1. Create a virtual environment.
2. Install dependencies with: python -m pip install -r career-ai-lab/requirements.txt
3. Run: python career-ai-lab/01-knowledge-workflow/agent.py
4. Run: python career-ai-lab/02-demand-forecast/forecast.py
5. Run: python career-ai-lab/03-data-quality-pipeline/pipeline.py
6. Test: python -m unittest discover -s career-ai-lab/tests -v

The code runs locally and is suited to a GitHub Codespace or another disposable Python environment. It does not require API keys, paid APIs, GPUs or real company datasets.

## Honest presentation

These are STARTED portfolio exercises. A repository commit demonstrates implementation activity, not employment, a deployed product or validated business impact. Only add metrics and accomplishments to a CV after independently reproducing and recording them. The knowledge workflow currently uses deterministic keyword retrieval; adding a real LLM, embedding search and adversarial evaluation is future work.

## Reference job listings

- FERI Junior AI Developer: https://feri.softgarden.io/job/68333198/
- statworx Junior ML Engineer: https://statworx.jobs.personio.com/job/2605138
- DB Systel Data Engineer: https://db.jobs/de-de/Suche/Data-Engineer-in-14067040?jobId=639051

See [ROADMAP.md](ROADMAP.md) for planned next steps. These links may cease to accept applications.