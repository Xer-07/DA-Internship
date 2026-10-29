# Week 03: Predictive Analytics Using Historical Data

> **Data Analytics Internship — Project 03 of 04**  
> **Status:** Completed & Ready for Submission  
> **Tutorial Reference:** [YouTube Tutorial Guide](https://youtu.be/zZwunHv3Zog?si=It9hIsL3U1a1dpf3)

---

## Project Overview & Objectives
The primary objective of this project is to build an enterprise predictive machine learning pipeline that models historical multi-year sales trends and forecasts future revenue trajectories with statistical confidence intervals. Using a 3-year daily operational dataset (1,096 observations), we engineer autoregressive lags, rolling window statistics, and seasonal indicators to train regression and machine learning ensemble algorithms.

This repository implements:
1. **Interactive Streamlit Forecasting Studio** (`dashboard/streamlit_forecasting_app.py`) with model selection, scenario simulation, and dynamic 95% confidence interval bands.
2. **Standalone Executive Web Dashboard** (`dashboard/web_forecasting_dashboard/index.html`) using Vanilla JavaScript and Chart.js that runs natively in any browser with zero external dependencies.
3. **Pre-Executed Jupyter Notebook** (`notebooks/03_predictive_forecasting_modeling.ipynb`) containing complete time series feature engineering, non-shuffled temporal validation, model training, and out-of-sample forward projections.
4. **Predictive Analytics Engine** (`src/predictive_engine.py`) automating Ridge Regression, Random Forest, Gradient Boosting, and ensemble modeling.
5. **C-Level Forecasting Strategy Report** (`reports/Predictive_Forecasting_Report.md`) detailing accuracy metrics, seasonal components, and economic scenario modeling.

---

## Executive Forecasting Metrics

- **Projected FY 2026 Net Revenue:** **$17,164,139.08** (+17.2% YoY Growth)
- **Holdout Validation Accuracy:** **93.97%** (Mean Absolute Percentage Error: **6.03%**)
- **Best-Performing Model R2 Score:** **0.7629** (Ridge Regularization)
- **95% Confidence Interval:** **+/- $2.78K Daily Variance** (Annual: **$16.14M - $18.18M**)
- **Bull Case Expansion Target:** **$19.22M** (+25.0% Growth)
- **Bear Case Economic Floor:** **$15.45M** (+8.0% Growth)

![Executive Forecasting Scorecard](reports/assets/forecasting_executive_summary_card.png)

---

## Key Features Implemented

### 1. Advanced Time Series Feature Engineering
- **Autoregressive Lags:** Prior-day (`t-1`), weekly (`t-7`), bi-weekly (`t-14`), and monthly (`t-30`) revenue lags.
- **Rolling Windows:** 7-day and 30-day rolling moving averages and volatility standard deviations.
- **Exogenous Predictors:** Daily marketing ad spend, website sessions, holiday indicator pulses, and consumer sentiment indices.

### 2. Multi-Model Benchmarking & Holdout Validation
- **Ridge Regression (L2):** Delivers superior generalization on unseen temporal test sets ($R^2 = 0.7629$, RMSE = $3,718.55).
- **Tree Ensembles:** Random Forest and Gradient Boosting Regressors mapping non-linear interaction terms and marketing elasticity.
- **Optimized Ensemble:** Hybrid weighted blend balancing bias and variance.

---

## Visual Analytics Preview

| Actual vs Holdout Predicted Revenue | 12-Month Out-of-Sample Forecast |
| :---: | :---: |
| ![Actual vs Predicted](reports/assets/actual_vs_predicted_time_series.png) | ![12M Forecast](reports/assets/future_12_month_forecast_trajectory.png) |

| Model Accuracy & Error Comparison | Feature Driver Importance Ranking |
| :---: | :---: |
| ![Model Accuracy](reports/assets/model_accuracy_error_benchmark.png) | ![Feature Importance](reports/assets/feature_importance_ranking.png) |

---

## Project Directory Structure

```text
Week 03 - Predictive Analytics Using Historical Data/
├── README.md                              # Comprehensive project documentation
├── requirements.txt                       # Python dependencies
├── data/
│   ├── raw/
│   │   ├── historical_sales_trend.csv     # 1,096 daily records (2023 - 2025)
│   │   └── historical_sales_trend.xlsx    # Multi-sheet Excel workbook with monthly summaries
│   └── processed/
│       ├── cleaned_time_series.csv        # Cleaned dataset with 20 engineered features
│       ├── forecast_predictions.csv       # Holdout actuals vs model predictions
│       ├── model_evaluation_metrics.json  # R2, RMSE, MAE, MAPE benchmark metrics
│       └── future_monthly_forecast.json   # 12-month forward projections & confidence intervals
├── notebooks/
│   └── 03_predictive_forecasting_modeling.ipynb # Pre-executed Jupyter Notebook
├── src/
│   ├── forecasting_data_generator.py      # Multi-year historical time series synthesizer
│   ├── predictive_engine.py               # Feature engineering, ML training & forecasting
│   └── generate_forecasting_charts.py     # High-resolution chart generator
├── dashboard/
│   ├── streamlit_forecasting_app.py       # Dynamic Streamlit + Plotly forecasting studio
│   └── web_forecasting_dashboard/         # Standalone Zero-Dependency Web Dashboard
│       ├── index.html                     # Executive Dashboard UI
│       ├── styles.css                     # Dark/light theme styling
│       ├── forecast_data.js               # Preloaded historical and forecast dataset
│       └── app.js                         # Dynamic Chart.js and scenario logic
└── reports/
    ├── Predictive_Forecasting_Report.md   # Full 8-section executive strategy report
    └── assets/                            # Rendered visual figures & KPI graphics
```

---

## How to Run

### Option 1: Standalone Web Dashboard (Instant - No Setup Needed!)
1. Navigate to: `Week 03 - Predictive Analytics Using Historical Data/dashboard/web_forecasting_dashboard/`
2. Double-click `index.html` to open it in Chrome, Edge, Safari, or Firefox.
3. Toggle between Base, Bull, and Bear scenarios, inspect the 12-month confidence bands, and export the forecast to CSV!

### Option 2: Interactive Streamlit Studio
```bash
# Install dependencies
pip install -r requirements.txt

# Launch interactive forecasting studio
streamlit run "Week 03 - Predictive Analytics Using Historical Data/dashboard/streamlit_forecasting_app.py"
```

### Option 3: Re-Run Predictive Pipeline & Charts
```bash
# Recompute ML models and future projections:
python "Week 03 - Predictive Analytics Using Historical Data/src/predictive_engine.py"

# Regenerate publication-quality charts:
python "Week 03 - Predictive Analytics Using Historical Data/src/generate_forecasting_charts.py"
```

---

## Deliverables & Verification Checklist
- [x] Historical daily sales dataset generated (CSV and Excel).
- [x] Autoregressive lag and rolling window features engineered.
- [x] Non-shuffled chronological train/test validation executed.
- [x] Multi-model training and accuracy evaluation completed (Ridge, RF, GBR, Ensemble).
- [x] 12-month out-of-sample forward projections generated with 95% confidence intervals.
- [x] Interactive Streamlit application with scenario simulation and Plotly charts.
- [x] Standalone zero-dependency Web Dashboard with Chart.js.
- [x] Complete, fully executed Jupyter Notebook with outputs.
- [x] High-resolution charts saved for reporting.
- [x] Executive Predictive Analytics Report completed.
