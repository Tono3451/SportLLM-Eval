const statusEl = document.getElementById("status");
const bodyEl = document.getElementById("results-body");
const fileInputEl = document.getElementById("file-input");
const resultsSelectEl = document.getElementById("results-select");
const reloadResultsBtn = document.getElementById("reload-results");
const exportBtn = document.getElementById("export-real-scores");
const exportComparisonBtn = document.getElementById("export-comparison");
const rebuildComparisonBtn = document.getElementById("rebuild-comparison");
const comparisonStatsEl = document.getElementById("comparison-stats");
const scoresCanvas = document.getElementById("scores-chart");
const tabButtons = Array.from(document.querySelectorAll(".tab-button"));
const tabPanels = Array.from(document.querySelectorAll(".tab-panel"));

const REAL_SCORE_STORAGE_KEY = "jsonl-real-scores";
let currentRows = [];
let currentSource = "";
let comparisonChart = null;

// ChartJS zoom y pan
let chartScaleMinX = 0;
let chartScaleMaxX = 100;
let chartScaleMinY = 0;
let chartScaleMaxY = 10;
let isDragging = false;
let dragStartX = 0;
let dragStartY = 0;

function setStatus(text) {
  statusEl.textContent = text;
}

function getStoredRealScores() {
  try {
    return JSON.parse(localStorage.getItem(REAL_SCORE_STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveRealScore(videoPath, value) {
  const map = getStoredRealScores();
  map[videoPath] = value;
  localStorage.setItem(REAL_SCORE_STORAGE_KEY, JSON.stringify(map));
}

function normalizeResultPath(fileName) {
  return `../results/${fileName}`;
}

function parseJsonl(text) {
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, idx) => {
      try {
        return JSON.parse(line);
      } catch (err) {
        throw new Error(`Linea ${idx + 1} no es JSON valido: ${err.message}`);
      }
    });
}

function parseNumberLike(value) {
  if (value === null || value === undefined || value === "") return NaN;
  if (typeof value === "number") return Number(value);
  if (typeof value === "string") {
    // buscar primer número con coma o punto
    const m = value.match(/[+-]?\d+[\.,]?\d*/);
    if (!m) return NaN;
    return parseFloat(m[0].replace(",", "."));
  }
  return NaN;
}

function extractPredictedScore(row) {
  if (row.score !== undefined && row.score !== null) {
    if (typeof row.score === "object") {
      // si objeto
      for (const key of ["score_final", "score", "value"]) {
        if (row.score[key] !== undefined) {
          const v = parseNumberLike(row.score[key]);
          if (!Number.isNaN(v)) return v;
        }
      }
    } else {
      // si string
      const v = parseNumberLike(row.score);
      if (!Number.isNaN(v)) return v;
    }
  }

  return NaN;
}

function renderRows(rows) {
  currentRows = rows;
  bodyEl.innerHTML = "";
  const storedScores = getStoredRealScores();

  rows.forEach((row) => {
    const tr = document.createElement("tr");

    const videoPath = row.video_path || "";
    const description = String(row.description ?? "");
    const scoreReasoning = typeof row.score === 'string' ? row.score : JSON.stringify(row.score ?? row.reasoner_json ?? "");

    const tdPath = document.createElement("td");
    tdPath.className = "video-path";
    tdPath.textContent = videoPath;

    const tdDescription = document.createElement("td");
    const descPre = document.createElement("pre");
    descPre.textContent = description;
    tdDescription.appendChild(descPre);

    const tdScoreReasoning = document.createElement("td");
    const scorePre = document.createElement("pre");
    scorePre.textContent = scoreReasoning;
    tdScoreReasoning.appendChild(scorePre);

    const tdRealScore = document.createElement("td");
    tdRealScore.textContent = storedScores[videoPath] ?? row.real_score ?? "";

    tr.appendChild(tdPath);
    tr.appendChild(tdDescription);
    tr.appendChild(tdScoreReasoning);
    tr.appendChild(tdRealScore);

    bodyEl.appendChild(tr);
  });

  setStatus(`Cargadas ${rows.length} filas`);
  if (!document.getElementById("tab-comparison").classList.contains("hidden")) {
    requestAnimationFrame(buildComparison);
  }
}

async function loadDefaultJsonl() {
  setStatus("Cargando indice de resultados...");
  try {
    const response = await fetch("../results/index.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const files = await response.json();
    resultsSelectEl.innerHTML = "";

    if (!Array.isArray(files) || files.length === 0) {
      const option = document.createElement("option");
      option.value = "";
      option.textContent = "No hay archivos en results";
      resultsSelectEl.appendChild(option);
      setStatus("No se encontraron archivos JSONL en results");
      return;
    }

    files.forEach((file) => {
      const option = document.createElement("option");
      option.value = normalizeResultPath(file.file_name);
      option.textContent = file.label || file.file_name;
      resultsSelectEl.appendChild(option);
    });

    resultsSelectEl.value = resultsSelectEl.options[0].value;
    await loadJsonlFromUrl(resultsSelectEl.value);
  } catch (err) {
    setStatus(`Error al cargar indice: ${err.message}`);
  }
}

async function loadJsonlFromUrl(url) {
  if (!url) {
    return;
  }

  currentSource = url;
  setStatus(`Cargando ${url}...`);
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const text = await response.text();
  const rows = parseJsonl(text);
  renderRows(rows);
}

resultsSelectEl.addEventListener("change", async (event) => {
  const url = event.target.value;
  if (!url) {
    return;
  }

  try {
    await loadJsonlFromUrl(url);
  } catch (err) {
    setStatus(`Error al cargar archivo: ${err.message}`);
  }
});

fileInputEl.addEventListener("change", async (event) => {
  const file = event.target.files?.[0];
  if (!file) {
    return;
  }

  setStatus(`Leyendo ${file.name}...`);
  try {
    const text = await file.text();
    const rows = parseJsonl(text);
    renderRows(rows);
  } catch (err) {
    setStatus(`Error en archivo: ${err.message}`);
  }
});

reloadResultsBtn.addEventListener("click", loadDefaultJsonl);

loadDefaultJsonl();

exportBtn.addEventListener("click", () => {
  if (!currentRows.length) {
    setStatus("No hay filas para exportar");
    return;
  }

  const storedScores = getStoredRealScores();
  const lines = ["video_path,real_score"];

  currentRows.forEach((row) => {
    const path = (row.video_path || "").replace(/"/g, '""');
    const realValue = storedScores[row.video_path] ?? row.real_score ?? "";
    const real = realValue.toString().replace(/"/g, '""');
    lines.push(`"${path}","${real}"`);
  });

  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "real_scores.csv";
  a.click();

  URL.revokeObjectURL(url);
  setStatus("CSV exportado");
});

function buildComparison() {
  const stored = getStoredRealScores();
  const rowsInfo = [];

  currentRows.forEach((row, idx) => {
    const path = row.video_path || "";
    const realRaw = stored[path] ?? row.real_score ?? null;
    const real = parseNumberLike(realRaw);
    const pred = extractPredictedScore(row);
    if (!Number.isNaN(real) && !Number.isNaN(pred)) {
      rowsInfo.push({ entryIndex: idx + 1, path, real, pred, err: pred - real });
    }
  });

  renderComparison(rowsInfo);
}

function statsFromRows(rowsInfo) {
  const n = rowsInfo.length;
  if (n === 0) return null;
  let sumErr = 0;
  let sumSq = 0;
  let sumReal = 0;
  let sumPred = 0;

  for (const r of rowsInfo) {
    sumErr += Math.abs(r.err);
    sumSq += r.err * r.err;
    sumReal += r.real;
    sumPred += r.pred;
  }

  const mae = sumErr / n;
  const rmse = Math.sqrt(sumSq / n);
  const meanReal = sumReal / n;
  const meanPred = sumPred / n;

  // pearson
  let cov = 0;
  let varR = 0;
  let varP = 0;
  for (const r of rowsInfo) {
    cov += (r.real - meanReal) * (r.pred - meanPred);
    varR += Math.pow(r.real - meanReal, 2);
    varP += Math.pow(r.pred - meanPred, 2);
  }
  const corr = cov / Math.sqrt(varR * varP || 1);
  const relativeError = (mae / 10) * 100;

  return { n, mae, rmse, meanReal, meanPred, corr, relativeError };
}

function renderComparison(rowsInfo) {
  const stats = statsFromRows(rowsInfo);
  if (!stats) {
    comparisonStatsEl.textContent = "No hay pares (real, pred) para comparar";
  } else {
    comparisonStatsEl.innerHTML = `Puntos: <b>${stats.n}</b> &nbsp; Error medio absoluto: <b>${stats.mae.toFixed(2)}</b> &nbsp; Error relativo: <b>${stats.relativeError.toFixed(1)}%</b> &nbsp; RMSE: <b>${stats.rmse.toFixed(2)}</b>`;
  }

  // Update zoom info
  const zoomInfoEl = document.getElementById("chart-zoom-info");
  if (zoomInfoEl) {
    const currentXRange = chartScaleMaxX - chartScaleMinX;
    const originalXRange = 100;
    const zoomFactor = originalXRange / currentXRange;
    const zoomLevel = zoomFactor.toFixed(1) + "x";
    zoomInfoEl.textContent = `Zoom: ${zoomLevel} | Rueda para zoom | Arrastra para mover | Doble-click para reiniciar`;
  }

  renderComparisonWithChartJs(rowsInfo);
}

function renderComparisonWithChartJs(rowsInfo) {
  if (!scoresCanvas) return;

  const labels = rowsInfo.map((row) => String(row.entryIndex));
  const realSeries = rowsInfo.map((row) => row.real);
  const predictedSeries = rowsInfo.map((row) => row.pred);

  // Reset scale ranges for new data
  chartScaleMinX = 0;
  chartScaleMaxX = labels.length > 0 ? labels.length : 1;
  chartScaleMinY = 0;
  chartScaleMaxY = 10;

  if (comparisonChart) {
    comparisonChart.data.labels = labels;
    comparisonChart.data.datasets[0].data = realSeries;
    comparisonChart.data.datasets[1].data = predictedSeries;
    comparisonChart.options.scales.x.min = undefined;
    comparisonChart.options.scales.x.max = undefined;
    comparisonChart.options.scales.y.min = 0;
    comparisonChart.options.scales.y.max = 10;
    comparisonChart.update();
    return;
  }

  comparisonChart = new Chart(scoresCanvas, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Score real",
          data: realSeries,
          borderColor: "#005f73",
          backgroundColor: "#005f73",
          tension: 0.25,
          pointRadius: 3,
          fill: false,
        },
        {
          label: "Score generado",
          data: predictedSeries,
          borderColor: "#0a9396",
          backgroundColor: "#0a9396",
          tension: 0.25,
          pointRadius: 3,
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { 
          title: { display: true, text: "Indice de la entrada JSON" },
          min: undefined,
          max: undefined,
        },
        y: { 
          title: { display: true, text: "Score sacado" }, 
          min: 0, 
          max: 10 
        },
      },
      plugins: {
        legend: { display: true },
      },
    },
  });
}



exportComparisonBtn?.addEventListener("click", () => {
  const stored = getStoredRealScores();
  const lines = ["video_path,real_score,pred_score,error"];
  for (const row of currentRows) {
    const path = row.video_path || "";
    const realRaw = stored[path] ?? row.real_score ?? null;
    const real = parseNumberLike(realRaw);
    const pred = extractPredictedScore(row);
    if (!Number.isNaN(real) && !Number.isNaN(pred)) {
      const err = pred - real;
      lines.push(`"${path.replace(/"/g, '""')}","${real}","${pred}","${err}"`);
    }
  }
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "comparison.csv";
  a.click();
  URL.revokeObjectURL(url);
  setStatus("CSV de comparación exportado");
});

rebuildComparisonBtn?.addEventListener("click", () => buildComparison());

function showTab(tabName) {
  tabButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === tabName);
  });

  tabPanels.forEach((panel) => {
    panel.classList.toggle("hidden", panel.id !== `tab-${tabName}`);
  });

  if (tabName === "comparison") {
    requestAnimationFrame(buildComparison);
  }
}

