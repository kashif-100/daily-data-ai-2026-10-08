"""AI Insights — turns the analysis findings into a plain-English report.

This is the 'AI integrated' layer: instead of a human reading spreadsheets,
the pipeline converts computed statistics into narrative insights and
recommendations automatically.
"""
import json

with open("findings.json") as f:
    d = json.load(f)

report = f"""# AI-Generated Sales Insights Report

## Executive summary
Over the analysis period the store processed **{d['total_orders']:,} orders**
worth **Rs {d['total_revenue']:,.0f}**, at an average order value of
**Rs {d['avg_order_value']:,.0f}**.

## Key findings
1. **{d['top_category']} is the revenue engine** — it contributes
   {d['top_category_share_pct']}% of total revenue. Marketing spend should
   skew toward this category.
2. **{d['fastest_growing_category']} is accelerating fastest** at
   +{d['fastest_growth_pct']}% year-on-year. This is where assortment
   expansion will pay off most.
3. **{d['top_region']} leads all regions.** Replicate its pricing and
   promotion playbook in lagging regions.
4. **Peak month was {d['best_month']}** (Rs {d['best_month_revenue']:,.0f}) —
   festive-season demand is real; stock up 6–8 weeks before October.

## Forecast (next 3 months)
Rs {d['forecast_next_3_months'][0]:,.0f} → Rs {d['forecast_next_3_months'][1]:,.0f} → Rs {d['forecast_next_3_months'][2]:,.0f}.
The trend model projects continued growth — plan inventory accordingly.

## Recommended actions
- Increase {d['fastest_growing_category']} inventory by ~20% ahead of the festive quarter.
- Run a targeted campaign in non-{d['top_region']} regions using {d['top_region']}'s winning creatives.
- Protect average order value with bundles in {d['top_category']}, the highest-share category.

*Report generated automatically by ai_insights.py — Day 1 of 15, daily-data-ai series.*
"""

with open("AI_INSIGHTS.md", "w") as f:
    f.write(report)

print(report)
