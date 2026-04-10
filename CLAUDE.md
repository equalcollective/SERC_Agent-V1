# SERC Agent — Command Registry

## Before Any Command

1. Read the prompt file completely before starting execution.
2. Never invent data. All numbers come from MCP tools.
3. Brand names are resolved live from `metrics_list_sellers` — do not rely on static files.

## Commands

| Command | Prompt File |
|---------|------------|
| `run_account_check --brand "[name]" --week "[YYYY-MM-DD]"` | `prompts/account_check.md` |

## Key Files

| File | Purpose |
|------|---------|
| `prompts/account_check.md` | Self-contained prompt — inputs, data fetching, analysis, output format, rules |
| `scripts/spc_baseline.py` | Python script — computes output columns, internal flags, status signals from 12 weeks of data |
