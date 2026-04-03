# SERC Agent V1

**Structured Equal Review & Check** — A centralized prompt and context repo for all AI-powered automations at Equal Collective.

This repo is the single source of truth for every prompt, context file, and rule that powers our Claude Code agents. Account checks, campaign analysis, negative keyword runs, and any future automation — all prompts live here.

## Data Sources

All prompts in this repo can pull from these 4 MCP-connected sources:

| Source | What it provides |
|--------|-----------------|
| **Notion** | Brand context, task history, AM action logs, client notes |
| **MB-Onboarding** | Account & product metrics — revenue, TACoS, sessions, CVR, ROAS, organic %, etc. |
| **Metabase** | Campaign data — spend, ACOS, CPC per campaign; search terms; placements; inventory |
| **SQP (MerchantBots)** | Search query performance — impression share, click share, purchase share per tag |

## Project Structure

```
├── CLAUDE.md                        # Master instructions for Claude Code
├── prompts/
│   └── account_check.md             # Weekly account check (V3)
│   └── (future prompts go here)
├── context/
│   ├── brand_names.md               # Canonical brand name list
│   ├── framework.md                 # Metric thresholds & causality chains
│   └── output_rules.md              # Output formatting rules
└── README.md
```

### Directories

- **`prompts/`** — Each prompt is a self-contained instruction set for a specific automation. New prompts get added here as we build more workflows.
- **`context/`** — Shared reference files that prompts pull from. Brand names, metric thresholds, formatting rules — anything reusable across multiple prompts.
- **`CLAUDE.md`** — The entry point. Tells Claude Code which files to read before executing any command.

## Current Prompts

### Account Check (`prompts/account_check.md`)
Runs a structured weekly review for an Amazon brand. Pulls metrics, traces causality, checks AM actions, and writes a full report to Notion.

```
run_account_check --brand "Brand Name" --week "YYYY-MM-DD"
```

Run all brands for an AM:
```
run account checks for all brands assigned to [AM name]
```

### More coming
As we build new automations (negative keyword runs, campaign audits, listing reviews, etc.), each will get its own prompt file in `prompts/` and an entry in this README.

## How it works

1. **CLAUDE.md** routes the command to the right prompt file
2. The prompt file defines the steps, data to pull, analysis to run, and output format
3. **Context files** provide shared rules (thresholds, brand names, formatting)
4. The agent executes against live MCP data and writes output to Notion

## Built by
[Equal Collective](https://equalcollective.com) — Amazon growth agency
