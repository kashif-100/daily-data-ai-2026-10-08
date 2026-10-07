"""Generate synthetic e-commerce sales data (2 years, seeded for reproducibility)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

categories = ["Electronics", "Clothing", "Home", "Sports"]
regions = ["North", "South", "East", "West"]
base_price = {"Electronics": 4500, "Clothing": 1200, "Home": 2800, "Sports": 1800}
# category growth trend per year (Electronics grows fastest)
growth = {"Electronics": 0.28, "Clothing": 0.10, "Home": 0.16, "Sports": 0.20}

rows = []
order_id = 1000
for day in pd.date_range("2024-01-01", "2025-12-31", freq="D"):
    # festive-season bump in Oct/Nov, dip in Feb
    seasonal = 1 + 0.45 * (day.month in (10, 11)) - 0.25 * (day.month == 2)
    weekend = 1.25 if day.dayofweek >= 5 else 1.0
    for cat in categories:
        year_frac = (day - pd.Timestamp("2024-01-01")).days / 365
        lam = 14 * (1 + growth[cat] * year_frac) * seasonal * weekend
        n_orders = rng.poisson(lam)
        for _ in range(n_orders):
            qty = int(rng.integers(1, 4))
            price = base_price[cat] * rng.uniform(0.7, 1.6)
            rows.append({
                "order_id": order_id,
                "date": day.date().isoformat(),
                "category": cat,
                "region": rng.choice(regions),
                "quantity": qty,
                "unit_price": round(price, 2),
                "revenue": round(qty * price, 2),
            })
            order_id += 1

df = pd.DataFrame(rows)
df.to_csv("data/sales_data.csv", index=False)
print(f"Wrote {len(df):,} orders to data/sales_data.csv")
