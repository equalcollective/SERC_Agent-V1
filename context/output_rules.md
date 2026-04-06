# Output Rules — Always Apply

1. Never invent numbers. Only use data from MCPs.
2. Every CRITICAL or WARNING metric must have actual numbers in the Notes / Alerts column.
3. Only add a cause or suggestion in Notes / Alerts if confident based on visible data. If not confident, just state the movement — the AM will investigate.
4. No framework labels in the output. No R1/R2/R3. Plain language only.
5. Alerts live inside the Metrics & Alerts table (Notes / Alerts column). There is no separate Alerts section.
6. Campaigns section: show ALL campaigns with key metrics and WoW changes. Flag with 🔴/⚠️/✅.
7. Context section: always a two-column table. Never prose.
8. Last Week section: reproduce the actions taken and alerts from the prior check.
9. The 30-second callout must use bullet points (What happened / Why if clear / Watch). "Why" only if confident — omit the line entirely if uncertain.
10. Symbol legend (🔴 ⚠️ ✅) must appear above the Metrics & Alerts table.
11. If TACoS target missing: warning flag in the Context section.
12. Assignee: read the **Account Owner** property from Brands DB. Resolve the user ID to a name using `notion-get-users`. Only the Account Owner property determines the assignee.
13. Investigation section: always present but left empty. It is a placeholder for the AM or future investigation procedure.
14. Actions & Follow-ups section: always present as an empty table for the AM to fill in.
