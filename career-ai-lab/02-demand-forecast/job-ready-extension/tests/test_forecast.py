import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forecast import FEATURES, past_only_features, run_experiment, synthetic_daily_demand


class ForecastingTests(unittest.TestCase):
    def test_original_demand_not_used_in_same_row_features(self):
        data = synthetic_daily_demand(days=180)
        before = past_only_features(data)
        modified = data.copy()
        modified.loc[179, "demand"] += 1_000_000
        after = past_only_features(modified)
        np.testing.assert_allclose(before.iloc[-1][FEATURES].astype(float), after.iloc[-1][FEATURES].astype(float))

    def test_lags_come_from_previous_observations(self):
        original = synthetic_daily_demand(days=180)
        prepared = past_only_features(original)
        t = 28
        self.assertAlmostEqual(prepared.iloc[0]["lag_1"], original.iloc[t - 1]["demand"])
        self.assertAlmostEqual(prepared.iloc[0]["lag_7"], original.iloc[t - 7]["demand"])
        self.assertAlmostEqual(prepared.iloc[0]["rolling_mean_28"], original.iloc[:t]["demand"].mean())

    def test_rejects_out_of_order_data(self):
        data = synthetic_daily_demand(days=180).iloc[::-1]
        with self.assertRaises(ValueError):
            past_only_features(data)

    def test_reproducible_metrics_and_split(self):
        a, b = run_experiment(seed=42), run_experiment(seed=42)
        self.assertEqual(a, b)
        self.assertGreater(a["train_rows"], a["test_rows"])
        self.assertGreater(a["test_rows"], 0)
        self.assertGreaterEqual(a["test_mae"], 0)


if __name__ == "__main__":
    unittest.main()
