# Output Rules

1. Never invent numbers. All data from MCPs.
2. Alert table: ALWAYS 7 columns — Metric, This Week, Last Week, WoW Change, Trend (4wk), vs Baseline, Notes. ALWAYS 6 rows — Revenue, TACoS, Organic %, Buy Box %, CVR, Sessions. Never skip a row even if healthy. If data unavailable, show "Data unavailable" in Notes.
3. vs Baseline column: show 12-week average from SPC script output. When current week is outside control limits, also show the breached limit. Example: `12wk avg: 8.7% (UCL: 10.2%)`.
4. WoW Change for percentage metrics (TACoS, Organic %, Buy Box %, CVR): show raw point change (e.g., −9.1), not relative %. For absolute metrics (Revenue, Sessions): show ±%.
5. Context metrics table: ALWAYS 6 rows — Ad Spend, ACOS, ROAS, CTR, CPC, Impressions. Never skip a row. This week vs Last week only. No notes. If data unavailable, show "Data unavailable".
6. Context section: two-column table (Client Goals, Important Notes). Show ⚠️ Not set for any empty field.
7. Assignee: Account Owner from Brands DB → resolve via `notion-get-users`.
8. Actions & Follow-ups: 3 columns — Action, Why, Check by. Always present as empty table. AM fills in, not the system.
9. Last Week section: reproduce AM actions and alerts from prior check. No analysis.
10. Every word must add information the AM cannot already see in the table. No filler.
11. The account check ends after Last Week. No investigation, no action recommendations, no diagnoses.
