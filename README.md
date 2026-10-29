# 💼 Data Analytics Internship Portfolio

Welcome to the official portfolio repository for the **Data Analytics Internship**. This repository tracks all project milestones, datasets, analytical notebooks, executive dashboards, and codebases structured on a strict **week-by-week** progression.

---

## 📅 4-Week Internship Project Roadmap

| Week | Milestone / Project Name | Key Methodologies & Tools | Due Date | Status |
| :---: | :--- | :--- | :---: | :---: |
| **01** | [**Sales & Revenue Analysis Dashboard**](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/) | Multi-source Ingestion, KPI Tracking, Streamlit & Web BI | **05 Nov 2026** | **✅ COMPLETED** |
| **02** | **Customer Segmentation Project** | RFM Modeling, K-Means Clustering, Scikit-Learn | **12 Nov 2026** | ⏳ Scheduled |
| **03** | **Predictive Analytics Using Historical Data** | Time Series Forecasting, Regression, Model Evaluation | **19 Nov 2026** | ⏳ Scheduled |
| **04** | **Data Cleaning & Reporting Automation** | Automated Workflows, Anomaly Detection, PDF Reports | **26 Nov 2026** | ⏳ Scheduled |

---

## 🌟 Week 1 Highlights: Sales & Revenue Analysis Dashboard

> **Project Directory:** [`Week 01 - Sales & Revenue Analysis Dashboard/`](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/)  
> **Tutorial Reference:** [YouTube Tutorial Guide](https://youtu.be/hhZ6EDiVboI?si=pcC3NkRkvTbOmbUK)

### Executive Metrics Summary
- **Total Net Revenue Analyzed:** **$5,649,578.26**
- **Net Operating Profit:** **$1,913,734.76** (Operating Margin: **33.87%**)
- **Transactions Audited:** **3,500 enterprise orders** across 450 unique corporate clients
- **Year-over-Year Growth:** **+17.65% top-line expansion**

### Deliverables Included:
1. **Interactive Web Dashboard:** Zero-dependency, modern dark-themed web application (`index.html`) using Vanilla JavaScript and Chart.js. Opens natively in any web browser with live slicers (Year, Region, Category, Segment) and instant CSV export.
2. **Streamlit Analytics App:** Full-fledged Python dashboard (`streamlit_app.py`) with Plotly interactive graphics and custom CSV/Excel upload support.
3. **Pre-Executed Jupyter Notebook:** [`01_sales_revenue_eda_and_kpis.ipynb`](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/notebooks/01_sales_revenue_eda_and_kpis.ipynb) containing comprehensive EDA, null audits, calendar feature engineering, and statistical visualizations.
4. **Multi-Source Data Architecture:** Raw and cleaned datasets in CSV, multi-sheet Excel, and SQLite database formats.
5. **C-Level Executive Strategy Report:** [`Executive_Sales_Insights_Report.md`](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/reports/Executive_Sales_Insights_Report.md) with data-backed business insights on discount sensitivity, category performance, and geographic expansion.

![Executive KPI Preview](./Week%2001%20-%20Sales%20%26%20Revenue%20Analysis%20Dashboard/reports/assets/kpi_summary_dashboard.png)

---

## 🛠️ Technology Stack & Libraries

- **Programming & Scripting:** Python 3.12, JavaScript (ES6+), HTML5, CSS3
- **Data Engineering & Manipulation:** Pandas, NumPy, OpenPyXL, XlsxWriter, SQLite3
- **Data Visualization & BI:** Matplotlib, Seaborn, Plotly Express, Chart.js
- **Web Application Frameworks:** Streamlit, Vanilla Web Platform (Zero dependencies)
- **Notebook & Reporting:** Jupyter Notebook (nbformat / nbconvert), Markdown

---

## 🚀 Quickstart & Evaluation Instructions

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

## 👤 Author
**Data Analytics Intern**  
*Repository maintained week-by-week for internship milestone verification and evaluation.*
