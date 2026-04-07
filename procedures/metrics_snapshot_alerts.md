# Procedure: Metrics Snapshot + Alerts

**Kind:** Sequential
**Status:** V1 — Active
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

Before this procedure runs, Procedure 1 reads from three Notion databases and assembles the brand's context. Here's exactly where each piece comes from:

**1. Brands database** (one row per client)

The system finds the brand's row and reads these properties:

| Property | What it is | How it's used |
|----------|-----------|---------------|
| **Client Goals** | One-line description of what the client wants (e.g., "Profitability only" or "Scale to $50K/month") | Shown in the Context section so the AM remembers what they're optimizing for. |
| **Important Notes** | Any constraints, conditions, or things to watch (e.g., "Client pausing in Q4", "Don't touch listing without approval") | Shown in Context for AM reference. |
| **Marketplace** | Which Amazon marketplace: US, UK, CA, EU, or IN | Determines which metrics-engine data to query. |
| **Account Owner** | The person (Notion user) assigned to manage this brand | Becomes the Assignee on the output task. Resolved from a user ID to a name. |

**2. Tasks database** (all work items)

The system searches for the most recent Account Check task for this brand. From that task's page content, it extracts:

- **Actions & Follow-ups section** — a table where the AM logged what they changed last week (e.g., "Increased bids on Campaign X", "Changed main image on Product Y"). This is reproduced in the "Last Week" section of the new check.
- **Alerts from the Metrics & Alerts table** — which metrics were flagged as critical or warning last week. This is also reproduced so the AM can see whether last week's problems got better or worse.

If no previous Account Check task exists for this brand, the system notes "First check for this brand" and skips the Last Week section.

### Part B — Metrics from the Metrics Engine

The Metrics Engine is an API (accessed via MCP) that holds all the Amazon numbers. It requires a **seller ID** and **marketplace** to run any query.

- **Seller ID** — The system looks up the brand name in the Metrics Engine to get the seller ID. This mapping is also listed in `context/brand_names.md` as a reference.
- **Account-level metrics (check week vs prior week)** — A side-by-side comparison: what each metric was this week vs last week, plus the absolute and percentage change.
- **Account-level metrics (last 4 weeks, weekly)** — Four weekly data points used to calculate a 4-week rolling average. This average is the baseline for "what's normal for this brand."
- **Campaign-level metrics (check week vs prior week)** — The same side-by-side comparison, but broken down per advertising campaign. Every campaign is included.

---

## Logic

### Step 1 — Pull alert metrics

Query the Metrics Engine for 6 metrics that generate alerts. Get two views:

1. **This week vs last week** — a direct comparison showing the change
2. **Last 4 weeks** — to calculate a rolling average as a baseline

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

In the same query, also pull 6 supporting metrics. These are **not** alerted on — they're shown for reference so the AM can glance at them without running a separate report.

| Metric | What it measures |
|--------|-----------------|
| Ad Spend | How much was spent on advertising |
| ACOS | Ad spend / ad sales (ad efficiency) |
| ROAS | Ad sales / ad spend (inverse of ACOS) |
| CTR | Click-through rate on ads |
| CPC | Cost per click on ads |
| Impressions | How many times ads were shown |

### Step 3 — Pull campaign metrics

Query the Metrics Engine for **all campaigns**, this week vs last week. Metrics per campaign: Spend, ACOS, Orders, Sales, ROAS.

Every campaign is shown — not just flagged ones. The AM needs the full picture.

### Step 4 — Classify alert metrics

For each of the 6 alert metrics, decide: is this **critical**, a **warning**, or **healthy**?

There are no rigid percentage thresholds. The system uses judgment by looking at:
- How much did it change week over week?
- How does it compare to the 4-week average?
- What is the brand's context? (e.g., a profitability-focused brand vs a growth brand)

**Specific logic per metric:**

