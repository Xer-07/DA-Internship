"""
Historical Time Series & Predictive Analytics Dataset Generator
Synthesizes a realistic 3-year daily enterprise sales history (2023 - 2025, 1,095 days)
with trend, seasonality, marketing drivers, holiday pulses, and macro features.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set seed for deterministic reproducibility
np.random.seed(42)

def generate_historical_time_series():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    n_days = len(date_range)

    # 1. Base Linear & Exponential Trend
    t = np.arange(n_days)
    base_trend = 12000 + 18.5 * t + 0.005 * (t ** 2)

    # 2. Weekly Seasonality (Mon=0 to Sun=6)
    # Higher sales Thursday - Saturday, lower on Monday - Tuesday
    day_of_week = date_range.dayofweek
    weekly_factors = np.array([0.88, 0.92, 0.98, 1.08, 1.18, 1.14, 0.94])
    weekly_seasonality = weekly_factors[day_of_week]

    # 3. Annual Seasonality (Day of Year)
    # Q4 surge (days 305 to 365), summer peak (days 180 to 215), post-holiday dip in Jan
    day_of_year = date_range.dayofyear
    annual_seasonality = (
        1.0 
        + 0.15 * np.sin(2 * np.pi * day_of_year / 365.25 - np.pi / 2)
        + 0.28 * np.exp(-((day_of_year - 335) / 25) ** 2) # Q4 Black Friday / Christmas surge
        + 0.10 * np.exp(-((day_of_year - 195) / 20) ** 2) # Mid-year Summer campaign
    )

    # 4. Marketing Spend & Exogenous Drivers
    # Marketing spend increases during holiday quarters
    base_mktg = np.random.normal(3200, 500, n_days)
    mktg_boost = np.where((date_range.month.isin([11, 12])), 2800, 0)
    marketing_spend = np.clip(base_mktg + mktg_boost + 0.05 * base_trend, 1000, 12000)
    
    # Website sessions driven by marketing spend + seasonality
    sessions = (marketing_spend * 4.2 + np.random.normal(6000, 800, n_days)).astype(int)
    sessions = np.clip(sessions, 5000, 60000)

    # 5. Promotional Discount Rates
    # Higher discounts in Nov/Dec and end of quarters
    discount_rate = np.random.beta(2, 20, n_days)
    discount_rate = np.where(date_range.month.isin([11, 12]), discount_rate + 0.08, discount_rate)
    discount_rate = np.clip(discount_rate, 0.0, 0.28)

    # 6. Holiday Indicator (US major shopping periods)
    holiday_dates = [
        # 2023
        "2023-01-01", "2023-05-29", "2023-07-04", "2023-09-04", "2023-11-24", "2023-11-27", "2023-12-25",
        # 2024
        "2024-01-01", "2024-05-27", "2024-07-04", "2024-09-02", "2024-11-29", "2024-12-02", "2024-12-25",
        # 2025
        "2025-01-01", "2025-05-26", "2025-07-04", "2025-09-01", "2025-11-28", "2025-12-01", "2025-12-25"
    ]
    holiday_set = set(pd.to_datetime(holiday_dates).strftime("%Y-%m-%d"))
    holiday_indicator = np.array([1 if d.strftime("%Y-%m-%d") in holiday_set else 0 for d in date_range])

    # 7. Macro Consumer Sentiment Index (Random walk with mean reversion around 100)
    macro_index = np.zeros(n_days)
    macro_index[0] = 98.5
    for i in range(1, n_days):
        macro_index[i] = macro_index[i-1] * 0.98 + 100 * 0.02 + np.random.normal(0, 0.4)

    # 8. Composite Revenue Construction
    noise = np.random.normal(1.0, 0.045, n_days)
    holiday_multiplier = 1.0 + holiday_indicator * 0.35
    mktg_elasticity = (marketing_spend / 3200) ** 0.18

    daily_revenue = (
        base_trend 
        * weekly_seasonality 
        * annual_seasonality 
        * mktg_elasticity 
        * holiday_multiplier 
        * (macro_index / 100) 
        * noise
    )

    # Derived metrics
    aov = np.random.normal(145.0, 12.0, n_days)
    orders = (daily_revenue / aov).astype(int)
    units_sold = (orders * np.random.uniform(1.8, 2.6, n_days)).astype(int)
    conversion_rate = np.round((orders / sessions) * 100, 2)
    cogs = daily_revenue * np.random.uniform(0.58, 0.65, n_days)
    gross_profit = daily_revenue - cogs

    df = pd.DataFrame({
        "Date": date_range.strftime("%Y-%m-%d"),
        "Revenue": np.round(daily_revenue, 2),
        "Units_Sold": units_sold,
        "Total_Orders": orders,
        "AOV": np.round(aov, 2),
        "Marketing_Spend": np.round(marketing_spend, 2),
        "Website_Sessions": sessions,
        "Conversion_Rate_Pct": conversion_rate,
        "Discount_Rate": np.round(discount_rate, 4),
        "Holiday_Indicator": holiday_indicator,
        "Consumer_Sentiment_Index": np.round(macro_index, 2),
        "Gross_Profit": np.round(gross_profit, 2)
    })

    return df

def save_forecasting_datasets(base_path):
    raw_dir = os.path.join(base_path, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    print("Generating 3-year historical time series dataset (1,095 daily observations)...")
    df = generate_historical_time_series()

    csv_path = os.path.join(raw_dir, "historical_sales_trend.csv")
    df.to_csv(csv_path, index=False)
    print(f"[OK] Saved Raw CSV: {csv_path} ({len(df):,} records)")

    excel_path = os.path.join(raw_dir, "historical_sales_trend.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Daily_History", index=False)
        
        # Monthly rollup sheet
        df_copy = df.copy()
        df_copy["Month"] = pd.to_datetime(df_copy["Date"]).dt.to_period("M").astype(str)
        monthly_rollup = df_copy.groupby("Month").agg(
            Monthly_Revenue=("Revenue", "sum"),
            Monthly_Profit=("Gross_Profit", "sum"),
            Monthly_Orders=("Total_Orders", "sum"),
            Total_Marketing=("Marketing_Spend", "sum"),
            Avg_AOV=("AOV", "mean")
        ).reset_index()
        monthly_rollup.to_excel(writer, sheet_name="Monthly_Summary", index=False)

    print(f"[OK] Saved Multi-Sheet Historical Excel: {excel_path}")
    return df

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    df = save_forecasting_datasets(project_root)
    print(f"Time Series Duration: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Cumulative Historical Revenue: ${df['Revenue'].sum():,.2f}")
    print(f"Mean Daily Revenue: ${df['Revenue'].mean():,.2f}")
    print(f"Total Completed Orders: {df['Total_Orders'].sum():,}")
