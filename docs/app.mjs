import { assess } from "./logic.mjs";

const form = document.getElementById("calculator");
const resultEl = document.getElementById("results");
const errorEl = document.getElementById("error");
const exportButton = document.getElementById("export");
let lastResult = null;

function value(id, optional = false) {
  const el = document.getElementById(id);
  const raw = el.value.trim();
  if (raw === "" && optional) return null;
  if (raw === "") throw new Error(`Please enter ${el.labels[0].textContent.trim()}.`);
  const number = Number(raw);
  if (!Number.isFinite(number)) throw new Error(`Invalid value for ${id}.`);
  return number;
}
function paragraph(parent, content, className = "") {
  const p = document.createElement("p");
  if (className) p.className = className;
  p.textContent = content;
  parent.append(p);
}
function heading(parent, content) {
  const h = document.createElement("h3");
  h.textContent = content;
  parent.append(h);
}
function render(data) {
  resultEl.replaceChildren();
  const context = document.createElement("div");
  context.className = "tag";
  context.textContent = data.context;
  resultEl.append(context);
  const metric = document.createElement("div");
  metric.className = "metric";
  const number = document.createElement("div");
  number.className = "number";
  number.textContent = data.ttkg.toFixed(2);
  const unit = document.createElement("div");
  unit.className = "unit";
  unit.textContent = "TTKG · dimensionless";
  metric.append(number, unit);
  resultEl.append(metric);
  heading(resultEl, "Historical interpretation");
  paragraph(resultEl, data.assumptionsMet ? data.historical :
    "Prerequisites unverified or unmet. Historical categories must not be applied.", "small");
  if (data.urineKCr !== null) {
    heading(resultEl, "Spot urine potassium/creatinine");
    paragraph(resultEl, `${data.urineKCr.toFixed(1)} mEq/g creatinine`);
    paragraph(resultEl, data.urineKCrInterpretation, "small");
  }
  const warning = document.createElement("div");
  warning.className = "notice";
  const strong = document.createElement("strong");
  strong.textContent = data.assumptionsMet ? "Interpret with caution" : "Prerequisites not confirmed";
  warning.append(strong);
  const list = document.createElement("ul");
  for (const message of data.warnings) {
    const li = document.createElement("li");
    li.textContent = message;
    list.append(li);
  }
  warning.append(list);
  resultEl.append(warning);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  errorEl.hidden = true;
  try {
    const result = assess({
      urineK: value("urineK"), plasmaK: value("plasmaK"),
      urineOsm: value("urineOsm"), plasmaOsm: value("plasmaOsm"),
      urineNa: value("urineNa", true), urineCr: value("urineCr", true)
    });
    lastResult = result;
    exportButton.disabled = false;
    render(result);
  } catch (err) {
    lastResult = null;
    exportButton.disabled = true;
    resultEl.replaceChildren();
    paragraph(resultEl, "Calculation unavailable until the inputs are valid.", "muted");
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  }
});
form.addEventListener("reset", () => {
  lastResult = null;
  exportButton.disabled = true;
  errorEl.hidden = true;
  resultEl.replaceChildren();
  paragraph(resultEl, "Enter measurements and select Calculate.", "muted");
});
exportButton.addEventListener("click", () => {
  if (!lastResult) return;
  const blob = new Blob([JSON.stringify(lastResult, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "ttkg-results.json";
  link.click();
  URL.revokeObjectURL(url);
});
