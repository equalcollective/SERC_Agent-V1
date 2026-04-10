#!/usr/bin/env python3
"""Account check analysis script.

Takes 12 weeks of metric data, computes output columns (This Week, Last Week,
WoW Change, Trend 4wk), internal flags (SPC, 3-week consecutive, Buy Box
threshold), and status signals. Returns structured JSON for the alert table.

Usage:
    python3 scripts/spc_baseline.py '<json>'
    echo '<json>' | python3 scripts/spc_baseline.py

Input JSON — keyed by metric key, each value is an array of weekly values
(oldest → newest, last element = target week):

    {
      "br_total_sales": [w1, w2, ..., w12],
      "cr_tacos_pct": [w1, w2, ..., w12],
      "cr_organic_pct": [w1, w2, ..., w12],
      "br_featured_offer_pct": [w1, w2, ..., w12],
      "br_cvr_pct": [w1, w2, ..., w12],
      "br_sessions": [w1, w2, ..., w12]
    }
"""

import json
import sys
import statistics

# Metric definitions in fixed row order
METRICS = [
    {
        "key": "br_total_sales",
        "display_name": "Revenue",
        "format": "$",
        "good_direction": "up",
    },
    {
        "key": "cr_tacos_pct",
        "display_name": "TACoS",
        "format": "%",
        "good_direction": "down",
    },
    {
        "key": "cr_organic_pct",
        "display_name": "Organic %",
        "format": "%",
        "good_direction": "up",
    },
    {
        "key": "br_featured_offer_pct",
        "display_name": "Buy Box %",
        "format": "%",
        "good_direction": "up",
        "threshold": 90,
    },
    {
        "key": "br_cvr_pct",
        "display_name": "CVR",
        "format": "%",
        "good_direction": "up",
    },
    {
        "key": "br_sessions",
        "display_name": "Sessions",
        "format": "#",
        "good_direction": "up",
    },
]


def format_value(value, fmt):
    """Format a value for display in the table."""
    if value is None:
        return "N/A"
    if fmt == "$":
        return f"${value:,.0f}"
    elif fmt == "%":
        return f"{value:.1f}%"
    elif fmt == "#":
        return f"{value:,.0f}"
    return str(value)


def compute_wow_change(this_week, last_week, fmt):
    """Compute week-over-week change as a formatted string.

    $ and # metrics → percentage change (e.g. +12.3%)
    % metrics → absolute point change (e.g. +2.1pp)
    """
    if this_week is None or last_week is None:
        return "N/A"

    if fmt in ("$", "#"):
        if last_week == 0:
            return "N/A" if this_week == 0 else "+∞%"
        pct = ((this_week - last_week) / abs(last_week)) * 100
        sign = "+" if pct > 0 else ""
        return f"{sign}{pct:.1f}%"
    else:
        diff = this_week - last_week
        sign = "+" if diff > 0 else ""
        return f"{sign}{diff:.1f}pp"


def compute_trend_4wk(values, fmt):
    """Compute 4-week trend: 4 data points + direction arrow.

    Direction: ↗ if latest > earliest, ↘ if latest < earliest, → if change < 2%.
    """
    if len(values) < 4:
        available = values[-len(values):]
        formatted = [format_value(v, fmt) for v in available]
        return " → ".join(formatted) + " →"

    last_4 = values[-4:]
    formatted = [format_value(v, fmt) for v in last_4]

    earliest, latest = last_4[0], last_4[-1]
    if earliest == 0:
        arrow = "↗" if latest > 0 else "→"
    else:
        pct_change = abs((latest - earliest) / earliest)
        if pct_change < 0.02:
            arrow = "→"
        elif latest > earliest:
            arrow = "↗"
        else:
            arrow = "↘"

    return " → ".join(formatted) + " " + arrow


def compute_spc(values):
    """Compute SPC baselines: mean, std dev, UCL, LCL, breach flags."""
    if len(values) < 3:
        return None

    mean = statistics.mean(values)
    std_dev = statistics.pstdev(values)
    ucl = mean + 2 * std_dev
    lcl = max(0, mean - 2 * std_dev)

    current = values[-1]

    return {
        "mean": round(mean, 2),
        "std_dev": round(std_dev, 2),
        "ucl": round(ucl, 2),
        "lcl": round(lcl, 2),
        "spc_breach_above": current > ucl,
        "spc_breach_below": current < lcl,
    }


