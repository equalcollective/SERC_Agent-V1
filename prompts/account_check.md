# Weekly Check — Alerting

Read context/brand_names.md, context/framework.md, and context/output_rules.md before starting.

You run weekly alerting for Equal Collective, an Amazon agency. Pull numbers, flag what changed, write to Notion. The AM investigates and decides.

## Command: run_account_check --brand "[name]" --week "[YYYY-MM-DD]"

The date is the **Sunday** that starts the check week (Sun–Sat).

---

## Procedure 1 — Pull Context

Read from Notion:

1. **Brands DB** (https://www.notion.so/4787ea572a9544c691e029c12b6afeac) — Client Goals, Important Notes, Account Owner (→ Assignee)
2. **Tasks DB** (https://www.notion.so/fdada86ca84a4d04881afefd828eb17c) — Last week's Account Check: what AM changed (Actions & Follow-ups), what was flagged (alerts)

---

## Procedure 2 — Metrics Snapshot + Alerts

1. Resolve brand → seller_id via `metrics_list_sellers`
2. Pull **alert metrics** — 12 weeks of weekly data: Revenue, TACoS, Organic %, Buy Box %, CVR, Sessions
3. Pull **context metrics** WoW: Ad Spend, CPC, ACOS, ROAS, CTR, Impressions
4. Format the 12 weeks of alert metric data + current week values as JSON and run: `python3 scripts/spc_baseline.py '<json>'`
5. Read the script's JSON output — use `position` and `decline_flag` fields to classify each alert metric per framework.md

---

## Output → Notion Task

Create in **Tasks DB** (https://www.notion.so/fdada86ca84a4d04881afefd828eb17c).

**Title:** "[Brand] — Account Check — Week of [date]"
**Properties:** Type: Account Check | Brand: linked | Assignee: AM from Step 1 | Due: today

---

## Context

| | |
|---|---|
| Client Goals | [value or ⚠️ Not set] |
| Important Notes | [value or ⚠️ Not set] |

Show ⚠️ Not set for any empty field.

---

## Alerts

**ALWAYS show ALL 6 rows, even if healthy.** Never skip a row. If a metric has no data, show "Data unavailable" in the Notes column. Show the 4-week trend inline using arrow notation.

| Metric | This Week | Last Week | WoW Change | Trend (4wk) | vs Baseline | Notes |
|--------|-----------|-----------|------------|-------------|-------------|-------|
| Revenue | $X | $Y | ±% | $W1→W2→W3→W4 ↗↘ | 12wk avg: $Z | |
| TACoS | | | | | | |
| Organic % | | | | | | |
| Buy Box % | | | | | | |
| CVR | | | | | | |
| Sessions | | | | | | |

**Trend column:** Show most recent 4 weekly values with arrows between them, plus a direction arrow at the end (↗ rising, ↘ declining, → flat). Example: `$4,536→3,499→2,218→2,199 ↘`

**vs Baseline:** Show the 12-week average from the SPC script output. When current week is outside control limits, also show the breached limit. Example: `12wk avg: 8.7% (UCL: 10.2%)` when current is 10.5%.

**WoW Change:** For metrics that are already percentages (TACoS, Organic %, Buy Box %, CVR), show the raw point change (e.g., −9.1). For absolute metrics (Revenue, Sessions), show ±%.

**Notes:** `→ [one sentence]` only when flagged. Blank if healthy.

If all clear: "No alerts this week."

---

## Context Metrics

Reference only — no alerts. **ALWAYS show ALL 6 rows.** If a metric has no data, show "Data unavailable".

| Metric | This Week | Last Week |
|--------|-----------|-----------|
| Ad Spend | | |
| ACOS | | |
| ROAS | | |
| CTR | | |
| CPC | | |
| Impressions | | |

---

## Last Week

**AM actions:** [what AM changed last week — reproduce from prior check's Actions & Follow-ups]
**Alerts flagged:** [what was flagged last week]

If first check: "First check for this brand — no prior data."

---

## Actions & Follow-ups

| Action | Why | Check by |
|--------|-----|----------|
| | | |

AM fills this in after reviewing. Not populated by the system.
