const actions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
const actionSymbols = ["↑", "↓", "←", "→"];

let n = 5;
let startCell = null;
let endCell = null;
let obstacles = new Set();

const gridEl = document.getElementById("grid");
const hintEl = document.getElementById("hint");
const resultsEl = document.getElementById("results");

document.getElementById("generateBtn").addEventListener("click", generateGrid);
document.getElementById("resetBtn").addEventListener("click", () => {
  document.getElementById("gridSize").value = String(n);
  startCell = null;
  endCell = null;
  obstacles = new Set();
  resultsEl.style.display = "none";
  generateGrid();
});
document.getElementById("calcBtn").addEventListener("click", calculateAll);

function getMaxObstacles() {
  return n - 2;
}

function keyOf(r, c) {
  return `${r},${c}`;
}

function parseKey(k) {
  return k.split(",").map(Number);
}

function generateGrid() {
  const input = parseInt(document.getElementById("gridSize").value, 10);
  if (Number.isNaN(input) || input < 5 || input > 9) {
    alert("請輸入 5 到 9 的整數。");
    return;
  }

  n = input;
  startCell = null;
  endCell = null;
  obstacles = new Set();
  resultsEl.style.display = "none";

  gridEl.innerHTML = "";
  gridEl.style.gridTemplateColumns = `repeat(${n}, 48px)`;

  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      cell.dataset.rc = keyOf(r, c);
      cell.textContent = String(r * n + c + 1);
      cell.addEventListener("click", () => onCellClick(r, c));
      gridEl.appendChild(cell);
    }
  }

  updateHint();
  paintGrid();
}

function onCellClick(r, c) {
  const k = keyOf(r, c);

  if (!startCell) {
    startCell = k;
    paintGrid();
    updateHint();
    return;
  }

  if (!endCell && k !== startCell) {
    endCell = k;
    paintGrid();
    updateHint();
    return;
  }

  if (k === startCell || k === endCell) {
    return;
  }

  if (obstacles.has(k)) {
    obstacles.delete(k);
  } else if (obstacles.size < getMaxObstacles()) {
    obstacles.add(k);
  }

  paintGrid();
  updateHint();
}

function updateHint() {
  if (!startCell) {
    hintEl.textContent = "1. 點擊一格設定起點（綠色）。";
  } else if (!endCell) {
    hintEl.textContent = "2. 點擊一格設定終點（紅色）。";
  } else if (obstacles.size < getMaxObstacles()) {
    const remain = getMaxObstacles() - obstacles.size;
    hintEl.textContent = `3. 設定障礙物（灰色），還需要 ${remain} 個。`;
  } else {
    hintEl.textContent = "設定完成，請點擊「計算 HW1-2 與 HW1-3」。";
  }
}

function paintGrid() {
  const cells = gridEl.querySelectorAll(".cell");
  cells.forEach((cell) => {
    const k = cell.dataset.rc;
    cell.classList.remove("start", "end", "obstacle");
    const [r, c] = parseKey(k);
    cell.textContent = String(r * n + c + 1);

    if (k === startCell) {
      cell.classList.add("start");
      cell.textContent = "S";
    } else if (k === endCell) {
      cell.classList.add("end");
      cell.textContent = "G";
    } else if (obstacles.has(k)) {
      cell.classList.add("obstacle");
      cell.textContent = "X";
    }
  });
}

function nextState(r, c, actionIdx, obstacleSet) {
  const [dr, dc] = actions[actionIdx];
  const nr = r + dr;
  const nc = c + dc;
  if (nr >= 0 && nr < n && nc >= 0 && nc < n && !obstacleSet.has(keyOf(nr, nc))) {
    return [nr, nc];
  }
  return [r, c];
}

function makeRandomPolicy(endKey, obstacleSet) {
  const policy = new Map();
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const k = keyOf(r, c);
      if (k === endKey || obstacleSet.has(k)) continue;
      policy.set(k, Math.floor(Math.random() * actions.length));
    }
  }
  return policy;
}

function policyEvaluation(policy, endKey, obstacleSet, gamma = 0.9, theta = 1e-4) {
  const values = new Map();
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      values.set(keyOf(r, c), 0);
    }
  }

  for (let it = 0; it < 5000; it++) {
    let delta = 0;
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const k = keyOf(r, c);
        if (k === endKey || obstacleSet.has(k)) continue;

        const oldV = values.get(k) || 0;
        const a = policy.get(k) ?? 0;
        const [nr, nc] = nextState(r, c, a, obstacleSet);
        const nk = keyOf(nr, nc);
        const reward = -1;
        const newV = nk === endKey ? reward : reward + gamma * (values.get(nk) || 0);
        values.set(k, newV);
        delta = Math.max(delta, Math.abs(oldV - newV));
      }
    }
    if (delta < theta) break;
  }
  return values;
}

function valueIteration(endKey, obstacleSet, gamma = 0.9, theta = 1e-4) {
  const values = new Map();
  const policy = new Map();

  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      values.set(keyOf(r, c), 0);
    }
  }

  for (let it = 0; it < 5000; it++) {
    let delta = 0;

    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const k = keyOf(r, c);
        if (k === endKey || obstacleSet.has(k)) continue;

        const oldV = values.get(k) || 0;
        const q = [];
        for (let a = 0; a < actions.length; a++) {
          const [nr, nc] = nextState(r, c, a, obstacleSet);
          const nk = keyOf(nr, nc);
          const reward = -1;
          q.push(nk === endKey ? reward : reward + gamma * (values.get(nk) || 0));
        }

        let bestA = 0;
        for (let i = 1; i < q.length; i++) {
          if (q[i] > q[bestA]) bestA = i;
        }

        policy.set(k, bestA);
        values.set(k, q[bestA]);
        delta = Math.max(delta, Math.abs(oldV - q[bestA]));
      }
    }

    if (delta < theta) break;
  }

  return { policy, values };
}

