"""
Enterprise Data Processing and KPI Analytics Engine
Handles multi-source ingestion (CSV, Excel, SQLite), data validation,
DAX-equivalent business measure calculations, and metrics export.
"""

import os
import json
import sqlite3
import pandas as pd
import numpy as np

class SalesDataPipeline:
    def __init__(self, data_path=None):
        self.data_path = data_path
        self.df = None
        self.kpis = {}

    def load_data(self, source_type="csv", path=None, sheet_name="Sales_Transactions"):
        """Ingests data from CSV, Excel, or SQLite Database"""
        file_path = path or self.data_path
        
        if source_type == "csv":
            self.df = pd.read_csv(file_path)
            print(f"[OK] Loaded {len(self.df):,} rows from CSV: {file_path}")
        elif source_type in ["excel", "xlsx"]:
            self.df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"[OK] Loaded {len(self.df):,} rows from Excel Sheet '{sheet_name}': {file_path}")
        elif source_type == "sqlite":
            conn = sqlite3.connect(file_path)
            self.df = pd.read_sql_query("SELECT * FROM sales_transactions", conn)
            conn.close()
            print(f"[OK] Loaded {len(self.df):,} rows from SQLite database: {file_path}")
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        self._preprocess()
        return self.df

    def _preprocess(self):
        """Standardizes types, dates, and adds calendar dimensions"""
        self.df["Order_Date"] = pd.to_datetime(self.df["Order_Date"])
        self.df["Ship_Date"] = pd.to_datetime(self.df["Ship_Date"])
        
        # Calendar attributes for slicing and temporal trends
        self.df["Year"] = self.df["Order_Date"].dt.year
        self.df["Quarter"] = "Q" + self.df["Order_Date"].dt.quarter.astype(str)
        self.df["YearQuarter"] = self.df["Year"].astype(str) + "-" + self.df["Quarter"]
        self.df["Month"] = self.df["Order_Date"].dt.strftime("%b")
        self.df["Month_Num"] = self.df["Order_Date"].dt.month
        self.df["YearMonth"] = self.df["Order_Date"].dt.strftime("%Y-%m")
        self.df["DayOfWeek"] = self.df["Order_Date"].dt.day_name()
        self.df["Shipping_Days"] = (self.df["Ship_Date"] - self.df["Order_Date"]).dt.days

    def export_to_sqlite(self, db_path):
        """Exports the cleaned dataset to SQLite to demonstrate multi-source database capability"""
        conn = sqlite3.connect(db_path)
        # Convert datetimes to strings for standard sqlite compatibility
        df_export = self.df.copy()
        df_export["Order_Date"] = df_export["Order_Date"].dt.strftime("%Y-%m-%d")
        df_export["Ship_Date"] = df_export["Ship_Date"].dt.strftime("%Y-%m-%d")
        df_export.to_sql("sales_transactions", conn, if_exists="replace", index=False)
        conn.close()
        print(f"[OK] Successfully exported dataset to SQLite database: {db_path}")

    def compute_all_kpis(self, filtered_df=None):
        """Calculates executive business metrics, DAX-equivalent measures, and dimensional aggregations"""
        df = filtered_df if filtered_df is not None else self.df
        if df is None or len(df) == 0:
            return {}

        total_orders = int(df["Order_ID"].nunique())
        total_customers = int(df["Customer_ID"].nunique())
        total_units = int(df["Quantity"].sum())
        total_gross_sales = float(df["Gross_Sales"].sum())
        total_discount = float(df["Discount_Amount"].sum())
        total_revenue = float(df["Revenue"].sum())
        total_cogs = float(df["COGS"].sum())
        total_profit = float(df["Profit"].sum())
        profit_margin = float(round((total_profit / total_revenue) * 100, 2)) if total_revenue > 0 else 0.0
        avg_order_value = float(round(total_revenue / total_orders, 2)) if total_orders > 0 else 0.0
        avg_customer_value = float(round(total_revenue / total_customers, 2)) if total_customers > 0 else 0.0
        avg_discount_rate = float(round(df["Discount_Rate"].mean() * 100, 2))

        # Monthly Trend
        monthly = df.groupby("YearMonth").agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Units=("Quantity", "sum")
        ).reset_index().sort_values("YearMonth")
        monthly_trend = [
            {
                "YearMonth": row["YearMonth"],
                "Revenue": round(float(row["Revenue"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Orders": int(row["Orders"]),
                "Units": int(row["Units"]),
                "Margin": round((float(row["Profit"]) / float(row["Revenue"]) * 100), 2) if row["Revenue"] > 0 else 0.0
            }
            for _, row in monthly.iterrows()
        ]

        # Category Breakdown
        cat_agg = df.groupby("Category").agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Units=("Quantity", "sum"),
            Orders=("Order_ID", "nunique")
        ).reset_index().sort_values("Revenue", ascending=False)
        categories = [
            {
                "Category": row["Category"],
                "Revenue": round(float(row["Revenue"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Units": int(row["Units"]),
                "Margin": round((float(row["Profit"]) / float(row["Revenue"]) * 100), 2) if row["Revenue"] > 0 else 0.0,
                "RevenueShare": round((float(row["Revenue"]) / total_revenue * 100), 2) if total_revenue > 0 else 0.0
            }
            for _, row in cat_agg.iterrows()
        ]

        # Sub-Category Breakdown
        subcat_agg = df.groupby(["Category", "Sub_Category"]).agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Units=("Quantity", "sum")
        ).reset_index().sort_values("Revenue", ascending=False)
        subcategories = [
            {
                "Category": row["Category"],
                "Sub_Category": row["Sub_Category"],
                "Revenue": round(float(row["Revenue"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Units": int(row["Units"]),
                "Margin": round((float(row["Profit"]) / float(row["Revenue"]) * 100), 2) if row["Revenue"] > 0 else 0.0
            }
            for _, row in subcat_agg.iterrows()
        ]

        # Top 10 Products by Revenue
        top_prod = df.groupby(["Product_ID", "Product_Name", "Category"]).agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Units_Sold=("Quantity", "sum"),
            Orders_Count=("Order_ID", "nunique")
        ).reset_index().sort_values("Revenue", ascending=False).head(10)
        top_products = [
            {
                "Product_ID": row["Product_ID"],
                "Product_Name": row["Product_Name"],
                "Category": row["Category"],
                "Revenue": round(float(row["Revenue"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Units_Sold": int(row["Units_Sold"]),
                "Orders_Count": int(row["Orders_Count"]),
                "Margin": round((float(row["Profit"]) / float(row["Revenue"]) * 100), 2) if row["Revenue"] > 0 else 0.0
            }
            for _, row in top_prod.iterrows()
        ]

        # Regional Performance
        reg_agg = df.groupby("Region").agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Units=("Quantity", "sum")
        ).reset_index().sort_values("Revenue", ascending=False)
        regional = [
            {
                "Region": row["Region"],
                "Revenue": round(float(row["Revenue"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Orders": int(row["Orders"]),
                "Units": int(row["Units"]),
                "Margin": round((float(row["Profit"]) / float(row["Revenue"]) * 100), 2) if row["Revenue"] > 0 else 0.0,
                "RevenueShare": round((float(row["Revenue"]) / total_revenue * 100), 2) if total_revenue > 0 else 0.0
            }
            for _, row in reg_agg.iterrows()
        ]

        # Customer Segments
        seg_agg = df.groupby("Segment").agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Customers=("Customer_ID", "nunique"),
            Orders=("Order_ID", "nunique")
        ).reset_index().sort_values("Revenue", ascending=False)
        segments = [
            {
                "Segment": row["Segment"],
                "Revenue": round(float(row["Revenue"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Customers": int(row["Customers"]),
                "Orders": int(row["Orders"]),
                "Margin": round((float(row["Profit"]) / float(row["Revenue"]) * 100), 2) if row["Revenue"] > 0 else 0.0,
                "RevenueShare": round((float(row["Revenue"]) / total_revenue * 100), 2) if total_revenue > 0 else 0.0
            }
            for _, row in seg_agg.iterrows()
        ]

        # Payment Methods
        pay_agg = df.groupby("Payment_Method").agg(
            Revenue=("Revenue", "sum"),
            Transactions=("Order_ID", "count")
        ).reset_index().sort_values("Revenue", ascending=False)
        payments = [
            {
                "Method": row["Payment_Method"],
                "Revenue": round(float(row["Revenue"]), 2),
                "Transactions": int(row["Transactions"]),
                "Share": round((float(row["Revenue"]) / total_revenue * 100), 2) if total_revenue > 0 else 0.0
            }
            for _, row in pay_agg.iterrows()
        ]

        # Discount Tier Sensitivity
        df_copy = df.copy()
        df_copy["Discount_Tier"] = pd.cut(
            df_copy["Discount_Rate"],
            bins=[-0.01, 0.001, 0.10, 0.20, 1.0],
            labels=["No Discount (0%)", "Low (1-10%)", "Moderate (11-20%)", "High (>20%)"]
        )
        disc_agg = df_copy.groupby("Discount_Tier", observed=False).agg(
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "count")
        ).reset_index()
        discount_impact = [
            {
                "Tier": str(row["Discount_Tier"]),
                "Revenue": round(float(row["Revenue"]), 2),
                "Profit": round(float(row["Profit"]), 2),
                "Orders": int(row["Orders"]),
                "Margin": round((float(row["Profit"]) / float(row["Revenue"]) * 100), 2) if row["Revenue"] > 0 else 0.0
            }
            for _, row in disc_agg.iterrows()
        ]

        # YoY Growth Comparison (2024 vs 2025 full calendar years)
        rev_2024 = float(df[df["Year"] == 2024]["Revenue"].sum())
        rev_2025 = float(df[df["Year"] == 2025]["Revenue"].sum())
        yoy_growth = round(((rev_2025 - rev_2024) / rev_2024 * 100), 2) if rev_2024 > 0 else 0.0

        self.kpis = {
            "ExecutiveSummary": {
                "TotalRevenue": round(total_revenue, 2),
                "TotalGrossSales": round(total_gross_sales, 2),
                "TotalDiscountAmount": round(total_discount, 2),
                "TotalCOGS": round(total_cogs, 2),
                "TotalProfit": round(total_profit, 2),
                "ProfitMarginPct": profit_margin,
                "TotalOrders": total_orders,
                "TotalCustomers": total_customers,
                "TotalUnitsSold": total_units,
                "AverageOrderValue": avg_order_value,
                "AverageRevenuePerCustomer": avg_customer_value,
                "AverageDiscountPct": avg_discount_rate,
                "YoYRevenueGrowthPct": yoy_growth
            },
            "MonthlyTrend": monthly_trend,
            "CategoryBreakdown": categories,
            "SubCategoryBreakdown": subcategories,
            "TopProducts": top_products,
            "RegionalPerformance": regional,
            "CustomerSegments": segments,
            "PaymentMethods": payments,
            "DiscountImpact": discount_impact
        }
        return self.kpis

    def save_metrics_json(self, output_path):
        """Saves calculated KPIs to JSON for dashboard rendering"""
        if not self.kpis:
            self.compute_all_kpis()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.kpis, f, indent=2)
        print(f"[OK] KPI Metrics JSON exported to: {output_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    csv_file = os.path.join(project_root, "data", "raw", "sales_data.csv")
    excel_file = os.path.join(project_root, "data", "raw", "sales_data.xlsx")
    sqlite_file = os.path.join(project_root, "data", "processed", "sales_database.sqlite")
    metrics_json = os.path.join(project_root, "data", "processed", "kpi_metrics_summary.json")

    pipeline = SalesDataPipeline(csv_file)
    pipeline.load_data(source_type="csv")
    
    # Export to SQLite database demonstrating DB capabilities
    pipeline.export_to_sqlite(sqlite_file)
    
    # Verify loading from SQLite
    db_pipeline = SalesDataPipeline()
    db_pipeline.load_data(source_type="sqlite", path=sqlite_file)

    # Compute and save KPIs
    kpis = pipeline.compute_all_kpis()
    pipeline.save_metrics_json(metrics_json)

    print("\n--- EXECUTIVE KPI SNAPSHOT ---")
    summary = kpis["ExecutiveSummary"]
    for k, v in summary.items():
        if "Revenue" in k or "Sales" in k or "Profit" in k or "COGS" in k or "Value" in k or "DiscountAmount" in k:
            print(f"  {k:28}: ${v:,.2f}")
        elif "Pct" in k:
            print(f"  {k:28}: {v:.2f}%")
        else:
            print(f"  {k:28}: {v:,}")
