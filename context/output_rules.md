# Output Rules

1. Never invent numbers. All data from MCPs.
2. Alert table: ALWAYS 7 columns — Metric, This Week, Last Week, WoW Change, Trend (4wk), vs Baseline, Notes. ALWAYS 6 rows — Revenue, TACoS, Organic %, Buy Box %, CVR, Sessions. Never skip a row even if healthy. If data unavailable, show "Data unavailable" in Notes.
3. vs Baseline column: show 12-week median. Example: `12wk med: 8.7%`. Reinforces the flag when current is far from normal.
4. WoW Change for percentage metrics (TACoS, Organic %, Buy Box %, CVR): show raw point change (e.g., −9.1), not relative %. For absolute metrics (Revenue, Sessions): show ±%.
5. Context metrics table: ALWAYS 6 rows — Ad Spend, ACOS, ROAS, CTR, CPC, Impressions. Never skip a row. This week vs Last week only. No notes. If data unavailable, show "Data unavailable".
6. Campaign table: two rows per campaign (This Wk / Last Wk stacked). Blank row between campaigns. Notes only when 2-check flags.
7. New campaigns (no prior week data) → flag "→ New campaign." Missing campaigns → flag "→ Not active this week."
8. Context section: two-column table. Show ⚠️ Not set for any empty field.
9. Top callout: bullet points (What happened / Why if clear / Watch). Omit "Why" if uncertain.
10. Assignee: Account Owner from Brands DB → resolve via `notion-get-users`.
11. Actions & Follow-ups: 3 columns — Action, Why, Check by. Always present as empty table. AM fills in, not the system.
12. Last Week section: reproduce AM actions and alerts from prior check. No analysis.
13. Every word must add information the AM cannot already see in the table. No filler.
14. The account check ends after Last Week. No investigation, no action recommendations, no diagnoses.
