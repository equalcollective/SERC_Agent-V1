# Output Rules

1. Never invent numbers. All data from MCPs.
2. Alert table: ALWAYS 6 rows — Revenue, TACoS, Organic %, Buy Box %, CVR, Sessions. Never skip a row even if healthy. Must include WoW Change column and Trend (4wk) column. If data unavailable, show "Data unavailable" in Notes. Notes: `→ [one sentence]` when flagged, blank if healthy.
3. WoW Change for percentage metrics (TACoS, Organic %, Buy Box %, CVR): show raw point change (e.g., −9.1), not relative %. For absolute metrics (Revenue, Sessions): show ±%.
4. Context metrics table: ALWAYS 6 rows — Ad Spend, ACOS, ROAS, CTR, CPC, Impressions. Never skip a row. This week vs Last week only. No notes. If data unavailable, show "Data unavailable".
5. Campaign table: two rows per campaign (This Wk / Last Wk stacked). Blank row between campaigns. Notes only when 2-check flags.
6. New campaigns (no prior week data) → flag "→ New campaign." Missing campaigns → flag "→ Not active this week."
7. Context section: two-column table. Show ⚠️ Not set for any empty field.
8. Top callout: bullet points (What happened / Why if clear / Watch). Omit "Why" if uncertain.
9. Assignee: Account Owner from Brands DB → resolve via `notion-get-users`.
10. Investigation section: always present, always empty.
11. Actions & Follow-ups: always present as empty table.
12. Last Week section: reproduce AM actions and alerts from prior check. No analysis.
13. Every word must add information the AM cannot already see in the table. No filler.
