# Alert Framework V2 — Statistical Process Control

Alerts are driven by statistical control limits computed from 12 weeks of history, not subjective judgment. A Python script handles all math — the LLM reads its output and uses it to populate the alert table.

## Lookback & Baseline

Pull **12 weeks** of weekly data for each alert metric. Display the most recent 4 in the trend column.

- **12-week mean** = the baseline for what's "normal" for this brand.
- **Control limits** = mean ± 2 standard deviations (UCL and LCL). Current week outside these limits = statistically unusual.
- **Consecutive decline rule**: If a metric has declined 3+ consecutive weeks, flag it regardless of whether it's inside control limits. A small uptick after weeks of decline is not recovery.

---

## How to Run the Script

After pulling 12 weeks of data, format it as JSON and run:

```
python3 scripts/spc_baseline.py '<json>'
```

**Input format:**
```json
{
  "metrics": {
    "Revenue": [w1, w2, ..., w12],
    "TACoS": [w1, w2, ..., w12],
    "Organic %": [...],
    "Buy Box %": [...],
    "CVR": [...],
    "Sessions": [...]
  },
  "current_week": {
    "Revenue": value,
    "TACoS": value,
    "Organic %": value,
    "Buy Box %": value,
    "CVR": value,
    "Sessions": value
  }
}
```

Values in `metrics` are ordered oldest → newest (week 1 through week 12). `current_week` is this week's value.

**Output fields per metric:**

| Field | What it means |
|-------|--------------|
| `mean` | 12-week arithmetic mean |
| `std_dev` | Population standard deviation |
| `ucl` | Upper control limit (mean + 2σ) |
| `lcl` | Lower control limit (mean − 2σ, floored at 0) |
| `current` | This week's value |
| `current_vs_mean_pct` | % difference from the mean |
| `position` | `below_lcl`, `above_ucl`, or `within_limits` |
| `consecutive_decline` | Number of consecutive declining weeks |
| `decline_flag` | `true` if 3+ consecutive declines |

**Fallback:** If the script fails or returns an error, note "SPC computation unavailable" in the output and skip baseline comparisons for that run.

---

## Alert Rules

Use the script's `position` and `decline_flag` fields to classify each metric. Flag a metric when **any** of its conditions fire.

### Revenue
- Data: `br_total_sales`
- Flag when: `position` is `below_lcl` (significant decline) or `above_ucl` (significant growth). Flag when `decline_flag` is `true`.

### TACoS
- Data: `cr_tacos_pct`
- **Inverted metric** — higher is worse.
- Flag when: `position` is `above_ucl` (efficiency worsening). Flag when `decline_flag` is `true` (consecutive increases).

### Organic %
- Data: `cr_organic_pct`
- Flag when: `position` is `below_lcl`. Below 30% and below LCL = serious — the brand is heavily ad-dependent.
- Flag when: `decline_flag` is `true`.

### Buy Box %
- Data: `br_featured_offer_pct`
- **Hard threshold**: Below 90% = ALWAYS flag, regardless of SPC position.
- Also flag when: `position` is `below_lcl`.
- Flag when: `decline_flag` is `true`.

### CVR
- Data: `br_cvr_pct`
- Flag when: `position` is `below_lcl`. Flag when `decline_flag` is `true`.

### Sessions
- Data: `br_sessions`
- Flag when: `position` is `below_lcl`. Flag when `decline_flag` is `true`.

---

## Output Format

- **WoW Change:** Percentage metrics (TACoS, Organic %, Buy Box %, CVR) → raw point change (e.g., −9.1). Absolute metrics (Revenue, Sessions) → ±%.
- **Trend (4wk):** Most recent 4 weekly values with arrows. Example: `$4,536→3,499→2,218→2,199 ↘`
- **vs Baseline:** Show 12-week average from the script output. When current week is outside control limits, also show the breached limit. Example: `12wk avg: 8.7% (UCL: 10.2%)`
- **Notes:** `→ [one sentence]` when flagged. Blank if healthy.

---

## Missing Data

- No prior Account Check → "First check for this brand." Skip Last Week section.
- Metric returns null → show as-is, do not alert, flag "Data unavailable"
- Fewer than 3 weeks of history → script returns `insufficient_data`. Note "X weeks of history — insufficient for SPC" next to baseline.
