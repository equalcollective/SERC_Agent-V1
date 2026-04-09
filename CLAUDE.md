# SERC Agent — Command Registry

## Before Any Command

1. Read `context/brand_names.md` to resolve brand names to seller IDs.
2. Read the prompt file and all listed context files completely before starting execution.
3. Never invent data. All numbers come from MCP tools.

## Commands

| Command | Prompt File | Context Files |
|---------|------------|---------------|
| `run_account_check --brand "[name]" --week "[YYYY-MM-DD]"` | `prompts/account_check.md` | `framework.md`, `output_rules.md` |
| `run_placement_check --brand "[name]" --week "[YYYY-MM-DD]"` | `prompts/placement_check.md` | `output_rules.md` |
| `run_negative_cleanup --brand "[name]" --week "[YYYY-MM-DD]" --days [30\|60]` | `prompts/negative_cleanup.md` | `output_rules.md` |

## Context Files

| File | Purpose |
|------|---------|
| `context/framework.md` | Alert framework — 6 alert metrics, SPC baseline method |
| `context/output_rules.md` | Formatting rules for Notion output |
| `context/brand_names.md` | Canonical brand name → seller ID mapping across systems |
| `scripts/spc_baseline.py` | Python script — computes mean, std dev, control limits from 12 weeks of data |
