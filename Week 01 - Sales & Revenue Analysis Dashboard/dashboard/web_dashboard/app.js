/**
 * Executive Sales & Revenue Analytics Application Logic
 * Pure Vanilla JavaScript with dynamic Chart.js instances and real-time slicers.
 */

// Global state
let currentFilteredData = [];
let currentPage = 1;
const rowsPerPage = 12;

// Chart references for cleanup and re-rendering
let charts = {
  monthlyTrend: null,
  regionalDonut: null,
  categoryBar: null,
  topProducts: null,
  segmentBar: null,
  discountSensitivity: null
};

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
  if (typeof rawSalesData === "undefined" || !rawSalesData.length) {
    console.error("Dataset 'rawSalesData' failed to load.");
    return;
  }

  currentFilteredData = [...rawSalesData];
  
  initEventListeners();
  applyFiltersAndRender();
});

/**
 * Attaches DOM event listeners for interactive slicers and buttons
 */
function initEventListeners() {
  // Slicer controls
  document.getElementById("yearFilter").addEventListener("change", applyFiltersAndRender);
  document.getElementById("regionFilter").addEventListener("change", applyFiltersAndRender);
  document.getElementById("categoryFilter").addEventListener("change", applyFiltersAndRender);
  document.getElementById("segmentFilter").addEventListener("change", applyFiltersAndRender);

  // Slicer reset
  document.getElementById("resetFiltersBtn").addEventListener("click", () => {
    document.getElementById("yearFilter").value = "All";
    document.getElementById("regionFilter").value = "All";
    document.getElementById("categoryFilter").value = "All";
    document.getElementById("segmentFilter").value = "All";
    document.getElementById("tableSearchInput").value = "";
    applyFiltersAndRender();
  });

  // Search input
  document.getElementById("tableSearchInput").addEventListener("input", () => {
    currentPage = 1;
    renderTable();
  });

  // Pagination buttons
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

  // Export CSV
  document.getElementById("exportCsvBtn").addEventListener("click", exportCurrentDataToCSV);

  // Print Executive PDF
  document.getElementById("printReportBtn").addEventListener("click", () => {
    window.print();
  });

  // Dark/Light Theme Toggle
  const themeToggle = document.getElementById("themeToggleBtn");
  themeToggle.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark-theme");
    document.body.classList.toggle("light-theme", !isDark);
    themeToggle.innerHTML = isDark ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
    // Re-render charts to adjust text color schemes
    renderAllCharts();
  });
}

/**
 * Filter data pipeline
 */
function applyFiltersAndRender() {
  const selectedYear = document.getElementById("yearFilter").value;
  const selectedRegion = document.getElementById("regionFilter").value;
  const selectedCategory = document.getElementById("categoryFilter").value;
  const selectedSegment = document.getElementById("segmentFilter").value;

  currentFilteredData = rawSalesData.filter(item => {
    if (selectedYear !== "All" && item.year.toString() !== selectedYear) return false;
    if (selectedRegion !== "All" && item.region !== selectedRegion) return false;
    if (selectedCategory !== "All" && item.category !== selectedCategory) return false;
    if (selectedSegment !== "All" && item.segment !== selectedSegment) return false;
    return true;
  });

  currentPage = 1;
  updateKPIs();
  renderAllCharts();
  renderTable();
}

/**
 * Calculates and animates KPI cards
 */
function updateKPIs() {
  const data = currentFilteredData;
  const totalRevenue = data.reduce((acc, cur) => acc + cur.revenue, 0);
  const totalProfit = data.reduce((acc, cur) => acc + cur.profit, 0);
  const totalOrders = new Set(data.map(d => d.id)).size;
  const totalCustomers = new Set(data.map(d => d.customer)).size;
  const totalUnits = data.reduce((acc, cur) => acc + cur.quantity, 0);
  const avgMargin = totalRevenue > 0 ? (totalProfit / totalRevenue * 100) : 0;
  const aov = totalOrders > 0 ? (totalRevenue / totalOrders) : 0;
  
  const totalGross = data.reduce((acc, cur) => acc + (cur.revenue + (cur.discount * cur.revenue)), 0);
  const totalCogs = totalRevenue - totalProfit;

  // Format currency helpers
  const fmtMoney = (val) => "$" + Number(val).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const fmtShort = (val) => "$" + (val >= 1e6 ? (val / 1e6).toFixed(2) + "M" : val >= 1e3 ? (val / 1e3).toFixed(1) + "K" : val.toFixed(0));

  document.getElementById("kpiRevenue").innerText = fmtMoney(totalRevenue);
  document.getElementById("kpiGross").innerText = fmtShort(totalGross);

  document.getElementById("kpiProfit").innerText = fmtMoney(totalProfit);
  document.getElementById("kpiCogs").innerText = fmtShort(totalCogs);
  document.getElementById("kpiMarginBadge").innerText = `${avgMargin.toFixed(1)}% Margin`;

  document.getElementById("kpiOrders").innerText = totalOrders.toLocaleString();
  document.getElementById("kpiCustomersBadge").innerText = `${totalCustomers.toLocaleString()} Buyers`;

  document.getElementById("kpiUnits").innerText = totalUnits.toLocaleString();
  
  document.getElementById("kpiAov").innerText = fmtMoney(aov);
  const arpc = totalCustomers > 0 ? totalRevenue / totalCustomers : 0;
  document.getElementById("kpiArpcBadge").innerText = `${fmtShort(arpc)} / Buyer`;
}

