"""
Customer Segmentation & Persona Analytics Studio
Built with Streamlit, Scikit-Learn & Plotly Express
Supports interactive K-Means re-clustering, 3D PCA visualization, and targeted marketing playbook.
"""

import os
import io
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import streamlit as st

st.set_page_config(
    page_title="Customer Segmentation Studio | ML Clustering",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dark UI styling
st.markdown("""
<style>
    .main { background-color: #0B0F19; }
    .persona-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
    }
    .persona-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .persona-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_customer_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "processed", "segmented_customers.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(base_dir, "data", "raw", "customer_data.csv")
    df = pd.read_csv(csv_path)
    return df

df = load_customer_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.image("https://img.icons8.com/fluency/96/user-group-man-woman.png", width=64)
st.sidebar.title("Clustering Controls")
st.sidebar.caption("Unsupervised Machine Learning & RFM Analytics")

# Interactive Cluster Count Slider
k_clusters = st.sidebar.slider("Number of Clusters (k)", min_value=2, max_value=8, value=5, step=1)

# Feature selection for clustering
st.sidebar.markdown("---")
st.sidebar.subheader("Clustering Features")
all_features = ["Annual_Income", "Spending_Score", "Recency_Days", "Frequency", "Monetary_Total", "Web_Visits_Per_Month"]
selected_features = st.sidebar.multiselect(
    "Select Model Attributes",
    all_features,
    default=all_features
)

# Region filter
regions = ["All Regions"] + sorted(df["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("Filter by Region", regions)

# Slicing data
view_df = df.copy()
if selected_region != "All Regions":
    view_df = view_df[view_df["Region"] == selected_region]

# Dynamic K-Means Execution
@st.cache_data
def run_dynamic_clustering(sub_df, features, k):
    if len(features) < 2 or len(sub_df) < k:
        return sub_df, None
    scaler = StandardScaler()
    scaled = scaler.fit_transform(sub_df[features])
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    labels = km.fit_predict(scaled)
    
    pca = PCA(n_components=min(3, len(features)), random_state=42)
    pca_res = pca.fit_transform(scaled)
    
    res_df = sub_df.copy()
    res_df["Dynamic_Cluster"] = [f"Cluster {l+1}" for l in labels]
    res_df["PCA_1"] = pca_res[:, 0]
    res_df["PCA_2"] = pca_res[:, 1]
    if pca_res.shape[1] >= 3:
        res_df["PCA_3"] = pca_res[:, 2]
    return res_df, km

clustered_df, km_model = run_dynamic_clustering(view_df, selected_features, k_clusters)

# ----------------- HEADER & EXECUTIVE SUMMARY -----------------
st.title("Customer Segmentation & Behavioral Analytics Studio")
st.markdown(f"**Persona Intelligence & RFM Profiling** | Audited Base: `{len(clustered_df):,}` Customers | Model Configuration: **K-Means ($k={k_clusters}$)**")

# TOP KPI SCORECARD
c1, c2, c3, c4, c5 = st.columns(5)
total_rev = clustered_df["Monetary_Total"].sum()
avg_inc = clustered_df["Annual_Income"].mean()
avg_score = clustered_df["Spending_Score"].mean()
avg_recency = clustered_df["Recency_Days"].mean()
avg_freq = clustered_df["Frequency"].mean()

with c1:
    st.metric("Total Customer Spend", f"${total_rev:,.0f}", "+14.2% YoY")
with c2:
    st.metric("Avg Annual Income", f"${avg_inc:,.0f}", "Baseline Demographics")
with c3:
    st.metric("Avg Spending Score", f"{avg_score:.1f} / 100", "Engagement Index")
with c4:
    st.metric("Avg Recency", f"{avg_recency:.0f} Days", "Purchase Lags")
with c5:
    st.metric("Avg Annual Orders", f"{avg_freq:.1f} Orders", "Order Velocity")

# ----------------- VISUALIZATIONS SECTION -----------------
st.markdown("---")
tab1, tab2, tab3, tab4 = st.tabs(["PCA Space & Clusters", "Demographic & Income Matrix", "RFM Segmentation", "Marketing Action Playbook"])

with tab1:
    col_pca1, col_pca2 = st.columns([7, 3])
    with col_pca1:
        # 2D PCA Cluster Map
        fig_pca = px.scatter(
            clustered_df,
            x="PCA_1",
            y="PCA_2",
            color="Dynamic_Cluster",
            hover_data=["Customer_ID", "Customer_Name", "Annual_Income", "Monetary_Total", "Preferred_Category"],
            title=f"Customer Behavioral Projections in 2D PCA Space (k={k_clusters})",
            template="plotly_dark",
            height=460
        )
        fig_pca.update_traces(marker=dict(size=8, opacity=0.75))
        fig_pca.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pca, use_container_width=True)

    with col_pca2:
        # Cluster Revenue Distribution
        cluster_rev = clustered_df.groupby("Dynamic_Cluster")["Monetary_Total"].sum().reset_index()
        fig_rev = px.pie(
            cluster_rev,
            values="Monetary_Total",
            names="Dynamic_Cluster",
            hole=0.55,
            title="Revenue Contribution by Cluster",
            template="plotly_dark",
            height=460
        )
        fig_rev.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_rev, use_container_width=True)

with tab2:
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        # Income vs Spending Score
        fig_inc = px.scatter(
            clustered_df,
            x="Annual_Income",
            y="Spending_Score",
            color="Dynamic_Cluster",
            size="Monetary_Total",
            hover_data=["Customer_Name", "Frequency", "AOV"],
            title="Annual Income vs Spending Score (Bubble Size = Total Spend)",
            template="plotly_dark",
            height=440
        )
        fig_inc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_inc, use_container_width=True)

    with col_d2:
        # Age vs Monetary Spend
        fig_age = px.scatter(
            clustered_df,
            x="Age",
            y="Monetary_Total",
            color="Dynamic_Cluster",
            trendline="lowess",
            title="Customer Age vs Annual Monetary Spend ($)",
            template="plotly_dark",
            height=440
        )
        fig_age.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_age, use_container_width=True)

with tab3:
    col_rfm1, col_rfm2 = st.columns(2)
    with col_rfm1:
        # Recency vs Frequency
        fig_rf = px.scatter(
            clustered_df,
            x="Recency_Days",
            y="Frequency",
            color="Dynamic_Cluster",
            title="Purchase Recency vs Order Frequency",
            template="plotly_dark",
            height=420
        )
        fig_rf.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_rf, use_container_width=True)

    with col_rfm2:
        # Frequency vs Monetary Total
        fig_fm = px.scatter(
            clustered_df,
            x="Frequency",
            y="Monetary_Total",
            color="Dynamic_Cluster",
            title="Order Frequency vs Annual Monetary Value",
            template="plotly_dark",
            height=420
        )
        fig_fm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fm, use_container_width=True)

with tab4:
    st.subheader("Targeted Omnichannel Marketing Playbook")
    
    # Generate Profile Summary Table
    summary_table = clustered_df.groupby("Dynamic_Cluster").agg(
        Users=("Customer_ID", "count"),
        Avg_Income=("Annual_Income", "mean"),
        Avg_Spend=("Monetary_Total", "mean"),
        Avg_Score=("Spending_Score", "mean"),
        Avg_Recency=("Recency_Days", "mean"),
        Avg_Frequency=("Frequency", "mean")
    ).reset_index()
    
    st.dataframe(summary_table, use_container_width=True)

    cols = st.columns(3)
    cols[0].markdown("""
    <div class="persona-card">
        <div class="persona-title">VIP Champions</div>
        <span class="persona-badge" style="background: rgba(16, 185, 129, 0.2); color: #34D399;">Top 18% Spend</span>
        <p style="color: #94A3B8; font-size: 0.85rem;"><strong>Action:</strong> Dedicated account executive, early access to flagship tech products, zero-minimum threshold shipping, exclusive VIP club events.</p>
    </div>
    """, unsafe_allow_html=True)

    cols[1].markdown("""
    <div class="persona-card">
        <div class="persona-title">Tech Enthusiasts</div>
        <span class="persona-badge" style="background: rgba(139, 92, 246, 0.2); color: #A78BFA;">High Velocity</span>
        <p style="color: #94A3B8; font-size: 0.85rem;"><strong>Action:</strong> Gamified loyalty drops, new device launch webinars, tech accessory cross-sells, fast-checkout push notifications.</p>
    </div>
    """, unsafe_allow_html=True)

    cols[2].markdown("""
    <div class="persona-card">
        <div class="persona-title">At-Risk / Lapsed</div>
        <span class="persona-badge" style="background: rgba(239, 68, 68, 0.2); color: #F87171;">Churn Alert</span>
        <p style="color: #94A3B8; font-size: 0.85rem;"><strong>Action:</strong> 20% discount reactivation coupon, feedback exit survey, direct email outreach from customer experience team.</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------- CUSTOMER SEARCH & EXPORT -----------------
st.markdown("---")
st.subheader("Customer Segment Explorer")
search_term = st.text_input("Search Customer by Name or ID:", "")
table_df = clustered_df
if search_term:
    table_df = clustered_df[
        clustered_df["Customer_Name"].str.lower().str.contains(search_term.lower()) |
        clustered_df["Customer_ID"].str.lower().str.contains(search_term.lower())
    ]

display_cols = ["Customer_ID", "Customer_Name", "Age", "Region", "Annual_Income", "Spending_Score", "Recency_Days", "Frequency", "Monetary_Total", "Dynamic_Cluster"]
st.dataframe(table_df[display_cols].head(300), use_container_width=True, height=280)

# Export Segmented CSV
csv_buff = io.StringIO()
table_df.to_csv(csv_buff, index=False)
st.download_button(
    "Export Segmented Customer List to CSV",
    data=csv_buff.getvalue(),
    file_name="segmented_customers_export.csv",
    mime="text/csv"
)

st.caption("Customer Segmentation Project • Data Analytics Internship Portfolio Week 2")
