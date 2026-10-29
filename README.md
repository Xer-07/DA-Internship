# Data Analytics Internship Portfolio

Welcome to the official portfolio repository for the **Data Analytics Internship**. This repository tracks all project milestones, datasets, analytical notebooks, executive dashboards, and codebases structured on a strict **week-by-week** progression.

---

## 4-Week Internship Project Roadmap

| Week | Milestone / Project Name | Key Methodologies & Tools | Due Date | Status |
| :---: | :--- | :--- | :---: | :---: |
| **01** | [**Sales & Revenue Analysis Dashboard**](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/) | Multi-source Ingestion, KPI Tracking, Streamlit & Web BI | **05 Nov 2026** | **COMPLETED** |
| **02** | [**Customer Segmentation Project**](./Week%2002%20-%20Customer%20Segmentation%20Project/) | RFM Modeling, K-Means Clustering, Scikit-Learn | **12 Nov 2026** | **COMPLETED** |
| **03** | [**Predictive Analytics Using Historical Data**](./Week%2003%20-%20Predictive%20Analytics%20Using%20Historical%20Data/) | Time Series Forecasting, Regression, Model Evaluation | **19 Nov 2026** | **COMPLETED** |
| **04** | [**Data Cleaning & Reporting Automation**](./Week%2004%20-%20Data%20Cleaning%20&%20Reporting%20Automation/) | Automated Workflows, Anomaly Detection, PDF Reports | **26 Nov 2026** | **COMPLETED** |

---

## Week 4 Highlights: Data Cleaning & Reporting Automation

