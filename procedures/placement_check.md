# Procedure: Placement Check

**Kind:** Sequential
**Status:** V1 — Active
**Prompt file:** `prompts/placement_check.md`

> Keep this file, the Notion page, and the prompt in sync. Change one → update the others.

---

## Trigger

On-demand. The AM runs this when they want to investigate placement performance — typically after the account check flags ACOS or spend issues and the AM wants to see WHERE the spend is going.

The AM triggers it by running:
`run_placement_check --brand "[brand name]" --week "[YYYY-MM-DD]"`

The date is the **Sunday** that starts the check week (Sun–Sat). Same convention as account check.

---

## Input

This procedure needs data from two places: Notion (to find the existing Account Check task) and the Metrics Engine (placement numbers).

### Part A — Find the existing Account Check task in Notion

The placement check writes its output into the **Investigation section** of an existing Account Check task. It does not create a new task.

1. **Tasks DB** — Search for the most recent Account Check task matching this brand and week. The task title follows the pattern: "[Brand] — Account Check — Week of [date]".
2. **Brands DB** — Read Marketplace and Account Owner for the brand.
3. **Seller ID** — Resolve brand name → seller_id via `metrics_list_sellers` (cross-ref `context/brand_names.md`).

If no Account Check task is found for this brand + week → stop and tell the AM: "No Account Check found for [brand] — Week of [date]. Run the account check first."

### Part B — Placement metrics from the Metrics Engine

The Metrics Engine holds placement data in the `rpt_sponsored_products_placement` table. Four raw metrics are available:

| Metric      | Key              | What it measures                 |
| ----------- | ---------------- | -------------------------------- |
| Spend       | `pl_spend`       | Ad spend by placement            |
| Sales       | `pl_sales`       | Ad-attributed sales by placement |
| Clicks      | `pl_clicks`      | Ad clicks by placement           |
| Impressions | `pl_impressions` | Ad impressions by placement      |

**Granularity constraint:** Placement metrics only support `daily` granularity. To get weekly totals, query 7 days of daily data and sum across days per placement.

**Two queries needed:**

1. **Account-level placement data (WoW):**
   - Metrics: `pl_spend`, `pl_sales`, `pl_clicks`, `pl_impressions`
   - Dimensions: `["placement"]`
   - Date ranges: check week (Sun–Sat) AND prior week (prior Sun–prior Sat)
   - Sum daily values across 7 days per placement to get weekly totals

2. **Campaign-level placement data (this week only):**
   - Metrics: `pl_spend`, `pl_sales`, `pl_clicks`, `pl_impressions`
   - Dimensions: `["placement", "campaign"]`
   - Date range: check week only
   - Sum daily values per (campaign, placement)

**Derived metrics** (computed from the summed weekly values — never from daily averages):

| Metric        | Formula                             | Notes                        |
| ------------- | ----------------------------------- | ---------------------------- |
| ACOS          | spend / sales × 100                 | If sales = 0, show "—"       |
| CPC           | spend / clicks                      | If clicks = 0, show "—"      |
| CTR           | clicks / impressions × 100          | If impressions = 0, show "—" |
| Spend Share % | placement_spend / total_spend × 100 | Share of total account spend |
| Sales Share % | placement_sales / total_sales × 100 | Share of total account sales |

**Not available at placement level:** Orders (Amazon does not report order counts per placement). This means CVR cannot be computed per placement.

---

## Logic

### Step 1 — Resolve brand

Look up the brand name in `context/brand_names.md` and confirm with `metrics_list_sellers`. Get the seller_id and marketplace.

### Step 2 — Find Account Check task

Search Notion Tasks DB for the Account Check task matching this brand and week. This task's Investigation section is where the output will be written.

### Step 3 — Pull account-level placement data

Query the Metrics Engine for `pl_spend`, `pl_sales`, `pl_clicks`, `pl_impressions` with `dimensions: ["placement"]` and `granularity: "daily"`.

Run for both check week and prior week. Sum across 7 days per placement to get weekly totals.

### Step 4 — Compute account-level derived metrics

For each placement (Top of Search, Rest of Search, Product Pages), for each week:

- ACOS = spend_sum / sales_sum × 100
- CPC = spend_sum / clicks_sum
- CTR = clicks_sum / impressions_sum × 100
- Spend % = placement_spend / total_spend × 100
- Sales % = placement_sales / total_sales × 100

