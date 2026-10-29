"""
Enterprise Sales & Revenue Analytics Dashboard
Built with Streamlit & Plotly
Supports CSV, Excel, and SQLite data sources with interactive slicers and KPI tracking.
"""

import os
import io
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure page metadata
st.set_page_config(
    page_title="Sales & Revenue Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern corporate aesthetics
st.markdown("""
<style>
    .main {
        background-color: #0F172A;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.85rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .metric-badge {
        font-size: 0.8rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
    }
    .badge-positive {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34D399;
    }
    .badge-neutral {
        background-color: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_default_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "processed", "cleaned_sales_data.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # Fallback path
        csv_path = os.path.join(base_dir, "data", "raw", "sales_data.csv")
        df = pd.read_csv(csv_path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])
    df["Year"] = df["Order_Date"].dt.year
    df["Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
    df["YearMonth"] = df["Order_Date"].dt.strftime("%Y-%m")
    return df

# Initialize Data
raw_df = load_default_data()

# ----------------- SIDEBAR CONTROLS & SLICERS -----------------
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
st.sidebar.title("Analytics Control")
st.sidebar.caption("Filter data & configure KPIs dynamically")

# File Upload Section (Allows importing CSV or Excel)
with st.sidebar.expander("📂 Import Custom Data (Excel/CSV)", expanded=False):
    uploaded_file = st.file_uploader("Upload CSV or XLSX file", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                raw_df = pd.read_csv(uploaded_file)
            else:
                raw_df = pd.read_excel(uploaded_file)
            raw_df["Order_Date"] = pd.to_datetime(raw_df["Order_Date"])
            raw_df["Ship_Date"] = pd.to_datetime(raw_df["Ship_Date"])
            raw_df["Year"] = raw_df["Order_Date"].dt.year
            raw_df["Quarter"] = "Q" + raw_df["Order_Date"].dt.quarter.astype(str)
            raw_df["YearMonth"] = raw_df["Order_Date"].dt.strftime("%Y-%m")
            st.success("Uploaded dataset loaded successfully!")
        except Exception as e:
            st.error(f"Error parsing file: {e}")

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Interactive Slicers")

# Date Range Slicer
min_date = raw_df["Order_Date"].min().date()
max_date = raw_df["Order_Date"].max().date()
date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Slicer
all_regions = ["All Regions"] + sorted(raw_df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Geographic Region", all_regions)

# Product Category Slicer
all_categories = ["All Categories"] + sorted(raw_df["Category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Product Category", all_categories)

# Customer Segment Slicer
all_segments = ["All Segments"] + sorted(raw_df["Segment"].dropna().unique().tolist())
selected_segment = st.sidebar.selectbox("Customer Segment", all_segments)

# Ship Mode Slicer
all_ship_modes = ["All Modes"] + sorted(raw_df["Ship_Mode"].dropna().unique().tolist())
selected_ship_mode = st.sidebar.selectbox("Shipping Mode", all_ship_modes)

# Apply Slicer Filtering
df = raw_df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df[(df["Order_Date"] >= start_d) & (df["Order_Date"] <= end_d)]

if selected_region != "All Regions":
    df = df[df["Region"] == selected_region]

if selected_category != "All Categories":
    df = df[df["Category"] == selected_category]

if selected_segment != "All Segments":
    df = df[df["Segment"] == selected_segment]

if selected_ship_mode != "All Modes":
    df = df[df["Ship_Mode"] == selected_ship_mode]

# ----------------- HEADER & EXECUTIVE SUMMARY -----------------
st.title("📈 Executive Sales & Revenue Dashboard")
st.markdown(f"**Enterprise Performance Monitoring** | Active Filter: `{selected_region}` • `{selected_category}` • `{selected_segment}` | Records: `{len(df):,}`")

# KPI Summary Computation
total_rev = df["Revenue"].sum() if len(df) > 0 else 0
total_profit = df["Profit"].sum() if len(df) > 0 else 0
net_margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
total_orders = df["Order_ID"].nunique() if len(df) > 0 else 0
total_units = df["Quantity"].sum() if len(df) > 0 else 0
aov = (total_rev / total_orders) if total_orders > 0 else 0

# KPI CARDS ROW
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Revenue</div>
        <div class="metric-value">${total_rev:,.0f}</div>
        <span class="metric-badge badge-positive">Net Inflow</span>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Net Profit</div>
        <div class="metric-value">${total_profit:,.0f}</div>
        <span class="metric-badge badge-positive">{net_margin:.1f}% Margin</span>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
        <span class="metric-badge badge-neutral">{df['Customer_ID'].nunique():,} Customers</span>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Units Sold</div>
        <div class="metric-value">{total_units:,}</div>
        <span class="metric-badge badge-neutral">Items Moved</span>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Order Value</div>
        <div class="metric-value">${aov:,.2f}</div>
        <span class="metric-badge badge-positive">AOV Metric</span>
    </div>
    """, unsafe_allow_html=True)

# ----------------- VISUALIZATIONS SECTION -----------------
st.markdown("### 📊 Financial & Revenue Analytics")

tab1, tab2, tab3 = st.tabs(["📈 Revenue Trends & Trajectory", "🏆 Products & Categories", "🗺️ Geographic & Channel Segments"])

with tab1:
    col_t1, col_t2 = st.columns([7, 3])
    
    with col_t1:
        # Monthly Revenue & Profit Trend Chart
        monthly_df = df.groupby("YearMonth").agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        ).reset_index()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_df["YearMonth"], y=monthly_df["Revenue"],
            mode="lines+markers", name="Net Revenue ($)",
            line=dict(color="#3B82F6", width=3),
            fill="tozeroy", fillcolor="rgba(59, 130, 246, 0.1)"
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly_df["YearMonth"], y=monthly_df["Profit"],
            mode="lines+markers", name="Net Profit ($)",
            line=dict(color="#10B981", width=2.5, dash="dot")
        ))
        fig_trend.update_layout(
            title="Monthly Revenue and Profit Trajectory Over Time",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_t2:
        # Profitability by Quarter Bar
        q_df = df.groupby("YearQuarter").agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum")).reset_index()
        fig_q = px.bar(
            q_df, x="YearQuarter", y=["Revenue", "Profit"],
            barmode="group",
            title="Quarterly Comparison",
            color_discrete_map={"Revenue": "#3B82F6", "Profit": "#10B981"},
            template="plotly_dark"
        )
        fig_q.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_q, use_container_width=True)

