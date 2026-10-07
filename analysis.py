"""Sales Performance Analyzer — EDA, trends, and a 3-month revenue forecast."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/sales_data.csv", parse_dates=["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

# ---- core metrics ----
total_revenue = df["revenue"].sum()
total_orders = len(df)
monthly = df.groupby("month")["revenue"].sum()
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)

# YoY growth per category (2024 vs 2025)
df["year"] = df["date"].dt.year
cat_yoy = (df.groupby(["category", "year"])["revenue"].sum()
             .unstack().assign(growth=lambda d: (d[2025] - d[2024]) / d[2024] * 100)
             ["growth"].sort_values(ascending=False))

# ---- charts ----
monthly.index = pd.to_datetime(monthly.index)
plt.figure(figsize=(10, 4))
plt.plot(monthly.index, monthly.values, marker="o")
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue (Rs)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_trend.png")
plt.close()

plt.figure(figsize=(8, 4))
plt.bar(cat_rev.index, cat_rev.values)
plt.title("Revenue by Category")
plt.ylabel("Revenue (Rs)")
plt.tight_layout()
plt.savefig("charts/category_bar.png")
plt.close()

# ---- forecast: linear regression on month index ----
X = [[i] for i in range(len(monthly))]
model = LinearRegression().fit(X, monthly.values)
future = model.predict([[len(monthly) + i] for i in range(3)]).tolist()

findings = {
    "total_revenue": round(total_revenue, 2),
    "total_orders": int(total_orders),
    "avg_order_value": round(total_revenue / total_orders, 2),
    "top_category": cat_rev.index[0],
    "top_category_share_pct": round(cat_rev.iloc[0] / total_revenue * 100, 1),
    "fastest_growing_category": cat_yoy.index[0],
    "fastest_growth_pct": round(cat_yoy.iloc[0], 1),
    "top_region": region_rev.index[0],
    "best_month": monthly.idxmax().strftime("%Y-%m"),
    "best_month_revenue": round(monthly.max(), 2),
    "forecast_next_3_months": [round(v, 2) for v in future],
}
with open("findings.json", "w") as f:
    json.dump(findings, f, indent=2)

print("Analysis complete. Charts in charts/, findings in findings.json")
print(json.dumps(findings, indent=2))
