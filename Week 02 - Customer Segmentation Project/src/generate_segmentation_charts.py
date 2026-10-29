"""
Customer Segmentation Visual Asset & Publication Chart Generator
Generates high-resolution figures for documentation, notebooks, and executive reports.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#E2E8F0"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#EDF2F7"
plt.rcParams["grid.linestyle"] = "--"

# Palette mapping for clusters
CLUSTER_COLORS = {
    "VIP Champions": "#10B981",        # Emerald Green
    "Loyal Mainstream": "#3B82F6",     # Royal Blue
    "Emerging Tech Lovers": "#8B5CF6", # Violet
    "Bargain Hunters": "#F59E0B",      # Warm Amber
    "At-Risk / Lapsed": "#EF4444"      # Crimson
}

def generate_segmentation_visuals(segmented_csv, eval_json, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(segmented_csv)
    with open(eval_json, "r", encoding="utf-8") as f:
        eval_metrics = json.load(f)

    print("Generating customer segmentation visual assets...")

    # 1. Elbow Method & Silhouette Score Curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    k_vals = eval_metrics["k_values"]
    wcss = eval_metrics["wcss"]
    sil_scores = eval_metrics["silhouette_scores"]

    # WCSS / Elbow Curve
    ax1.plot(k_vals, wcss, marker="o", color="#2563EB", linewidth=2.5, markersize=7)
    ax1.axvline(x=5, color="#EF4444", linestyle="--", linewidth=1.5, label="Optimal Elbow (k=5)")
    ax1.set_title("The Elbow Method (WCSS vs Clusters)", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlabel("Number of Clusters (k)", fontweight="bold")
    ax1.set_ylabel("Within-Cluster Sum of Squares (Inertia)", fontweight="bold")
    ax1.legend(frameon=True, facecolor="white")

    # Silhouette Score Curve
    ax2.plot(k_vals, sil_scores, marker="s", color="#10B981", linewidth=2.5, markersize=7)
    ax2.axvline(x=5, color="#EF4444", linestyle="--", linewidth=1.5, label="Optimal Peak (k=5)")
    ax2.set_title("Silhouette Coefficient vs Clusters (k)", fontsize=13, fontweight="bold", pad=12)
    ax2.set_xlabel("Number of Clusters (k)", fontweight="bold")
    ax2.set_ylabel("Silhouette Score", fontweight="bold")
    ax2.legend(frameon=True, facecolor="white")

    plt.suptitle("Clustering Optimization: Elbow & Silhouette Validation", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "elbow_and_silhouette_analysis.png")
    plt.savefig(chart1_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {chart1_path}")

    # 2. PCA 2D Cluster Scatter Plot
    plt.figure(figsize=(11, 7), dpi=300)
    unique_names = sorted(df["Cluster_Name"].unique())
    for name in unique_names:
        sub = df[df["Cluster_Name"] == name]
        color = CLUSTER_COLORS.get(name, "#6B7280")
        plt.scatter(sub["PCA_1"], sub["PCA_2"], c=color, label=f"{name} (n={len(sub):,})",
                    alpha=0.65, edgecolors="none", s=50)

    # Plot Cluster Centroids in PCA Space
    centroids = df.groupby("Cluster_Name")[["PCA_1", "PCA_2"]].mean()
    plt.scatter(centroids["PCA_1"], centroids["PCA_2"], c="black", marker="X", s=220, linewidths=2, edgecolors="white", label="Centroids", zorder=5)

    plt.title("Customer Behavioral Segments in 2D PCA Space (82.5% Variance Explained)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Principal Component 1 (Purchasing Power & Engagement)", fontweight="bold")
    plt.ylabel("Principal Component 2 (Recency vs Price Elasticity)", fontweight="bold")
    plt.legend(frameon=True, facecolor="white", loc="best", fontsize=9.5)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "pca_clusters_2d_scatter.png")
    plt.savefig(chart2_path)
    plt.close()
    print(f"[OK] Generated: {chart2_path}")

    # 3. Income vs Spending Score Clusters
    plt.figure(figsize=(11, 6.5), dpi=300)
    for name in unique_names:
        sub = df[df["Cluster_Name"] == name]
        color = CLUSTER_COLORS.get(name, "#6B7280")
        plt.scatter(sub["Annual_Income"], sub["Spending_Score"], c=color, label=name, alpha=0.65, edgecolors="none", s=50)

    # Centroids
    cen_inc = df.groupby("Cluster_Name")[["Annual_Income", "Spending_Score"]].mean()
    plt.scatter(cen_inc["Annual_Income"], cen_inc["Spending_Score"], c="black", marker="X", s=220, linewidths=2, edgecolors="white", label="Cluster Centers", zorder=5)

    plt.title("Customer Segmentation: Annual Income vs Spending Score", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Annual Income (USD $)", fontweight="bold")
    plt.ylabel("Behavioral Spending Score (1 - 100)", fontweight="bold")
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f"${x*1e-3:.0f}K"))
    plt.legend(frameon=True, facecolor="white", loc="best", fontsize=9.5)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "income_vs_spending_score_clusters.png")
    plt.savefig(chart3_path)
    plt.close()
    print(f"[OK] Generated: {chart3_path}")

    # 4. RFM Metrics Distribution by Cluster (Boxplots)
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300)
    rfm_metrics = [
        ("Recency_Days", "Recency (Days Since Last Order)", "Days", False),
        ("Frequency", "Frequency (Orders in Last 12M)", "Orders", False),
        ("Monetary_Total", "Monetary Spend (Annual Total $)", "$", True)
    ]

    for ax, (col, title, unit, is_money) in zip(axes, rfm_metrics):
        sns.boxplot(data=df, x="Cluster_Name", y=col, ax=ax, palette=CLUSTER_COLORS, hue="Cluster_Name", legend=False, width=0.55)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlabel("")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right", fontsize=8.5)
        if is_money:
            ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: f"${y*1e-3:.0f}K"))

    plt.suptitle("Recency, Frequency, and Monetary (RFM) Distribution Across Personas", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "rfm_distribution_by_cluster.png")
    plt.savefig(chart4_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {chart4_path}")

    # 5. Radar / Spider Chart Comparing Personas
    categories_radar = ["Income", "Spend", "Score", "Frequency", "Visits", "LowRecency"]
    N = len(categories_radar)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Normalize cluster means between 0 and 1
    agg_radar = df.groupby("Cluster_Name").agg(
        Income=("Annual_Income", "mean"),
        Spend=("Monetary_Total", "mean"),
        Score=("Spending_Score", "mean"),
        Frequency=("Frequency", "mean"),
        Visits=("Web_Visits_Per_Month", "mean"),
        LowRecency=("Recency_Days", lambda x: 365 - x.mean()) # Inverted recency so higher is better
    )
    norm_radar = (agg_radar - agg_radar.min()) / (agg_radar.max() - agg_radar.min() + 1e-6)

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)
    plt.xticks(angles[:-1], categories_radar, color="#475569", size=10, fontweight="bold")

    for name in unique_names:
        values = norm_radar.loc[name].values.flatten().tolist()
        values += values[:1]
        color = CLUSTER_COLORS.get(name, "#6B7280")
        ax.plot(angles, values, linewidth=2, linestyle="solid", label=name, color=color)
        ax.fill(angles, values, color=color, alpha=0.1)

    plt.title("Cluster Persona Multidimensional Radar Comparison", size=14, fontweight="bold", pad=25)
    plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), frameon=True, facecolor="white")
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, "cluster_persona_radar_profiles.png")
    plt.savefig(chart5_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {chart5_path}")

    # 6. Executive Persona Card Graphic
    fig, ax = plt.subplots(figsize=(14, 3.4), dpi=300)
    ax.axis("off")
    cards = [
        {"name": "VIP Champions", "count": f"{len(df[df['Cluster_Name']=='VIP Champions']):,}", "share": "18.0%", "spend": "$18.4K", "strat": "Exclusive Retention", "color": "#10B981"},
        {"name": "Loyal Mainstream", "count": f"{len(df[df['Cluster_Name']=='Loyal Mainstream']):,}", "share": "31.0%", "spend": "$7.6K", "strat": "Category Upsell", "color": "#3B82F6"},
        {"name": "Tech Lovers", "count": f"{len(df[df['Cluster_Name']=='Emerging Tech Lovers']):,}", "share": "17.0%", "spend": "$8.8K", "strat": "Early Gadget Drops", "color": "#8B5CF6"},
        {"name": "Bargain Hunters", "count": f"{len(df[df['Cluster_Name']=='Bargain Hunters']):,}", "share": "22.6%", "spend": "$2.1K", "strat": "Flash Clearances", "color": "#F59E0B"},
        {"name": "At-Risk / Lapsed", "count": f"{len(df[df['Cluster_Name']=='At-Risk / Lapsed']):,}", "share": "11.6%", "spend": "$3.8K", "strat": "Win-Back Offers", "color": "#EF4444"}
    ]

    import matplotlib.patches as mpatches
    card_w = 0.17
    spacing = 0.03
    for i, c in enumerate(cards):
        x0 = 0.015 + i * (card_w + spacing)
        rect = mpatches.FancyBboxPatch((x0, 0.08), card_w, 0.84, transform=ax.transAxes,
                                      facecolor="#F8FAFC", edgecolor=c["color"], linewidth=2,
                                      boxstyle="round,pad=0.02", clip_on=False)
        ax.add_patch(rect)
        ax.text(x0 + 0.012, 0.74, c["name"], transform=ax.transAxes, fontsize=10.5, fontweight="bold", color="#1E293B")
        ax.text(x0 + 0.012, 0.52, c["spend"], transform=ax.transAxes, fontsize=17, fontweight="bold", color=c["color"])
        ax.text(x0 + 0.012, 0.32, f"{c['count']} users ({c['share']})", transform=ax.transAxes, fontsize=8.5, fontweight="bold", color="#64748B")
        ax.text(x0 + 0.012, 0.15, c["strat"], transform=ax.transAxes, fontsize=8, fontweight="bold", color=c["color"])

    plt.tight_layout()
    chart6_path = os.path.join(output_dir, "cluster_executive_summary_card.png")
    plt.savefig(chart6_path, bbox_inches="tight")
    plt.close()
    print(f"[OK] Generated: {chart6_path}")

    print("\nAll Customer Segmentation visual charts successfully created!")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    seg_csv = os.path.join(project_root, "data", "processed", "segmented_customers.csv")
    eval_json = os.path.join(project_root, "data", "processed", "elbow_silhouette_metrics.json")
    out_dir = os.path.join(project_root, "reports", "assets")
    generate_segmentation_visuals(seg_csv, eval_json, out_dir)
