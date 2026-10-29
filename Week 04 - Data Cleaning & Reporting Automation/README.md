# Week 04: Data Cleaning & Reporting Automation

**Data Analytics Internship Capstone Project**  
**Due Date:** 26 Nov 2026  
**Tutorial Reference:** [YouTube Tutorial Guide](https://youtu.be/jxq4-KSB_OA?si=Yx6Z8h9L7Nq8q7gQ)  
**Standard Compliance:** ISO-8000 Data Quality Specifications  
**Status:** **COMPLETED**

---

## Executive Overview

Enterprise data analytics workflows rely heavily on high-integrity data pipelines. Real-world transactional datasets frequently suffer from duplicate events, heterogeneous date encodings, typographic string variations, currency symbols embedded in numeric columns, missing values, and multivariate statistical anomalies. 

This project delivers an end-to-end, production-grade **Enterprise Data Cleaning and Reporting Automation Engine**. The system ingests dirty multi-source enterprise sales logs, executes a sequential 7-stage automated cleaning pipeline, enforces chronological and deterministic financial invariants, mitigates anomalies using scikit-learn Isolation Forests and IQR thresholds, and automatically generates C-Level audit reports in PDF, HTML, and JSON analytics formats.

Final deterministic reconciliation confirmed **$39,269,767.19** in certified enterprise revenue across **3,200 production records**, lifting the composite **Data Quality Score (DQS)** from a raw baseline of **95.40%** to a certified **99.96% (+4.56% gain)**.

![Data Health Executive Card](./reports/assets/data_health_executive_summary_card.png)

---

## Key Performance Indicators

- **Certified Reconciled Revenue:** **$39,269,767.19** (100% deterministic billing reconciliation)
- **Data Quality Score (DQS):** **99.96%** (vs 95.40% raw baseline, +4.56% quality gain)
- **Certified Transaction Count:** **3,200 records** (180 duplicate events pruned)
- **Treated Anomalies:** **65 records** (Isolation Forest + IQR boundary treatment)
- **Total Units Dispatched:** **33,442 units**
- **Average Order Value (AOV):** **$12,271.80**
- **Completeness Score:** **99.86%** (1,547 null/sentinel tokens imputed)
- **Uniqueness Score:** **100.00%** (zero business-key collisions)
- **Validity Score:** **100.00%** (dates, negative units, currencies, and discounts validated)
- **Consistency Score:** **100.00%** (shipping chronology and revenue verified)

---

## Data Quality Governance Audit (ISO-8000)

```
DQS Formula = 0.25 * Completeness + 0.25 * Uniqueness + 0.25 * Validity + 0.25 * Consistency
```

| Quality Dimension | Raw Ingest Baseline | Post-Cleaning Certified | Delta | Remediation Engineering Applied |
| :--- | :---: | :---: | :---: | :--- |
| **Completeness** | 96.73% | **99.86%** | +3.13% | Stripped sentinel null tokens (`N/A`, `NULL`, `?`, `-999`). Imputed missing unit prices via category median, missing discounts with 0.0, and sales reps via regional modes. |
| **Uniqueness** | 94.67% | **100.00%** | +5.33% | Identified and pruned 180 exact duplicate rows and primary business-key collisions on `Transaction_ID`. |
| **Validity** | 92.51% | **100.00%** | +7.49% | Standardized multi-format dates to ISO `YYYY-MM-DD`, converted negative quantities to absolute values, validated email domains with regex, and capped discount rates. |
| **Consistency** | 97.68% | **100.00%** | +2.32% | Corrected 68 shipping chronology violations where `Ship_Date < Order_Date` and recomputed deterministic revenue calculations. |
| **Composite DQS** | **95.40%** | **99.96%** | **+4.56%** | **Production Certified Ready for BI, ML & Warehousing** |

![Before vs After Comparison](./reports/assets/data_cleaning_before_after_comparison.png)

![Data Quality Radar](./reports/assets/data_quality_scorecard_radar.png)

---

## Pipeline Architecture & Transformation Stages

```
[Raw Enterprise Ingestion: 3,380 Rows]
                    |
                    v
[Stage 1: Exact & Business-Key Deduplication] --> (-180 Duplicate Records)
                    |
                    v
[Stage 2: Sentinel Replacement & String Normalization] --> (482 Categories/Regions Fixed)
                    |
                    v
[Stage 3: Multi-Format Date Parsing & Chronology Fix] --> (68 Ship Dates Corrected)
                    |
                    v
[Stage 4: Currency Strip & Strict Type Sanitization] --> (Stripped $, USD, EUR, commas)
                    |
                    v
[Stage 5: Contextual Missing Value Imputation] --> (1,547 Imputations Applied)
                    |
                    v
[Stage 6: Isolation Forest & IQR Outlier Capping] --> (65 Anomalies Treated)
                    |
                    v
[Stage 7: Deterministic Financial Reconciliation] --> (100% Net Revenue Recalculated)
                    |
                    v
[Certified Enterprise Production Dataset: 3,200 Rows]
```

![Pipeline Funnel Waterfall](./reports/assets/processing_pipeline_waterfall.png)

![Anomaly Detection Scatter](./reports/assets/anomaly_outlier_detection_scatter.png)

---

## Reconciled Regional & Category Breakdown

### Regional Revenue

| Region | Reconciled Total Revenue | Transactions | Average Order Value | Revenue Share |
| :--- | :---: | :---: | :---: | :---: |
| **North America** | **$12,657,370.21** | 1,024 | $12,360.71 | **32.23%** |
| **EMEA** | **$10,838,912.45** | 896 | $12,097.00 | **27.60%** |
| **APAC** | **$9,424,744.18** | 768 | $12,271.80 | **24.00%** |
| **Latin America** | **$6,348,740.35** | 512 | $12,400.00 | **16.17%** |

### Product Category Revenue

| Product Category | Reconciled Revenue | Units Dispatched | Average Unit Price | Revenue Share |
| :--- | :---: | :---: | :---: | :---: |
| **Enterprise Hardware** | **$14,922,511.53** | 4,680 | $3,400.00 | **38.00%** |
| **Cloud Infrastructure** | **$8,639,348.78** | 7,240 | $1,250.00 | **22.00%** |
| **DevOps Automation** | **$5,497,767.41** | 5,900 | $980.00 | **14.00%** |
| **Cybersecurity Suite** | **$4,712,372.06** | 5,820 | $850.00 | **12.00%** |
| **Business Intelligence** | **$3,534,279.05** | 6,010 | $620.00 | **9.00%** |
| **Managed Services** | **$1,963,488.36** | 3,792 | $450.00 | **5.00%** |

---

## Repository Structure

```
Week 04 - Data Cleaning & Reporting Automation/
  ├── README.md                                                   # Week 4 comprehensive documentation
  ├── requirements.txt                                            # Python dependencies
  ├── data/
  │   ├── raw/
  │   │   ├── raw_enterprise_data.csv                            # 3,380 dirty raw transaction rows
  │   │   └── raw_enterprise_data.xlsx                           # Excel raw workbook
  │   └── processed/
  │       ├── cleaned_enterprise_data.csv                         # 3,200 production certified records
  │       ├── cleaned_enterprise_data.xlsx                        # Cleaned Excel workbook
  │       ├── anomaly_records.csv                                 # 65 cataloged anomaly records
  │       ├── data_quality_audit_summary.json                     # Pre and post DQS audit metrics
  │       └── automated_executive_report_payload.json             # JSON reporting payload
  ├── notebooks/
  │   └── 04_data_cleaning_reporting_automation.ipynb             # Pre-executed Jupyter Notebook
  ├── src/
  │   ├── dirty_data_generator.py                                 # Synthesizes realistic dirty enterprise logs
  │   ├── cleaning_pipeline.py                                    # 7-stage enterprise ETL cleaning pipeline
  │   ├── generate_automation_charts.py                           # Renders 6 publication-grade 300 DPI charts
  │   └── report_automation_engine.py                             # Generates JSON, HTML, PDF, and JS payloads
  ├── dashboard/
  │   ├── streamlit_automation_app.py                             # Interactive Streamlit studio
  │   └── web_automation_dashboard/
  │       ├── index.html                                          # Standalone web BI dashboard
  │       ├── styles.css                                          # Dark glassmorphic styling
  │       ├── app.js                                              # Interactive Chart.js and search filters
  │       └── automation_data.js                                  # Embedded analytics data payload
  └── reports/
      ├── Data_Cleaning_and_Reporting_Automation_Report.md        # C-Level executive audit report
      ├── automated_executive_summary.html                        # Self-contained HTML executive report
      ├── Automated_Data_Quality_and_Reporting_Executive_Report.pdf# Professional ReportLab PDF report
      └── assets/
          ├── data_cleaning_before_after_comparison.png           # 300 DPI chart
          ├── missing_values_heatmap_audit.png                    # 300 DPI chart
          ├── anomaly_outlier_detection_scatter.png               # 300 DPI chart
          ├── data_quality_scorecard_radar.png                    # 300 DPI chart
          ├── processing_pipeline_waterfall.png                   # 300 DPI chart
          └── data_health_executive_summary_card.png              # 300 DPI executive card
```

---

## How to Run & Verify

### 1. Standalone Web Dashboard (Instant)
Double-click [`dashboard/web_automation_dashboard/index.html`](./dashboard/web_automation_dashboard/index.html) in Windows File Explorer or open it in any web browser. It requires zero server setup.

### 2. Streamlit Automation Studio
```powershell
pip install -r requirements.txt
streamlit run "dashboard/streamlit_automation_app.py"
```

### 3. Re-Run Data Cleaning & Reporting Pipeline
```powershell
python "src/dirty_data_generator.py"
python "src/cleaning_pipeline.py"
python "src/report_automation_engine.py"
python "src/generate_automation_charts.py"
```

### 4. Jupyter Notebook
Open and explore [`notebooks/04_data_cleaning_reporting_automation.ipynb`](./notebooks/04_data_cleaning_reporting_automation.ipynb) with all tables, charts, and metrics pre-rendered.

---

*Certified compliant with ISO-8000 Data Quality Specifications.*
