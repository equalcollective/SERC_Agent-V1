"""Aggregate Goal Crazy campaign, targeting, and placement data into 5 time buckets."""
import json
from collections import defaultdict
from datetime import date

PLACEMENT_FILE = "/root/.claude/projects/-home-user-SERC-Agent-V1/e96a8aa5-4cb7-4792-add7-f3be86db5270/tool-results/mcp-e00989df-60a1-4fff-95ad-85b32d554fc5-metrics_query_metrics-1776149216736.txt"

# Time buckets (Sunday-Saturday)
BUCKETS = {
    "TW":  ("2026-04-05", "2026-04-11", 1),   # This Week
    "LW":  ("2026-03-29", "2026-04-04", 1),   # Last Week
    "L4W": ("2026-03-15", "2026-04-11", 4),   # Last 4 weeks (avg)
    "L2M": ("2026-02-15", "2026-04-11", 8),   # Last 2 months (avg)
    "L3M": ("2026-01-18", "2026-04-11", 12),  # Last 3 months (total)
}


def in_bucket(d, s, e):
    return s <= d <= e


def load_placement():
    with open(PLACEMENT_FILE) as f:
        outer = json.load(f)
    inner = json.loads(outer["result"])
    return inner["results"]


# ---------- CAMPAIGN DATA (from earlier query) ----------
# 12 weeks weekly data, by campaign. Each row = (week_start, week_end, campaign, spend, sales, orders, clicks, impressions)
CAMPAIGN_ROWS = [
    ("2026-01-25","2026-01-31","Pro all",0.0,0.0,0,0,4),
    ("2026-02-01","2026-02-07","Booster All ASINs",4.73,34.95,1,14,5297),
    ("2026-02-22","2026-02-28","Pro all",7.07,0.0,0,2,473),
    ("2026-02-15","2026-02-21","Branded KWs",15.77,104.85,3,19,187),
    ("2026-02-08","2026-02-14","Booster All ASINs",4.69,0.0,0,13,2850),
    ("2026-02-15","2026-02-21","Pro all",0.0,0.0,0,0,32),
    ("2026-04-05","2026-04-11","Booster All ASINs",6.28,0.0,0,16,3992),
    ("2026-03-01","2026-03-07","Booster All ASINs",9.21,0.0,0,25,5434),
    ("2026-03-01","2026-03-07","Branded KWs",25.65,209.7,6,18,1318),
    ("2026-03-29","2026-04-04","Booster All ASINs",9.38,34.95,1,25,11104),
    ("2026-04-05","2026-04-11","Pro all",0.0,0.0,0,0,0),
    ("2026-01-25","2026-01-31","Branded KWs",8.22,34.95,1,14,187),
    ("2026-03-01","2026-03-07","Pro all",5.43,0.0,0,1,150),
    ("2026-02-08","2026-02-14","Branded KWs",23.25,139.8,4,10,141),
    ("2026-01-11","2026-01-17","Pro all",1.19,0.0,0,1,13),
    ("2026-01-18","2026-01-24","Pro all",0.0,0.0,0,0,9),
    ("2026-03-22","2026-03-28","Pro all",0.0,0.0,0,0,43),
    ("2026-03-15","2026-03-21","Booster All ASINs",10.84,34.95,1,32,4725),
    ("2026-03-08","2026-03-14","Pro all",0.0,0.0,0,0,11),
    ("2026-02-01","2026-02-07","Branded KWs",3.85,34.95,1,7,182),
    ("2026-02-08","2026-02-14","Pro all",0.0,0.0,0,0,419),
    ("2026-01-18","2026-01-24","Branded KWs",5.88,220.65,4,13,216),
    ("2026-01-11","2026-01-17","Branded KWs",32.5,173.7,6,24,572),
    ("2026-03-29","2026-04-04","Branded KWs",11.58,209.7,6,12,227),
    ("2026-03-29","2026-04-04","Pro all",0.0,0.0,0,0,19),
    ("2026-03-22","2026-03-28","Branded KWs",11.18,209.7,6,15,178),
    ("2026-03-08","2026-03-14","Branded KWs",3.06,69.9,2,6,144),
    ("2026-04-05","2026-04-11","Branded KWs",16.8,174.75,5,11,125),
    ("2026-02-15","2026-02-21","Booster All ASINs",13.18,0.0,0,35,7145),
    ("2026-03-08","2026-03-14","Booster All ASINs",10.4,34.95,1,29,6151),
    ("2026-01-18","2026-01-24","Booster All ASINs",22.57,28.95,1,60,16373),
    ("2026-03-15","2026-03-21","Pro all",0.0,0.0,0,0,28),
    ("2026-03-15","2026-03-21","Branded KWs",5.98,0.0,0,5,235),
    ("2026-01-11","2026-01-17","Booster All ASINs",29.13,28.95,1,78,9189),
    ("2026-02-22","2026-02-28","Booster All ASINs",15.1,0.0,0,41,13169),
    ("2026-02-01","2026-02-07","Pro all",0.0,0.0,0,0,2),
    ("2026-03-22","2026-03-28","Booster All ASINs",10.8,0.0,0,29,6071),
    ("2026-01-25","2026-01-31","Booster All ASINs",16.46,0.0,0,45,5024),
    ("2026-02-22","2026-02-28","Branded KWs",6.85,69.9,2,9,126),
]

CAMPAIGN_TYPE = {
    "Booster All ASINs": "Auto (SP)",
    "Branded KWs":       "Manual · Keyword (SP)",
    "Pro all":           "Manual · Keyword (SP)",
}


