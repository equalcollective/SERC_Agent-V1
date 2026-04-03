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
