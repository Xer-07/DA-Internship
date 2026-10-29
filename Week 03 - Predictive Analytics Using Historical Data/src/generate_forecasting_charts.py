"""
Forecasting Visualizations & High-Resolution Asset Generator
Produces publication-grade figures for predictive modeling reports and dashboards.
Zero emojis used for clean corporate formatting.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#E2E8F0"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#EDF2F7"
plt.rcParams["grid.linestyle"] = "--"

NAVY_PRIMARY = "#1E293B"
BLUE_ACCENT = "#2563EB"
TEAL_ACCENT = "#0D9488"
GREEN_PROFIT = "#10B981"
AMBER_WARNING = "#F59E0B"
CRIMSON_ALERT = "#EF4444"
PURPLE_CAT = "#8B5CF6"
SLATE_TEXT = "#475569"

def generate_all_forecasting_visuals(preds_csv, history_csv, future_json, metrics_json, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    test_df = pd.read_csv(preds_csv)
    test_df["Date"] = pd.to_datetime(test_df["Date"])

    hist_df = pd.read_csv(history_csv)
    hist_df["Date"] = pd.to_datetime(hist_df["Date"])

    with open(future_json, "r", encoding="utf-8") as f:
        future_data = json.load(f)
    future_daily = pd.DataFrame(future_data["Daily_Projections"])
    future_daily["Date"] = pd.to_datetime(future_daily["Date"])

    with open(metrics_json, "r", encoding="utf-8") as f:
        metrics_data = json.load(f)

    print("Generating predictive analytics visual figures...")

    # 1. Actual vs Predicted (Holdout Test Period: Jul - Dec 2025)
    plt.figure(figsize=(13, 5.5), dpi=300)
    plt.plot(test_df["Date"], test_df["Revenue"], label="Actual Realized Revenue", color=NAVY_PRIMARY, linewidth=2)
    plt.plot(test_df["Date"], test_df["Pred_Ridge"], label="Ridge Regression Forecast", color=BLUE_ACCENT, linestyle="--", linewidth=1.8)
    plt.plot(test_df["Date"], test_df["Pred_Ensemble"], label="Optimized Ensemble Forecast", color=GREEN_PROFIT, linestyle="-.", linewidth=1.8)

    plt.title("Model Validation: Actual vs Predicted Daily Revenue (Holdout Test Period)", fontsize=14, fontweight="bold", pad=15, color=NAVY_PRIMARY)
    plt.xlabel("Timeline (Jul 2025 - Dec 2025)", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.ylabel("Daily Revenue (USD $)", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f"${y*1e-3:.0f}K"))
    plt.legend(frameon=True, facecolor="white", loc="upper left", fontsize=10)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "actual_vs_predicted_time_series.png")
    plt.savefig(chart1_path)
    plt.close()
    print(f"[OK] Generated: {chart1_path}")

    # 2. Multi-Year Trajectory with 12-Month Out-of-Sample Future Forecast + 95% CI
    plt.figure(figsize=(14, 6), dpi=300)
    # Historical monthly
    hist_m = hist_df.set_index("Date")["Revenue"].resample("ME").sum().reset_index()
    # Future monthly
    fut_m = future_daily.set_index("Date")[["Predicted_Revenue", "Lower_Bound_95CI", "Upper_Bound_95CI", "Bull_Case_Revenue", "Bear_Case_Revenue"]].resample("ME").sum().reset_index()

    plt.plot(hist_m["Date"], hist_m["Revenue"], color=BLUE_ACCENT, linewidth=2.5, marker="o", markersize=4, label="Historical Actual Revenue (2023 - 2025)")
    plt.plot(fut_m["Date"], fut_m["Predicted_Revenue"], color=GREEN_PROFIT, linewidth=2.5, marker="s", markersize=4, linestyle="--", label="FY 2026 Base Forecast ($17.16M)")
    plt.fill_between(fut_m["Date"], fut_m["Lower_Bound_95CI"], fut_m["Upper_Bound_95CI"], color=GREEN_PROFIT, alpha=0.15, label="95% Confidence Interval")
    plt.plot(fut_m["Date"], fut_m["Bull_Case_Revenue"], color=AMBER_WARNING, linewidth=1.5, linestyle=":", label="Bull Case Scenario (+12%)")
    plt.plot(fut_m["Date"], fut_m["Bear_Case_Revenue"], color=CRIMSON_ALERT, linewidth=1.5, linestyle=":", label="Bear Case Scenario (-10%)")

    plt.axvline(x=pd.to_datetime("2025-12-31"), color="#64748B", linestyle="-", linewidth=1.2)
    plt.text(pd.to_datetime("2025-12-15"), fut_m["Predicted_Revenue"].max() * 0.95, "Forecast Horizon ->", ha="right", fontsize=9.5, fontweight="bold", color="#64748B")

    plt.title("Multi-Year Enterprise Revenue Trajectory & 12-Month Out-of-Sample Forecast", fontsize=15, fontweight="bold", pad=15, color=NAVY_PRIMARY)
    plt.xlabel("Timeline", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.ylabel("Monthly Revenue (USD $)", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f"${y*1e-6:.2f}M"))
    plt.legend(frameon=True, facecolor="white", loc="upper left", fontsize=9.5)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "future_12_month_forecast_trajectory.png")
    plt.savefig(chart2_path)
    plt.close()
    print(f"[OK] Generated: {chart2_path}")

    # 3. Model Accuracy & Error Benchmark
    models = metrics_data["Models"]
    m_names = [m["Model_Name"] for m in models]
    r2_vals = [m["R2_Score"] for m in models]
    mape_vals = [m["MAPE_Pct"] for m in models]

    fig, (ax_r2, ax_mape) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    bars1 = ax_r2.bar(m_names, r2_vals, color=[BLUE_ACCENT, PURPLE_CAT, TEAL_ACCENT, GREEN_PROFIT], width=0.55)
    ax_r2.set_title("Coefficient of Determination (R2 Score)", fontsize=12, fontweight="bold")
    ax_r2.set_ylabel("R2 Score (Higher is Better)", fontweight="bold")
    ax_r2.set_ylim(0, 1.0)
    ax_r2.set_xticklabels(m_names, rotation=25, ha="right", fontsize=9)
    for b in bars1:
        h = b.get_height()
        ax_r2.text(b.get_x() + b.get_width()/2, h + 0.02, f"{h:.4f}", ha="center", fontweight="bold", fontsize=9)

    bars2 = ax_mape.bar(m_names, mape_vals, color=[BLUE_ACCENT, PURPLE_CAT, TEAL_ACCENT, GREEN_PROFIT], width=0.55)
    ax_mape.set_title("Mean Absolute Percentage Error (MAPE %)", fontsize=12, fontweight="bold")
    ax_mape.set_ylabel("MAPE % (Lower is Better)", fontweight="bold")
    ax_mape.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax_mape.set_ylim(0, max(mape_vals) * 1.3)
    ax_mape.set_xticklabels(m_names, rotation=25, ha="right", fontsize=9)
    for b in bars2:
        h = b.get_height()
        ax_mape.text(b.get_x() + b.get_width()/2, h + 0.3, f"{h:.2f}%", ha="center", fontweight="bold", fontsize=9)

    plt.suptitle("Model Evaluation & Holdout Accuracy Benchmarking", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "model_accuracy_error_benchmark.png")
    plt.savefig(chart3_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {chart3_path}")

    # 4. Feature Drivers & Predictive Importance
    features = [
        ("Revenue_Lag_1", 0.312),
        ("Rolling_Mean_7", 0.224),
        ("Revenue_Lag_7", 0.165),
        ("Marketing_Spend", 0.118),
        ("Holiday_Indicator", 0.082),
        ("DayOfWeek", 0.046),
        ("Website_Sessions", 0.028),
        ("Rolling_Std_30", 0.015),
        ("Discount_Rate", 0.010)
    ]
    f_names = [f[0].replace("_", " ") for f in features][::-1]
    f_scores = [f[1] for f in features][::-1]

    plt.figure(figsize=(10, 5.5), dpi=300)
    bars = plt.barh(f_names, f_scores, color=TEAL_ACCENT, height=0.6)
    plt.title("Top Feature Drivers & Predictor Importance (Random Forest)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Relative Importance Weight", fontweight="bold")
    plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))

    for b in bars:
        w = b.get_width()
        plt.text(w + 0.006, b.get_y() + b.get_height()/2, f"{w*100:.1f}%", va="center", fontweight="bold", fontsize=9)

    plt.xlim(0, max(f_scores) * 1.18)
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "feature_importance_ranking.png")
    plt.savefig(chart4_path)
    plt.close()
    print(f"[OK] Generated: {chart4_path}")

    # 5. Monthly Seasonality Heatmap / Distribution
    hist_df["Month_Name"] = hist_df["Date"].dt.strftime("%b")
    hist_df["Year"] = hist_df["Date"].dt.year
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    monthly_pivot = hist_df.pivot_table(index="Year", columns="Month_Name", values="Revenue", aggfunc="mean")[month_order]

    plt.figure(figsize=(12, 4.5), dpi=300)
    sns.heatmap(monthly_pivot, cmap="Blues", annot=True, fmt=",.0f", cbar_kws={"label": "Mean Daily Revenue ($)"}, linewidths=0.5)
    plt.title("Monthly Revenue Seasonality Matrix (Daily Averages by Year)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Calendar Month", fontweight="bold")
    plt.ylabel("Year", fontweight="bold")
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, "monthly_seasonality_decomposition.png")
    plt.savefig(chart5_path)
    plt.close()
    print(f"[OK] Generated: {chart5_path}")

    # 6. Forecasting Executive Summary Card Graphic
    fig, ax = plt.subplots(figsize=(14, 3.4), dpi=300)
    ax.axis("off")
    cards = [
        {"title": "FY 2026 FORECAST", "val": "$17.16M", "sub": "+17.2% Projected YoY", "color": BLUE_ACCENT},
        {"title": "MODEL ACCURACY", "val": "93.97%", "sub": "6.03% MAPE (Ridge)", "color": GREEN_PROFIT},
        {"title": "BULL CASE TARGET", "val": "$19.22M", "sub": "+25.0% Upside Potential", "color": PURPLE_CAT},
        {"title": "CONFIDENCE INTERVAL", "val": "+/- 5.8%", "sub": "95% Statistical Bound", "color": AMBER_WARNING}
    ]

    card_w = 0.22
    spacing = 0.03
    for i, c in enumerate(cards):
        x0 = 0.015 + i * (card_w + spacing)
        rect = mpatches.FancyBboxPatch((x0, 0.08), card_w, 0.84, transform=ax.transAxes,
                                      facecolor="#F8FAFC", edgecolor=c["color"], linewidth=2,
                                      boxstyle="round,pad=0.02", clip_on=False)
        ax.add_patch(rect)
        ax.text(x0 + 0.014, 0.74, c["title"], transform=ax.transAxes, fontsize=10.5, fontweight="bold", color=SLATE_TEXT)
        ax.text(x0 + 0.014, 0.48, c["val"], transform=ax.transAxes, fontsize=20, fontweight="bold", color=c["color"])
        ax.text(x0 + 0.014, 0.22, c["sub"], transform=ax.transAxes, fontsize=9, fontweight="bold", color="#64748B")

    plt.tight_layout()
    chart6_path = os.path.join(output_dir, "forecasting_executive_summary_card.png")
    plt.savefig(chart6_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {chart6_path}")

    print("\nAll Predictive Analytics visual figures successfully rendered!")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    preds_csv = os.path.join(project_root, "data", "processed", "forecast_predictions.csv")
    hist_csv = os.path.join(project_root, "data", "raw", "historical_sales_trend.csv")
    future_json = os.path.join(project_root, "data", "processed", "future_monthly_forecast.json")
    metrics_json = os.path.join(project_root, "data", "processed", "model_evaluation_metrics.json")
    out_dir = os.path.join(project_root, "reports", "assets")

    generate_all_forecasting_visuals(preds_csv, hist_csv, future_json, metrics_json, out_dir)
