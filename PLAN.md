# Online Orders Dashboard — Section 1 Plan

**Dataset:** `online_orders.csv` (E-commerce 1) — 3,548 orders from an online shop, Jan 1 – Dec 31, 2025.

## Step 1 — Three purposes of a dashboard

1. **Monitor** — show the current state of key numbers (revenue, orders, returns) at a glance.
2. **Compare and spot patterns** — reveal trends, peaks and differences between groups (months, categories, regions).
3. **Support decisions** — answer specific questions quickly so someone can act (e.g. plan stock, change discount policy).

## Step 2 — Goal and audience

- **Goal:** Help the shop's sales manager see when and where revenue comes from, which categories cause returns, and whether discounts pay off.
- **Audience:** The sales/marketing manager, checking it **weekly** (and before planning seasonal promotions).

## Step 3 — Key questions

| # | Question | Columns | Chart |
|---|----------|---------|-------|
| 1 | How do sales change across the year (holiday and July sale peaks)? | `order_date`, `revenue`, `order_id` | Line chart of monthly revenue (USD), with points and hover tooltips |
| 2 | Which category earns the most, and which has the most returns? | `category`, `revenue`, `returned` | Two labeled bar charts: revenue by category (USD) and return rate by category (%) |
| 3 | Do discounts bring bigger orders? | `discount_pct`, `units`, `revenue` | Bar chart of average units and average order value (USD) per discount level |
| 4 | Do returned orders get lower ratings? | `returned`, `rating_1to5` | Bar chart of average rating, returned vs kept |

## Step 4 — Wireframe

See `wireframe.svg` (open it in a browser and screenshot it for submission).

- **Sidebar filters**
  - `st.date_input` → `order_date` (date range)
  - `st.multiselect` → `category`
  - `st.multiselect` → `region`
  - `st.multiselect` → `device`
  - `st.radio` → `customer_type` (All / New / Returning)
- **Main area**
  - KPI row (`st.metric` ×5): Total revenue (USD), Orders, Avg order value (USD), Return rate (%), Avg rating (1–5)
  - Row 1: Monthly revenue line chart (Q1), full width
  - Row 2: Revenue by category bar | Return rate by category bar (Q2)
  - Row 3: Discount vs order size bars (Q3) | Rating: returned vs kept bar (Q4)
  - Insights panel: 4 takeaway sentences with numbers, one per question
  - Expander: raw filtered data + data notes

## Step 5 — Gallery walk votes

i had to leave for work at 1:30 that day, so i wasn't able to do this part
