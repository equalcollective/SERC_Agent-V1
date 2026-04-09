# Procedure: Metrics Snapshot + Alerts

**Kind:** Sequential
**Status:** V2 — Active
**Notion page:** [Procedure: Metrics Snapshot + Alerts](https://www.notion.so/33afde5f52828133981ff3341958804d)
**Prompt file:** `prompts/account_check.md`

> Keep this file, the Notion page, and the prompt in sync. Change one → update the others.

---

## Trigger

This procedure runs **every week**, for every active brand. It runs after the Pull Context procedure has finished — meaning the brand's context (goals, last week's actions) has already been assembled.

The Account Manager triggers it by running:
`run_account_check --brand "[brand name]" --week "[YYYY-MM-DD]"`

The date is the **Sunday** that starts the check week. The week is Sunday through Saturday.

---

## Input

This procedure needs data from two places: Notion (brand context) and the Metrics Engine (numbers). The brand context is collected first by Procedure 1 (Pull Context). The metrics are pulled directly by this procedure.

### Part A — Brand context from Notion (collected by Procedure 1: Pull Context)

Before this procedure runs, Procedure 1 reads from two Notion databases and assembles the brand's context. Here's exactly where each piece comes from:

**1. Brands database** (https://www.notion.so/4787ea572a9544c691e029c12b6afeac)

The system finds the brand's row and reads these properties:

| Property | What it is | How it's used |
|----------|-----------|---------------|
| **Client Goals** | One-line description of what the client wants (e.g., "Profitability only" or "Scale to $50K/month") | Shown in the Context section so the AM remembers what they're optimizing for. |
| **Important Notes** | Any constraints, conditions, or things to watch (e.g., "Client pausing in Q4", "Don't touch listing without approval") | Shown in Context for AM reference. |
| **Account Owner** | The person (Notion user) assigned to manage this brand | Becomes the Assignee on the output task. Resolved from a user ID to a name. |

**2. Tasks database** (https://www.notion.so/fdada86ca84a4d04881afefd828eb17c)

The system searches for the most recent Account Check task for this brand. From that task's page content, it extracts:

- **Actions & Follow-ups section** — a table where the AM logged what they changed last week (e.g., "Increased bids on Campaign X", "Changed main image on Product Y"). This is reproduced in the "Last Week" section of the new check.
- **Alerts from the Metrics & Alerts table** — which metrics were flagged last week. This is also reproduced so the AM can see whether last week's problems got better or worse.

If no previous Account Check task exists for this brand, the system notes "First check for this brand" and skips the Last Week section.

### Part B — Metrics from the Metrics Engine

The Metrics Engine is an API (accessed via MCP) that holds all the Amazon numbers. It requires a **seller ID** and **marketplace** to run any query.

- **Seller ID** — The system looks up the brand name in the Metrics Engine to get the seller ID. This mapping is also listed in `context/brand_names.md` as a reference.
- **Account-level alert metrics (12 weeks, weekly)** — 12 weekly data points used to compute statistical baselines via the SPC script.
- **Account-level context metrics (check week vs prior week)** — A side-by-side comparison of supporting metrics for AM reference.

---

## Logic

### Step 1 — Pull alert metrics

Query the Metrics Engine for 6 metrics that generate alerts. Get **12 weeks of weekly data** for the SPC baseline computation.

The 6 alert metrics are:

| Metric | What it measures | Why it matters |
|--------|-----------------|----------------|
| **Revenue** | Total sales (ads + organic) | The ultimate business outcome |
| **TACoS** | Ad spend as a % of total sales | Profitability signal — are ads eating into margin? |
| **Organic %** | What share of revenue comes without ads | Ad dependency — is the brand building equity or renting traffic? |
| **Buy Box %** | How often the listing has the "Add to Cart" button | Losing Buy Box is the most destructive event for a listing |
| **CVR** | What % of visitors buy | Conversion health — is the listing working? |
| **Sessions** | Number of unique visitors | Traffic/visibility — are people finding the product? |

### Step 2 — Pull context metrics

In the same query, also pull 6 supporting metrics (this week vs last week). These are **not** alerted on — they're shown for reference so the AM can glance at them without running a separate report.

| Metric | What it measures |
|--------|-----------------|
| Ad Spend | How much was spent on advertising |
| ACOS | Ad spend / ad sales (ad efficiency) |
| ROAS | Ad sales / ad spend (inverse of ACOS) |
| CTR | Click-through rate on ads |
| CPC | Cost per click on ads |
| Impressions | How many times ads were shown |

### Step 3 — Run SPC baseline script

Format the 12 weeks of alert metric data + current week values as JSON and run:

```
python3 scripts/spc_baseline.py '<json>'
```

The script computes for each metric: mean, standard deviation, upper control limit (UCL = mean + 2σ), lower control limit (LCL = mean − 2σ), consecutive decline count, and position classification.

Read the JSON output. See `context/framework.md` for the full input/output schema.

### Step 4 — Classify alert metrics

For each of the 6 alert metrics, use the script's output to determine if it should be flagged:

- **`position` = `below_lcl` or `above_ucl`** → metric is outside normal statistical range. Flag it.
- **`decline_flag` = `true`** → 3+ consecutive weeks of decline. Flag it even if within limits.
- **TACoS is inverted**: `above_ucl` = bad (efficiency worsening).
- **Buy Box % hard threshold**: Below 90% = always flag, regardless of SPC position.

The script's `summary.flagged_metrics` field lists all metrics that triggered. Use this as the starting point, then apply the Buy Box hard threshold check.

---

## Output

The output is a new **Account Check task** created in the Notion Tasks database (https://www.notion.so/fdada86ca84a4d04881afefd828eb17c). It is linked to the brand, assigned to the Account Manager, and due today.

**Task title:** "[Brand] — Account Check — Week of [date]"
**Task properties:** Type = Account Check, Brand = linked, Assignee = AM, Due = today

**The task page contains these sections, in order:**

### 1. Context

A two-column table showing the brand's key context:
- Client Goals (or ⚠️ Not set)
- Important Notes (or ⚠️ Not set)

Show ⚠️ Not set for any empty field.

### 2. Alerts

A table with the 6 alert metrics. Columns: Metric, This Week, Last Week, WoW Change, Trend (4wk), vs Baseline, Notes.

- **WoW Change:** For percentage metrics (TACoS, Organic %, Buy Box %, CVR) show raw point change (e.g., −9.1). For absolute metrics (Revenue, Sessions) show ±%.
- **Trend (4wk):** All 4 weekly values with arrows between them, plus a direction arrow at the end. Example: `$4,536→3,499→2,218→2,199 ↘`. This replaces a graph — the AM sees the full trajectory at a glance.
- **vs Baseline:** Show the 12-week average from the SPC script. When current is outside control limits, also show the breached limit. Example: `12wk avg: 8.7% (UCL: 10.2%)`.

The **Notes** column is blank for healthy metrics. For flagged metrics: `→ [one sentence]`

If all metrics are healthy: "No alerts this week."

### 3. Context Metrics

A smaller reference table showing the 6 context metrics. Columns: Metric, This Week, Last Week. No notes, no alerts — just the numbers for the AM to see.

### 4. Last Week

Reproduces two things from the prior week's Account Check task:
- What the AM changed (from Actions & Follow-ups)
- What was flagged (from last week's alerts)

If this is the first check for the brand: "First check for this brand — no prior data."

### 5. Actions & Follow-ups

Always present. An empty table for the AM to fill in:

| Action | Why | Check by |
|--------|-----|----------|
| | | |
