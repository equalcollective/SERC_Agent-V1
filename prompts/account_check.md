# Weekly Check — Alerting

Read context/amazon.md, context/brand_names.md, context/framework.md, and context/output_rules.md before starting.

You run weekly alerting for Equal Collective, an Amazon agency. Pull numbers, flag what changed, write to Notion. The AM investigates and decides.

## Command: run_account_check --brand "[name]" --week "[YYYY-MM-DD]"

The date is the **Sunday** that starts the check week (Sun–Sat).

---

## Procedure 1 — Pull Context

Read from Notion:

1. **Brands DB** — Client Goals, Important Notes, Marketplace, Account Owner (→ Assignee)
2. **Tasks DB** — Last week's Account Check: what AM changed (Actions & Follow-ups), what was flagged (alerts)

---

## Procedure 2 — Metrics Snapshot + Alerts

1. Resolve brand → seller_id via `metrics_list_sellers`
2. Pull **alert metrics** WoW + 4-week weekly data: Revenue, TACoS, Organic %, Buy Box %, CVR, Sessions
3. Pull **context metrics** WoW: Ad Spend, CPC, ACOS, ROAS, CTR, Impressions
4. Pull **campaign metrics** WoW (all campaigns): Spend, ACOS, Orders, Sales, ROAS
5. Classify alert metrics using framework.md — use judgment, no rigid thresholds
6. Flag campaigns using the 2-check model from framework.md

---

## Output → Notion Task

**Title:** "[Brand] — Account Check — Week of [date]"
**Properties:** Type: Account Check | Brand: linked | Assignee: AM from Step 1 | Due: today

---

**[RED/AMBER/GREEN callout]**

**RED** = something is broken or brand is losing money — look today
**AMBER** = something trending wrong — investigate this week
**GREEN** = all healthy — no action needed

- **What happened:** [one bullet — key movement with numbers]
- **Why (if clear):** [omit if uncertain]
- **Watch:** [what metric to check first]

---

## Context

| | |
|---|---|
| Client Goals | [value or ⚠️ Not set] |
| Important Notes | [value or ⚠️ Not set] |
| Marketplace | [value] |

Show ⚠️ Not set for any empty field.

---

## Alerts

**ALWAYS show ALL 6 rows, even if healthy.** Never skip a row. If a metric has no data, show "Data unavailable" in the Notes column. Show the 4-week trend inline using arrow notation.

| Metric | This Week | Last Week | WoW Change | Trend (4wk) | Notes |
|--------|-----------|-----------|------------|-------------|-------|
| Revenue | $X | $Y | ±% | $W1→W2→W3→W4 ↗↘ | |
| TACoS | | | | | |
| Organic % | | | | | |
| Buy Box % | | | | | |
| CVR | | | | | |
| Sessions | | | | | |

**Trend column:** Show all 4 weekly values with arrows between them, plus a direction arrow at the end (↗ rising, ↘ declining, → flat). Example: `$4,536→3,499→2,218→2,199 ↘`

**WoW Change:** For metrics that are already percentages (TACoS, Organic %, Buy Box %, CVR), show the raw point change (e.g., "48.5% → 39.4%" = −9.1 points, write as "−9.1"). For absolute metrics (Revenue, Sessions), show ±%.

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

## Campaigns

Overview for AM. AM investigates and takes action on flagged campaigns separately.

Show two rows per campaign — This Week and Last Week stacked — so the AM can compare vertically. Add a blank row between campaigns for visual separation.

| Campaign | Week | Spend | ACOS | Orders | ROAS | Notes |
|----------|------|-------|------|--------|------|-------|
| Campaign A | This Wk | | | | | |
| | Last Wk | | | | | |
| | | | | | | |
| Campaign B | This Wk | | | | | |
| | Last Wk | | | | | |

If a campaign exists this week but did not exist last week → note: "→ New campaign, no prior week data"
If a campaign existed last week but not this week → note: "→ Campaign not active this week"

Flag using 2-check model. `→ [one sentence]` only when flagged. Blank if healthy.

---

## Last Week

**AM actions:** [what AM changed last week — reproduce from prior check]
**Alerts flagged:** [what was flagged last week]

If first check: "First check for this brand — no prior data."

---

## Investigation

_Empty — for AM notes or future investigation procedure._

---

## Actions & Follow-ups

| What I changed | Before → After | Why | Expected outcome | Check on |
|----------------|----------------|-----|------------------|----------|
| | | | | |