def agg_campaign(bucket_key):
    s, e, n_weeks = BUCKETS[bucket_key]
    agg = defaultdict(lambda: dict(spend=0.0, sales=0.0, orders=0, clicks=0, imps=0))
    for ws, we, camp, sp, sa, od, cl, im in CAMPAIGN_ROWS:
        if not in_bucket(ws, s, e):
            continue
        a = agg[camp]
        a["spend"] += sp
        a["sales"] += sa
        a["orders"] += od
        a["clicks"] += cl
        a["imps"]   += im
    out = {}
    for camp, v in agg.items():
        roas = v["sales"] / v["spend"] if v["spend"] else None
        cvr  = v["orders"] / v["clicks"] * 100 if v["clicks"] else None
        acos = v["spend"] / v["sales"] * 100 if v["sales"] else None
        out[camp] = dict(
            spend=round(v["spend"], 2),
            sales=round(v["sales"], 2),
            orders=v["orders"],
            clicks=v["clicks"],
            imps=v["imps"],
            roas=round(roas, 2) if roas is not None else None,
            cvr=round(cvr, 2) if cvr is not None else None,
            acos=round(acos, 2) if acos is not None else None,
            n_weeks=n_weeks,
        )
    return out


def agg_placement(placement_rows, bucket_key):
    s, e, n_weeks = BUCKETS[bucket_key]
    agg = defaultdict(lambda: dict(spend=0.0, sales=0.0, clicks=0, imps=0))
    for r in placement_rows:
        d = r["daily_start"]
        if not in_bucket(d, s, e):
            continue
        p = r["placement"]
        a = agg[p]
        a["spend"] += r["pl_spend"]
        a["sales"] += r["pl_sales"]
        a["clicks"] += r["pl_clicks"]
        a["imps"]   += r["pl_impressions"]
    out = {}
    for p, v in agg.items():
        roas = v["sales"] / v["spend"] if v["spend"] else None
        out[p] = dict(
            spend=round(v["spend"], 2),
            sales=round(v["sales"], 2),
            clicks=v["clicks"],
            imps=v["imps"],
            roas=round(roas, 2) if roas is not None else None,
            n_weeks=n_weeks,
        )
    return out


def totals_row(d):
    """Build totals for a bucket's campaign dict."""
    spend = sum(v["spend"] for v in d.values())
    sales = sum(v["sales"] for v in d.values())
    orders = sum(v["orders"] for v in d.values())
    clicks = sum(v["clicks"] for v in d.values())
    imps = sum(v["imps"] for v in d.values())
    roas = round(sales/spend, 2) if spend else None
    cvr = round(orders/clicks*100, 2) if clicks else None
    acos = round(spend/sales*100, 2) if sales else None
    return dict(spend=round(spend,2), sales=round(sales,2), orders=orders,
                clicks=clicks, imps=imps, roas=roas, cvr=cvr, acos=acos)


def main():
    placement_rows = load_placement()
    print(f"Loaded {len(placement_rows)} placement rows")

    result = {"buckets": {}, "placement_buckets": {}, "campaign_types": CAMPAIGN_TYPE}
    for k in BUCKETS:
        campaigns = agg_campaign(k)
        placements = agg_placement(placement_rows, k)
        result["buckets"][k] = {
            "campaigns": campaigns,
            "totals": totals_row(campaigns),
        }
        result["placement_buckets"][k] = placements

    with open("/tmp/goal_crazy_agg.json", "w") as f:
        json.dump(result, f, indent=2)

    # Pretty print
    print("\n=== CAMPAIGN TOTALS ===")
    for k in ["TW","LW","L4W","L2M","L3M"]:
        t = result["buckets"][k]["totals"]
        n = BUCKETS[k][2]
        avg_spend = round(t["spend"]/n, 2)
        avg_sales = round(t["sales"]/n, 2)
        print(f"{k:4s} ({n}w) | spend={t['spend']:>7.2f} (avg/wk {avg_spend:>6.2f}) | sales={t['sales']:>7.2f} (avg/wk {avg_sales:>6.2f}) | roas={t['roas']} | cvr={t['cvr']} | acos={t['acos']}")

    print("\n=== PER CAMPAIGN BY BUCKET (spend / sales / roas) ===")
    camps = sorted({c for k in BUCKETS for c in result["buckets"][k]["campaigns"]})
    for c in camps:
        print(f"\n-- {c} [{CAMPAIGN_TYPE.get(c,'?')}]")
        for k in ["TW","LW","L4W","L2M","L3M"]:
            v = result["buckets"][k]["campaigns"].get(c)
            if v:
                n = BUCKETS[k][2]
                avg_s = round(v["spend"]/n,2)
                print(f"  {k:4s} spend={v['spend']:>7.2f} (avg/wk {avg_s:>6.2f}) sales={v['sales']:>7.2f} roas={v['roas']} cvr={v['cvr']} acos={v['acos']}")

    print("\n=== PLACEMENTS BY BUCKET ===")
    placements = sorted({p for k in BUCKETS for p in result["placement_buckets"][k]})
    for p in placements:
        print(f"\n-- {p}")
        for k in ["TW","LW","L4W","L2M","L3M"]:
            v = result["placement_buckets"][k].get(p)
            if v:
                n = BUCKETS[k][2]
                avg_s = round(v["spend"]/n,2)
                print(f"  {k:4s} spend={v['spend']:>7.2f} (avg/wk {avg_s:>6.2f}) sales={v['sales']:>7.2f} roas={v['roas']}")


if __name__ == "__main__":
    main()
