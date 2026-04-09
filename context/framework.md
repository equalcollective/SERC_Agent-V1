# Alert Framework V1

Alert metrics checked every week. No rigid thresholds — use judgment based on WoW change, trend, and brand context.

## Lookback & Baseline

Pull **12 weeks** of weekly data for each alert metric. Display the most recent 4 in the trend column, but use all 12 to judge:

- **12-week median** = the baseline for what's "normal" for this brand. Compare current week to this median. If current is significantly below (or above for TACoS), flag it — even if WoW looks flat.
- **Consecutive decline rule**: If a metric has declined 3+ consecutive weeks, flag it regardless of WoW direction. A small uptick after 4 weeks of decline is not recovery.

These two rules prevent the system from "forgetting" a meaningful shift after the 4-week window moves past it.

**Output format:**
- **WoW Change:** Percentage metrics → raw point change. Absolute metrics → ±%.
- **Trend (4wk):** Most recent 4 weekly values with arrows. Example: `$4,536→3,499→2,218→2,199 ↘`
- **vs Baseline:** Show when current week is meaningfully different from 12-week median. Example: `12wk median: 8.7% — current 6.6%`
- **Notes:** `→ [one sentence]` when flagged. Blank if healthy.

---

## Revenue
- Data: `br_total_sales`
- Flag when: Significant decline WoW, especially if also below 12-week median. Also flag significant growth.

## TACoS
- Data: `cr_tacos_pct`
- Flag when: Significant increase WoW, or sustained multi-week rise. Also flag if meaningfully above 12-week median.

## Organic %
- Data: `cr_organic_pct`
- Flag when: Meaningful drop WoW. Sustained multi-week decline. Below 30% and declining = serious.

## Buy Box %
- Data: `br_featured_offer_pct`
- Flag when: Below 90% = always flag. Also flag significant drop WoW even if above 90%.

## CVR
- Data: `br_cvr_pct`
- Flag when: Notable drop WoW, especially combined with being below 12-week median. Flag if 3+ consecutive weeks of decline even if this week ticked up.

## Sessions
- Data: `br_sessions`
- Flag when: Significant drop WoW, especially if also below 12-week median.

---

## Campaign Alerts (2-check model)

For each campaign, run 2 independent checks:

1. **Spend efficiency**: Spend up significantly but orders flat or down? Flag.
2. **Direction**: ACOS worsening WoW? Flag.

Status per campaign: ⚠️ if either check fires, ✅ if neither fires.

---

## Missing Data

- No prior Account Check → "First check for this brand." Skip last week section.
- Metric returns null → show as-is, do not alert, flag "Data unavailable"
- Fewer than 12 weeks of data → use whatever is available, note "X weeks of history" next to baseline
