# Amazon — Platform Context

This file gives the agent foundational knowledge about how Amazon works. Use it to reason about metric movements, causality, and recommendations.

---

## How Amazon Advertising Works

### Sponsored Products (SP)
The primary ad type. CPC (cost-per-click) auction — you bid on keywords or ASIN targets, and pay only when a shopper clicks.

- **Auto campaigns:** Amazon chooses which searches to show ads on, based on listing content. Four targeting groups: Close Match, Loose Match, Substitutes, Complements.
- **Manual campaigns:** AM chooses specific keywords or ASIN targets.
- **Match types (manual keywords only):**
  - **Broad:** Ad shows for searches containing the keyword in any order, plus related terms
  - **Phrase:** Ad shows for searches containing the keyword in order
  - **Exact:** Ad shows only for the specific keyword
- **ASIN targeting:** Target specific competitor or complementary product pages (B0XXXXXXX format). Separate from keyword targeting — different strategy, different analysis.

### Placements
Where the ad appears on Amazon:
- **Top of Search (TOS):** First row of search results. Highest CTR and CVR, highest CPC. Most competitive.
- **Rest of Search (RoS):** Below the first row. Lower CTR, lower CPC.
- **Product Pages (PP):** Ads on competitor/related product detail pages. Variable performance.
- **Placement modifiers:** AMs can bid up (e.g., +50%) for TOS to win more of that placement.

### Campaign Budget
- Daily budget per campaign. Amazon may overspend up to 25% on a given day but averages out over the month.
- **Budget capping:** When a campaign exhausts its daily budget, ads stop showing mid-day. This means impressions and clicks are cut off — sessions drop, but it looks like an organic problem if you don't check budget utilization.

---

## Key Metrics — What They Mean in Amazon Context

### Revenue & Sales
- **Total Sales (Revenue):** All product sales — organic + ad-attributed.
- **Ad Sales:** Sales attributed to ad clicks within a 7-day window.
- **Organic Sales:** Total sales minus ad sales. Revenue the brand earns without direct ad attribution.
- **Organic %:** Organic sales / total sales. Higher = less dependent on ads. A healthy brand grows organic % over time.

### Advertising Efficiency
- **ACOS (Advertising Cost of Sales):** `ad_spend / ad_sales`. Lower is better. Measures how efficiently ads convert to ad revenue. ACOS of 30% means you spend $0.30 for every $1 of ad revenue.
- **ROAS (Return on Ad Spend):** `ad_sales / ad_spend`. The inverse of ACOS. ROAS of 3.0 means $3 of ad revenue per $1 spent.
- **TACoS (Total Advertising Cost of Sales):** `ad_spend / total_sales`. The most important efficiency metric. Measures ad dependency across all revenue. Lower TACoS = more organic revenue supporting the business. TACoS rising while ACOS is stable means organic revenue is dropping.
- **CPC (Cost Per Click):** Average price paid per ad click. Rising CPC with stable performance = more competition. Rising CPC with declining orders = bid too high or targeting too broad.

### Traffic & Conversion
- **Sessions:** Unique visitors to product pages. Top-of-funnel metric. Sessions come from ads, organic search, and external traffic.
- **Impressions:** Number of times ads are shown. Impressions without clicks = CTR problem (listing/image). Impressions dropping = bid/budget/relevance problem.
- **CTR (Click-Through Rate):** `clicks / impressions`. Measures how compelling the listing appears in search results. Main drivers: main image, title, price, rating, review count.
- **CVR (Conversion Rate):** `orders / sessions`. Measures how well the listing converts visitors into buyers. Main drivers: price, images, bullets, reviews, A+ content, Buy Box %, availability.

### Buy Box
- **Buy Box %:** Percentage of page views where your offer is the "featured offer" (the Add to Cart button).
- **Only the Buy Box winner gets the sale.** If Buy Box is 70%, you are losing 30% of potential sales to other sellers (3P sellers, Amazon itself, or suppressed listing).
- **Buy Box factors:** Price (most important), fulfillment method (FBA wins over FBM), seller metrics (feedback, defect rate), inventory availability.
- **Buy Box below 90% = CRITICAL.** This is the single most damaging metric drop — every other metric (CVR, ROAS, revenue) is suppressed when Buy Box is lost.
- **Common causes:** Competitor undercuts on price, inventory stockout (Amazon suppresses your offer), 3P seller hijacking the listing, pricing error.

---

## How Organic Rank Works

Amazon's A9/A10 algorithm ranks products in search results based on:
1. **Sales velocity** — products that sell more rank higher (flywheel effect)
2. **Relevance** — listing content matching the search query
3. **Conversion rate** — products that convert well rank higher
4. **Price competitiveness** — relative to similar products
5. **Availability** — in-stock products rank higher than low-stock

### The Flywheel
`Sales velocity → higher organic rank → more impressions → more sessions → more sales → even higher rank`

