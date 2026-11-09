# Online Orders 2025 — Streamlit Dashboard

Interactive dashboard for `data/online_orders.csv` (synthetic 2025 orders from an online shop).
It answers four questions for a sales manager:

1. How do sales change across the year?
2. Which category earns the most, and which has the most returns?
3. Do discounts bring bigger orders?
4. Do returned orders get lower ratings?

**Live app:** https://lab43adamlong-8epbkoaccqletvg2sqwn4n.streamlit.app/

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files

| File | Purpose |
|------|---------|
| `app.py` | The dashboard (sections: load, filters, KPIs, charts, insights, data notes) |
| `data/online_orders.csv` | Dataset |
| `requirements.txt` | streamlit, pandas, altair |
| `PLAN.md` | Section 1 plan: goal, audience, questions, wireframe notes |
| `wireframe.svg` | Section 1 wireframe |

## Data handling

The file has no blank values, but the app drops any row with a blank field before charting and
reports how many rows were dropped (in the "About the data" expander).