/**
 * Global chart color palettes & themes
 */
function getChartTheme() {
  const isDark = document.body.classList.contains("dark-theme");
  return {
    textColor: isDark ? "#94A3B8" : "#475569",
    gridColor: isDark ? "rgba(255, 255, 255, 0.05)" : "rgba(0, 0, 0, 0.05)",
    fontFamily: "'Plus Jakarta Sans', sans-serif"
  };
}

/**
 * Renders all 6 analytical charts
 */
function renderAllCharts() {
  const theme = getChartTheme();
  Chart.defaults.color = theme.textColor;
  Chart.defaults.font.family = theme.fontFamily;

  renderMonthlyTrend(theme);
  renderRegionalDonut(theme);
  renderCategoryBar(theme);
  renderTopProducts(theme);
  renderSegmentBar(theme);
  renderDiscountSensitivity(theme);
}

// 1. Monthly Trend Chart
function renderMonthlyTrend(theme) {
  const ctx = document.getElementById("monthlyTrendChart").getContext("2d");
  if (charts.monthlyTrend) charts.monthlyTrend.destroy();

  // Aggregate by Year-Month
  const monthlyMap = {};
  currentFilteredData.forEach(d => {
    const ym = d.date.substring(0, 7);
    if (!monthlyMap[ym]) monthlyMap[ym] = { revenue: 0, profit: 0 };
    monthlyMap[ym].revenue += d.revenue;
    monthlyMap[ym].profit += d.profit;
  });

  const sortedMonths = Object.keys(monthlyMap).sort();
  const revData = sortedMonths.map(m => Math.round(monthlyMap[m].revenue));
  const profitData = sortedMonths.map(m => Math.round(monthlyMap[m].profit));

  const blueGradient = ctx.createLinearGradient(0, 0, 0, 300);
  blueGradient.addColorStop(0, "rgba(59, 130, 246, 0.45)");
  blueGradient.addColorStop(1, "rgba(59, 130, 246, 0.0)");

  charts.monthlyTrend = new Chart(ctx, {
    type: "line",
    data: {
      labels: sortedMonths,
      datasets: [
        {
          label: "Net Revenue ($)",
          data: revData,
          borderColor: "#3B82F6",
          backgroundColor: blueGradient,
          fill: true,
          tension: 0.35,
          borderWidth: 2.5,
          pointRadius: 3,
          pointHoverRadius: 6
        },
        {
          label: "Net Profit ($)",
          data: profitData,
          borderColor: "#10B981",
          borderDash: [5, 4],
          backgroundColor: "transparent",
          fill: false,
          tension: 0.35,
          borderWidth: 2,
          pointRadius: 2.5,
          pointHoverRadius: 5
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
            label: (ctx) => ` ${ctx.dataset.label}: $${ctx.parsed.y.toLocaleString()}`
          }
        }
      },
      scales: {
        x: { grid: { color: theme.gridColor } },
        y: {
          grid: { color: theme.gridColor },
          ticks: {
            callback: (v) => "$" + (v >= 1e3 ? (v / 1e3).toFixed(0) + "K" : v)
          }
        }
      }
    }
  });
}

