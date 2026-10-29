/**
 * Predictive Analytics & Forecasting Studio - Application Logic
 * Pure Vanilla JavaScript with dynamic Chart.js instances, confidence intervals, and scenario simulations.
 * Zero emojis for clean corporate formatting.
 */

let currentFilteredDaily = [];
let currentPage = 1;
const rowsPerPage = 12;

let charts = {
  trajectory: null,
  modelComp: null,
  features: null,
  seasonality: null
};

document.addEventListener("DOMContentLoaded", () => {
  if (typeof forecastMasterData === "undefined" || !forecastMasterData.dailyForecast) {
    console.error("forecastMasterData failed to load.");
    return;
  }

  currentFilteredDaily = [...forecastMasterData.dailyForecast];

  initEventListeners();
  applyFiltersAndRender();
});

function initEventListeners() {
  document.getElementById("scenarioFilter").addEventListener("change", applyFiltersAndRender);
  document.getElementById("modelFilter").addEventListener("change", applyFiltersAndRender);
  document.getElementById("horizonFilter").addEventListener("change", applyFiltersAndRender);

  document.getElementById("resetFiltersBtn").addEventListener("click", () => {
    document.getElementById("scenarioFilter").value = "Base";
    document.getElementById("modelFilter").value = "Ensemble";
    document.getElementById("horizonFilter").value = "Full";
    document.getElementById("tableSearchInput").value = "";
    applyFiltersAndRender();
  });

  document.getElementById("tableSearchInput").addEventListener("input", () => {
    currentPage = 1;
    renderTable();
  });

  document.getElementById("prevPageBtn").addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      renderTable();
    }
  });

  document.getElementById("nextPageBtn").addEventListener("click", () => {
    const totalPages = Math.ceil(getSearchedData().length / rowsPerPage);
    if (currentPage < totalPages) {
      currentPage++;
      renderTable();
    }
  });

  document.getElementById("exportCsvBtn").addEventListener("click", exportForecastCSV);

  document.getElementById("printReportBtn").addEventListener("click", () => {
    window.print();
  });

  const themeToggle = document.getElementById("themeToggleBtn");
  themeToggle.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark-theme");
    document.body.classList.toggle("light-theme", !isDark);
    themeToggle.innerHTML = isDark ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
    renderAllCharts();
  });
}

function applyFiltersAndRender() {
  const scenario = document.getElementById("scenarioFilter").value;
  const horizon = document.getElementById("horizonFilter").value;

  currentFilteredDaily = forecastMasterData.dailyForecast.filter(d => {
    const dt = new Date(d.Date);
    const month = dt.getMonth() + 1; // 1-12
    if (horizon === "H1" && month > 6) return false;
    if (horizon === "Q4" && month < 10) return false;
    return true;
  });

  currentPage = 1;
  updateKPIs(scenario);
  renderAllCharts(scenario);
  renderTable(scenario);
}

function updateKPIs(scenario) {
  let multiplier = 1.0;
  let growth = 17.2;

  if (scenario === "Bull") {
    multiplier = 1.12;
    growth = 25.0;
  } else if (scenario === "Bear") {
    multiplier = 0.90;
    growth = 8.0;
  }

  const baseTotal = currentFilteredDaily.reduce((acc, cur) => acc + cur.Predicted_Revenue, 0);
  const totalRev = Math.round(baseTotal * multiplier);

  document.getElementById("kpiForecastRev").innerText = "$" + totalRev.toLocaleString();
  document.getElementById("kpiGrowthBadge").innerText = `+${growth.toFixed(1)}% YoY`;
}

function getChartTheme() {
  const isDark = document.body.classList.contains("dark-theme");
  return {
    textColor: isDark ? "#94A3B8" : "#475569",
    gridColor: isDark ? "rgba(255, 255, 255, 0.05)" : "rgba(0, 0, 0, 0.05)",
    fontFamily: "'Plus Jakarta Sans', sans-serif"
  };
}

function renderAllCharts(scenario) {
  const theme = getChartTheme();
  Chart.defaults.color = theme.textColor;
  Chart.defaults.font.family = theme.fontFamily;

  renderTrajectoryChart(theme, scenario);
  renderModelComparison(theme);
  renderFeatureImportance(theme);
  renderSeasonalityChart(theme);
}