> **Project Directory:** [`Week 04 - Data Cleaning & Reporting Automation/`](./Week%2004%20-%20Data%20Cleaning%20&%20Reporting%20Automation/)  
> **Tutorial Reference:** [YouTube Tutorial Guide](https://youtu.be/jxq4-KSB_OA?si=Yx6Z8h9L7Nq8q7gQ)

### Executive Quality & Financial Results
- **Certified Reconciled Revenue:** **$39,269,767.19** (100% deterministic billing reconciliation)
- **Data Quality Score (DQS):** **99.96%** (vs 95.40% raw ingest baseline, **+4.56% quality gain**)
- **Certified Transaction Count:** **3,200 records** (180 duplicate events pruned)
- **Treated Anomalies:** **65 records** (Isolation Forest + IQR boundary treatment)
- **Automated Imputations:** **1,547 missing cells / sentinel tokens** contextually imputed
- **Governance Dimensions:** 100% Uniqueness, 100% Validity, 100% Consistency, 99.86% Completeness

### Deliverables Included:
1. **Interactive Automation Studio:** Dynamic Streamlit application (`streamlit_automation_app.py`) featuring live pipeline execution, quality radar scorecard, and anomaly detective.
2. **Standalone Web Dashboard:** Zero-dependency web application (`index.html`) using Vanilla JavaScript and Chart.js with pipeline funnels, dimension scorecards, and live transaction ledger.
3. **Pre-Executed Jupyter Notebook:** [`04_data_cleaning_reporting_automation.ipynb`](./Week%2004%20-%20Data%20Cleaning%20&%20Reporting%20Automation/notebooks/04_data_cleaning_reporting_automation.ipynb) featuring step-by-step pipeline audits, scikit-learn Isolation Forest, and deterministic financial reconciliations.
4. **Enterprise ETL Pipeline:** Modular script (`cleaning_pipeline.py`) automating deduplication, schema standardization, date parsing, chronology repair, and outlier treatment.
5. **Automated Reporting Engine:** Generator script (`report_automation_engine.py`) compiling automated C-Level PDF, HTML, and JSON analytics payloads.
6. **Executive Audit Report:** [`Data_Cleaning_and_Reporting_Automation_Report.md`](./Week%2004%20-%20Data%20Cleaning%20&%20Reporting%20Automation/reports/Data_Cleaning_and_Reporting_Automation_Report.md) detailing ISO-8000 metrics and financial breakdowns.

![Data Quality Summary Preview](./Week%2004%20-%20Data%20Cleaning%20&%20Reporting%20Automation/reports/assets/data_health_executive_summary_card.png)

---

## Week 3 Highlights: Predictive Analytics Using Historical Data

> **Project Directory:** [`Week 03 - Predictive Analytics Using Historical Data/`](./Week%2003%20-%20Predictive%20Analytics%20Using%20Historical%20Data/)  
> **Tutorial Reference:** [YouTube Tutorial Guide](https://youtu.be/zZwunHv3Zog?si=It9hIsL3U1a1dpf3)

### Executive Forecasting Projections
- **FY 2026 Forecast Revenue:** **$17,164,139.08** (+17.2% top-line projected expansion)
- **Model Accuracy (Holdout Test):** **93.97% Accuracy** (6.03% MAPE across 184 test days)
- **Top Regression Model R2:** **0.7629** (Ridge Regularization with engineered lag and rolling window features)
- **95% Confidence Interval:** Annual bounds statistically constrained to **$16.14M (Lower)** - **$18.18M (Upper)**
- **Scenario Planning:** Bull Case yields **$19.22M (+25.0%)**, Bear Case maintains **$15.45M (+8.0%)**

### Deliverables Included:
1. **Interactive Forecasting Studio:** Dynamic Streamlit application (`streamlit_forecasting_app.py`) with model selection, scenario toggling, and 95% confidence interval bands.
2. **Standalone Web Dashboard:** Zero-dependency web application (`index.html`) using Vanilla JavaScript and Chart.js with interactive time series trajectories and scenario slicers.
3. **Pre-Executed Jupyter Notebook:** [`03_predictive_forecasting_modeling.ipynb`](./Week%2003%20-%20Predictive%20Analytics%20Using%20Historical%20Data/notebooks/03_predictive_forecasting_modeling.ipynb) featuring lag engineering, chronological splits, model evaluations, and forward forecasts.
4. **Predictive Engine Pipeline:** Production script (`predictive_engine.py`) automating feature pipelines, multi-model evaluation, and 12-month projections.
5. **C-Level Forecasting Report:** [`Predictive_Forecasting_Report.md`](./Week%2003%20-%20Predictive%20Analytics%20Using%20Historical%20Data/reports/Predictive_Forecasting_Report.md) detailing accuracy metrics, seasonal components, and economic scenario modeling.

![Predictive Forecasting Preview](./Week%2003%20-%20Predictive%20Analytics%20Using%20Historical%20Data/reports/assets/forecasting_executive_summary_card.png)

---

## Week 2 Highlights: Customer Segmentation Project

> **Project Directory:** [`Week 02 - Customer Segmentation Project/`](./Week%2002%20-%20Customer%20Segmentation%20Project/)  
> **Tutorial Reference:** [YouTube Tutorial Guide](https://youtu.be/-LGwdrajMZ0?si=ci95cNWGApC8WKqF)

### Customer Behavioral Personas Uncovered
- **VIP Champions (18.0%):** Top spenders ($18,372/yr average spend) generating **41.1% of enterprise revenue** with 14.2 days recency.
- **Loyal Mainstream (31.0%):** Core steady account base ($7,560/yr spend) driving consistent volume across regions.
- **Emerging Tech Lovers (17.0%):** Younger high-velocity gadget adopters ($8,757/yr spend, 24.5 web visits/month).
- **Bargain Hunters (22.6%):** Price-sensitive deal seekers ($2,080/yr spend) responsive to clearance campaigns.
- **At-Risk / Lapsed (11.6%):** Dormant high-potential customers (210.8 days recency) targeted for win-back reactivation.

### Deliverables Included:
1. **Interactive Segmentation Studio:** Dynamic Streamlit application (`streamlit_segmentation_app.py`) with real-time cluster tuning ($k \in [2, 8]$) and Plotly 2D/3D scatter plots.
2. **Standalone Web Dashboard:** Zero-dependency web application (`index.html`) using Vanilla JavaScript and Chart.js featuring interactive 2D PCA cluster maps, income vs spending score projections, and customer search.
3. **Pre-Executed Jupyter Notebook:** [`02_customer_segmentation_clustering.ipynb`](./Week%2002%20-%20Customer%20Segmentation%20Project/notebooks/02_customer_segmentation_clustering.ipynb) with pre-rendered Elbow method, Silhouette score curves, PCA, and RFM boxplots.
4. **Machine Learning Pipeline:** End-to-end `scikit-learn` script (`segmentation_engine.py`) automating scaling, K-Means, and PCA dimensionality reduction (82.5% variance explained).
5. **Strategic Marketing Playbook:** [`Customer_Segmentation_Strategy_Report.md`](./Week%2002%20-%20Customer%20Segmentation%20Project/reports/Customer_Segmentation_Strategy_Report.md) outlining targeted multi-channel campaigns.

![Customer Segmentation Preview](./Week%2002%20-%20Customer%20Segmentation%20Project/reports/assets/cluster_executive_summary_card.png)

---

## Week 1 Highlights: Sales & Revenue Analysis Dashboard

> **Project Directory:** [`Week 01 - Sales & Revenue Analysis Dashboard/`](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/)  
> **Tutorial Reference:** [YouTube Tutorial Guide](https://youtu.be/hhZ6EDiVboI?si=pcC3NkRkvTbOmbUK)

### Executive Metrics Summary
- **Total Net Revenue Analyzed:** **$5,649,578.26**
- **Net Operating Profit:** **$1,913,734.76** (Operating Margin: **33.87%**)
- **Transactions Audited:** **3,500 enterprise orders** across 450 unique corporate clients
- **Year-over-Year Growth:** **+17.65% top-line expansion**

### Deliverables Included:
1. **Interactive Web Dashboard:** Zero-dependency, modern dark-themed web application (`index.html`) using Vanilla JavaScript and Chart.js.
2. **Streamlit Analytics App:** Full-fledged Python dashboard (`streamlit_app.py`) with Plotly interactive graphics.
3. **Pre-Executed Jupyter Notebook:** [`01_sales_revenue_eda_and_kpis.ipynb`](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/notebooks/01_sales_revenue_eda_and_kpis.ipynb).
4. **Multi-Source Data Architecture:** Raw and cleaned datasets in CSV, multi-sheet Excel, and SQLite database formats.
5. **C-Level Executive Strategy Report:** [`Executive_Sales_Insights_Report.md`](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/reports/Executive_Sales_Insights_Report.md).

![Executive KPI Preview](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/reports/assets/kpi_summary_dashboard.png)

---

## Technology Stack & Libraries

- **Programming & Scripting:** Python 3.12, JavaScript (ES6+), HTML5, CSS3
- **Data Engineering & Manipulation:** Pandas, NumPy, OpenPyXL, XlsxWriter, SQLite3
- **Data Visualization & BI:** Matplotlib, Seaborn, Plotly Express, Chart.js
- **Web Application Frameworks:** Streamlit, Vanilla Web Platform (Zero dependencies)
- **Notebook & Reporting:** Jupyter Notebook (nbformat / nbconvert), Markdown

---

## Quickstart & Evaluation Instructions

### 1. View the Standalone Web Dashboard (Instant)
Simply open the following file in Google Chrome, Microsoft Edge, or Mozilla Firefox:
```text
Week 01 - Sales & Revenue Analysis Dashboard/dashboard/web_dashboard/index.html
```

### 2. Run the Streamlit Dashboard
```bash
# Clone the repository
git clone <YOUR_GITHUB_REPO_URL>
cd "DA Internship"

# Install requirements
pip install -r requirements.txt

# Launch interactive Streamlit application
streamlit run "Week 01 - Sales & Revenue Analysis Dashboard/dashboard/streamlit_app.py"
```

### 3. Inspect the Jupyter Notebook
Open [`Week 01 - Sales & Revenue Analysis Dashboard/notebooks/01_sales_revenue_eda_and_kpis.ipynb`](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/notebooks/01_sales_revenue_eda_and_kpis.ipynb) directly in GitHub or VS Code / Jupyter Lab to review all pre-rendered charts and statistical tables.

---

## Author
**Data Analytics Intern**  
*Repository maintained week-by-week for internship milestone verification and evaluation.*
