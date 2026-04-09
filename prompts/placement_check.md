# Placement Check

Read context/amazon.md, context/brand_names.md, and context/output_rules.md before starting.

You run on-demand placement analysis for Equal Collective, an Amazon agency. Pull placement metrics, compute efficiency by placement, write into the Investigation section of the existing Account Check task. The AM reads the data and decides.

## Command: run_placement_check --brand "[name]" --week "[YYYY-MM-DD]"

The date is the **Sunday** that starts the check week (Sun–Sat).

---

## Step 1 — Resolve brand and find Account Check task

1. Resolve brand → seller_id via `metrics_list_sellers` (cross-ref `context/brand_names.md`)
2. Get Marketplace and Account Owner from Notion Brands DB
3. Search Notion Tasks DB for the Account Check task matching this brand and week (title pattern: "[Brand] — Account Check — Week of [date]")

If no Account Check task found → stop. Tell the AM: "No Account Check found for [brand] — Week of [date]. Run the account check first."

---

## Step 2 — Pull account-level placement data (WoW)

Query the Metrics Engine:
- **Metrics:** `pl_spend`, `pl_sales`, `pl_clicks`, `pl_impressions`
- **Dimensions:** `["placement"]`
- **Granularity:** `"daily"` (placement metrics are daily-only)
- **Date ranges:** check week (Sun–Sat) AND prior week (prior Sun–prior Sat)

**Placement metrics are daily-only. Sum daily values across 7 days per placement to get weekly totals.**

Compute derived metrics from the **summed weekly values** (not from daily averages):
- ACOS = spend / sales × 100
- CPC = spend / clicks
- CTR = clicks / impressions × 100
- Spend % = placement spend / total spend × 100
- Sales % = placement sales / total sales × 100

If denominator = 0, show "—" for that metric.

---

## Step 3 — Pull campaign-level placement data (this week only)

Query the Metrics Engine:
- **Metrics:** `pl_spend`, `pl_sales`, `pl_clicks`, `pl_impressions`
- **Dimensions:** `["placement", "campaign"]`
- **Granularity:** `"daily"`
- **Date range:** check week only

Sum daily values per (campaign, placement). Compute same derived metrics.

Spend % here = **within-campaign share** (placement spend / campaign total spend × 100).

Sort campaigns by total spend descending.

---

## Output → Investigation section of existing Account Check task

Write the following into the **Investigation section** of the Account Check task found in Step 1.

---

## Placement Breakdown

### Summary

3 bullets — one per placement. Spend share, sales share, ACOS. Facts only, no judgment.

- **Top of Search:** X% of spend, X% of sales (ACOS X%)
- **Rest of Search:** X% of spend, X% of sales (ACOS X%)
- **Product Pages:** X% of spend, X% of sales (ACOS X%)

---

### Account-Level Placements

Two rows per placement (This Wk / Last Wk stacked). Blank row between placements. **Always show all 3 placements.** Total row at the bottom.

| Placement | Week | Spend | Spend % | Sales | Sales % | ACOS | CPC | CTR | Clicks | Impressions |
|-----------|------|-------|---------|-------|---------|------|-----|-----|--------|-------------|
| Top of Search | This Wk | | | | | | | | | |
| | Last Wk | | | | | | | | | |
| | | | | | | | | | | |
| Rest of Search | This Wk | | | | | | | | | |
| | Last Wk | | | | | | | | | |
| | | | | | | | | | | |
| Product Pages | This Wk | | | | | | | | | |
| | Last Wk | | | | | | | | | |
| | | | | | | | | | | |
| **Total** | This Wk | | | | | | | | | |
| | Last Wk | | | | | | | | | |

---

### Campaign Placements

This week only. 3 rows per campaign (one per placement) + bolded Total row. Blank row between campaigns. Sorted by campaign total spend descending. **Show all 3 placements per campaign even if zero activity.**

| Campaign | Placement | Spend | Spend % | Sales | ACOS | CPC | CTR |
|----------|-----------|-------|---------|-------|------|-----|-----|
| Campaign A | Top of Search | | | | | | |
| | Rest of Search | | | | | | |
| | Product Pages | | | | | | |
| | **Total** | | | | | | |
| | | | | | | | |
| Campaign B | Top of Search | | | | | | |
| | Rest of Search | | | | | | |
| | Product Pages | | | | | | |
| | **Total** | | | | | | |

Spend % = within-campaign share (each campaign's total = 100%).

---

Ends after Campaign Placements. No recommendations, no actions, no investigation notes. The AM reads and decides.