Handle division by zero: if the denominator is 0, show "—" for that metric.

Also compute a **Total** row: sum all placements for each week.

### Step 5 — Pull campaign-level placement data

Query the Metrics Engine for `pl_spend`, `pl_sales`, `pl_clicks`, `pl_impressions` with `dimensions: ["placement", "campaign"]` and `granularity: "daily"`.

Check week only. Sum across 7 days per (campaign, placement).

### Step 6 — Compute campaign-level derived metrics

Same derivations as Step 4, but:

- Spend % = within-campaign share (placement_spend / campaign_total_spend × 100)
- Sort campaigns by total spend descending (biggest spenders first)

### Step 7 — Generate summary

Write 3 bullet points, one per placement: spend share, sales share, ACOS. Pure factual statements — no judgment, no severity, no recommendations.

### Step 8 — Write to Investigation section

Append the placement breakdown (summary + both tables) into the Investigation section of the existing Account Check task.

---

## Output

The output is written into the **Investigation section** of the existing Account Check Notion task. It does not create a new task.

### Placement Breakdown heading

`## Placement Breakdown`

### Summary

3 bullets — one per placement. Spend share, sales share, ACOS. Facts only.

```
- Top of Search: X% of spend, X% of sales (ACOS X%)
- Rest of Search: X% of spend, X% of sales (ACOS X%)
- Product Pages: X% of spend, X% of sales (ACOS X%)
```

### Account-Level Placements (WoW)

Two rows per placement (This Wk / Last Wk stacked). Blank row between placements. Total row at the bottom.

| Placement      | Week    | Spend | Spend % | Sales | Sales % | ACOS | CPC | CTR | Clicks | Impressions |
| -------------- | ------- | ----- | ------- | ----- | ------- | ---- | --- | --- | ------ | ----------- |
| Top of Search  | This Wk | $X    | X%      | $X    | X%      | X%   | $X  | X%  | X      | X           |
|                | Last Wk | $X    | X%      | $X    | X%      | X%   | $X  | X%  | X      | X           |
|                |         |       |         |       |         |      |     |     |        |             |
| Rest of Search | This Wk | $X    | X%      | $X    | X%      | X%   | $X  | X%  | X      | X           |
|                | Last Wk | $X    | X%      | $X    | X%      | X%   | $X  | X%  | X      | X           |
|                |         |       |         |       |         |      |     |     |        |             |
| Product Pages  | This Wk | $X    | X%      | $X    | X%      | X%   | $X  | X%  | X      | X           |
|                | Last Wk | $X    | X%      | $X    | X%      | X%   | $X  | X%  | X      | X           |
|                |         |       |         |       |         |      |     |     |        |             |
| **Total**      | This Wk | $X    | 100%    | $X    | 100%    | X%   | $X  | X%  | X      | X           |
|                | Last Wk | $X    | 100%    | $X    | 100%    | X%   | $X  | X%  | X      | X           |

### Campaign Placements (This Week)

3 rows per campaign (one per placement) + a bolded Total row. Blank row between campaigns. Sorted by campaign total spend descending.

| Campaign   | Placement      | Spend  | Spend %  | Sales  | ACOS   | CPC    | CTR    |
| ---------- | -------------- | ------ | -------- | ------ | ------ | ------ | ------ |
| Campaign A | Top of Search  | $X     | X%       | $X     | X%     | $X     | X%     |
|            | Rest of Search | $X     | X%       | $X     | X%     | $X     | X%     |
|            | Product Pages  | $X     | X%       | $X     | X%     | $X     | X%     |
|            | **Total**      | **$X** | **100%** | **$X** | **X%** | **$X** | **X%** |
|            |                |        |          |        |        |        |        |
| Campaign B | Top of Search  | $X     | X%       | $X     | X%     | $X     | X%     |
|            | Rest of Search | $X     | X%       | $X     | X%     | $X     | X%     |
|            | Product Pages  | $X     | X%       | $X     | X%     | $X     | X%     |
|            | **Total**      | **$X** | **100%** | **$X** | **X%** | **$X** | **X%** |

Spend % = within-campaign share (each campaign's total = 100%).

Show all 3 placements for every campaign, even if a placement has zero activity (show as $0 / 0).

### Nothing else

The placement check ends after the Campaign Placements table. No recommendations, no actions, no investigation notes. The AM reads the data and decides.
