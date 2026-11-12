# 02 — Synthetic Demand Forecasting

**Inspired by:** statworx (Junior) Machine Learning Engineer (forecasting, time-series ML, evaluation, maintainable pipelines).

## Current MVP
Reproducible synthetic daily demand with weekly seasonality and a promotion flag; lag/rolling features using **only past observed demand**, chronological train/test holdout, a seasonal-naive benchmark and a scikit-learn HistGradientBoostingRegressor.

Run: python career-ai-lab/02-demand-forecast/forecast.py

The backtest is **one-step ahead**: at each test day, demand from preceding days is assumed to have already been observed. It is NOT a multi-day production forecast or a claim of performance on real data.

## Next milestones
1. Walk-forward cross-validation, stronger seasonal baselines.
2. Add XGBoost/LightGBM and an optional neural forecasting comparison.
3. Quantile forecasts, prediction intervals, drift and leakage checks.
4. Reproducible data/version snapshots and a simple Streamlit UI.
5. Explain errors, uncertainty, limitations and model selection decisions.

Synthetic data only. No business outcome or guaranteed model advantage is claimed.