function buildPolicyMatrix(policy, endKey, obstacleSet) {
  const m = [];
  for (let r = 0; r < n; r++) {
    const row = [];
    for (let c = 0; c < n; c++) {
      const k = keyOf(r, c);
      if (obstacleSet.has(k)) row.push("X");
      else if (k === endKey) row.push("G");
      else row.push(actionSymbols[policy.get(k) ?? 0]);
    }
    m.push(row);
  }
  return m;
}

function buildValueMatrix(values, endKey, obstacleSet) {
  const m = [];
  for (let r = 0; r < n; r++) {
    const row = [];
    for (let c = 0; c < n; c++) {
      const k = keyOf(r, c);
      if (obstacleSet.has(k)) row.push("X");
      else if (k === endKey) row.push(0);
      else row.push(Number((values.get(k) || 0).toFixed(2)));
    }
    m.push(row);
  }
  return m;
}

function computeOptimalPath(startKey, endKey, policy, obstacleSet) {
  const path = [];
  if (!startKey || !endKey) return path;

  let current = startKey;
  path.push(current);
  const visited = new Set();

  for (let i = 0; i < n * n; i++) {
    if (current === endKey) break;
    if (visited.has(current)) break;
    visited.add(current);

    const [r, c] = parseKey(current);
    const a = policy.get(current);
    if (a === undefined) break;

    const [nr, nc] = nextState(r, c, a, obstacleSet);
    const nextK = keyOf(nr, nc);
    if (nextK === current) break;
    current = nextK;
    path.push(current);
  }

  return path;
}

function renderMatrix(targetId, matrix, isValue = false, pathSet = new Set(), markPath = false) {
  const container = document.getElementById(targetId);
  container.innerHTML = "";
  container.style.gridTemplateColumns = `repeat(${n}, 52px)`;

  let minV = Infinity;
  let maxV = -Infinity;

  if (isValue) {
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const v = matrix[r][c];
        if (v !== "X") {
          minV = Math.min(minV, Number(v));
          maxV = Math.max(maxV, Number(v));
        }
      }
    }
  }

  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const cell = document.createElement("div");
      cell.className = "mcell";
      const v = matrix[r][c];
      const k = keyOf(r, c);

      if (v === "X") {
        cell.classList.add("obstacle");
        cell.textContent = "X";
      } else if (v === "G") {
        cell.classList.add("goal");
        cell.textContent = "G";
      } else {
        cell.textContent = isValue ? Number(v).toFixed(2) : v;
        if (isValue) {
          const ratio = maxV === minV ? 0.5 : (Number(v) - minV) / (maxV - minV);
          if (ratio < 0.2) cell.classList.add("v1");
          else if (ratio < 0.4) cell.classList.add("v2");
          else if (ratio < 0.6) cell.classList.add("v3");
          else if (ratio < 0.8) cell.classList.add("v4");
          else cell.classList.add("v5");
        }
      }

      if (markPath && pathSet.has(k) && v !== "X") {
        cell.classList.add("path");
      }

      container.appendChild(cell);
    }
  }
}

function calculateAll() {
  if (!startCell || !endCell) {
    alert("請先設定起點與終點。");
    return;
  }
  if (obstacles.size !== getMaxObstacles()) {
    alert(`障礙物數量需為 n-2 = ${getMaxObstacles()}。`);
    return;
  }

  const obstacleSet = new Set(obstacles);
  const endKey = endCell;

  const randomPolicy = makeRandomPolicy(endKey, obstacleSet);
  const randomValues = policyEvaluation(randomPolicy, endKey, obstacleSet);
  const randomPolicyMatrix = buildPolicyMatrix(randomPolicy, endKey, obstacleSet);
  const randomValueMatrix = buildValueMatrix(randomValues, endKey, obstacleSet);

  const optimal = valueIteration(endKey, obstacleSet);
  const optimalPolicyMatrix = buildPolicyMatrix(optimal.policy, endKey, obstacleSet);
  const optimalValueMatrix = buildValueMatrix(optimal.values, endKey, obstacleSet);
  const path = computeOptimalPath(startCell, endKey, optimal.policy, obstacleSet);
  const pathSet = new Set(path);

  renderMatrix("randomPolicy", randomPolicyMatrix, false);
  renderMatrix("randomValue", randomValueMatrix, true);
  renderMatrix("optimalPolicy", optimalPolicyMatrix, false, pathSet, true);
  renderMatrix("optimalValue", optimalValueMatrix, true);

  const pathInfo = document.getElementById("pathInfo");
  if (path.length > 0 && path[path.length - 1] === endKey) {
    const s = path
      .map((k) => {
        const [r, c] = parseKey(k);
        return `(${r},${c})`;
      })
      .join(" -> ");
    pathInfo.textContent = `最佳路徑（步數 ${path.length - 1}）：${s}`;
  } else {
    pathInfo.textContent = "無法從起點到達終點（可能被障礙物阻擋）。";
  }

  resultsEl.style.display = "block";
  resultsEl.scrollIntoView({ behavior: "smooth" });
}

generateGrid();