// 2. Regional Donut Chart
function renderRegionalDonut(theme) {
  const ctx = document.getElementById("regionalDonutChart").getContext("2d");
  if (charts.regionalDonut) charts.regionalDonut.destroy();

  const regMap = {};
  currentFilteredData.forEach(d => {
    regMap[d.region] = (regMap[d.region] || 0) + d.revenue;
  });

  const regions = Object.keys(regMap);
  const values = regions.map(r => Math.round(regMap[r]));

  charts.regionalDonut = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: regions,
      datasets: [{
        data: values,
        backgroundColor: ["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B"],
        borderWidth: 2,
        borderColor: document.body.classList.contains("dark-theme") ? "#111827" : "#FFFFFF"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "68%",
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 12, padding: 14 } },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.label}: $${ctx.parsed.toLocaleString()}`
          }
        }
      }
    }
  });
}

// 3. Category & Subcategory Bar Chart
function renderCategoryBar(theme) {
  const ctx = document.getElementById("categoryBarChart").getContext("2d");
  if (charts.categoryBar) charts.categoryBar.destroy();

  const catMap = {};
  currentFilteredData.forEach(d => {
    if (!catMap[d.category]) catMap[d.category] = { revenue: 0, profit: 0 };
    catMap[d.category].revenue += d.revenue;
    catMap[d.category].profit += d.profit;
  });

  const categories = Object.keys(catMap);
  const revs = categories.map(c => Math.round(catMap[c].revenue));
  const profits = categories.map(c => Math.round(catMap[c].profit));

  charts.categoryBar = new Chart(ctx, {
    type: "bar",
    data: {
      labels: categories,
      datasets: [
        {
          label: "Revenue ($)",
          data: revs,
          backgroundColor: "#3B82F6",
          borderRadius: 6
        },
        {
          label: "Profit ($)",
          data: profits,
          backgroundColor: "#10B981",
          borderRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "top", labels: { boxWidth: 12 } },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: $${ctx.parsed.y.toLocaleString()}`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
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

// 4. Top 10 High Performing Products
function renderTopProducts(theme) {
  const ctx = document.getElementById("topProductsChart").getContext("2d");
  if (charts.topProducts) charts.topProducts.destroy();

  const prodMap = {};
  currentFilteredData.forEach(d => {
    prodMap[d.product] = (prodMap[d.product] || 0) + d.revenue;
  });

  const sortedProds = Object.keys(prodMap)
    .sort((a, b) => prodMap[b] - prodMap[a])
    .slice(0, 8); // Top 8 for clean card height

  const labels = sortedProds.map(p => p.length > 22 ? p.substring(0, 20) + "..." : p);
  const values = sortedProds.map(p => Math.round(prodMap[p]));

  charts.topProducts = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Total Sales ($)",
        data: values,
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
            title: (items) => sortedProds[items[0].dataIndex],
            label: (ctx) => ` Revenue: $${ctx.parsed.x.toLocaleString()}`
          }
        }
      },
      scales: {
        x: {
          grid: { color: theme.gridColor },
          ticks: {
            callback: (v) => "$" + (v >= 1e3 ? (v / 1e3).toFixed(0) + "K" : v)
          }
        },
        y: { grid: { display: false } }
      }
    }
  });
}

// 5. Customer Segment Bar Chart
function renderSegmentBar(theme) {
  const ctx = document.getElementById("segmentBarChart").getContext("2d");
  if (charts.segmentBar) charts.segmentBar.destroy();

  const segMap = {};
  currentFilteredData.forEach(d => {
    segMap[d.segment] = (segMap[d.segment] || 0) + d.revenue;
  });

  const segments = Object.keys(segMap);
  const values = segments.map(s => Math.round(segMap[s]));

  charts.segmentBar = new Chart(ctx, {
    type: "bar",
    data: {
      labels: segments,
      datasets: [{
        label: "Segment Revenue ($)",
        data: values,
        backgroundColor: ["#8B5CF6", "#F59E0B", "#3B82F6"],
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
            label: (ctx) => ` Revenue: $${ctx.parsed.y.toLocaleString()}`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: theme.gridColor },
          ticks: { callback: (v) => "$" + (v >= 1e3 ? (v / 1e3).toFixed(0) + "K" : v) }
        }
      }
    }
  });
}

