# Evidence-based roadmap

## Done in starter commit
- [x] Three job-relevant, **synthetic-data-only** project designs
- [x] Python entry points for retrieval, forecasting and ETL
- [x] Small unit/contract-test suite
- [x] Honest scope and limitations documented

## Next iteration — implementation and verified evidence
- [ ] Run the tests in a fresh GitHub Codespace and capture actual output
- [ ] Agent: add an optional real LLM provider adapter with mock mode, prompt-injection tests and citation scoring
- [ ] Agent: define 20 synthetic test questions, check unauthorized retrieval = 0
- [ ] Forecast: walk-forward evaluation, XGBoost/LightGBM comparison and honest error analysis
- [ ] Forecast: quantify uncertainty and publish charts using only synthetic observations
- [ ] Pipeline: SQL persistence with replay-safe loads and data-quality dashboard
- [ ] Add CI workflow and a reproducible demo recording
- [ ] Publish measured methods/results and update CV only with verified implementation outcomes

## Suggested weekly cadence
Week 1: run and study the three starters. Week 2: extend the forecast. Week 3: improve retrieval/agent. Week 4: pipeline+CI and write a one-page case study.

## Presentation ethics
Inspired by public role requirements at FERI, statworx and DB Systel; not commissioned, endorsed or affiliated. Do not imply that these demonstrations are live customer deployments or that repository content is employer-owned.