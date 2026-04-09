#!/usr/bin/env python3
"""SPC baseline calculator for account check alerts.

Takes 12 weeks of metric history + current week values, computes
statistical process control baselines (mean, std dev, UCL, LCL),
detects consecutive declines, and classifies each metric's position
relative to control limits.

Usage:
    python3 scripts/spc_baseline.py '<json>'
    echo '<json>' | python3 scripts/spc_baseline.py
"""

import json
import sys
import statistics

# Metrics where higher values are worse (inverted alerting logic)
INVERTED_METRICS = {"TACoS"}

# Minimum weeks of history required for SPC computation
MIN_WEEKS = 3


def compute_baseline(values, current, inverted=False):
    """Compute SPC baseline for a single metric.

    Args:
        values: List of historical weekly values (oldest → newest).
        current: Current week's value.
        inverted: If True, higher = worse (e.g. TACoS).

    Returns:
        Dict with mean, std_dev, ucl, lcl, position, etc.
    """
    weeks = len(values)
    result = {
        "mean": None,
        "std_dev": None,
        "ucl": None,
        "lcl": None,
        "current": current,
        "current_vs_mean_pct": None,
        "position": "insufficient_data",
        "consecutive_decline": 0,
        "decline_flag": False,
        "weeks_of_history": weeks,
    }

    if weeks < MIN_WEEKS:
        return result

    mean = statistics.mean(values)
    std_dev = statistics.pstdev(values)

    ucl = mean + 2 * std_dev
    lcl = max(0, mean - 2 * std_dev)

    # Percentage difference from mean
    if mean != 0:
        current_vs_mean_pct = round(((current - mean) / abs(mean)) * 100, 2)
    else:
        current_vs_mean_pct = None

    # Classify position relative to control limits
    if current > ucl:
        position = "above_ucl"
    elif current < lcl:
        position = "below_lcl"
    else:
        position = "within_limits"

    # Consecutive decline detection (walk from newest backward)
    consecutive = detect_consecutive_decline(values, inverted)

    result.update({
        "mean": round(mean, 2),
        "std_dev": round(std_dev, 2),
        "ucl": round(ucl, 2),
        "lcl": round(lcl, 2),
        "current_vs_mean_pct": current_vs_mean_pct,
        "position": position,
        "consecutive_decline": consecutive,
        "decline_flag": consecutive >= 3,
    })

    return result


def detect_consecutive_decline(values, inverted=False):
    """Count consecutive weeks of decline from the most recent week backward.

    For normal metrics, decline = value went down.
    For inverted metrics (TACoS), decline = value went up (getting worse).
    """
    if len(values) < 2:
        return 0

    count = 0
    for i in range(len(values) - 1, 0, -1):
        if inverted:
            # For TACoS: "decline" means value increased (worsening)
            if values[i] > values[i - 1]:
                count += 1
            else:
                break
        else:
            # For normal metrics: "decline" means value decreased
            if values[i] < values[i - 1]:
                count += 1
            else:
                break

    return count


def main():
    # Read input from CLI arg or stdin
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = sys.stdin.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        sys.exit(1)

    metrics_history = data.get("metrics", {})
    current_week = data.get("current_week", {})

    if not metrics_history:
        print(json.dumps({"error": "No metrics provided"}), file=sys.stderr)
        sys.exit(1)

    results = {}
    flagged = []
    decline_warnings = []

    for name, values in metrics_history.items():
        current = current_week.get(name)
        if current is None:
            continue

        inverted = name in INVERTED_METRICS
        baseline = compute_baseline(values, current, inverted)
        results[name] = baseline

        # Determine if this metric should be flagged
        pos = baseline["position"]
        if inverted:
            if pos == "above_ucl":
                flagged.append(name)
        else:
            if pos == "below_lcl" or pos == "above_ucl":
                flagged.append(name)

        if baseline["decline_flag"]:
            decline_warnings.append(name)
            if name not in flagged:
                flagged.append(name)

    output = {
        "metrics": results,
        "summary": {
            "flagged_metrics": flagged,
            "decline_warnings": decline_warnings,
            "total_metrics": len(results),
        },
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
