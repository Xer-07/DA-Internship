/**
 * Customer Segmentation Studio - Application Logic
 * Interactive Chart.js visualizations, persona slicing, and client-side customer explorer.
 */

let currentFilteredData = [];
let currentPage = 1;
const rowsPerPage = 12;

let charts = {
  pcaScatter: null,
  personaRevenueDonut: null,
  incomeScoreScatter: null,
  rfmBar: null
};

const CLUSTER_COLORS = {
  "VIP Champions": "#10B981",
  "Loyal Mainstream": "#3B82F6",
  "Emerging Tech Lovers": "#8B5CF6",
  "Bargain Hunters": "#F59E0B",
  "At-Risk / Lapsed": "#EF4444"
};

document.addEventListener("DOMContentLoaded", () => {
  if (typeof rawCustomerData === "undefined" || !rawCustomerData.length) {
    console.error("rawCustomerData dataset failed to load.");
    return;
  }

  currentFilteredData = [...rawCustomerData];

  initEventListeners();
  applyFiltersAndRender();
});

function initEventListeners() {
  document.getElementById("clusterFilter").addEventListener("change", applyFiltersAndRender);
  document.getElementById("regionFilter").addEventListener("change", applyFiltersAndRender);
  document.getElementById("categoryFilter").addEventListener("change", applyFiltersAndRender);

  document.getElementById("resetFiltersBtn").addEventListener("click", () => {
    document.getElementById("clusterFilter").value = "All";
    document.getElementById("regionFilter").value = "All";
    document.getElementById("categoryFilter").value = "All";
    document.getElementById("tableSearchInput").value = "";
    applyFiltersAndRender();
  });

  // Persona card quick filter clicks
  document.querySelectorAll(".persona-card").forEach(card => {
    card.addEventListener("click", () => {
      const cluster = card.getAttribute("data-cluster");
      document.getElementById("clusterFilter").value = cluster;
      applyFiltersAndRender();
    });
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

  document.getElementById("exportCsvBtn").addEventListener("click", exportCustomerCSV);

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
  const selectedCluster = document.getElementById("clusterFilter").value;
  const selectedRegion = document.getElementById("regionFilter").value;
  const selectedCategory = document.getElementById("categoryFilter").value;

  currentFilteredData = rawCustomerData.filter(item => {
    if (selectedCluster !== "All" && item.clusterName !== selectedCluster) return false;
    if (selectedRegion !== "All" && item.region !== selectedRegion) return false;
    if (selectedCategory !== "All" && item.category !== selectedCategory) return false;
    return true;
  });

  currentPage = 1;
  updatePersonaMetrics();
  renderAllCharts();
  renderTable();
}

function updatePersonaMetrics() {
  const data = currentFilteredData;
  const clusters = ["VIP Champions", "Loyal Mainstream", "Emerging Tech Lovers", "Bargain Hunters", "At-Risk / Lapsed"];
  const ids = {
    "VIP Champions": "vipSpend",
    "Loyal Mainstream": "mainstreamSpend",
    "Emerging Tech Lovers": "techSpend",
    "Bargain Hunters": "bargainSpend",
    "At-Risk / Lapsed": "atriskSpend"
  };

  clusters.forEach(c => {
    const sub = data.filter(d => d.clusterName === c);
    const avgSpend = sub.length ? sub.reduce((acc, cur) => acc + cur.monetary, 0) / sub.length : 0;
    const elem = document.getElementById(ids[c]);
    if (elem) {
      elem.innerText = "$" + Math.round(avgSpend).toLocaleString();
    }
  });
}

function getChartTheme() {
  const isDark = document.body.classList.contains("dark-theme");
  return {
    textColor: isDark ? "#94A3B8" : "#475569",
    gridColor: isDark ? "rgba(255, 255, 255, 0.05)" : "rgba(0, 0, 0, 0.05)",
    fontFamily: "'Plus Jakarta Sans', sans-serif"
  };
}

function renderAllCharts() {
  const theme = getChartTheme();
  Chart.defaults.color = theme.textColor;
  Chart.defaults.font.family = theme.fontFamily;

  renderPcaScatter(theme);
  renderPersonaRevenueDonut(theme);
  renderIncomeScoreScatter(theme);
  renderRfmBar(theme);
}

// 1. 2D PCA Scatter Plot
function renderPcaScatter(theme) {
  const ctx = document.getElementById("pcaScatterChart").getContext("2d");
  if (charts.pcaScatter) charts.pcaScatter.destroy();

  const datasets = [];
  const clusters = ["VIP Champions", "Loyal Mainstream", "Emerging Tech Lovers", "Bargain Hunters", "At-Risk / Lapsed"];

  clusters.forEach(c => {
    const points = currentFilteredData
      .filter(d => d.clusterName === c)
      .map(d => ({ x: d.pca1, y: d.pca2, name: d.name, income: d.income, spend: d.monetary }));

    datasets.push({
      label: c,
      data: points,
      backgroundColor: CLUSTER_COLORS[c],
      borderColor: "transparent",
      pointRadius: 4.5,
      pointHoverRadius: 7
    });
  });

  charts.pcaScatter = new Chart(ctx, {
    type: "scatter",
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const raw = ctx.raw;
              return ` ${raw.name} (${ctx.dataset.label}) - Spend: $${raw.spend.toLocaleString()}`;
            }
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: "PCA Component 1 (Purchasing Power & Volume)", color: theme.textColor },
          grid: { color: theme.gridColor }
        },
        y: {
          title: { display: true, text: "PCA Component 2 (Price Sensitivity & Recency)", color: theme.textColor },
          grid: { color: theme.gridColor }
        }
      }
    }
  });
}

