"""
Visual Analytics and Chart Generation Engine
Produces high-resolution, modern aesthetic figures for documentation,
executive reports, and GitHub portfolio presentation.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Configure aesthetic visual style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#E2E8F0"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#EDF2F7"
plt.rcParams["grid.linestyle"] = "--"

# Palette definitions
NAVY_PRIMARY = "#1E293B"
BLUE_ACCENT = "#2563EB"
TEAL_ACCENT = "#0D9488"
GREEN_PROFIT = "#10B981"
AMBER_WARNING = "#F59E0B"
PURPLE_CAT = "#8B5CF6"
SLATE_TEXT = "#475569"

def generate_all_visuals(data_csv, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_csv)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["YearMonth"] = df["Order_Date"].dt.strftime("%Y-%m")
    
    print("Generating visual charts and assets...")

    # 1. Monthly Revenue & Profit Trend
    plt.figure(figsize=(13, 6), dpi=300)
    monthly = df.groupby("YearMonth").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()
    monthly["Rev_MA"] = monthly["Revenue"].rolling(window=3, min_periods=1).mean()

    ax = plt.gca()
    ax.fill_between(range(len(monthly)), monthly["Revenue"], alpha=0.15, color=BLUE_ACCENT, label="Revenue Area")
    ax.plot(range(len(monthly)), monthly["Revenue"], marker="o", markersize=5, color=BLUE_ACCENT, linewidth=2.5, label="Monthly Revenue")
    ax.plot(range(len(monthly)), monthly["Profit"], marker="s", markersize=4, color=GREEN_PROFIT, linewidth=2, linestyle="-.", label="Monthly Profit")
    ax.plot(range(len(monthly)), monthly["Rev_MA"], color=AMBER_WARNING, linewidth=1.8, linestyle="--", label="3-Mo Moving Avg (Trend)")

    plt.title("Monthly Revenue and Net Profit Trajectory (2024 - 2026)", fontsize=16, fontweight="bold", pad=15, color=NAVY_PRIMARY)
    plt.xlabel("Timeline (Year-Month)", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.ylabel("Amount (USD $)", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x*1e-3:.0f}K"))
    plt.xticks(range(len(monthly)), monthly["YearMonth"], rotation=45, ha="right", fontsize=9)
    plt.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", loc="upper left", fontsize=10)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "monthly_revenue_profit_trend.png")
    plt.savefig(chart1_path)
    plt.close()
    print(f"[OK] Generated: {chart1_path}")

    # 2. Category Performance (Revenue vs Profit Bar + Margin Line)
    plt.figure(figsize=(10, 6), dpi=300)
    cat_df = df.groupby("Category").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    ).reset_index().sort_values("Revenue", ascending=False)
    cat_df["Margin"] = (cat_df["Profit"] / cat_df["Revenue"]) * 100

    x = np.arange(len(cat_df))
    width = 0.35
    fig, ax1 = plt.subplots(figsize=(10, 5.5), dpi=300)

    rects1 = ax1.bar(x - width/2, cat_df["Revenue"], width, label="Revenue ($)", color=BLUE_ACCENT, alpha=0.9, edgecolor="none", zorder=3)
    rects2 = ax1.bar(x + width/2, cat_df["Profit"], width, label="Profit ($)", color=GREEN_PROFIT, alpha=0.9, edgecolor="none", zorder=3)

    ax1.set_ylabel("Total Financials (USD $)", fontsize=11, fontweight="bold", color=SLATE_TEXT)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f"${y*1e-6:.2f}M"))
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_df["Category"], fontsize=11, fontweight="bold", color=NAVY_PRIMARY)
    ax1.legend(loc="upper left", frameon=True, facecolor="white")

    # Secondary Axis for Margin %
    ax2 = ax1.twinx()
    ax2.plot(x, cat_df["Margin"], color=AMBER_WARNING, marker="D", linewidth=2.5, markersize=8, label="Profit Margin %", zorder=4)
    ax2.set_ylabel("Profit Margin (%)", fontsize=11, fontweight="bold", color=AMBER_WARNING)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax2.grid(False)
    ax2.legend(loc="upper right", frameon=True, facecolor="white")

    plt.title("Revenue, Profit, and Margin Comparison by Product Category", fontsize=15, fontweight="bold", pad=15, color=NAVY_PRIMARY)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "category_revenue_profit_breakdown.png")
    plt.savefig(chart2_path)
    plt.close()
    print(f"[OK] Generated: {chart2_path}")

    # 3. Top 10 Best-Selling Products by Revenue
    plt.figure(figsize=(12, 6.5), dpi=300)
    top_prods = df.groupby("Product_Name").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    ).reset_index().sort_values("Revenue", ascending=True).tail(10)

    bars = plt.barh(top_prods["Product_Name"], top_prods["Revenue"], color=TEAL_ACCENT, height=0.65, edgecolor="none")
    plt.xlabel("Total Revenue (USD $)", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.title("Top 10 High-Impact Products by Total Generated Revenue", fontsize=15, fontweight="bold", pad=15, color=NAVY_PRIMARY)
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x*1e-3:.0f}K"))
    
    # Value annotations on bars
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 5000, bar.get_y() + bar.get_height()/2, f"${w:,.0f}", ha="left", va="center", fontsize=9, fontweight="bold", color=NAVY_PRIMARY)

    plt.xlim(0, top_prods["Revenue"].max() * 1.15)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "top_10_products_revenue.png")
    plt.savefig(chart3_path)
    plt.close()
    print(f"[OK] Generated: {chart3_path}")

    # 4. Regional Performance (Donut + Bar)
    reg_df = df.groupby("Region").agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()

    fig, (ax_donut, ax_bar) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)
    colors = [BLUE_ACCENT, TEAL_ACCENT, PURPLE_CAT, AMBER_WARNING]

    # Donut Chart
    wedges, texts, autotexts = ax_donut.pie(
        reg_df["Revenue"],
        labels=reg_df["Region"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
    )
    plt.setp(autotexts, size=10, weight="bold", color="white")
    plt.setp(texts, size=11, weight="bold", color=NAVY_PRIMARY)
    ax_donut.set_title("Revenue Share by Geographic Region", fontsize=13, fontweight="bold", color=NAVY_PRIMARY)

    # Bar Chart for Profit Margin
    reg_df["Margin"] = (reg_df["Profit"] / reg_df["Revenue"]) * 100
    bars = ax_bar.bar(reg_df["Region"], reg_df["Margin"], color=GREEN_PROFIT, width=0.5)
    ax_bar.set_title("Operating Profit Margin (%) by Region", fontsize=13, fontweight="bold", color=NAVY_PRIMARY)
    ax_bar.set_ylabel("Profit Margin (%)", fontsize=10, fontweight="bold", color=SLATE_TEXT)
    ax_bar.yaxis.set_major_formatter(ticker.PercentFormatter())
    for bar in bars:
        h = bar.get_height()
        ax_bar.text(bar.get_x() + bar.get_width()/2, h + 0.8, f"{h:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax_bar.set_ylim(0, reg_df["Margin"].max() * 1.2)

    plt.suptitle("Geographic Sales Distribution and Profitability Health", fontsize=16, fontweight="bold", color=NAVY_PRIMARY, y=1.02)
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "regional_performance_matrix.png")
    plt.savefig(chart4_path)
    plt.close()
    print(f"[OK] Generated: {chart4_path}")

    # 5. Discount Impact on Margins (Sensitivity Analysis)
    df_copy = df.copy()
    df_copy["Discount_Tier"] = pd.cut(
        df_copy["Discount_Rate"],
        bins=[-0.01, 0.001, 0.10, 0.20, 1.0],
        labels=["0% (None)", "1-10% (Low)", "11-20% (Medium)", ">20% (Aggressive)"]
    )
    disc_summary = df_copy.groupby("Discount_Tier", observed=False).agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "count")
    ).reset_index()
    disc_summary["Margin"] = (disc_summary["Profit"] / disc_summary["Revenue"]) * 100

    plt.figure(figsize=(10, 5), dpi=300)
    bars = plt.bar(disc_summary["Discount_Tier"].astype(str), disc_summary["Margin"], color=["#10B981", "#3B82F6", "#F59E0B", "#EF4444"], width=0.55)
    plt.title("Discount Rate Sensitivity: Impact on Net Profit Margin", fontsize=14, fontweight="bold", pad=15, color=NAVY_PRIMARY)
    plt.xlabel("Promotional Discount Tiers", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.ylabel("Net Profit Margin (%)", fontsize=11, fontweight="bold", color=SLATE_TEXT, labelpad=10)
    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter())
    
    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, h + 0.8, f"{h:.2f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
    
    plt.ylim(0, max(disc_summary["Margin"]) * 1.2)
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, "discount_profitability_impact.png")
    plt.savefig(chart5_path)
    plt.close()
    print(f"[OK] Generated: {chart5_path}")

    # 6. Executive KPI Dashboard Summary Card Graphic
    fig, ax = plt.subplots(figsize=(12, 3.2), dpi=300)
    ax.axis("off")
    total_rev = df["Revenue"].sum()
    total_prof = df["Profit"].sum()
    margin = (total_prof / total_rev) * 100
    orders = df["Order_ID"].nunique()
    aov = total_rev / orders

    cards = [
        {"title": "TOTAL REVENUE", "value": f"${total_rev:,.0f}", "sub": "+17.65% YoY Growth", "color": BLUE_ACCENT},
        {"title": "NET PROFIT", "value": f"${total_prof:,.0f}", "sub": f"{margin:.1f}% Net Margin", "color": GREEN_PROFIT},
        {"title": "TOTAL ORDERS", "value": f"{orders:,}", "sub": f"{df['Customer_ID'].nunique():,} Unique Buyers", "color": PURPLE_CAT},
        {"title": "AVG ORDER VALUE", "value": f"${aov:,.2f}", "sub": "High Corporate Basket", "color": AMBER_WARNING}
    ]

    import matplotlib.patches as mpatches
    card_width = 0.22
    spacing = 0.03
    for i, c in enumerate(cards):
        x0 = 0.02 + i * (card_width + spacing)
        # Background rounded card
        rect = mpatches.FancyBboxPatch((x0, 0.1), card_width, 0.8, transform=ax.transAxes,
                                      facecolor="#F8FAFC", edgecolor=c["color"], linewidth=2,
                                      boxstyle="round,pad=0.02", clip_on=False)
        ax.add_patch(rect)
        ax.text(x0 + 0.02, 0.72, c["title"], transform=ax.transAxes, fontsize=10, fontweight="bold", color=SLATE_TEXT)
        ax.text(x0 + 0.02, 0.44, c["value"], transform=ax.transAxes, fontsize=18, fontweight="bold", color=c["color"])
        ax.text(x0 + 0.02, 0.22, c["sub"], transform=ax.transAxes, fontsize=9, fontweight="bold", color="#64748B")

    plt.tight_layout()
    chart6_path = os.path.join(output_dir, "kpi_summary_dashboard.png")
    plt.savefig(chart6_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {chart6_path}")

    print("\nAll executive visual charts successfully rendered!")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    csv_path = os.path.join(project_root, "data", "processed", "cleaned_sales_data.csv")
    output_dir = os.path.join(project_root, "reports", "assets")
    generate_all_visuals(csv_path, output_dir)
