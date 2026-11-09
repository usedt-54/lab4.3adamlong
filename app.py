"""
Online Orders 2025 — Streamlit dashboard (Mini Project, Section 2).

Data: data/online_orders.csv (synthetic, generated for class).
Run locally with:  streamlit run app.py
"""
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "online_orders.csv"
BAR_COLOR = "#2b6cb0"  # one color for all bars; meaning comes from labels, not color

# ---------------------------------------------------------------------------
# 1. PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Online Orders Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# 2. LOAD DATA (cached: the script reruns on every widget change)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data(path: Path) -> tuple[pd.DataFrame, int]:
    """Read the CSV, parse dates, and drop rows with blank values.

    Returns the clean DataFrame and how many rows were dropped, so the
    page can report it in a caption.
    """
    raw = pd.read_csv(path, parse_dates=["order_date"])
    clean = raw.dropna()
    clean = clean.assign(
        month=clean["order_date"].dt.to_period("M").dt.to_timestamp(),
        is_returned=clean["returned"].eq("Yes"),
        # 0.1 -> "10%" for readable axis labels
        discount_label=(clean["discount_pct"] * 100).round().astype(int).astype(str) + "%",
    )
    return clean, len(raw) - len(clean)


df, n_dropped = load_data(DATA_PATH)


# ---------------------------------------------------------------------------
# 3. SIDEBAR FILTERS
# ---------------------------------------------------------------------------
def sidebar_filters(data: pd.DataFrame) -> pd.DataFrame:
    """Draw the sidebar widgets and return the rows that match them."""
    with st.sidebar:
        st.title("🛒 Filters")

        min_d, max_d = data["order_date"].min().date(), data["order_date"].max().date()
        date_range = st.date_input(
            "Order date range", value=(min_d, max_d), min_value=min_d, max_value=max_d
        )
        categories = st.multiselect(
            "Category", sorted(data["category"].unique()), default=sorted(data["category"].unique())
        )
        regions = st.multiselect(
            "Region", sorted(data["region"].unique()), default=sorted(data["region"].unique())
        )
        devices = st.multiselect(
            "Device", sorted(data["device"].unique()), default=sorted(data["device"].unique())
        )
        customer = st.radio("Customer type", ["All", "New", "Returning"], horizontal=True)

    # While the user is mid-way through picking a range, date_input returns
    # only the start date; treat that as a one-day range until they finish.
    if isinstance(date_range, (tuple, list)):
        start = date_range[0]
        end = date_range[1] if len(date_range) > 1 else date_range[0]
    else:
        start = end = date_range

    mask = (
        data["order_date"].dt.date.between(start, end)
        & data["category"].isin(categories)
        & data["region"].isin(regions)
        & data["device"].isin(devices)
    )
    if customer != "All":
        mask &= data["customer_type"].eq(customer)
    return data[mask]


filtered = sidebar_filters(df)

st.title("🛒 Online Orders 2025")
st.caption(
    "For the sales manager: where revenue comes from, which categories get returned, "
    "and whether discounts pay off. Use the sidebar to filter."
)

if filtered.empty:
    st.warning("No orders match these filters. Widen the date range or select at least one option in each list.")
    st.stop()


# ---------------------------------------------------------------------------
# 4. KPI ROW
# ---------------------------------------------------------------------------
def show_kpis(data: pd.DataFrame) -> None:
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total revenue", f"${data['revenue'].sum():,.0f}")
    k2.metric("Orders", f"{len(data):,}")
    k3.metric("Avg order value", f"${data['revenue'].mean():,.2f}")
    k4.metric("Return rate", f"{data['is_returned'].mean():.1%}")
    k5.metric("Avg rating", f"{data['rating_1to5'].mean():.2f} / 5")


show_kpis(filtered)


# ---------------------------------------------------------------------------
# 5. CHARTS
# ---------------------------------------------------------------------------
def labeled_bars(data, x, y, x_title, y_title, y_format, tooltip, sort=None, y_domain=None):
    """Single-color bar chart with the value printed above each bar."""
    scale = alt.Scale(domain=y_domain) if y_domain else alt.Undefined
    base = alt.Chart(data).encode(
        x=alt.X(x, title=x_title, sort=sort, axis=alt.Axis(labelAngle=0, labelFontSize=13, titleFontSize=13)),
        y=alt.Y(y, title=y_title, scale=scale, axis=alt.Axis(format=y_format, labelFontSize=12, titleFontSize=13)),
        tooltip=tooltip,
    )
    bars = base.mark_bar(color=BAR_COLOR)
    # White label just inside the top of each bar: readable in light and dark themes.
    text = base.mark_text(baseline="top", dy=6, fontSize=13, fontWeight="bold", color="white").encode(
        text=alt.Text(y, format=y_format)
    )
    return (bars + text).properties(height=300)


