const canvas = document.getElementById("polygonCanvas");
const ctx = canvas.getContext("2d");
const select = document.getElementById("ccmSelect");
const tooltip = document.getElementById("tooltip");
const count = document.getElementById("count");
const finishCount = document.getElementById("finish-count");

let polygonsCache = [];
let statusMap = {};
let ccm = '';
let scaleFactor = 1.0;
let offsetX = 0;
let offsetY = 0;
let isDragging = false;
let dragStart = { x: 0, y: 0 };
let animationFrameId = null;

// 📦 LocalStorage 키
const STORAGE_KEY = "parkingStatusMap";

// 📥 로컬스토리지에서 상태값 불러오기
function loadStatusFromStorage() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      statusMap = JSON.parse(saved);
    } catch (e) {
      console.warn("⚠️ 상태값 로드 실패:", e);
      statusMap = {};
    }
  }
}

// 💾 로컬스토리지에 상태값 저장
function saveStatusToStorage() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(statusMap));
}

// 🔄 다시 그리기 예약
function requestRedraw() {
  if (animationFrameId !== null) cancelAnimationFrame(animationFrameId);
  animationFrameId = requestAnimationFrame(() => {
    drawPolygons(polygonsCache);
    animationFrameId = null;
  });
}

// 📏 캔버스 리사이징
function resizeCanvas() {
  canvas.width = window.innerWidth - 40;
  canvas.height = window.innerHeight - 100;
  requestRedraw();
}
window.addEventListener("resize", resizeCanvas);

// 🧩 폴리곤 그리기
function drawPolygons(polygons) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.setTransform(scaleFactor, 0, 0, scaleFactor, offsetX, offsetY);

  polygons.forEach((poly) => {
    const points = poly.points;
    const label = poly.label;
    const hasStatus = !!statusMap[label];

    ctx.beginPath();
    ctx.moveTo(points[0][0], points[0][1]);
    for (let i = 1; i < points.length; i++) {
      ctx.lineTo(points[i][0], points[i][1]);
    }
    ctx.closePath();

    ctx.fillStyle = hasStatus ? "rgba(0, 200, 0, 0.3)" : "rgba(255, 0, 0, 0.3)";
    ctx.strokeStyle = "#000";
    ctx.lineWidth = 1;
    ctx.fill();
    ctx.stroke();

    const cx = points.reduce((sum, p) => sum + p[0], 0) / points.length;
    const cy = points.reduce((sum, p) => sum + p[1], 0) / points.length;

    ctx.fillStyle = "black";
    ctx.font = "6px sans-serif";
    let splitLabel = label.split(",")

    ctx.fillText(`${splitLabel[1]},${splitLabel[2]}`, cx-5, cy+5);
  });
  updateCounts();
}

// 🌐 API로 폴리곤 로딩
async function loadPolygons(ccmValue) {
  const res = await fetch(`/canvas/polygons?ccm=${ccmValue}`);
  const data = await res.json();
  polygonsCache = data;
  offsetX = 0;
  offsetY = 0;
  scaleFactor = 1.0;
  requestRedraw();
}

// 🔀 CCM 선택 변경
select.addEventListener("change", () => {
  loadPolygons(select.value);
});

// 🔍 마우스 휠 줌
canvas.addEventListener("wheel", (event) => {
  event.preventDefault();
  const zoom = event.deltaY < 0 ? 1.1 : 0.9;
  const mx = event.offsetX;
  const my = event.offsetY;
  const worldX = (mx - offsetX) / scaleFactor;
  const worldY = (my - offsetY) / scaleFactor;
  scaleFactor *= zoom;
  scaleFactor = Math.min(Math.max(scaleFactor, 0.2), 5);
  offsetX = mx - worldX * scaleFactor;
  offsetY = my - worldY * scaleFactor;
  requestRedraw();
}, { passive: false });