with tab2:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        # Category Breakdown
        cat_df = df.groupby("Category").agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum")
        ).reset_index().sort_values("Revenue", ascending=False)
        fig_cat = px.bar(
            cat_df, x="Category", y="Revenue",
            color="Category",
            text="Revenue",
            title="Total Revenue by Product Category",
            color_discrete_sequence=["#3B82F6", "#8B5CF6", "#0D9488"],
            template="plotly_dark"
        )
        fig_cat.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig_cat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_p2:
        # Top 10 Best Performing Products
        top_10 = df.groupby("Product_Name").agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum")
        ).reset_index().sort_values("Revenue", ascending=True).tail(10)
        fig_top = px.bar(
            top_10, y="Product_Name", x="Revenue",
            orientation="h",
            title="Top 10 Products by Revenue Contribution",
            color="Revenue",
            color_continuous_scale="Viridis",
            template="plotly_dark"
        )
        fig_top.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_top, use_container_width=True)

with tab3:
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        # Regional Revenue Share Donut Chart
        reg_df = df.groupby("Region")["Revenue"].sum().reset_index()
        fig_reg = px.pie(
            reg_df, values="Revenue", names="Region",
            hole=0.55,
            title="Regional Revenue Contribution Share",
            color_discrete_sequence=px.colors.qualitative.Prism,
            template="plotly_dark"
        )
        fig_reg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col_g2:
        # Customer Segment Breakdown
        seg_df = df.groupby("Segment").agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum")).reset_index()
        fig_seg = px.bar(
            seg_df, x="Segment", y="Revenue",
            color="Segment",
            title="Revenue Generated Across Customer Segments",
            color_discrete_sequence=["#F59E0B", "#10B981", "#3B82F6"],
            template="plotly_dark"
        )
        fig_seg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=380
        )
        st.plotly_chart(fig_seg, use_container_width=True)

# ----------------- INTERACTIVE DATA EXPLORER & EXPORT -----------------
st.markdown("---")
st.subheader("🔍 Interactive Transactions Explorer")

search_term = st.text_input("Quick Search by Customer Name, Order ID, or Product Name:", "")
filtered_table = df
if search_term:
    search_lower = search_term.lower()
    filtered_table = df[
        df["Customer_Name"].str.lower().str.contains(search_lower, na=False) |
        df["Order_ID"].str.lower().str.contains(search_lower, na=False) |
        df["Product_Name"].str.lower().str.contains(search_lower, na=False)
    ]

# Display data table
cols_to_show = ["Order_ID", "Order_Date", "Customer_Name", "Segment", "Region", "Category", "Product_Name", "Quantity", "Revenue", "Profit", "Profit_Margin_Pct"]
st.dataframe(
    filtered_table[cols_to_show].head(500),
    use_container_width=True,
    height=300
)

# Download CSV Action
csv_buffer = io.StringIO()
filtered_table.to_csv(csv_buffer, index=False)
st.download_button(
    label="📥 Export Filtered Data to CSV",
    data=csv_buffer.getvalue(),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.caption("Sales & Revenue Analysis Dashboard • Data Analytics Internship Portfolio Week 1")