# --- Q1: monthly revenue trend (interactive: hover + scroll-zoom/drag-pan) ---
monthly = filtered.groupby("month", as_index=False).agg(
    revenue=("revenue", "sum"), orders=("order_id", "count")
)
st.subheader("1. How do sales change across the year?")
line = (
    alt.Chart(monthly)
    .mark_line(point=alt.OverlayMarkDef(size=70), color=BAR_COLOR, strokeWidth=3)
    .encode(
        x=alt.X("month:T", title="Month (2025)", scale=alt.Scale(padding=20), axis=alt.Axis(format="%b", labelFontSize=13, titleFontSize=13)),
        y=alt.Y("revenue:Q", title="Revenue (USD)", axis=alt.Axis(format="$,.0f", labelFontSize=12, titleFontSize=13)),
        tooltip=[
            alt.Tooltip("month:T", title="Month", format="%B %Y"),
            alt.Tooltip("revenue:Q", title="Revenue (USD)", format="$,.0f"),
            alt.Tooltip("orders:Q", title="Orders", format=","),
        ],
    )
    .properties(height=320)
    .interactive()  # scroll to zoom, drag to pan, double-click to reset
)
st.altair_chart(line, width="stretch")
st.caption(
    "Line chart of total revenue (USD) per month for the filtered orders. "
    "Hover a point to see revenue and order count; scroll to zoom, double-click to reset."
)

# --- Q2: category revenue and return rate ---
by_cat = (
    filtered.groupby("category", as_index=False)
    .agg(revenue=("revenue", "sum"), orders=("order_id", "count"), return_rate=("is_returned", "mean"))
    .sort_values("revenue", ascending=False)
)
cat_order = by_cat["category"].tolist()  # same category order in both charts

st.subheader("2. Which category earns the most, and which has the most returns?")
c1, c2 = st.columns(2, gap="medium")
with c1:
    st.altair_chart(
        labeled_bars(
            by_cat, "category:N", "revenue:Q", "Category", "Revenue (USD)", "$,.0f",
            [alt.Tooltip("category:N", title="Category"),
             alt.Tooltip("revenue:Q", title="Revenue (USD)", format="$,.0f"),
             alt.Tooltip("orders:Q", title="Orders", format=",")],
            sort=cat_order,
        ),
        width="stretch",
    )
    st.caption("Bar chart of total revenue (USD) by product category, highest first. Values are printed on each bar.")
with c2:
    st.altair_chart(
        labeled_bars(
            by_cat, "category:N", "return_rate:Q", "Category", "Orders returned (%)", ".1%",
            [alt.Tooltip("category:N", title="Category"),
             alt.Tooltip("return_rate:Q", title="Return rate", format=".1%"),
             alt.Tooltip("orders:Q", title="Orders", format=",")],
            sort=cat_order,
        ),
        width="stretch",
    )
    st.caption("Bar chart of the share of orders returned in each category (%). Same category order as the revenue chart.")

# --- Q3 and Q4 side by side ---
by_disc = filtered.groupby("discount_label", as_index=False).agg(
    avg_order=("revenue", "mean"), avg_units=("units", "mean"), orders=("order_id", "count"),
    pct=("discount_pct", "first"),
).sort_values("pct")

by_ret = filtered.groupby("returned", as_index=False).agg(
    avg_rating=("rating_1to5", "mean"), orders=("order_id", "count")
)
by_ret["status"] = by_ret["returned"].map({"Yes": "Returned", "No": "Kept"})

c3, c4 = st.columns(2, gap="medium")
with c3:
    st.subheader("3. Do discounts bring bigger orders?")
    st.altair_chart(
        labeled_bars(
            by_disc, "discount_label:N", "avg_order:Q", "Discount", "Average order value (USD)", "$,.2f",
            [alt.Tooltip("discount_label:N", title="Discount"),
             alt.Tooltip("avg_order:Q", title="Avg order value (USD)", format="$,.2f"),
             alt.Tooltip("avg_units:Q", title="Avg units per order", format=".2f"),
             alt.Tooltip("orders:Q", title="Orders", format=",")],
            sort=by_disc["discount_label"].tolist(),
        ),
        width="stretch",
    )
    st.caption("Bar chart of average order value (USD) at each discount level. Hover a bar to see average units per order.")
