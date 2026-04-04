# Framework Reference

## Metric check thresholds

- CRITICAL: >20% negative WoW, OR hard floor breached
- WARNING: 10-20% negative WoW, OR 3+ consecutive weeks of decline
- CLEARED: within normal range or improving

Hard floors:

- Buy Box %: below 90% on any active product = CRITICAL
- ROAS: below 1.0 on any active product = CRITICAL
- Inventory: below 3 weeks of cover = CRITICAL
- Campaign ACOS: above 60% = WARNING (or above break-even if COGS available)

## Known causality chains

When a metric moves, check these chains first:

- Bid increased → CPC up → Spend up → TACoS up (if revenue flat or down)
- Bid decreased → CPC down → Impressions down → Sessions down → Revenue down
- Budget increased → More impressions → More clicks → More orders
- Budget hitting cap → Impressions cut mid-day → Sessions drop → Revenue drop
- New keyword added → Spend up on that term → ACOS changes based on keyword quality
- Negative added → Spend drops on that term → Sessions drop slightly → ACOS improves
- Listing change (image/title/price) → CTR or CVR changes → Revenue changes
- Price increase → CVR drops → Buy Box % may drop
- Price decrease → CVR improves → Buy Box may improve
- Low inventory (<3 weeks) → Amazon throttles ad impressions → Sessions drop organically
- Buy Box % drops → CVR drops → ROAS drops → Revenue drops
- Placement modifier change → ACOS shifts between TOS and other placements
- Budget exhaustion → MTD spend >90% of budget before month 80% elapsed → campaigns will run out of budget before month end → impressions and sessions drop in final week
- Inventory-advertising loop → Inventory <6 weeks → Amazon throttles ad impressions and organic rank → Organic % drops → TACoS rises (even without ad changes)
- Stockout recovery lag → Inventory was CRITICAL 2-4 weeks ago, now restocked → organic rank still suppressed → sessions/revenue may take 2-3 weeks to recover
- Unexplained session drop → Sessions down + no bid/budget/keyword changes → possible market shift or competitive displacement → flag SQP investigation in Section E
- Unexplained CVR drop → CVR down + no listing/price/Buy Box changes → check reviews/ratings for changes, or flag SQP investigation (possible new competitor)
- CPC rising, impressions stable → more advertisers competing in the auction → not necessarily losing share, but cost of traffic is increasing
- Halo effect shift → Direct ACOS looks worse but total sales (direct + other SKU) are up → check Advertised Product Report for halo sales before cutting spend

## Trend-based alerts

In addition to WoW thresholds, check for multi-week patterns:

- 3+ consecutive weeks decline on any metric → WARNING regardless of individual WoW change (a 5%/week decline for 4 weeks = 19% total, but each week is below the 10% WoW threshold)
- Accelerating decline (each week's drop is worse than the prior week) → CRITICAL if total cumulative decline exceeds 15%
- Expected reversion not materializing → if an AM action was taken 2+ weeks ago and the metric has not responded as expected → WARNING with specific follow-up

When flagging trend alerts, always state the trend duration and cumulative impact: "Sessions declining 3 consecutive weeks: -4%, -6%, -8% (cumulative -17%)."

## Follow-up escalation

When loading AM action history (Step 2), extract "Check on" dates from Section F:

- Due this week → surface in Section D with the original action context
- 1 week overdue → WARNING in Section D: "Follow-up from [date] has not been addressed: [action description]"
- 2+ weeks overdue → CRITICAL in 30-second callout: "OVERDUE: [action] was expected to be checked on [date], now [N] days overdue"

## Budget pacing thresholds

When monthly ad budget is available from Brand Hub:

- Calculate MTD spend (sum daily ad_spend from month start to check week end)
- Calculate projected monthly spend (MTD spend / days elapsed * days in month)
- CRITICAL: projected spend > 115% of budget OR < 70% of budget
- WARNING: projected spend > 105% of budget OR < 80% of budget

## Active product definition

A product is active if: sessions > 0 in at least 2 of the last 4 weeks.
If a product does not meet this: skip from all tables. Add count below product table.

## Negatives reminder trigger

If any search term has spend > $10 AND 0 orders in the last 14 days:
Add reminder below Section B: "⚠️ Run negatives this week — [N] wasted terms found."
AM runs: run_negatives --brand "[name]" --lookback 14

## Inventory warning triggers

- < 3 weeks cover: CRITICAL — recommend reducing ad spend to avoid stockout before restock
- < 6 weeks cover: WARNING — notify AM to coordinate restock