// 1. Historical & 12M Out-of-Sample Forecast
function renderTrajectoryChart(theme, scenario) {
  const ctx = document.getElementById("forecastTrajectoryChart").getContext("2d");
  if (charts.trajectory) charts.trajectory.destroy();

  const history = forecastMasterData.monthlyHistory;
  const forecast = forecastMasterData.monthlyForecast;

  const labels = [];
  const histData = [];
  const foreData = [];
  const upperData = [];
  const lowerData = [];

  let mult = scenario === "Bull" ? 1.12 : scenario === "Bear" ? 0.90 : 1.0;

  history.forEach(h => {
    labels.push(h.Month);
    histData.push(Math.round(h.Revenue));
    foreData.push(null);
    upperData.push(null);
    lowerData.push(null);
  });

  // Connect last point of history to first point of forecast
  const lastHist = histData[histData.length - 1];

  forecast.forEach((f, idx) => {
    labels.push(f.Month);
    histData.push(null);
    const val = Math.round(f.Projected_Revenue * mult);
    foreData.push(val);
    upperData.push(Math.round(f.Upper_Bound * mult));
    lowerData.push(Math.round(f.Lower_Bound * mult));
  });

  charts.trajectory = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Historical Actuals ($)",
          data: histData,
          borderColor: "#3B82F6",
          backgroundColor: "rgba(59, 130, 246, 0.1)",
          borderWidth: 2.5,
          tension: 0.3,
          pointRadius: 2
        },
        {
          label: "Projected Forecast ($)",
          data: foreData,
          borderColor: "#10B981",
          borderDash: [5, 4],
          borderWidth: 2.5,
          tension: 0.3,
          pointRadius: 3
        },
        {
          label: "Upper 95% Bound",
          data: upperData,
          borderColor: "rgba(245, 158, 11, 0.4)",
          borderWidth: 1,
          pointRadius: 0,
          fill: false
        },
        {
          label: "Lower 95% Bound",
          data: lowerData,
          borderColor: "rgba(239, 68, 68, 0.4)",
          backgroundColor: "rgba(16, 185, 129, 0.08)",
          borderWidth: 1,
          pointRadius: 0,
          fill: "-1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: "index",
          intersect: false,
          callbacks: {
            label: (ctx) => ctx.parsed.y ? ` ${ctx.dataset.label}: $${ctx.parsed.y.toLocaleString()}` : ""
          }
        }
      },
      scales: {
        x: { grid: { color: theme.gridColor } },
        y: {
          grid: { color: theme.gridColor },
          ticks: {
            callback: (v) => "$" + (v >= 1e6 ? (v / 1e6).toFixed(1) + "M" : (v / 1e3).toFixed(0) + "K")
          }
        }
      }
    }
  });
}

// 2. Model Accuracy Comparison
function renderModelComparison(theme) {
  const ctx = document.getElementById("modelComparisonChart").getContext("2d");
  if (charts.modelComp) charts.modelComp.destroy();

  const models = forecastMasterData.modelMetrics;
  const labels = models.map(m => m.Model_Name.replace(" Regressor", ""));
  const r2Data = models.map(m => m.R2_Score);

  charts.modelComp = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "R2 Score",
        data: r2Data,
        backgroundColor: ["#3B82F6", "#8B5CF6", "#06B6D4", "#10B981"],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` R2: ${ctx.parsed.y.toFixed(4)}`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: theme.gridColor },
          min: 0,
          max: 1.0
        }
      }
    }
  });
}

// 3. Feature Importance
function renderFeatureImportance(theme) {
  const ctx = document.getElementById("featureImportanceChart").getContext("2d");
  if (charts.features) charts.features.destroy();

  const features = [
    { name: "Revenue Lag (t-1)", weight: 31.2 },
    { name: "7-Day Rolling Mean", weight: 22.4 },
    { name: "Revenue Lag (t-7)", weight: 16.5 },
    { name: "Marketing Ad Spend", weight: 11.8 },
    { name: "Holiday Indicator", weight: 8.2 },
    { name: "Day of Week", weight: 4.6 },
    { name: "Website Sessions", weight: 2.8 }
  ];

  charts.features = new Chart(ctx, {
    type: "bar",
    data: {
      labels: features.map(f => f.name),
      datasets: [{
        label: "Explanatory Weight (%)",
        data: features.map(f => f.weight),
        backgroundColor: "#06B6D4",
        borderRadius: 5
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` Importance: ${ctx.parsed.x}%`
          }
        }
      },
      scales: {
        x: {
          grid: { color: theme.gridColor },
          ticks: { callback: (v) => v + "%" }
        },
        y: { grid: { display: false } }
      }
    }
  });
}

