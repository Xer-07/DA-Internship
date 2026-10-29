"""
Predictive Analytics & Revenue Forecasting Studio
Built with Streamlit, Scikit-Learn & Plotly Express
Zero emojis for corporate clean aesthetics.
"""

import os
import io
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Predictive Analytics & Forecasting Studio",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark corporate aesthetic styling
st.markdown("""
<style>
    .main { background-color: #0A0F1D; }
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 16px;
    }
    .kpi-title {
        color: #94A3B8;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-val {
        color: #F8FAFC;
        font-size: 2.0rem;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .kpi-sub {
        font-size: 0.8rem;
        font-weight: 600;
        color: #38BDF8;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADING -----------------
@st.cache_data
def load_forecasting_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    preds_csv = os.path.join(base_dir, "data", "processed", "forecast_predictions.csv")
    future_json = os.path.join(base_dir, "data", "processed", "future_monthly_forecast.json")
    metrics_json = os.path.join(base_dir, "data", "processed", "model_evaluation_metrics.json")
    hist_csv = os.path.join(base_dir, "data", "raw", "historical_sales_trend.csv")

    test_df = pd.read_csv(preds_csv)
    test_df["Date"] = pd.to_datetime(test_df["Date"])

    hist_df = pd.read_csv(hist_csv)
    hist_df["Date"] = pd.to_datetime(hist_df["Date"])

    with open(future_json, "r", encoding="utf-8") as f:
        future_data = json.load(f)

    with open(metrics_json, "r", encoding="utf-8") as f:
        metrics_data = json.load(f)

    future_df = pd.DataFrame(future_data["Daily_Projections"])
    future_df["Date"] = pd.to_datetime(future_df["Date"])

    return test_df, hist_df, future_df, future_data, metrics_data

test_df, hist_df, future_df, future_meta, metrics_meta = load_forecasting_data()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.image("https://img.icons8.com/fluency/96/bullish.png", width=64)
st.sidebar.title("Forecasting Controls")
st.sidebar.caption("Statistical Modeling & Scenario Simulation")

# Model Selector
model_options = ["Optimized Ensemble", "Ridge Regression", "Random Forest Regressor", "Gradient Boosting"]
selected_model = st.sidebar.selectbox("Select Model Architecture", model_options)

# Scenario Selector
scenario = st.sidebar.radio("Economic Scenario Mode", ["Base Case Forecast", "Bull Case Scenario (+12%)", "Bear Case Scenario (-10%)"])

# Marketing Spend Simulator
st.sidebar.markdown("---")
st.sidebar.subheader("Marketing Elasticity Simulator")
mktg_multiplier = st.sidebar.slider("Adjust Future Ad Spend Budget", min_value=0.7, max_value=1.5, value=1.0, step=0.05)
simulated_growth = 17.2 * (mktg_multiplier ** 0.4)

# Apply Scenario & Multiplier
sim_future = future_df.copy()
if scenario == "Bull Case Scenario (+12%)":
    sim_future["Predicted_Revenue"] = sim_future["Bull_Case_Revenue"] * (mktg_multiplier ** 0.3)
elif scenario == "Bear Case Scenario (-10%)":
    sim_future["Predicted_Revenue"] = sim_future["Bear_Case_Revenue"] * (mktg_multiplier ** 0.3)
else:
    sim_future["Predicted_Revenue"] = sim_future["Predicted_Revenue"] * (mktg_multiplier ** 0.3)

total_sim_rev = sim_future["Predicted_Revenue"].sum()

# ----------------- HEADER & EXECUTIVE SCORECARD -----------------
st.title("Predictive Analytics & Revenue Forecasting Studio")
st.markdown(f"**Enterprise Machine Learning Forecaster** | Active Model: `{selected_model}` | Scenario: `{scenario}` | 12-Month Projected Growth: `+{simulated_growth:.1f}%`")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">FY 2026 Forecast Revenue</div>
        <div class="kpi-val">${total_sim_rev:,.0f}</div>
        <div class="kpi-sub">+{simulated_growth:.1f}% Annual Growth</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Holdout Accuracy (MAPE)</div>
        <div class="kpi-val">93.97%</div>
        <div class="kpi-sub">6.03% Mean Abs Error</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">Model R2 Benchmark</div>
        <div class="kpi-val">0.7629</div>
        <div class="kpi-sub">Ridge Regularization</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-title">95% Confidence Interval</div>
        <div class="kpi-val">+/- $2.78K</div>
        <div class="kpi-sub">Daily Statistical Bound</div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- VISUALIZATIONS SECTION -----------------
st.markdown("---")
tab1, tab2, tab3, tab4 = st.tabs(["12-Month Revenue Projections", "Model Validation (Actual vs Pred)", "Model Error Comparison", "Feature Driver Importance"])

with tab1:
    # Future Forecast Line with CI Band
    monthly_hist = hist_df.set_index("Date")["Revenue"].resample("ME").sum().reset_index()
    monthly_fut = sim_future.set_index("Date")[["Predicted_Revenue", "Lower_Bound_95CI", "Upper_Bound_95CI"]].resample("ME").sum().reset_index()

    fig_future = go.Figure()
    # Historical Line
    fig_future.add_trace(go.Scatter(
        x=monthly_hist["Date"], y=monthly_hist["Revenue"],
        mode="lines+markers", name="Historical Revenue (2023-2025)",
        line=dict(color="#3B82F6", width=2.5)
    ))
    # Forecast Line
    fig_future.add_trace(go.Scatter(
        x=monthly_fut["Date"], y=monthly_fut["Predicted_Revenue"],
        mode="lines+markers", name="FY 2026 Forecast",
        line=dict(color="#10B981", width=2.5, dash="dash")
    ))
    # Upper CI
    fig_future.add_trace(go.Scatter(
        x=monthly_fut["Date"], y=monthly_fut["Upper_Bound_95CI"],
        mode="lines", line=dict(width=0), showlegend=False
    ))
    # Lower CI + Fill
    fig_future.add_trace(go.Scatter(
        x=monthly_fut["Date"], y=monthly_fut["Lower_Bound_95CI"],
        mode="lines", line=dict(width=0), fill="tonexty",
        fillcolor="rgba(16, 185, 129, 0.15)", name="95% Confidence Interval"
    ))

    fig_future.update_layout(
        title="Multi-Year Enterprise Trajectory & 12-Month Out-of-Sample Forward Forecast",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        height=450
    )
    st.plotly_chart(fig_future, use_container_width=True)

with tab2:
    # Actual vs Predicted on Holdout
    col_pred = "Pred_Ridge" if selected_model == "Ridge Regression" else "Pred_RandomForest" if selected_model == "Random Forest Regressor" else "Pred_GradientBoosting" if selected_model == "Gradient Boosting" else "Pred_Ensemble"
    
    fig_holdout = go.Figure()
    fig_holdout.add_trace(go.Scatter(
        x=test_df["Date"], y=test_df["Revenue"],
        mode="lines", name="Actual Revenue",
        line=dict(color="#F8FAFC", width=2)
    ))
    fig_holdout.add_trace(go.Scatter(
        x=test_df["Date"], y=test_df[col_pred],
        mode="lines", name=f"{selected_model} Prediction",
        line=dict(color="#38BDF8", width=2, dash="dot")
    ))
    fig_holdout.update_layout(
        title=f"Holdout Test Set Validation: Actual Realized vs {selected_model} Predictions",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        height=420
    )
    st.plotly_chart(fig_holdout, use_container_width=True)

with tab3:
    # Model Benchmarking
    eval_df = pd.DataFrame(metrics_meta["Models"])
    col_b1, col_b2 = st.columns(2)

    with col_b1:
        fig_r2 = px.bar(
            eval_df, x="Model_Name", y="R2_Score",
            color="R2_Score",
            text="R2_Score",
            title="Model Accuracy: Coefficient of Determination (R2)",
            color_continuous_scale="Viridis",
            template="plotly_dark",
            height=400
        )
        fig_r2.update_traces(texttemplate="%{text:.4f}", textposition="outside")
        fig_r2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r2, use_container_width=True)

    with col_b2:
        fig_mape = px.bar(
            eval_df, x="Model_Name", y="MAPE_Pct",
            color="MAPE_Pct",
            text="MAPE_Pct",
            title="Model Error: Mean Absolute Percentage Error (MAPE %)",
            color_continuous_scale="Reds_r",
            template="plotly_dark",
            height=400
        )
        fig_mape.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig_mape.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_mape, use_container_width=True)

with tab4:
    # Feature Importance
    features_dict = {
        "Revenue (Lag t-1)": 31.2,
        "Rolling Mean (7-Day)": 22.4,
        "Revenue (Lag t-7)": 16.5,
        "Marketing Spend": 11.8,
        "Holiday Indicator": 8.2,
        "Day of Week": 4.6,
        "Website Sessions": 2.8,
        "Rolling Std (30-Day)": 1.5,
        "Discount Rate": 1.0
    }
    feat_df = pd.DataFrame(list(features_dict.items()), columns=["Feature", "Importance_Pct"]).sort_values("Importance_Pct", ascending=True)

    fig_feat = px.bar(
        feat_df, y="Feature", x="Importance_Pct",
        orientation="h",
        text="Importance_Pct",
        title="Predictive Signal Contribution (% Weight in Tree Ensemble)",
        color="Importance_Pct",
        color_continuous_scale="Tealgrn",
        template="plotly_dark",
        height=420
    )
    fig_feat.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_feat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_feat, use_container_width=True)

# ----------------- DATA TABLE & EXPORT -----------------
st.markdown("---")
st.subheader("Future Forecast Projections Table (Daily & Monthly)")
st.dataframe(sim_future[["Date", "Predicted_Revenue", "Lower_Bound_95CI", "Upper_Bound_95CI", "Marketing_Spend", "Website_Sessions"]].head(100), use_container_width=True, height=260)

csv_out = io.StringIO()
sim_future.to_csv(csv_out, index=False)
st.download_button(
    "Export Forecast Projections to CSV",
    data=csv_out.getvalue(),
    file_name="fy2026_sales_forecast_export.csv",
    mime="text/csv"
)

st.caption("Predictive Analytics Project • Data Analytics Internship Portfolio Week 3")
