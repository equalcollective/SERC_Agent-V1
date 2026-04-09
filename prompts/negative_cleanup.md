# Negative Cleanup

Read context/amazon.md, context/brand_names.md, and context/output_rules.md before starting.

You run on-demand negative keyword/target analysis for Equal Collective, an Amazon agency. Pull search term metrics, surface the worst performers by spend, write into the Investigation section of the existing Account Check task. The AM reads the data and decides what to negate.

## Command: run_negative_cleanup --brand "[name]" --week "[YYYY-MM-DD]" --days [30|60]

- `--week`: Sunday that starts the check week (Sun–Sat)
- `--days`: Lookback period — 30 or 60 days ending on the check week Saturday

---

## Step 1 — Resolve brand and find Account Check task

1. Resolve brand → seller_id via `metrics_list_sellers` (cross-ref `context/brand_names.md`)
2. Get Marketplace from Notion Brands DB
3. Search Notion Tasks DB for the Account Check task matching this brand and week (title pattern: "[Brand] — Account Check — Week of [date]")

If no Account Check task found → stop. Tell the AM: "No Account Check found for [brand] — Week of [date]. Run the account check first."

---

## Step 2 — Compute date range

- End date = check week Sunday + 6 days (Saturday)
- Start date = end date − (days − 1)
- This gives exactly `days` calendar days inclusive

---

## Step 3 — Pull search term data

Query the Metrics Engine:
- **Metrics:** `st_spend`, `st_clicks`, `st_orders`, `st_sales`
- **Dimensions:** `["search_term", "search_term_type", "campaign", "ad_group"]`
- **Granularity:** `"daily"` (search term metrics are daily-only)
- **Date range:** start date to end date from Step 2

**Search term metrics are daily-only. The metrics engine sums daily values across the date range per unique dimension combination.**

Compute derived metrics from the summed values:
- ACOS = st_spend / st_sales × 100 (if st_sales = 0, show "—")
- CPC = st_spend / st_clicks (if st_clicks = 0, show "—")

---

## Step 4 — Compute account-level context

Before splitting into tables, compute totals across ALL returned search terms:
- Total spend across all search terms
- Total orders
- Total sales
- Overall ACOS = total spend / total sales × 100

This baseline lets the AM compare individual terms against the account average.

---

## Step 5 — Classify and sort

**Split into two groups:**
- **ASIN targets:** search_term matches pattern `b0` + 8 alphanumeric characters (case-insensitive), OR search_term_type indicates ASIN targeting.
- **Keywords:** everything else.

**Sort each group by spend descending** (biggest spenders first).

**No minimum spend threshold** — include every term with any spend. AM decides what's actionable.

**Cap at 50 rows per table** (keyword + ASIN). If more exist, note the overflow count and total spend of remaining terms.

---

## Step 6 — Handle edge cases

- **No search term data returned:** Write "No search term data available for [brand] in this period." into Investigation and stop.
- **All terms have strong performance:** Still show them — AM gets the full picture.
- **Existing content in Investigation section:** Append below existing content (do not overwrite placement check or other investigation data).

---

## Output → Investigation section of existing Account Check task

Write the following into the **Investigation section** of the Account Check task found in Step 1.

---

## Negative Cleanup

**[30|60]-day lookback ending [end date]**

**Total search term spend: $X | Orders: Y | Sales: $Z | Overall ACOS: X%**

### Summary

- **Keyword terms:** X total, $Y spend (Z with 0 orders = $W wasted)
- **ASIN targets:** X total, $Y spend (Z with 0 orders = $W wasted)

> All suggestions default to Exact negative (safest). AM may choose Phrase for multi-word terms where all variations are irrelevant.

---

### Keyword Negative Candidates

Sorted by spend descending. Every keyword term with any spend is included.

| # | Search Term | Campaign | Ad Group | Spend | Clicks | Orders | Sales | ACOS | Suggested Neg |
|---|-------------|----------|----------|-------|--------|--------|-------|------|---------------|
| 1 | | | | | | | | | Exact |

- ACOS = "—" when sales = 0
- Suggested Neg = "Exact" for all in V1
- If > 50 terms: "Showing top 50 of X keyword terms by spend. Remaining Y terms totaled $Z in spend."
- If 0 terms: "No keyword search terms found."

---

### ASIN Negative Candidates

Same structure. Sorted by spend descending.

| # | ASIN Target | Campaign | Ad Group | Spend | Clicks | Orders | Sales | ACOS | Suggested Neg |
|---|-------------|----------|----------|-------|--------|--------|-------|------|---------------|
| 1 | | | | | | | | | Exact |

- If > 50 targets: "Showing top 50 of X ASIN targets by spend. Remaining Y targets totaled $Z in spend."
- If 0 targets: "No ASIN targets found."

---

Same search term can appear in multiple rows (different campaign/ad group). AM needs to see each occurrence to know where to add the negative.

Ends after ASIN table. No further recommendations, no actions. AM reads and decides.
