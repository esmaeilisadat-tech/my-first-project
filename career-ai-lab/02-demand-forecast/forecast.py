"""Synthetic one-step-ahead demand forecasting; evaluation avoids random splits."""
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error


def generate_demand(days: int = 420, seed: int = 42):
    if days < 80:
        raise ValueError("At least 80 days needed")
    rng = np.random.default_rng(seed)
    t = np.arange(days)
    promotion = ((t % 29) < 4).astype(float)
    weekly = 10 * np.sin(2 * np.pi * t / 7)
    demand = np.maximum(
        1.0, 65 + 0.04 * t + weekly + 7 * promotion + rng.normal(0, 3, days)
    )
    return demand, promotion


def build_features(demand, promotion, min_history: int = 14):
    """Features for day d use history through d-1, never demand[d]."""
    if len(demand) != len(promotion):
        raise ValueError("Inputs must have equal length")
    if min_history < 7:
        raise ValueError("At least 7 history days needed")
    indices = np.arange(min_history, len(demand))
    X = np.asarray(
        [
            [
                demand[day - 1],
                demand[day - 7],
                float(np.mean(demand[day - 7 : day])),
                promotion[day],  # Scheduled promotion is known beforehand.
                day % 7,
            ]
            for day in indices
        ],
        dtype=float,
    )
    return X, np.asarray(demand[indices], dtype=float), indices


def evaluate(seed: int = 42) -> dict:
    demand, promotion = generate_demand(seed=seed)
    X, y, days = build_features(demand, promotion)
    cut = int(len(y) * 0.8)
    if cut < 1 or cut >= len(y):
        raise ValueError("Invalid split")
    model = HistGradientBoostingRegressor(
        learning_rate=0.06, max_iter=120, max_leaf_nodes=15, random_state=seed
    )
    model.fit(X[:cut], y[:cut])
    predicted = model.predict(X[cut:])
    # Seasonal-naive is evaluated on exactly the same one-step-ahead test days.
    baseline = demand[days[cut:] - 7]
    return {
        "train_samples": cut,
        "test_samples": len(y) - cut,
        "first_test_day": int(days[cut]),
        "ml_mae": round(float(mean_absolute_error(y[cut:], predicted)), 3),
        "seasonal_naive_mae": round(float(mean_absolute_error(y[cut:], baseline)), 3),
        "evaluation": "synthetic chronological one-step-ahead holdout",
    }


if __name__ == "__main__":
    for metric, value in evaluate().items():
        print(f"{metric}: {value}")