tabButtons.forEach((button) => {
  button.addEventListener("click", () => showTab(button.dataset.tab));
});

window.addEventListener("resize", () => {
  if (!document.getElementById("tab-comparison").classList.contains("hidden")) {
    requestAnimationFrame(buildComparison);
  }
});

// Chart.js zoom and pan controls
if (scoresCanvas) {
  scoresCanvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
    
    if (!comparisonChart) return;
    
    const xRange = chartScaleMaxX - chartScaleMinX;
    const yRange = chartScaleMaxY - chartScaleMinY;
    const xCenter = (chartScaleMinX + chartScaleMaxX) / 2;
    const yCenter = (chartScaleMinY + chartScaleMaxY) / 2;
    const newXRange = xRange / zoomFactor;
    const newYRange = yRange / zoomFactor;
    chartScaleMinX = xCenter - newXRange / 2;
    chartScaleMaxX = xCenter + newXRange / 2;
    chartScaleMinY = yCenter - newYRange / 2;
    chartScaleMaxY = yCenter + newYRange / 2;
    
    comparisonChart.options.scales.x.min = chartScaleMinX;
    comparisonChart.options.scales.x.max = chartScaleMaxX;
    comparisonChart.options.scales.y.min = chartScaleMinY;
    comparisonChart.options.scales.y.max = chartScaleMaxY;
    comparisonChart.update();
    
    // Update zoom info
    const zoomInfoEl = document.getElementById("chart-zoom-info");
    if (zoomInfoEl) {
      const currentXRange = chartScaleMaxX - chartScaleMinX;
      const originalXRange = 100;
      const chartZoomFactor = originalXRange / currentXRange;
      zoomInfoEl.textContent = `Zoom: ${chartZoomFactor.toFixed(1)}x | Rueda para zoom | Arrastra para mover | Doble-click para reiniciar`;
    }
  });

  scoresCanvas.addEventListener("mousedown", (e) => {
    isDragging = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;
  });

  scoresCanvas.addEventListener("mousemove", (e) => {
    if (!isDragging || !comparisonChart) return;
    
    const deltaX = (e.clientX - dragStartX) * 0.5;
    const deltaY = -(e.clientY - dragStartY) * 0.5;
    const xRange = chartScaleMaxX - chartScaleMinX;
    const yRange = chartScaleMaxY - chartScaleMinY;
    chartScaleMinX -= deltaX * (xRange / 400);
    chartScaleMaxX -= deltaX * (xRange / 400);
    chartScaleMinY -= deltaY * (yRange / 400);
    chartScaleMaxY -= deltaY * (yRange / 400);
    
    comparisonChart.options.scales.x.min = chartScaleMinX;
    comparisonChart.options.scales.x.max = chartScaleMaxX;
    comparisonChart.options.scales.y.min = chartScaleMinY;
    comparisonChart.options.scales.y.max = chartScaleMaxY;
    comparisonChart.update();
    
    dragStartX = e.clientX;
    dragStartY = e.clientY;
  });

  scoresCanvas.addEventListener("mouseup", () => {
    isDragging = false;
  });

  scoresCanvas.addEventListener("mouseleave", () => {
    isDragging = false;
  });

  scoresCanvas.addEventListener("dblclick", () => {
    if (!comparisonChart) return;
    
    chartScaleMinX = 0;
    chartScaleMaxX = 100;
    chartScaleMinY = 0;
    chartScaleMaxY = 10;
    
    comparisonChart.options.scales.x.min = undefined;
    comparisonChart.options.scales.x.max = undefined;
    comparisonChart.options.scales.y.min = 0;
    comparisonChart.options.scales.y.max = 10;
    comparisonChart.update();
    
    const zoomInfoEl = document.getElementById("chart-zoom-info");
    if (zoomInfoEl) {
      zoomInfoEl.textContent = "Zoom: 1x | Rueda para zoom | Arrastra para mover | Doble-click para reiniciar";
    }
  });
}

showTab("raw");
