# Interview Notes — Day 1: Sales Performance Analyzer 🎤

Read this before any interview. Every answer below is grounded in what this
project *actually* does — never bluff beyond it.

## 30-second pitch
"I built a sales analytics pipeline on two years of e-commerce data — about
55,000 orders. It does EDA with pandas, visualizes monthly trends and category
breakdowns, forecasts revenue three months out with linear regression, and then
an AI insights module auto-generates a plain-English report with findings and
business recommendations."

## Project walkthrough
**Q: Walk me through the project end to end.**
A: "Three scripts. `generate_data.py` creates seeded synthetic sales data —
four categories, four regions, two years, with realistic seasonality like a
festive-season spike. `analysis.py` loads it with pandas, computes KPIs,
monthly trends, YoY growth per category, plots two charts, and fits a linear
regression on the month index to forecast three months ahead. Everything lands
in `findings.json`. Then `ai_insights.py` reads that JSON and writes a
narrative report — the top category, fastest grower, best region, forecast,
and recommended actions."

**Q: Why synthetic data?**
A: "For a portfolio project it keeps everything reproducible — fixed seed, no
external dependencies. In production I'd swap in real transaction exports; the
pipeline itself wouldn't change, only the loader."

## Python / pandas
**Q: How did you compute the monthly trend?**
A: "Parsed dates with `parse_dates`, derived a month period column with the
`.dt` accessor, then `groupby('month')['revenue'].sum()`. All vectorized —
no Python loops over rows."

**Q: How did you compute year-on-year growth per category?**
A: "Grouped by category and year, unstacked years into columns, then
`(2025 − 2024) / 2024 × 100`. Electronics came out at +26.8%."

**Q: Why pandas instead of pure Python or SQL?**
A: "Vectorized operations over 55k rows run in milliseconds, and the
groupby/reshaping API maps directly onto analyst questions. For larger-than-
memory data I'd reach for SQL or chunked processing."

## Machine learning
**Q: Why linear regression for the forecast?**
A: "It's the right *baseline*: the monthly series has a clear upward trend,
and linear regression captures that with one feature and zero tuning. Every
forecasting project should start with a dumb baseline before trying anything
fancy — otherwise you can't tell if complexity is helping."

**Q: What are its limitations here?**
A: "Three honest ones. First, it assumes the trend is linear forever — it
can't model the festive-season spikes you can see in the chart. Second, I
didn't do a train/test split, so there's no measured out-of-sample error.
Third, one feature (time index) means it can't use any real drivers like
marketing spend."

**Q: How would you evaluate the forecast properly?**
A: "Walk-forward validation: train on the first N months, predict month N+1,
roll forward, and average the error. Metrics: MAE for interpretability, RMSE
if large misses hurt more, MAPE for percentage terms."

**Q: How would you improve it?**
A: "Add seasonal features — month dummies or Fourier terms — so the model can
learn the October/November spike. Then try SARIMA or Prophet, which handle
trend + seasonality natively, and compare against the linear baseline on
walk-forward MAE. More data and real drivers like promotions would help most."

**Q: Any overfitting risk?**
A: "Very low here — one feature, 24 monthly points, a linear model can't
memorize much. Overfitting becomes the real concern the moment I add dozens
of seasonal dummies or switch to gradient boosting; that's when I'd add
regularization and proper validation."

## Data analyst thinking
**Q: What KPIs did you track and why?**
A: "Total revenue, order count, average order value — the health trio. Then
category share to see concentration risk, YoY growth per category for momentum,
and best month/region to find what's working."

**Q: What was the key insight?**
A: "Electronics is 46% of revenue AND the fastest grower at +26.8% YoY —
concentration and momentum in the same category. That's both the biggest
opportunity and the biggest risk, and it drove the inventory recommendation."

**Q: How did analysis become recommendations?**
A: "Each recommendation traces to a finding: stock up before October because
the data shows a festive spike; push Electronics inventory because it's the
fastest grower; copy the East region's playbook because it leads. Analysis
without a 'so what' is just arithmetic."

## The "AI integrated" part
**Q: What does AI-integrated mean in this project?**
A: "Two layers. The ML layer is the regression forecast — the machine learns
the trend from data instead of me hardcoding it. The second layer is automated
narrative generation: `ai_insights.py` turns computed statistics into a
readable report with findings and actions. It's template-based NLG — honest,
deterministic, no API key needed."

**Q: Why not use an LLM API for the report?**
A: "Trade-offs. Templates are deterministic, free, and reproducible — the
numbers in the report always match `findings.json` exactly. An LLM would write
more fluently but could hallucinate numbers. For a v2, I'd use an LLM with the
JSON injected as context and a strict 'only use these numbers' instruction."

## With more time, I would…
- Validate with walk-forward MAE/RMSE instead of shipping an unevaluated forecast
- Add seasonal modeling (SARIMA or Prophet) and beat the linear baseline
- Build a Streamlit dashboard so a non-technical user can filter by category/region
- Plug in a real dataset via the same loader interface
