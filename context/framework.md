# Framework Reference

## Metric check thresholds

- CRITICAL: >20% negative WoW, OR hard floor breached
- WARNING: 10–20% negative WoW
- CLEARED: within normal range or improving

Hard floors:

- Buy Box %: below 90% on any active product = CRITICAL
- ROAS: below 1.0 = CRITICAL
- Campaign ACOS: above 60% = WARNING (or above break-even if COGS available from Products DB)

## Known causality chains (reference only)

These are common patterns on Amazon. Use them only when the data clearly supports a connection — do not speculate.

- Bid increased → CPC up → Spend up → TACoS up (if revenue flat or down)
- Bid decreased → CPC down → Impressions down → Sessions down → Revenue down
- Budget hitting cap → Impressions cut mid-day → Sessions drop → Revenue drop
- Listing change (image/title/price) → CTR or CVR changes → Revenue changes
- Price increase → CVR drops → Buy Box % may drop
- Buy Box % drops → CVR drops → ROAS drops → Revenue drops

## Active product definition

A product is active if: sessions > 0 in at least 2 of the last 4 weeks.