// 2. Persona Revenue Share Donut
function renderPersonaRevenueDonut(theme) {
  const ctx = document.getElementById("personaRevenueDonut").getContext("2d");
  if (charts.personaRevenueDonut) charts.personaRevenueDonut.destroy();

  const clusterMap = {};
  currentFilteredData.forEach(d => {
    clusterMap[d.clusterName] = (clusterMap[d.clusterName] || 0) + d.monetary;
  });

  const labels = Object.keys(clusterMap);
  const data = labels.map(l => Math.round(clusterMap[l]));
  const colors = labels.map(l => CLUSTER_COLORS[l] || "#6B7280");

  charts.personaRevenueDonut = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderWidth: 2,
        borderColor: document.body.classList.contains("dark-theme") ? "#111726" : "#FFFFFF"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "66%",
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 10, padding: 12 } },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.label}: $${ctx.parsed.toLocaleString()}`
          }
        }
      }
    }
  });
}

// 3. Income vs Spending Score Scatter
function renderIncomeScoreScatter(theme) {
  const ctx = document.getElementById("incomeScoreScatter").getContext("2d");
  if (charts.incomeScoreScatter) charts.incomeScoreScatter.destroy();

  const datasets = [];
  const clusters = ["VIP Champions", "Loyal Mainstream", "Emerging Tech Lovers", "Bargain Hunters", "At-Risk / Lapsed"];

  clusters.forEach(c => {
    const points = currentFilteredData
      .filter(d => d.clusterName === c)
      .map(d => ({ x: d.income, y: d.score, name: d.name, spend: d.monetary }));

    datasets.push({
      label: c,
      data: points,
      backgroundColor: CLUSTER_COLORS[c],
      pointRadius: 4,
      pointHoverRadius: 6
    });
  });

  charts.incomeScoreScatter = new Chart(ctx, {
    type: "scatter",
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.raw.name}: Inc: $${ctx.raw.x.toLocaleString()} | Score: ${ctx.raw.y}/100`
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: "Annual Income ($)", color: theme.textColor },
          grid: { color: theme.gridColor },
          ticks: { callback: (v) => "$" + (v / 1e3).toFixed(0) + "K" }
        },
        y: {
          title: { display: true, text: "Spending Score (1 - 100)", color: theme.textColor },
          grid: { color: theme.gridColor }
        }
      }
    }
  });
}

