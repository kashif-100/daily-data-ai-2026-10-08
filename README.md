# Day 1 — Sales Performance Analyzer 📊

Data-analyst project with an AI insights layer. Part of a 15-day daily series:
one data + AI project every day.

## What it does
1. **`generate_data.py`** — creates 2 years of synthetic e-commerce sales
   (54,787 orders across 4 categories × 4 regions, seeded).
2. **`analysis.py`** — pandas EDA: monthly revenue trend, category/region
   breakdowns, year-on-year growth, plus a scikit-learn linear-regression
   forecast of the next 3 months. Saves charts to `charts/`.
3. **`ai_insights.py`** — the AI layer: converts the computed statistics into
   a plain-English narrative report (`AI_INSIGHTS.md`) with findings and
   recommended actions. No human needed to read the spreadsheets.

## Headline findings
- **Rs 33.2 Cr** total revenue across **54,787 orders** (avg order Rs 6,068)
- **Electronics** drives 46.3% of revenue and grows fastest (+26.8% YoY)
- **East** is the top region; peak month was **2025-10** (festive season)
- Forecast: revenue keeps climbing over the next 3 months

## How to run
```bash
pip install -r requirements.txt
python generate_data.py
python analysis.py
python ai_insights.py
```

## Files
| File | Purpose |
|---|---|
| `generate_data.py` | Synthetic sales data generator |
| `data/sales_data.csv` | Generated dataset |
| `analysis.py` | EDA + charts + forecast → `findings.json` |
| `ai_insights.py` | Auto-generated narrative report → `AI_INSIGHTS.md` |
| `charts/` | Monthly trend & category charts |
| `findings.json` | Machine-readable results |