def compute_consecutive(values):
    """Compute 3-week consecutive decline and increase flags.

    Checks the last 3 week-over-week transitions (requires 4 data points).
    """
    if len(values) < 4:
        return {"three_week_decline": False, "three_week_increase": False}

    last_4 = values[-4:]
    decline = all(last_4[i + 1] < last_4[i] for i in range(3))
    increase = all(last_4[i + 1] > last_4[i] for i in range(3))

    return {
        "three_week_decline": decline,
        "three_week_increase": increase,
    }


def compute_status(meta, this_week, last_week, spc, consecutive):
    """Determine status signal (🟢/🟡/🔴) based on business meaning.

    Rules:
    - Buy Box < 90% → always 🔴
    - SPC breach or 3-week streak in bad direction → 🔴
    - SPC breach or 3-week streak in good direction → 🟢
    - WoW improvement → 🟢, WoW decline → 🟡, flat → 🟢
    - Tie-break: yellow/green → green, yellow/red → red
    """
    good_dir = meta["good_direction"]
    threshold = meta.get("threshold")

    breach_above = spc["spc_breach_above"] if spc else False
    breach_below = spc["spc_breach_below"] if spc else False
    three_decline = consecutive["three_week_decline"]
    three_increase = consecutive["three_week_increase"]

    # Buy Box special rule
    if threshold is not None and this_week is not None and this_week < threshold:
        return "🔴"

    if good_dir == "up":
        # Bad: breach below or 3-week decline
        if breach_below or three_decline:
            return "🔴"
        # Good: breach above or 3-week increase
        if breach_above or three_increase:
            return "🟢"
        # WoW direction
        if this_week is not None and last_week is not None:
            if this_week > last_week:
                return "🟢"
            elif this_week < last_week:
                return "🟡"
        return "🟢"

    elif good_dir == "down":
        # Bad: breach above or 3-week increase (TACoS going up = bad)
        if breach_above or three_increase:
            return "🔴"
        # Good: breach below or 3-week decline (TACoS going down = good)
        if breach_below or three_decline:
            return "🟢"
        # WoW direction (going down = good for TACoS)
        if this_week is not None and last_week is not None:
            if this_week < last_week:
                return "🟢"
            elif this_week > last_week:
                return "🟡"
        return "🟢"

    return "🟡"


def analyze_metric(meta, values):
    """Run full analysis for a single metric. Returns a result dict."""
    fmt = meta["format"]

    if not values or len(values) == 0:
        return {
            "metric": meta["display_name"],
            "status": "🟡",
            "this_week": "N/A",
            "last_week": "N/A",
            "wow_change": "N/A",
            "trend_4wk": "N/A",
            "flags": {
                "spc_breach_above": None,
                "spc_breach_below": None,
                "three_week_decline": False,
                "three_week_increase": False,
                "buy_box_below_90": None,
            },
            "spc": None,
            "weeks_of_data": 0,
        }

    this_week = values[-1] if len(values) >= 1 else None
    last_week = values[-2] if len(values) >= 2 else None

    # Output columns
    wow = compute_wow_change(this_week, last_week, fmt)
    trend = compute_trend_4wk(values, fmt)

    # Internal flags
    spc = compute_spc(values)
    consecutive = compute_consecutive(values)
    buy_box_below_90 = None
    if meta.get("threshold") is not None and this_week is not None:
        buy_box_below_90 = this_week < meta["threshold"]

    # Status signal
    status = compute_status(meta, this_week, last_week, spc, consecutive)

    return {
        "metric": meta["display_name"],
        "status": status,
        "this_week": format_value(this_week, fmt),
        "last_week": format_value(last_week, fmt),
        "wow_change": wow,
        "trend_4wk": trend,
        "this_week_raw": this_week,
        "last_week_raw": last_week,
        "flags": {
            "spc_breach_above": spc["spc_breach_above"] if spc else None,
            "spc_breach_below": spc["spc_breach_below"] if spc else None,
            "three_week_decline": consecutive["three_week_decline"],
            "three_week_increase": consecutive["three_week_increase"],
            "buy_box_below_90": buy_box_below_90,
        },
        "spc": {
            "mean": spc["mean"],
            "std_dev": spc["std_dev"],
            "ucl": spc["ucl"],
            "lcl": spc["lcl"],
        } if spc else None,
        "weeks_of_data": len(values),
    }


def main():
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = sys.stdin.read()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        sys.exit(1)

    results = []
    for meta in METRICS:
        values = data.get(meta["key"])
        results.append(analyze_metric(meta, values))

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