// 👆 드래그 이동
canvas.addEventListener("mousedown", (e) => {
  isDragging = true;
  dragStart = { x: e.clientX - offsetX, y: e.clientY - offsetY };
});
canvas.addEventListener("mousemove", (e) => {
  if (isDragging) {
    offsetX = e.clientX - dragStart.x;
    offsetY = e.clientY - dragStart.y;
    requestRedraw();
  }
});
canvas.addEventListener("mouseup", () => isDragging = false);
canvas.addEventListener("mouseleave", () => isDragging = false);

// 🖱 클릭 → 상태 입력
canvas.addEventListener("click", (event) => {
  const canvasX = (event.offsetX - offsetX) / scaleFactor;
  const canvasY = (event.offsetY - offsetY) / scaleFactor;

  ctx.setTransform(1, 0, 0, 1, 0, 0);

  for (const poly of polygonsCache) {
    const pts = poly.points;
    ctx.beginPath();
    ctx.moveTo(pts[0][0] * scaleFactor + offsetX, pts[0][1] * scaleFactor + offsetY);
    for (let i = 1; i < pts.length; i++) {
      ctx.lineTo(pts[i][0] * scaleFactor + offsetX, pts[i][1] * scaleFactor + offsetY);
    }
    ctx.closePath();

    if (ctx.isPointInPath(event.offsetX, event.offsetY)) {
      const status = prompt(`📝 "${poly.label}" 주차면의 상태 입력:`);
      if (status && status.trim() !== "") {
        statusMap[poly.label] = status.trim();
        saveStatusToStorage();
        requestRedraw();
      }
      break;
    }
  }
});

function updateCounts() {
  count.textContent = polygonsCache.length;
  let filled = polygonsCache.filter(poly => statusMap[poly.label]).length;
  finishCount.textContent = filled;
}

canvas.addEventListener("mousemove", (e) => {
  if (isDragging) {
    offsetX = e.clientX - dragStart.x;
    offsetY = e.clientY - dragStart.y;
    requestRedraw();
    tooltip.style.visibility = "hidden";
    return;
  }

  const canvasX = (e.offsetX - offsetX) / scaleFactor;
  const canvasY = (e.offsetY - offsetY) / scaleFactor;

  let found = false;
  ctx.save();
  ctx.setTransform(1, 0, 0, 1, 0, 0); // reset to default

  for (const poly of polygonsCache) {
    const label = poly.label;
    const points = poly.points;

    ctx.beginPath();
    ctx.moveTo(points[0][0] * scaleFactor + offsetX, points[0][1] * scaleFactor + offsetY);
    for (let i = 1; i < points.length; i++) {
      ctx.lineTo(points[i][0] * scaleFactor + offsetX, points[i][1] * scaleFactor + offsetY);
    }
    ctx.closePath();

    if (ctx.isPointInPath(e.offsetX, e.offsetY)) {
      const status = statusMap[label];
      if (status) {
        tooltip.style.left = `${e.pageX + 10}px`;
        tooltip.style.top = `${e.pageY + 10}px`;
        tooltip.innerText = `입력값: ${status}`;
        tooltip.style.visibility = "visible";
        found = true;
      }
      break;
    }
  }

  if (!found) {
    tooltip.style.visibility = "hidden";
  }

  ctx.restore();
});

canvas.addEventListener("mouseleave", () => {
  isDragging = false;
  tooltip.style.visibility = "hidden";
});


document.getElementById("exportExcelBtn").addEventListener("click", () => {

  let item = localStorage.getItem("parkingStatusMap");
  const entries = Object.entries(JSON.parse(item));

  const data = entries.map(([key, value]) => {
    const [ccm, scm, usm] = key.split(",");
    return {
      KEY : key,
      CCM: ccm,
      SCM: scm,
      USM: usm,
      PKS: value
    };
  });

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "주차면 상태");
  XLSX.writeFile(workbook, "주차면_상태값.xlsx");
});

// 🚀 초기화
loadStatusFromStorage();
resizeCanvas();
loadPolygons(select.value);