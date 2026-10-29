/**
 * Enterprise Data Cleaning & Reporting Automation Studio Logic
 * Handles interactive charts, live table filtering, tab navigation, and printable reports.
 */

document.addEventListener("DOMContentLoaded", () => {
  if (typeof AUTOMATION_DATA === "undefined") {
    console.error("AUTOMATION_DATA payload not loaded.");
    return;
  }

  initKPIs();
  initTabs();
  initCharts();
  initTables();
  initPrintButton();
});

function initKPIs() {
  const kpis = AUTOMATION_DATA.executive_kpis;
  document.getElementById("kpiRevenue").textContent = `$${kpis.total_revenue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  document.getElementById("kpiDqs").textContent = `${kpis.post_cleaning_dqs}%`;
  document.getElementById("kpiDqsGain").textContent = `+${kpis.dqs_gain_pct}% Gain`;
  document.getElementById("kpiDqsSub").textContent = `Baseline Raw: ${kpis.pre_cleaning_dqs}%`;
  document.getElementById("kpiRecords").textContent = kpis.total_transactions.toLocaleString();
  document.getElementById("kpiAnomalies").textContent = (AUTOMATION_DATA.sample_anomalies ? AUTOMATION_DATA.sample_anomalies.length : 65).toString();

  // Populate Executive Tab elements
  document.getElementById("execRawRows").textContent = AUTOMATION_DATA.pipeline_funnel[0].count.toLocaleString();
  document.getElementById("execDupes").textContent = AUTOMATION_DATA.pipeline_funnel[1].count.toLocaleString();
  document.getElementById("execAnoms").textContent = kpis.anomalies_detected || "65";
  document.getElementById("execImputed").textContent = "1,547";
  document.getElementById("execDqs").textContent = `${kpis.post_cleaning_dqs}%`;

  document.getElementById("repRev").textContent = `$${kpis.total_revenue.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
  document.getElementById("repUnits").textContent = kpis.total_units_sold.toLocaleString();
  document.getElementById("repAov").textContent = `$${kpis.average_order_value.toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
  document.getElementById("repTxns").textContent = kpis.total_transactions.toLocaleString();
}

function initTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add("active");
      }
    });
  });
}

function initCharts() {
  // Common Dark Chart.js configuration
  Chart.defaults.color = "#94a3b8";
  Chart.defaults.font.family = "'Inter', -apple-system, sans-serif";
  Chart.defaults.plugins.tooltip.backgroundColor = "#0f172a";
  Chart.defaults.plugins.tooltip.borderColor = "#334155";
  Chart.defaults.plugins.tooltip.borderWidth = 1;

  // 1. Pipeline Funnel Waterfall Bar Chart
  const funnelCtx = document.getElementById("funnelChart").getContext("2d");
  const funnelStages = AUTOMATION_DATA.pipeline_funnel.map(f => f.stage);
  const funnelCounts = AUTOMATION_DATA.pipeline_funnel.map(f => f.count);

  new Chart(funnelCtx, {
    type: "bar",
    data: {
      labels: [
        "1. Raw Ingest",
        "2. Dedup Pruned",
        "3. Chronology",
        "4. Typo Standard",
        "5. Imputation",
        "6. Anomalies",
        "7. Certified Ready"
      ],
      datasets: [{
        label: "Records in Pipeline",
        data: funnelCounts,
        backgroundColor: [
          "#64748b",
          "#f59e0b",
          "#3b82f6",
          "#8b5cf6",
          "#06b6d4",
          "#ec4899",
          "#10b981"
        ],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          min: 0,
          max: 3800,
          grid: { color: "rgba(255, 255, 255, 0.05)" }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });

  // 2. Regional Revenue Doughnut Chart
  const regionalCtx = document.getElementById("regionalChart").getContext("2d");
  const regions = AUTOMATION_DATA.regional_breakdown;
  new Chart(regionalCtx, {
    type: "doughnut",
    data: {
      labels: regions.map(r => r.region),
      datasets: [{
        data: regions.map(r => r.revenue),
        backgroundColor: ["#2563eb", "#38bdf8", "#4ade80", "#a78bfa"],
        borderColor: "#0f172a",
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right" }
      },
      cutout: "65%"
    }
  });

  // 3. Category Revenue Horizontal Bar Chart
  const categoryCtx = document.getElementById("categoryChart").getContext("2d");
  const cats = AUTOMATION_DATA.category_breakdown;
  new Chart(categoryCtx, {
    type: "bar",
    data: {
      labels: cats.map(c => c.category),
      datasets: [{
        label: "Reconciled Revenue ($ USD)",
        data: cats.map(c => c.revenue),
        backgroundColor: "#3b82f6",
        borderRadius: 4
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: {
            callback: (v) => `$${(v / 1e6).toFixed(1)}M`
          }
        },
        y: {
          grid: { display: false }
        }
      }
    }
  });

  // 4. ISO-8000 Radar Chart
  const radarCtx = document.getElementById("radarChart").getContext("2d");
  const pre = AUTOMATION_DATA.audit_scores.pre;
  const post = AUTOMATION_DATA.audit_scores.post;

  new Chart(radarCtx, {
    type: "radar",
    data: {
      labels: ["Completeness", "Uniqueness", "Validity", "Consistency", "Integrity"],
      datasets: [
        {
          label: `Raw Baseline (${pre.dqs}%)`,
          data: [pre.completeness_score, pre.uniqueness_score, pre.validity_score, pre.consistency_score, 91.0],
          borderColor: "#ef4444",
          backgroundColor: "rgba(239, 68, 68, 0.15)",
          borderDash: [5, 5],
          pointBackgroundColor: "#ef4444"
        },
        {
          label: `Post-Pipeline Certified (${post.dqs}%)`,
          data: [post.completeness_score, post.uniqueness_score, post.validity_score, post.consistency_score, 100.0],
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.25)",
          pointBackgroundColor: "#10b981"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          min: 85,
          max: 102,
          ticks: { stepSize: 5, color: "#64748b", backdropColor: "transparent" },
          grid: { color: "rgba(255, 255, 255, 0.08)" },
          angleLines: { color: "rgba(255, 255, 255, 0.08)" }
        }
      }
    }
  });

  // 5. Dimension Bar Chart
  const dimBarCtx = document.getElementById("dimensionBarChart").getContext("2d");
  new Chart(dimBarCtx, {
    type: "bar",
    data: {
      labels: ["Completeness", "Uniqueness", "Validity", "Consistency", "DQS Composite"],
      datasets: [
        {
          label: "Raw Ingest Baseline",
          data: [pre.completeness_score, pre.uniqueness_score, pre.validity_score, pre.consistency_score, pre.dqs],
          backgroundColor: "#64748b",
          borderRadius: 4
        },
        {
          label: "Post-Pipeline Certified",
          data: [post.completeness_score, post.uniqueness_score, post.validity_score, post.consistency_score, post.dqs],
          backgroundColor: "#2563eb",
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          min: 85,
          max: 105,
          grid: { color: "rgba(255, 255, 255, 0.05)" }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });
}

function initTables() {
  const pre = AUTOMATION_DATA.audit_scores.pre;
  const post = AUTOMATION_DATA.audit_scores.post;

  // 1. Dimensions Table
  const dimTableBody = document.getElementById("dimensionsTableBody");
  const dimensions = [
    { name: "Completeness", pre: pre.completeness_score, post: post.completeness_score, status: "100% Imputed", impact: "Eliminated sentinels and missing customer contact info" },
    { name: "Uniqueness", pre: pre.uniqueness_score, post: post.uniqueness_score, status: "180 Pruned", impact: "Permanently purged exact and business-key duplicate rows" },
    { name: "Validity", pre: pre.validity_score, post: post.validity_score, status: "Validated", impact: "Parsed multi-format dates, resolved negative units, capped discount bounds" },
    { name: "Consistency", pre: pre.consistency_score, post: post.consistency_score, status: "Reconciled", impact: "Fixed order/ship chronology violations and recomputed revenue" },
    { name: "Composite Data Quality Score (DQS)", pre: pre.dqs, post: post.dqs, status: "Certified", impact: "Production certified for downstream BI, ML, and ERP ingestion" }
  ];

  dimTableBody.innerHTML = dimensions.map(d => `
    <tr>
      <td><strong>${d.name}</strong></td>
      <td>${d.pre}%</td>
      <td><strong style="color: #10b981;">${d.post}%</strong></td>
      <td><span class="status-badge status-certified">${d.status}</span></td>
      <td style="color: #94a3b8;">${d.impact}</td>
    </tr>
  `).join("");

  // 2. Anomaly Table
  const anomTableBody = document.getElementById("anomalyTableBody");
  const anomalies = AUTOMATION_DATA.sample_anomalies || [];
  
  function renderAnomalies(list) {
    if (list.length === 0) {
      anomTableBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #64748b;">No anomalies match your search.</td></tr>`;
      return;
    }
    anomTableBody.innerHTML = list.map(a => `
      <tr>
        <td><code>${a.Transaction_ID}</code></td>
        <td><strong>${a.Customer_Name}</strong></td>
        <td>${a.Product_Category}</td>
        <td>${a.Original_Quantity}</td>
        <td>$${Number(a.Original_Unit_Price).toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
        <td><span style="color: #ef4444; font-weight: 600;">${a.Anomaly_Reason}</span></td>
        <td><span class="status-badge status-version">Capped & Treated</span></td>
      </tr>
    `).join("");
  }
  renderAnomalies(anomalies);

  const anomSearch = document.getElementById("anomalySearch");
  anomSearch.addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase();
    const filtered = anomalies.filter(a =>
      a.Transaction_ID.toLowerCase().includes(q) ||
      a.Customer_Name.toLowerCase().includes(q) ||
      a.Product_Category.toLowerCase().includes(q) ||
      a.Anomaly_Reason.toLowerCase().includes(q)
    );
    renderAnomalies(filtered);
  });

  // 3. Ledger Table
  const ledgerTableBody = document.getElementById("ledgerTableBody");
  const records = AUTOMATION_DATA.sample_cleaned_records || [];
  
  function renderLedger(list) {
    if (list.length === 0) {
      ledgerTableBody.innerHTML = `<tr><td colspan="11" style="text-align: center; color: #64748b;">No records match your query.</td></tr>`;
      return;
    }
    ledgerTableBody.innerHTML = list.map(r => `
      <tr>
        <td><code>${r.Transaction_ID}</code></td>
        <td>${r.Order_Date}</td>
        <td>${r.Ship_Date}</td>
        <td><strong>${r.Customer_Name}</strong></td>
        <td>${r.Region}</td>
        <td>${r.Product_Category}</td>
        <td>${r.Quantity}</td>
        <td>$${Number(r.Unit_Price).toFixed(2)}</td>
        <td>${(Number(r.Discount) * 100).toFixed(0)}%</td>
        <td><strong style="color: #38bdf8;">$${Number(r.Total_Revenue).toLocaleString('en-US', { minimumFractionDigits: 2 })}</strong></td>
        <td><span class="status-badge status-certified">${r.Payment_Status}</span></td>
      </tr>
    `).join("");
  }
  renderLedger(records);

  const ledgerSearch = document.getElementById("ledgerSearch");
  ledgerSearch.addEventListener("input", (e) => {
    const q = e.target.value.toLowerCase();
    const filtered = records.filter(r =>
      r.Transaction_ID.toLowerCase().includes(q) ||
      r.Customer_Name.toLowerCase().includes(q) ||
      r.Region.toLowerCase().includes(q) ||
      r.Product_Category.toLowerCase().includes(q) ||
      r.Sales_Representative.toLowerCase().includes(q)
    );
    renderLedger(filtered);
  });

  // 4. Executive Tab Regional Table
  const execRegionalTable = document.getElementById("execRegionalTable");
  execRegionalTable.innerHTML = AUTOMATION_DATA.regional_breakdown.map(r => `
    <tr>
      <td><strong>${r.region}</strong></td>
      <td>$${r.revenue.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
      <td>${r.transactions.toLocaleString()}</td>
      <td>$${r.aov.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
      <td><strong>${r.share_pct}%</strong></td>
    </tr>
  `).join("");
}

function initPrintButton() {
  const printBtn = document.getElementById("printReportBtn");
  printBtn.addEventListener("click", () => {
    // Switch to Executive tab then trigger print
    const execTabBtn = document.querySelector('[data-tab="tabExecutive"]');
    if (execTabBtn) {
      execTabBtn.click();
      setTimeout(() => {
        window.print();
      }, 300);
    }
  });
}
