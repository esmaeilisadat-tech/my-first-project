"""Offline smoke/contract checks for the three starter projects."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


agent = load("knowledge_workflow", "01-knowledge-workflow/agent.py")
pipeline = load("data_quality_pipeline", "03-data-quality-pipeline/pipeline.py")
forecast = load("demand_forecast", "02-demand-forecast/forecast.py")


class KnowledgeWorkflowTests(unittest.TestCase):
    def test_staff_cannot_retrieve_finance_document(self):
        response = agent.answer_with_sources("invoice finance", "staff")
        self.assertEqual(response["status"], "insufficient_evidence")
        self.assertNotIn("DOC-101", response["citations"])

    def test_analyst_receives_cited_document(self):
        response = agent.answer_with_sources("invoice", "analyst")
        self.assertEqual(response["citations"], ["DOC-101"])

    def test_unknown_role_is_rejected(self):
        with self.assertRaises(ValueError):
            agent.answer_with_sources("invoice", "administrator")


class ForecastTests(unittest.TestCase):
    def test_lag_features_never_use_target_day(self):
        import numpy as np
        demand = np.arange(50.0)
        promo = np.zeros(50)
        X, y, days = forecast.build_features(demand, promo)
        self.assertEqual(int(days[0]), 14)
        self.assertEqual(float(X[0, 0]), 13.0)
        self.assertEqual(float(X[0, 1]), 7.0)
        self.assertEqual(float(X[0, 2]), 10.0)
        self.assertEqual(float(y[0]), 14.0)

    def test_evaluation_is_reproducible(self):
        self.assertEqual(forecast.evaluate(seed=42), forecast.evaluate(seed=42))


class PipelineTests(unittest.TestCase):
    def test_rejects_duplicates_and_invalid_rows(self):
        rows = [
            {"event_id": "1", "station": "FRA", "day": "2026-11-01", "passengers": 12},
            {"event_id": "1", "station": "FRA", "day": "2026-11-01", "passengers": 100},
            {"event_id": "2", "station": "FRA", "day": "2026-11-01", "passengers": -1},
        ]
        result = pipeline.process(rows)
        self.assertEqual(result["quality"]["accepted_rows"], 1)
        self.assertEqual(result["quality"]["rejected_rows"], 2)
        self.assertEqual(result["daily_totals"][0]["passengers"], 12)

    def test_empty_input(self):
        self.assertEqual(pipeline.process([])["daily_totals"], [])


if __name__ == "__main__":
    unittest.main()