with c4:
    st.subheader("4. Do returned orders get lower ratings?")
    st.altair_chart(
        labeled_bars(
            by_ret, "status:N", "avg_rating:Q", "Order outcome", "Average rating (1–5 stars)", ".2f",
            [alt.Tooltip("status:N", title="Outcome"),
             alt.Tooltip("avg_rating:Q", title="Avg rating", format=".2f"),
             alt.Tooltip("orders:Q", title="Orders", format=",")],
            sort=["Kept", "Returned"],
            y_domain=[0, 5],  # full 1–5 scale so the gap isn't visually exaggerated
        ),
        width="stretch",
    )
    st.caption("Bar chart of the average customer rating (1–5) for orders that were kept versus returned.")


# ---------------------------------------------------------------------------
# 6. INSIGHTS (computed from the filtered data, so they update with filters)
# ---------------------------------------------------------------------------
def build_insights() -> list[str]:
    notes = []

    # Q1: peak month vs the typical month
    peak = monthly.loc[monthly["revenue"].idxmax()]
    if len(monthly) > 1:
        median = monthly["revenue"].median()
        notes.append(
            f"**Seasonality:** {peak['month']:%B} is the peak month with ${peak['revenue']:,.0f} "
            f"in revenue from {peak['orders']:,} orders, {peak['revenue'] / median - 1:.0%} above "
            f"the median month (${median:,.0f})."
        )
    else:
        notes.append(f"**Seasonality:** only {peak['month']:%B} is selected (${peak['revenue']:,.0f}); widen the date range to compare months.")

    # Q2: top earner and most-returned category
    top = by_cat.iloc[0]
    worst = by_cat.loc[by_cat["return_rate"].idxmax()]
    share = top["revenue"] / by_cat["revenue"].sum()
    notes.append(
        f"**Categories:** {top['category']} earns the most (${top['revenue']:,.0f}, {share:.0%} of revenue). "
        f"{worst['category']} has the highest return rate at {worst['return_rate']:.1%} of its orders."
    )

    # Q3: compare no discount with the deepest discount present
    if len(by_disc) > 1:
        lo, hi = by_disc.iloc[0], by_disc.iloc[-1]
        # Treat a change of under 5% in units per order as "no real change".
        unit_change = hi["avg_units"] / lo["avg_units"] - 1
        if abs(unit_change) < 0.05:
            verdict = "units per order barely move, so discounts are not bringing bigger orders"
        elif unit_change > 0:
            verdict = f"customers buy {unit_change:.0%} more units per order, so deeper discounts do grow basket size"
        else:
            verdict = f"customers buy {-unit_change:.0%} fewer units per order"
        notes.append(
            f"**Discounts:** orders at {hi['discount_label']} off average ${hi['avg_order']:,.2f} versus "
            f"${lo['avg_order']:,.2f} at {lo['discount_label']}; {verdict} "
            f"({hi['avg_units']:.2f} vs {lo['avg_units']:.2f} units)."
        )
    else:
        notes.append("**Discounts:** only one discount level is in the filtered data, so there is nothing to compare.")

    # Q4: rating gap between returned and kept orders
    r = by_ret.set_index("status")["avg_rating"]
    if {"Kept", "Returned"} <= set(r.index):
        notes.append(
            f"**Ratings:** returned orders average {r['Returned']:.2f} stars versus {r['Kept']:.2f} for kept "
            f"orders, a gap of {r['Kept'] - r['Returned']:.2f} stars."
        )
    else:
        notes.append("**Ratings:** the filtered orders are all kept or all returned, so there is no rating gap to compare.")
    return notes


st.subheader("💡 Insights")
with st.container(border=True):
    for line_text in build_insights():
        # Escape "$" so Streamlit doesn't read "$...$" pairs as LaTeX math.
        st.markdown("- " + line_text.replace("$", r"\$"))
    st.caption("These sentences are calculated from the filtered data and update when you change the filters.")


# ---------------------------------------------------------------------------
# 7. DATA NOTES AND RAW DATA
# ---------------------------------------------------------------------------
with st.expander("About the data and raw rows"):
    st.caption(
        f"Source: data/online_orders.csv, synthetic orders generated for class (Jan–Dec 2025). "
        f"Blank values: rows with any blank field are dropped before charting; "
        f"{n_dropped} row(s) were dropped from this file. "
        f"Revenue = units × unit price × (1 − discount), in USD."
    )
    st.dataframe(
        filtered.drop(columns=["month", "is_returned", "discount_label"]),
        hide_index=True,
        width="stretch",
    )
