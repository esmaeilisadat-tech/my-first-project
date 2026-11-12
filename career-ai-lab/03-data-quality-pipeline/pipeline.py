"""Deterministic synthetic batch ETL with rejected-row audit trail."""
from collections import defaultdict
from datetime import date
import json


ALLOWED_STATIONS = {"FRA", "DA", "WI"}


def process(records: list[dict]) -> dict:
    seen: set[str] = set()
    daily: dict[tuple[str, str], int] = defaultdict(int)
    rejected = []
    accepted = 0
    for row_number, item in enumerate(records, start=1):
        try:
            event_id = item["event_id"]
            station = item["station"]
            day = item["day"]
            passengers = item["passengers"]
            if not isinstance(event_id, str) or not event_id.strip():
                raise ValueError("missing_event_id")
            if event_id in seen:
                raise ValueError("duplicate_event_id")
            if station not in ALLOWED_STATIONS:
                raise ValueError("unknown_station")
            if not isinstance(day, str) or date.fromisoformat(day).isoformat() != day:
                raise ValueError("invalid_day")
            if type(passengers) is not int or passengers < 0:
                raise ValueError("invalid_passengers")
        except (KeyError, TypeError, ValueError) as exc:
            rejected.append({"row_number": row_number, "reason": str(exc)})
            continue
        seen.add(event_id)
        daily[(day, station)] += passengers
        accepted += 1
    output = [
        {"day": day, "station": station, "passengers": count}
        for (day, station), count in sorted(daily.items())
    ]
    return {
        "daily_totals": output,
        "quality": {
            "input_rows": len(records),
            "accepted_rows": accepted,
            "rejected_rows": len(rejected),
            "rejections": rejected,
        },
        "lineage": {"source": "synthetic_demo", "transform": "validate_dedupe_daily_sum_v1"},
    }


if __name__ == "__main__":
    sample = [
        {"event_id": "e1", "station": "FRA", "day": "2026-11-01", "passengers": 50},
        {"event_id": "e2", "station": "FRA", "day": "2026-11-01", "passengers": 12},
        {"event_id": "e2", "station": "FRA", "day": "2026-11-01", "passengers": 999},
        {"event_id": "e3", "station": "DA", "day": "2026-11-02", "passengers": -5},
    ]
    print(json.dumps(process(sample), indent=2))