// 4. Monthly Seasonality
function renderSeasonalityChart(theme) {
  const ctx = document.getElementById("seasonalityBarChart").getContext("2d");
  if (charts.seasonality) charts.seasonality.destroy();

  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const seasonalityIndex = [22400, 23100, 24500, 25200, 26800, 27400, 29200, 28600, 27900, 29500, 36800, 39400];

  charts.seasonality = new Chart(ctx, {
    type: "bar",
    data: {
      labels: months,
      datasets: [{
        label: "Historical Mean Daily Revenue ($)",
        data: seasonalityIndex,
        backgroundColor: months.map(m => m === "Nov" || m === "Dec" ? "#10B981" : "#3B82F6"),
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` Mean Daily Rev: $${ctx.parsed.y.toLocaleString()}`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: theme.gridColor },
          ticks: { callback: (v) => "$" + (v / 1e3).toFixed(0) + "K" }
        }
      }
    }
  });
}

function getSearchedData() {
  const query = document.getElementById("tableSearchInput").value.trim().toLowerCase();
  if (!query) return currentFilteredDaily;
  return currentFilteredDaily.filter(d => d.Date.toLowerCase().includes(query));
}

function renderTable(scenario = "Base") {
  let mult = scenario === "Bull" ? 1.12 : scenario === "Bear" ? 0.90 : 1.0;
  const searched = getSearchedData();
  const totalRows = searched.length;
  const totalPages = Math.ceil(totalRows / rowsPerPage) || 1;

  if (currentPage > totalPages) currentPage = totalPages;

  const startIdx = (currentPage - 1) * rowsPerPage;
  const pageRows = searched.slice(startIdx, startIdx + rowsPerPage);

  const tbody = document.getElementById("forecastTableBody");
  tbody.innerHTML = "";

  if (pageRows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 24px; color: var(--text-muted);">No forecast records match your filter criteria.</td></tr>`;
  } else {
    pageRows.forEach(row => {
      const pred = Math.round(row.Predicted_Revenue * mult);
      const low = Math.round(row.Lower_Bound_95CI * mult);
      const upp = Math.round(row.Upper_Bound_95CI * mult);
      const bull = Math.round(row.Bull_Case_Revenue);
      const bear = Math.round(row.Bear_Case_Revenue);

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${row.Date}</strong></td>
        <td style="color: #10B981; font-weight: 700;">$${pred.toLocaleString()}</td>
        <td style="color: #F87171;">$${low.toLocaleString()}</td>
        <td style="color: #FBBF24;">$${upp.toLocaleString()}</td>
        <td style="color: #A78BFA;">$${bull.toLocaleString()}</td>
        <td style="color: #94A3B8;">$${bear.toLocaleString()}</td>
        <td>$${Math.round(row.Marketing_Spend).toLocaleString()}</td>
        <td>${row.Website_Sessions.toLocaleString()}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  const endDisplay = Math.min(startIdx + rowsPerPage, totalRows);
  document.getElementById("paginationInfo").innerText = totalRows > 0 ? `Showing ${startIdx + 1} to ${endDisplay} of ${totalRows.toLocaleString()} days` : "0 days";
  document.getElementById("currentPageBadge").innerText = `Page ${currentPage} of ${totalPages}`;
  document.getElementById("prevPageBtn").disabled = currentPage <= 1;
  document.getElementById("nextPageBtn").disabled = currentPage >= totalPages;
}

function exportForecastCSV() {
  const scenario = document.getElementById("scenarioFilter").value;
  let mult = scenario === "Bull" ? 1.12 : scenario === "Bear" ? 0.90 : 1.0;
  const data = getSearchedData();

  if (!data.length) {
    alert("No forecast data available to export.");
    return;
  }

  const headers = ["Date", "Projected_Revenue", "Lower_Bound_95CI", "Upper_Bound_95CI", "Bull_Scenario", "Bear_Scenario", "Planned_Marketing_Spend", "Estimated_Sessions"];
  let csv = "data:text/csv;charset=utf-8," + headers.join(",") + "\n";

  data.forEach(d => {
    const row = [
      d.Date,
      Math.round(d.Predicted_Revenue * mult),
      Math.round(d.Lower_Bound_95CI * mult),
      Math.round(d.Upper_Bound_95CI * mult),
      Math.round(d.Bull_Case_Revenue),
      Math.round(d.Bear_Case_Revenue),
      Math.round(d.Marketing_Spend),
      d.Website_Sessions
    ];
    csv += row.join(",") + "\n";
  });

  const encoded = encodeURI(csv);
  const link = document.createElement("a");
  link.setAttribute("href", encoded);
  link.setAttribute("download", `forecast_projections_${scenario.toLowerCase()}_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
