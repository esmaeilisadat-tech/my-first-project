# Retail Demand Forecasting — job-focused extension

Status: **v0.1 prototype, synthetic data only**. No real-data validation or live deployment.

## Building on previous course exercises

- [Educx Neural Networks, Tag 09 RNN/LSTM](https://github.com/esmaeilisadat-tech/Educx-Neuronale-Netze/tree/main/Tag_09_RNN_LSTM/notebooks): chronological synthetic time-series exercises, multi-step LSTM, GRU comparison.
- [ML Engineering, Gradient Boosting Expert](https://github.com/esmaeilisadat-tech/ML_Engineering_Portfolio-/blob/main/gradient-boosting-performance-tuning/notebooks/Experte.ipynb): LightGBM/Optuna, XGBoost, CatBoost on tabular house prices.

This extension combines the learning goals of those exercises for **retail demand**. Those notebooks did not themselves establish commercial forecasting performance.

## Relevance to real job requirements

[statworx (Junior) ML Engineer](https://statworx.jobs.personio.com/job/2605138): demand forecasting, tabular/time-series models, robust evaluation, and maintainable ML pipelines.

## Current v0.1 implementation

- Synthetic demand with trend, weekly/annual variation, promotions and random noise
- Lags 1/7/14 and shifted rolling 7/28-day means to avoid using same-day target
- Chronological 70/15/15 train/validation/test splits
- Seasonal-naive baseline vs Ridge and HistGradientBoostingRegressor
- Model chosen on validation MAE; independent test MAE/RMSE reported once
- Offline unit checks for leakage, lags, ordering and deterministic results

**Important:** this is *one-step-ahead*, and previous days' actual demand is assumed available at inference time. It is not an independent multi-day forecast.

## Run (Python 3.11+)

```bash
python -m pip install -r career-ai-lab/02-demand-forecast/job-ready-extension/requirements.txt
python -m unittest discover -s career-ai-lab/02-demand-forecast/job-ready-extension/tests -v
python career-ai-lab/02-demand-forecast/job-ready-extension/forecast.py
```

## Next milestones

1. Walk-forward backtests for several horizons and baseline comparisons
2. Integrate LightGBM and XGBoost *correctly* with time-aware tuning (reuse knowledge from original house-price exercise)
3. Adapt LSTM architecture from original Tag09 exercise and compare on identical splits/horizons
4. Add a licensed public retail dataset, error analysis, intervals and reproducible charts
5. Add CI, Streamlit and a concise model card with measured limitations

Tested locally prior to publication in an equivalent Python implementation. This branch's remote CI and deployments are not yet verified.

**CV phrasing (in progress):** Developing a synthetic retail-demand forecasting Python portfolio extension using time-based validation, explicit baselines and regression-model comparisons. Real-data evaluation and neural architectures are planned.

Independent educational project; not affiliated with statworx, FERI or DB Systel.