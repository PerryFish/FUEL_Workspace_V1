#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics-dir", required=True)
    args = parser.parse_args()

    metrics_dir = Path(args.metrics_dir)
    metrics = load_json(metrics_dir / "metrics.json")
    lifecycle = load_json(metrics_dir / "goal_lifecycle.json")
    if not lifecycle:
        lifecycle = {
            key: metrics.get(key)
            for key in [
                "raw_goal_msg_count",
                "unique_goal_count_quantized_0p5m",
                "unique_goal_count_quantized_1p0m",
                "goal_lifecycle_goal_switch_count",
                "same_goal_max_duration_sec",
                "goal_republish_count",
                "true_repeated_goal_count",
                "too_close_goal_event_count",
                "goal_retire_event_count",
                "goal_retire_reasons",
                "escape_goal_count",
            ]
        }

    raw = int(lifecycle.get("raw_goal_msg_count") or 0)
    unique_1m = int(lifecycle.get("unique_goal_count_quantized_1p0m") or 0)
    switches = int(lifecycle.get("goal_switch_count") or metrics.get("goal_lifecycle_goal_switch_count") or 0)
    same_max = float(lifecycle.get("same_goal_max_duration_sec") or 0.0)
    true_repeat = int(lifecycle.get("true_repeated_goal_count") or 0)
    retire_count = int(lifecycle.get("goal_retire_event_count") or 0)
    escape_count = int(lifecycle.get("escape_goal_count") or 0)
    republish_count = int(lifecycle.get("goal_republish_count") or 0)

    if raw <= 0:
        result = "FAIL_NO_GOAL"
        cause = "NO_GOAL_MESSAGES"
    elif same_max >= 90.0:
        result = "PARTIAL"
        cause = "SAME_GOAL_HELD_TOO_LONG"
    elif unique_1m < 5:
        result = "PARTIAL"
        cause = "LOW_UNIQUE_GOAL_DIVERSITY"
    elif true_repeat > max(2, switches // 2):
        result = "PARTIAL"
        cause = "TRUE_REPEATED_GOAL"
    else:
        result = "PASS"
        cause = "GOAL_LIFECYCLE_HEALTHY"

    summary = {
        "metrics_dir": str(metrics_dir),
        "raw_goal_msg_count": raw,
        "unique_goal_count_quantized_0p5m": lifecycle.get("unique_goal_count_quantized_0p5m", 0),
        "unique_goal_count_quantized_1p0m": unique_1m,
        "goal_switch_count": switches,
        "same_goal_max_duration_sec": same_max,
        "goal_republish_count": republish_count,
        "true_repeated_goal_count": true_repeat,
        "goal_retire_event_count": retire_count,
        "goal_retire_reasons": lifecycle.get("goal_retire_reasons", {}),
        "escape_goal_count": escape_count,
        "result": result,
        "main_goal_lifecycle_cause": cause,
    }

    with (metrics_dir / "goal_lifecycle_analysis.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    with (metrics_dir / "goal_lifecycle_analysis.md").open("w", encoding="utf-8") as f:
        f.write(f"# Goal Lifecycle Analysis {metrics_dir.name}\n\n")
        for key, value in summary.items():
            f.write(f"- {key}: {value}\n")
        f.write("\n## Interpretation\n\n")
        if cause == "SAME_GOAL_HELD_TOO_LONG":
            f.write("The same quantized active goal remained selected too long.\n")
        elif cause == "LOW_UNIQUE_GOAL_DIVERSITY":
            f.write("Goal selection did not diversify enough for a 300s run.\n")
        elif cause == "TRUE_REPEATED_GOAL":
            f.write("Retired goals were selected again within the short-term memory window.\n")
        elif cause == "NO_GOAL_MESSAGES":
            f.write("No active exploration goal messages were observed.\n")
        else:
            f.write("Goal lifecycle metrics met the configured health thresholds.\n")

    print("P2C_GOAL_LIFECYCLE_ANALYSIS_RESULT")
    for key in [
        "raw_goal_msg_count",
        "unique_goal_count_quantized_0p5m",
        "unique_goal_count_quantized_1p0m",
        "goal_switch_count",
        "same_goal_max_duration_sec",
        "goal_republish_count",
        "true_repeated_goal_count",
        "goal_retire_event_count",
        "escape_goal_count",
        "result",
        "main_goal_lifecycle_cause",
    ]:
        print(f"{key}={summary[key]}")
    return 0 if result in ("PASS", "PARTIAL") else 1


if __name__ == "__main__":
    raise SystemExit(main())