- **Revenue** — Flag significant declines, especially if also below 4-week average. Also flag significant growth (growth is an opportunity).
- **TACoS** — Flag significant increases WoW or sustained multi-week rises. TACoS rising means ads are eating a bigger share of sales.
- **Organic %** — Flag meaningful drops in percentage points. A sustained multi-week decline is concerning. Below 30% and still declining is serious — the brand is heavily ad-dependent.
- **Buy Box %** — Below 90% = always flag (this is an Amazon platform reality). Also flag significant drops even if still above 90%.
- **CVR** — Flag notable drops, especially if CVR is also below the 4-week average.
- **Sessions** — Flag significant drops, especially if below 4-week average.

### Step 5 — Classify campaigns

For each campaign, run 2 independent checks:

1. **Spend efficiency** — Did spend go up significantly but orders stayed flat or went down? This means money is being wasted.
2. **Direction** — Is ACOS worse than last week? This means the campaign is trending toward being less efficient.

If either check fires → flag the campaign with a one-line note.
If neither fires → campaign is healthy, no note needed.

### Step 6 — Determine overall severity

Based on all the alert classifications:
- **RED** — Something is broken or the brand is losing money. AM should look at this **today**.
- **AMBER** — Something is trending in the wrong direction. AM should investigate **this week**.
- **GREEN** — All metrics are healthy. No action needed.

A short explanation of what RED/AMBER/GREEN means is included at the top of the output so that someone reading for the first time understands the severity levels.

---

## Output

The output is a new **Account Check task** created in the Notion Tasks database. It is linked to the brand, assigned to the Account Manager, and due today.

**Task title:** "[Brand] — Account Check — Week of [date]"
**Task properties:** Type = Account Check, Brand = linked, Assignee = AM, Due = today, Priority = High

**The task page contains these sections, in order:**

### 1. Top callout (RED/AMBER/GREEN)

A colored callout box at the very top. Color matches severity. Contains a 30-second summary in bullet points:
- **What happened** — the single most important metric movement, with actual numbers
- **Why (if clear)** — only if the data clearly points to a cause. Omitted entirely if uncertain.
- **Watch** — which metric the AM should look at first

### 2. Context

A two-column table showing the brand's key context:
- Client Goals (or ⚠️ Not set)
- Important Notes (or ⚠️ Not set)
- Marketplace

Show ⚠️ Not set for any empty field.

### 3. Alerts

A table with the 6 alert metrics. Columns: Metric, This Week, Last Week, WoW Change, Trend (4wk), Notes.

- **WoW Change:** For percentage metrics (TACoS, Organic %, Buy Box %, CVR) show raw point change (e.g., −9.1). For absolute metrics (Revenue, Sessions) show ±%.
- **Trend (4wk):** All 4 weekly values with arrows between them, plus a direction arrow at the end. Example: `$4,536→3,499→2,218→2,199 ↘`. This replaces a graph — the AM sees the full trajectory at a glance.

The **Notes** column is blank for healthy metrics. For flagged metrics: `→ [one sentence]`

If all metrics are healthy: "No alerts this week."

### 4. Context Metrics

A smaller reference table showing the 6 context metrics. Columns: Metric, This Week, Last Week. No notes, no alerts — just the numbers for the AM to see.

### 5. Campaigns

Two rows per campaign — This Wk and Last Wk stacked vertically — with a blank separator row between campaigns. Columns: Campaign, Week, Spend, ACOS, Orders, ROAS, Notes.

This is an overview. The AM investigates and takes action on flagged campaigns separately.

- If a campaign is new this week (no prior data): "→ New campaign, no prior week data"
- If a campaign existed last week but not this week: "→ Campaign not active this week"

The Notes column uses `→ [one sentence]` format, only when the 2-check model flags something. Blank if healthy.

### 6. Last Week

Reproduces two things from the prior week's Account Check task:
- What the AM changed (from Actions & Follow-ups)
- What was flagged (from last week's alerts)

If this is the first check for the brand: "First check for this brand — no prior data."

### 7. Investigation

Always present. Always empty. This is a placeholder for the AM to write investigation notes, or for a future investigation procedure.

### 8. Actions & Follow-ups

Always present. An empty table for the AM to fill in:

| What I changed | Before → After | Why | Expected outcome | Check on |
|----------------|----------------|-----|------------------|----------|
| | | | | |
