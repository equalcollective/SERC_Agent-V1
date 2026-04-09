# Procedure: Negative Cleanup

**Kind:** Sequential
**Status:** V1 — Active
**Prompt file:** `prompts/negative_cleanup.md`

> Keep this file and the prompt in sync. Change one → update the other.

---

## Trigger

On-demand. The AM runs this when they want to identify search terms and ASIN targets wasting ad spend — typically after the account check flags ACOS or spend issues.

The AM triggers it by running:
`run_negative_cleanup --brand "[brand name]" --week "[YYYY-MM-DD]" --days [30|60]`

- `--week`: Sunday that starts the check week (Sun–Sat). Used to find the Account Check task to write into.
- `--days`: Lookback period. 30 or 60 days ending on the Saturday of the check week.

---

## Input

This procedure needs data from two places: Notion (to find the existing Account Check task) and the Metrics Engine (search term numbers).

### Part A — Find the existing Account Check task in Notion

The negative cleanup writes its output into the **Investigation section** of an existing Account Check task. It does not create a new task.

1. **Tasks DB** — Search for the most recent Account Check task matching this brand and week. Title pattern: "[Brand] — Account Check — Week of [date]".
2. **Brands DB** — Read Marketplace for the brand.
3. **Seller ID** — Resolve brand name → seller_id via `metrics_list_sellers` (cross-ref `context/brand_names.md`).

If no Account Check task is found for this brand + week → stop and tell the AM: "No Account Check found for [brand] — Week of [date]. Run the account check first."

### Part B — Search term metrics from the Metrics Engine

The search term report (`rpt_sponsored_products_search_term`) contains both keyword search terms and ASIN search terms in a single table. One query pulls everything.

**One query needed:**

- **Metrics:** `st_spend`, `st_clicks`, `st_orders`, `st_sales`
- **Dimensions:** `["search_term", "search_term_type", "campaign", "ad_group"]`
- **Granularity:** `"daily"` (search term metrics are daily-only)
- **Date range:**
  - End date = check week Sunday + 6 days (Saturday)
  - Start date = end date − (days − 1)
  - Example: --week "2026-03-29" --days 30 → range 2026-03-06 to 2026-04-04

The metrics engine sums daily values across the date range per unique (search_term, search_term_type, campaign, ad_group) combination.

**Derived metrics** (computed from the summed period values):

| Metric | Formula | Notes |
|--------|---------|-------|
| ACOS | st_spend / st_sales × 100 | If sales = 0, show "—" |
| CPC | st_spend / st_clicks | If clicks = 0, show "—" |

**Why search terms, not targets:** The targeting report (`rpt_sponsored_products_targeting`) shows how the AM's configured keywords/ASINs perform in aggregate. The search term report shows what customers actually searched or which product pages triggered impressions. For negative cleanup, the AM needs the actual search terms that wasted money, not the targets they already set up. A keyword target "dog food" might match search term "cat food" — the search term report reveals this; the targeting report does not.

---

## Logic

### Step 1 — Resolve brand

Look up the brand name in `context/brand_names.md` and confirm with `metrics_list_sellers`. Get the seller_id and marketplace.

### Step 2 — Find Account Check task

Search Notion Tasks DB for the Account Check task matching this brand and week.

### Step 3 — Compute date range

- End date = check week Sunday + 6 days (Saturday)
- Start date = end date − (days − 1)
- This gives exactly `days` calendar days inclusive

### Step 4 — Pull search term data

Query the Metrics Engine with the parameters from Part B above.

### Step 5 — Compute account-level context

Before splitting into tables, compute totals across ALL returned search terms:
- Total search term spend
- Total orders
- Total sales
- Overall ACOS (total spend / total sales × 100)

This gives the AM a baseline to compare individual terms against.

### Step 6 — Classify search terms as keyword or ASIN

Split results into two groups:

- **ASIN targets:** search_term matches the pattern `b0` followed by 8 alphanumeric characters (case-insensitive), OR search_term_type indicates ASIN targeting. Either condition is sufficient.
- **Keyword terms:** everything else.

### Step 7 — Sort

Sort each group by spend descending (biggest spenders first).

No minimum spend threshold — every term with any spend is included. The AM can see Orders and Sales columns to instantly spot the worst offenders (high spend, zero/low sales).

### Step 8 — Add suggested negative type

For each term, include a suggested negative match type:
- Default: **Exact** (safest — blocks only this specific search term, doesn't accidentally block good traffic)

A note at the top of the output explains: "All suggestions default to Exact negative (safest). AM may choose Phrase for multi-word terms where all variations are irrelevant."

### Step 9 — Cap at 50 rows per table

If more than 50 keyword or ASIN terms exist, show the top 50 by spend. Include a note with the overflow count and total spend of remaining terms.

### Step 10 — Write to Investigation section

Append the negative cleanup output into the Investigation section of the existing Account Check task. If other investigation content already exists (e.g., placement check), append below it — do not overwrite.

---

## Output

The output is written into the **Investigation section** of the existing Account Check Notion task. It does not create a new task.

### Negative Cleanup heading

`## Negative Cleanup`

`[30|60]-day lookback ending [end date]`

### Account context

A single line showing the baseline across all search terms in the period:

```
Total search term spend: $X | Orders: Y | Sales: $Z | Overall ACOS: X%
```

### Summary

```
- Keyword terms: X total, $Y spend (Z with 0 orders = $W wasted)
- ASIN targets: X total, $Y spend (Z with 0 orders = $W wasted)
```

> All suggestions default to Exact negative (safest). AM may choose Phrase for multi-word terms where all variations are irrelevant.

### Keyword Negative Candidates

Sorted by spend descending. Every keyword term with any spend is included.

| # | Search Term | Campaign | Ad Group | Spend | Clicks | Orders | Sales | ACOS | Suggested Neg |
|---|-------------|----------|----------|-------|--------|--------|-------|------|---------------|
| 1 | | | | | | | | | Exact |

- `#` column is a row number for easy reference
- ACOS shows "—" when sales = 0
- Suggested Neg = "Exact" for all in V1
- Max 50 rows. If more: "Showing top 50 of X keyword terms by spend. Remaining Y terms totaled $Z in spend."
- If 0 keyword terms: "No keyword search terms found."

### ASIN Negative Candidates

Same structure as keyword table, sorted by spend descending.

| # | ASIN Target | Campaign | Ad Group | Spend | Clicks | Orders | Sales | ACOS | Suggested Neg |
|---|-------------|----------|----------|-------|--------|--------|-------|------|---------------|
| 1 | | | | | | | | | Exact |

- Column header says "ASIN Target" instead of "Search Term"
- Max 50 rows with overflow note
- If 0 ASIN terms: "No ASIN targets found."

The same search term can appear in multiple rows if it triggered in different campaign/ad group combinations. This is correct — the AM needs to see each occurrence to know where to add the negative.

### Nothing else

The negative cleanup ends after the ASIN table. No further recommendations, no actions. The AM reads the data and decides what to negate.
