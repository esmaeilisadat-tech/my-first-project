"""Synthetic one-step-ahead retail demand forecasting.

Features for day t depend on observed demand before t or known promotions only.
This is not a production or multi-horizon forecasting system.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["lag_1", "lag_7", "lag_14", "rolling_mean_7", "rolling_mean_28", "promotion", "day_of_week", "trend"]


def synthetic_daily_demand(days: int = 500, seed: int = 42) -> pd.DataFrame:
    if days < 150:
        raise ValueError("Need at least 150 days for chronological evaluation")
    rng = np.random.default_rng(seed)
    idx = np.arange(days)
    dates = pd.date_range("2024-01-01", periods=days, freq="D")
    promotion = ((idx % 32) < 5).astype(int)
    weekly = 13.0 * np.cos(2 * np.pi * (idx - 5) / 7)
    annual = 8.0 * np.sin(2 * np.pi * idx / 365)
    demand = np.maximum(1, 80 + 0.035 * idx + 18 * promotion + weekly + annual + rng.normal(0, 5, days))
    return pd.DataFrame({"date": dates, "demand": demand, "promotion": promotion})


def past_only_features(data: pd.DataFrame) -> pd.DataFrame:
    if not data["date"].is_monotonic_increasing or data["date"].duplicated().any():
        raise ValueError("Dates must be unique, chronological and increasing")
    if not data["demand"].notna().all():
        raise ValueError("Demand cannot be missing")
    if not data["promotion"].isin([0, 1]).all():
        raise ValueError("Promotion must be a binary, known-ahead-of-time feature")
    result = data.copy()
    for lag in [1, 7, 14]:
        result[f"lag_{lag}"] = result["demand"].shift(lag)
    for window in [7, 28]:
        result[f"rolling_mean_{window}"] = result["demand"].shift(1).rolling(window).mean()
    result["day_of_week"] = result["date"].dt.dayofweek
    result["trend"] = np.arange(len(result))
    return result.dropna(subset=FEATURES).reset_index(drop=True)


def mae(y, prediction) -> float:
    return round(float(mean_absolute_error(y, prediction)), 4)


def rmse(y, prediction) -> float:
    return round(float(np.sqrt(mean_squared_error(y, prediction))), 4)


def candidate_models(seed: int = 42):
    return {
        "ridge": make_pipeline(StandardScaler(), Ridge(alpha=5.0)),
        "hist_gradient_boosting": HistGradientBoostingRegressor(
            max_iter=120, max_leaf_nodes=15, learning_rate=0.05, random_state=seed
        ),
    }


def run_experiment(seed: int = 42) -> dict:
    frame = past_only_features(synthetic_daily_demand(seed=seed))
    n = len(frame)
    train_end, val_end = int(n * 0.70), int(n * 0.85)
    train, validation, test = frame.iloc[:train_end], frame.iloc[train_end:val_end], frame.iloc[val_end:]
    X_train, y_train = train[FEATURES], train["demand"]
    X_val, y_val = validation[FEATURES], validation["demand"]
    X_test, y_test = test[FEATURES], test["demand"]

    val_errors = {"seasonal_naive": mae(y_val, validation["lag_7"])}
    for name, model in candidate_models(seed).items():
        model.fit(X_train, y_train)
        val_errors[name] = mae(y_val, model.predict(X_val))

    # Freeze model choice using validation only, without looking at test outcomes.
    champion = min(val_errors, key=val_errors.get)
    if champion == "seasonal_naive":
        test_prediction = test["lag_7"].to_numpy()
    else:
        model = candidate_models(seed)[champion]
        model.fit(frame.iloc[:val_end][FEATURES], frame.iloc[:val_end]["demand"])
        test_prediction = model.predict(X_test)

    return {
        "evaluation": "synthetic chronological one-step-ahead; previous actuals available",
        "train_rows": len(train),
        "validation_rows": len(validation),
        "test_rows": len(test),
        "first_test_date": str(test["date"].iloc[0].date()),
        "validation_mae": val_errors,
        "selected_by_validation": champion,
        "test_mae": mae(y_test, test_prediction),
        "test_rmse": rmse(y_test, test_prediction),
        "test_seasonal_naive_mae": mae(y_test, test["lag_7"]),
    }


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2))
