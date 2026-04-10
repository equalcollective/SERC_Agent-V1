# Procedure: Weekly Account Check — Alerts

**Kind:** Sequential
**Status:** V3 — Active
**Prompt file:** `prompts/account_check.md`

> The prompt file is the source of truth. This file is a summary for orientation.

---

## Trigger

Runs **every week** for every active brand. The AM triggers it:

```
run_account_check --brand "[brand name]" --week "[YYYY-MM-DD]"
```

The date is the **Sunday** that starts the check week (Sun–Sat).

---

## Input

### User

- **Brand name** — confirmed against `metrics_list_sellers`
- **Week start date** — confirmed as a Sunday (YYYY-MM-DD)

### Metrics Engine (MCP)

- **Seller ID** — resolved via `metrics_list_sellers`
- **6 metrics, 12 weeks, weekly:** Revenue, TACoS, Organic %, Buy Box %, CVR, Sessions

---

## Logic

### Step 1 — Confirm inputs

Resolve brand from `metrics_list_sellers`. Confirm week is a Sunday. Do not proceed until both are confirmed.

### Step 2 — Fetch data

Query Metrics Engine for 12 weeks of weekly data (target week minus 11 weeks through target week) for all 6 metrics.

### Step 3 — Run analysis script

Format data as JSON, run `python3 scripts/spc_baseline.py '<json>'`. The script computes:
- Output columns: This Week, Last Week, WoW Change, Trend (4wk)
- Internal flags: SPC breach, 3-week consecutive movement, Buy Box threshold
- Status signal: 🟢/🟡/🔴

### Step 4 — Write notes

Review each metric's 12-week shape independently. Write a note (max 150 chars, starts with `→`) for any metric that warrants the AM's attention. Internal flags inform reasoning but are never shown as labels.

### Step 5 — Output to Notion

Find the target Account Check page in the Tasks DB. Find the "Alerts" heading. Insert a 7-column table (Status, Metric, This Week, Last Week, WoW Change, Trend (4wk), Notes) with exactly 6 data rows in fixed order.

---

## Output

A Notion table inserted under the "Alerts" heading on the brand's Account Check page.

**7 columns:** Status | Metric | This Week | Last Week | WoW Change | Trend (4wk) | Notes

**6 rows (fixed order):** Revenue, TACoS, Organic %, Buy Box %, CVR, Sessions

No Context section. No Last Week section. No Actions section. Just the alert table.
