# Alert Framework V1

## Alert Metrics (Tier 1 — generate alerts)

These 6 metrics are checked every week. Use judgment to flag — no rigid percentage thresholds. Compare WoW, compare to 4-week average, consider the brand's context.

### Revenue
- Data: `br_total_sales`
- Why: the ultimate business outcome. If revenue drops and nobody notices, nothing else matters.
- Flag when: significant decline WoW, especially if also below 4wk avg. Also flag significant growth.

### TACoS
- Data: `cr_tacos_pct`
- Why: TACoS connects ad spend to total revenue. Rising TACoS means ads are eating a bigger share of sales.
- Flag when: significant increase WoW, or sustained multi-week rise. Also flag if TACoS is meaningfully above 4wk avg.
- Always show WoW direction and vs 4wk avg

### Organic %
- Data: `cr_organic_pct`
- Why: answers "is the brand building equity or renting traffic?" Declining organic % = ad dependency.
- Flag when: meaningful drop in percentage points WoW, or sustained multi-week decline. Below 30% and declining = serious.

### Buy Box %
- Data: `br_featured_offer_pct`
- Why: losing Buy Box is the most destructive event for a listing. Everything collapses.
- Hard floor: below 90% = always flag (Amazon platform reality)
- Also flag: significant drop WoW even if still above 90%

### CVR
- Data: `br_cvr_pct`
- Why: the conversion bottleneck. If traffic is fine but CVR drops, the listing is failing.
- Flag when: notable drop WoW, especially if combined with being below 4wk avg.

### Sessions
- Data: `br_sessions`
- Why: sessions = traffic. Drop in sessions means fewer people are seeing the product.
- Flag when: significant drop WoW, especially if also below 4wk avg.

---

## Context Metrics (Tier 2 — show, no alerts)

Ad Spend, CPC, Impressions, CTR, ACOS, ROAS

Show this week vs last week. No notes, no alerts. These are for AM reference.

---

## Campaign Alerts (2-check model)

For each campaign, run 2 independent checks:

1. **Spend efficiency**: Spend up significantly but orders flat or down? Flag.
2. **Direction**: ACOS worsening WoW? Flag.

Status per campaign: ⚠️ if either check fires, ✅ if neither fires.

---

## AM Actions

Read last week's Actions & Follow-ups from Tasks DB. Note what the AM did. No connection analysis — just record what was done for context.

---

## Missing Data

- No prior Account Check → "First check for this brand." Skip last week section.
- Metric returns null → show as-is, do not alert, flag "Data unavailable"
