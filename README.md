# SERC Agent V1

**Structured Equal Review & Check Agent** — An AI-powered system that runs weekly account checks for Amazon brands managed by Equal Collective.

## What it does

SERC pulls data from 4 sources, analyzes what changed and why, and writes a structured account check to Notion — ready for the Account Manager to review and act on.

### Data Sources
| Source | What it provides |
|--------|-----------------|
| **Notion** | Brand context (goals, budgets, COGS), previous account check history, AM action logs |
| **MB-Onboarding** | Account & product-level metrics — revenue, TACoS, sessions, CVR, ROAS, organic %, and more |
| **Metabase** | Campaign-level data — spend, ACOS, CPC per campaign; search terms; placement reports; inventory |
| **SQP (MerchantBots)** | Search query performance — impression share, click share, purchase share per tag |

### Output Structure
Each account check writes a Notion task with:
- **30-second summary** — what happened, why, what to do today
- **A — Metrics & Alerts** — account-level table with inline alerts and actions
- **B — Campaign Intelligence** — auto vs manual split, campaign performance with insights, top search terms, placement analysis
- **C — Client Context** — TACoS target, COGS, budget, goals
- **D — Last Week's Actions** — verdict on every previous action (Worked / Failed / Inconclusive)
- **E — Investigation Notes** — flagged questions for the AM to fill in
- **F — Actions Taken** — AM logs what they changed this week

## Project Structure

```
├── CLAUDE.md                    # Instructions for Claude Code
├── prompts/
│   └── account_check.md         # Main account check prompt (V3)
├── context/
│   ├── brand_names.md           # Canonical brand name list
│   ├── framework.md             # Metric thresholds & causality chains
│   └── output_rules.md          # Output formatting rules
└── README.md
```

## How to run

This agent runs inside [Claude Code](https://claude.ai/claude-code). To run an account check:

```
run_account_check --brand "Brand Name" --week "YYYY-MM-DD"
```

Or run all brands for an Account Manager:

```
run account checks for all brands assigned to [AM name]
```

## Key concepts

- **CRITICAL / WARNING / CLEARED** — every metric is classified each week based on WoW change and hard floors
- **Causality mapping** — when a metric moves >10%, the agent traces it back to AM actions or campaign changes
- **AM Action Log** — the agent reads the last 4 weeks of actions to connect past changes to current results
- **Partial week detection** — if the latest week has incomplete data, it's shown in a collapsed toggle, not the main table

## Built by
[Equal Collective](https://equalcollective.com) — Amazon growth agency
