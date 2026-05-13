const statusEl = document.getElementById("status");
const bodyEl = document.getElementById("results-body");
const fileInputEl = document.getElementById("file-input");
const resultsSelectEl = document.getElementById("results-select");
const reloadResultsBtn = document.getElementById("reload-results");
const exportBtn = document.getElementById("export-real-scores");

const REAL_SCORE_STORAGE_KEY = "jsonl-real-scores";
let currentRows = [];
let currentSource = "";

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

function renderRows(rows) {
  currentRows = rows;
  bodyEl.innerHTML = "";
  const storedScores = getStoredRealScores();

  rows.forEach((row) => {
    const tr = document.createElement("tr");

    const videoPath = row.video_path || "";
    const description = String(row.description ?? "");
    const scoreReasoning = String(row.score ?? "");

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
    const input = document.createElement("input");
    input.type = "number";
    input.step = "0.1";
    input.min = "0";
    input.max = "10";
    input.className = "real-score-input";
    input.placeholder = "0.0 - 10";
    input.value = storedScores[videoPath] ?? row.real_score ?? "";

    input.addEventListener("input", () => {
      saveRealScore(videoPath, input.value);
    });

    tdRealScore.appendChild(input);

    tr.appendChild(tdPath);
    tr.appendChild(tdDescription);
    tr.appendChild(tdScoreReasoning);
    tr.appendChild(tdRealScore);

    bodyEl.appendChild(tr);
  });

  setStatus(`Cargadas ${rows.length} filas`);
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