This is why advertising matters beyond direct ROAS — ads generate sales velocity that improves organic rank, which generates organic sales (the "halo" of advertising on organic).

### Rank Destruction
Anything that breaks the flywheel is dangerous:
- **Stockout:** Rank drops within days. Recovery takes 2-4 weeks even after restocking. The longer the stockout, the harder the recovery.
- **Price spike:** CVR drops → sales velocity drops → rank drops.
- **Buy Box loss:** Even if you have stock, no Buy Box = no sales = rank drops.
- **Listing suppression:** Amazon can suppress listings for compliance issues, removing them from search entirely.

---

## How Inventory Affects Everything

### Amazon's Throttling Behavior
When inventory is low, Amazon actively throttles:
- **Ad impressions:** Amazon reduces ad delivery to prevent selling out and creating bad customer experience
- **Organic rank:** Low-stock products are deprioritized in organic search results
- **Buy Box:** Very low inventory can trigger Buy Box suppression

### Inventory Thresholds
- **< 3 weeks cover:** CRITICAL. Stockout imminent. Reduce ad spend immediately to extend runway. Expedite restock.
- **< 6 weeks cover:** WARNING. Plan restock. Amazon may begin throttling.
- **< 10 weeks cover:** Monitor. Restock should be in progress.
- **Stockout (0 units):** All ad spend is wasted (no conversions possible). Organic rank is collapsing. Pause campaigns immediately.

### Stockout Recovery Lag
After restocking, rank does not recover immediately:
- Days 1-7: Inventory available, but organic impressions still suppressed
- Weeks 2-3: Rank begins recovering as sales velocity rebuilds
- Weeks 3-4+: Full recovery (if the stockout was short). Longer stockouts = longer recovery.

AMs must anticipate this lag — "we restocked but revenue is still down" is expected for 2-3 weeks.

---

## Halo Effect

### What It Is
When ads on Product A lead to purchases of Product B (same brand, different product). This happens because:
- Customer clicks an ad for Product A, visits the listing
- They see Product B in "Frequently Bought Together," variations, or brand store
- They buy Product B instead of (or in addition to) Product A

### Why It Matters
- **True ACOS is lower than reported.** If Product A's ad generates $100 in direct sales and $40 in halo sales, the true ACOS is based on $140, not $100.
- **Some products are "ad magnets"** — they drive disproportionate halo sales. These products are more valuable to advertise even if their direct ACOS looks high.
- **Amazon reports this data** in the Advertised Product Report (`seven_day_advertised_sku_sales` vs `seven_day_other_sku_sales`) and the Purchased Product Report (`advertised_asin` vs `purchased_asin`).

### How to Use It
- If a product has >20% halo sales, its advertising budget should be evaluated on total sales (direct + halo), not direct alone.
- Cross-sell patterns (which products drive sales of which other products) inform campaign structure and listing optimization.

---

## Search Query Performance (SQP)

### What It Is
Brand Analytics data from Amazon showing how a brand performs on specific search queries compared to the overall market. Only available to sellers enrolled in Brand Registry.

### Key Metrics
- **Impression Share:** What % of total impressions on this query does the brand capture
- **Click Share:** What % of total clicks on this query goes to the brand
- **Cart Add Share:** What % of add-to-cart events are the brand's products
- **Purchase Share:** What % of purchases from this query are the brand's products
- **Brand CTR vs Market CTR:** Is the brand's click-through rate above or below the market average
- **Brand CVR vs Market CVR:** Is the brand's conversion rate above or below the market average

### When to Use SQP
SQP is an investigation tool, not a routine check. Use it when:
- Sessions dropped without a clear campaign cause (check if search volume dropped market-wide)
- CTR has been declining 3+ consecutive weeks (check if competitive pressure is increasing)
- Purchase share is declining while impressions are stable (competitor may be winning conversions)
- Revenue dropped but ad metrics are stable (possible competitive displacement)

SQP distinguishes "our performance dropped" from "the entire market dropped" — critical for avoiding wasted investigation.

---

## Product Lifecycle Modes

Each ASIN has a lifecycle stage that determines the appropriate advertising strategy:

- **Launch:** New product. Goal is sales velocity to establish organic rank. High ACOS is acceptable (investing in rank). Aggressive bidding, broad targeting.
- **Grow:** Established product, scaling. Moderate ACOS target. Expanding keyword coverage, testing new targets. Budget increases justified by growth.
- **Sustain:** Mature product, profitable. Tight ACOS target. Optimize for efficiency. Focus on proven keywords, reduce waste.
- **Harvest:** End-of-life or cash cow. Minimize ad spend, protect margin. Only the most efficient keywords. Let organic carry the product.

The lifecycle mode determines how to interpret metrics:
- Launch ASIN with 80% ACOS? Expected — investing in rank.
- Sustain ASIN with 80% ACOS? Problem — should be below target.
- Harvest ASIN with increasing spend? Wrong direction — should be declining.