// 4. RFM Attribute Bar Chart
function renderRfmBar(theme) {
  const ctx = document.getElementById("rfmBarChart").getContext("2d");
  if (charts.rfmBar) charts.rfmBar.destroy();

  const clusters = ["VIP Champions", "Loyal Mainstream", "Emerging Tech Lovers", "Bargain Hunters", "At-Risk / Lapsed"];
  const avgRecency = [];
  const avgFrequency = [];

  clusters.forEach(c => {
    const sub = currentFilteredData.filter(d => d.clusterName === c);
    const rec = sub.length ? sub.reduce((acc, cur) => acc + cur.recency, 0) / sub.length : 0;
    const freq = sub.length ? sub.reduce((acc, cur) => acc + cur.frequency, 0) / sub.length : 0;
    avgRecency.push(Math.round(rec));
    avgFrequency.push(Math.round(freq));
  });

  charts.rfmBar = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["VIP", "Mainstream", "Tech", "Bargain", "At-Risk"],
      datasets: [
        {
          label: "Avg Frequency (Orders)",
          data: avgFrequency,
          backgroundColor: "#8B5CF6",
          borderRadius: 6
        },
        {
          label: "Avg Recency (Days / 10)",
          data: avgRecency.map(r => Math.round(r / 10)),
          backgroundColor: "#3B82F6",
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top", labels: { boxWidth: 12 } }
      },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: theme.gridColor } }
      }
    }
  });
}

function getSearchedData() {
  const query = document.getElementById("tableSearchInput").value.trim().toLowerCase();
  if (!query) return currentFilteredData;
  return currentFilteredData.filter(d =>
    d.id.toLowerCase().includes(query) ||
    d.name.toLowerCase().includes(query) ||
    d.city.toLowerCase().includes(query) ||
    d.region.toLowerCase().includes(query) ||
    d.clusterName.toLowerCase().includes(query)
  );
}

function renderTable() {
  const searched = getSearchedData();
  const totalRows = searched.length;
  const totalPages = Math.ceil(totalRows / rowsPerPage) || 1;

  if (currentPage > totalPages) currentPage = totalPages;

  const startIdx = (currentPage - 1) * rowsPerPage;
  const pageRows = searched.slice(startIdx, startIdx + rowsPerPage);

  const tbody = document.getElementById("customerTableBody");
  tbody.innerHTML = "";

  if (pageRows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; padding: 24px; color: var(--text-muted);">No customer records match your filter criteria.</td></tr>`;
  } else {
    pageRows.forEach(row => {
      const tr = document.createElement("tr");
      const badgeColor = CLUSTER_COLORS[row.clusterName] || "#6B7280";
      tr.innerHTML = `
        <td><strong>${row.id}</strong></td>
        <td>${row.name}</td>
        <td>${row.age}</td>
        <td>${row.region}</td>
        <td>${row.city}</td>
        <td>$${row.income.toLocaleString()}</td>
        <td><strong>${row.score}</strong>/100</td>
        <td>${row.recency}d</td>
        <td>${row.frequency}</td>
        <td style="color: #10B981; font-weight: 700;">$${row.monetary.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
        <td><span class="badge" style="background: ${badgeColor}22; color: ${badgeColor}; border: 1px solid ${badgeColor}44;">${row.clusterName}</span></td>
      `;
      tbody.appendChild(tr);
    });
  }

  const endDisplay = Math.min(startIdx + rowsPerPage, totalRows);
  document.getElementById("paginationInfo").innerText = totalRows > 0 ? `Showing ${startIdx + 1} to ${endDisplay} of ${totalRows.toLocaleString()} customers` : "0 customers";
  document.getElementById("currentPageBadge").innerText = `Page ${currentPage} of ${totalPages}`;
  document.getElementById("prevPageBtn").disabled = currentPage <= 1;
  document.getElementById("nextPageBtn").disabled = currentPage >= totalPages;
}

function exportCustomerCSV() {
  const data = getSearchedData();
  if (!data.length) {
    alert("No data available to export.");
    return;
  }

  const headers = ["Customer_ID", "Name", "Gender", "Age", "Region", "City", "Annual_Income", "Spending_Score", "Recency_Days", "Frequency", "Monetary_Total", "AOV", "Preferred_Category", "Cluster_Name", "PCA_1", "PCA_2"];
  let csv = "data:text/csv;charset=utf-8," + headers.join(",") + "\n";

  data.forEach(d => {
    const row = [
      d.id,
      `"${d.name.replace(/"/g, '""')}"`,
      d.gender,
      d.age,
      d.region,
      `"${d.city}"`,
      d.income,
      d.score,
      d.recency,
      d.frequency,
      d.monetary,
      d.aov,
      `"${d.category}"`,
      `"${d.clusterName}"`,
      d.pca1,
      d.pca2
    ];
    csv += row.join(",") + "\n";
  });

  const encoded = encodeURI(csv);
  const link = document.createElement("a");
  link.setAttribute("href", encoded);
  link.setAttribute("download", `customer_segments_export_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