// 6. Discount Tier Sensitivity Chart
function renderDiscountSensitivity(theme) {
  const ctx = document.getElementById("discountSensitivityChart").getContext("2d");
  if (charts.discountSensitivity) charts.discountSensitivity.destroy();

  const tiers = {
    "0% Discount": { rev: 0, prof: 0 },
    "1-10% Discount": { rev: 0, prof: 0 },
    "11-20% Discount": { rev: 0, prof: 0 },
    ">20% Discount": { rev: 0, prof: 0 }
  };

  currentFilteredData.forEach(d => {
    let t = ">20% Discount";
    if (d.discount === 0) t = "0% Discount";
    else if (d.discount <= 0.10) t = "1-10% Discount";
    else if (d.discount <= 0.20) t = "11-20% Discount";

    tiers[t].rev += d.revenue;
    tiers[t].prof += d.profit;
  });

  const tierNames = Object.keys(tiers);
  const margins = tierNames.map(t => tiers[t].rev > 0 ? ((tiers[t].prof / tiers[t].rev) * 100).toFixed(1) : 0);

  charts.discountSensitivity = new Chart(ctx, {
    type: "bar",
    data: {
      labels: tierNames,
      datasets: [{
        label: "Net Profit Margin (%)",
        data: margins,
        backgroundColor: ["#10B981", "#3B82F6", "#F59E0B", "#EF4444"],
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
            label: (ctx) => ` Margin: ${ctx.parsed.y}%`
          }
        }
      },
      scales: {
        x: { grid: { display: false } },
        y: {
          grid: { color: theme.gridColor },
          ticks: { callback: (v) => v + "%" }
        }
      }
    }
  });
}

/**
 * Filtered search dataset helper
 */
function getSearchedData() {
  const query = document.getElementById("tableSearchInput").value.trim().toLowerCase();
  if (!query) return currentFilteredData;
  return currentFilteredData.filter(d => 
    d.id.toLowerCase().includes(query) ||
    d.customer.toLowerCase().includes(query) ||
    d.product.toLowerCase().includes(query) ||
    d.region.toLowerCase().includes(query) ||
    d.category.toLowerCase().includes(query)
  );
}

/**
 * Render paginated table rows
 */
function renderTable() {
  const searched = getSearchedData();
  const totalRows = searched.length;
  const totalPages = Math.ceil(totalRows / rowsPerPage) || 1;

  if (currentPage > totalPages) currentPage = totalPages;

  const startIdx = (currentPage - 1) * rowsPerPage;
  const pageRows = searched.slice(startIdx, startIdx + rowsPerPage);

  const tbody = document.getElementById("salesTableBody");
  tbody.innerHTML = "";

  if (pageRows.length === 0) {
    tbody.innerHTML = `<tr><td colspan="11" style="text-align:center; padding: 24px; color: var(--text-muted);">No transactions match your search filter.</td></tr>`;
  } else {
    pageRows.forEach(row => {
      const tr = document.createElement("tr");
      const marginClass = row.margin >= 30 ? "text-success" : row.margin > 15 ? "text-warning" : "text-danger";
      tr.innerHTML = `
        <td><strong>${row.id}</strong></td>
        <td>${row.date}</td>
        <td>${row.customer}</td>
        <td><span class="badge ${row.segment === 'Corporate' ? 'badge-info' : row.segment === 'Consumer' ? 'badge-purple' : 'badge-warning'}">${row.segment}</span></td>
        <td>${row.region}</td>
        <td>${row.category}</td>
        <td title="${row.product}">${row.product.length > 25 ? row.product.substring(0, 24) + '...' : row.product}</td>
        <td>${row.quantity}</td>
        <td>$${row.revenue.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
        <td style="color: #10B981; font-weight:600;">$${row.profit.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
        <td><strong>${row.margin}%</strong></td>
      `;
      tbody.appendChild(tr);
    });
  }

  // Update pagination info
  const endDisplay = Math.min(startIdx + rowsPerPage, totalRows);
  document.getElementById("paginationInfo").innerText = totalRows > 0 ? `Showing ${startIdx + 1} to ${endDisplay} of ${totalRows.toLocaleString()} orders` : "0 orders";
  document.getElementById("currentPageBadge").innerText = `Page ${currentPage} of ${totalPages}`;
  document.getElementById("prevPageBtn").disabled = currentPage <= 1;
  document.getElementById("nextPageBtn").disabled = currentPage >= totalPages;
}

/**
 * Client-side CSV Exporter
 */
function exportCurrentDataToCSV() {
  const data = getSearchedData();
  if (!data.length) {
    alert("No data available to export.");
    return;
  }

  const headers = ["Order_ID", "Order_Date", "Customer", "Segment", "Region", "Category", "SubCategory", "Product", "Quantity", "Discount", "Revenue", "Profit", "Margin_Pct"];
  let csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\n";

  data.forEach(d => {
    const row = [
      d.id,
      d.date,
      `"${d.customer.replace(/"/g, '""')}"`,
      d.segment,
      d.region,
      d.category,
      `"${d.subCategory.replace(/"/g, '""')}"`,
      `"${d.product.replace(/"/g, '""')}"`,
      d.quantity,
      d.discount,
      d.revenue,
      d.profit,
      d.margin
    ];
    csvContent += row.join(",") + "\n";
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `apex_sales_export_${new Date().toISOString().slice(0, 10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
