# Output Rules — Always Apply

1. Never invent numbers. Only use data from MCPs.
2. Product-level table in Section A: show active ASINs only (sessions > 0 in 2+ of last 4 weeks). Sort by revenue. If >8 ASINs: top 5 + any flagged, count the rest. Include inventory weeks of cover inline. One sentence Note per flagged product.
3. Every significant metric change (>10% WoW) must have a cause and action in the "Notes / Alerts" column of the metrics table in Section A.
4. No framework labels in the output. No R1/R2/R3. Plain language only.
5. Alerts live inside the metrics table (Section A, "Notes / Alerts" column). Each flagged row must end with "Do this now:" and one specific action. There is no separate Alerts section.
6. Section B (Campaign Intelligence) always shown when Metabase data is available.
7. Section D: every action from last week gets a verdict. Do not skip any.
8. Negatives reminder: only show if wasted spend found ($10+ spend, 0 orders, 14 days). Never show if none found. Place below the metrics table in Section A.
9. SQP: never in the main output. Only in Section E when a specific alert requires it.
10. Partial week data: collapsed toggle only. Never a second full table.
11. If TACoS target missing from Brand Hub: orange warning callout in Section C.
12. Inventory < 3 weeks cover: always flag as CRITICAL in the metrics table Notes / Alerts column.
13. Section C (Client Context): always a two-column table. Never prose.
14. The 30-second callout at the top must use bullet points (What happened / Why / Do today). No paragraphs of prose.
15. Symbol legend (🔴 ⚠️ ✅) must appear above the metrics table so the reader knows what each symbol means.
16. Campaign Intelligence: "Top Search Terms" are actual customer search terms from the Search Term Report, not advertiser keywords. Always label them as search terms.
17. Campaign table must show ALL campaigns with plain-language Status and Action columns. Status describes the trajectory (not just "Healthy"). Action gives one sentence on what to do or consider. Show good campaigns too — scaling opportunities matter. Separate keyword targets from ASIN targets (B0XXXXXXX) into different tables.
18. Section E (Investigation Notes): leave empty for the AM. Only include question prompts and any flagged questions. Never pre-fill answers.
19. Assignee: read the **Account Owner** property from the Brand Hub database entry. Resolve the user ID to a name using `notion-get-users`. Do NOT pull names from Sales Notes, Contact Details, or any other field. Only the Account Owner property determines the assignee.
20. Budget Pacing: always include in Section C if monthly budget is available in Brand Hub. If pacing is flagged (CRITICAL or WARNING per framework.md), also add to Section A Notes column with projected spend vs budget.
21. Trend alerts: when a metric has declined 3+ consecutive weeks, note the trend duration and cumulative decline in the Notes column, even if no single week exceeded the 10% WoW threshold.
22. Follow-up enforcement: overdue follow-ups (from "Check on" dates in previous weeks' Section F) must appear in Section D. Follow-ups 2+ weeks overdue must appear in the 30-second callout.
23. Halo Effect: show in Section B only when halo sales data exists in Metabase. Omit entirely if no halo data. A product with >20% halo is more valuable to advertise than its direct ACOS suggests — note this in the table when relevant.
