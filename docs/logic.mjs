/**
 * Educational potassium-handling calculations. No patient information is stored.
 * Numeric conventions match the Python calculator in ttkg_calc.py.
 */
export function assess({ urineK, plasmaK, urineOsm, plasmaOsm, urineNa = null, urineCr = null }) {
  const values = { urineK, plasmaK, urineOsm, plasmaOsm };
  if (urineNa !== null) values.urineNa = urineNa;
  if (urineCr !== null) values.urineCr = urineCr;
  for (const [key, value] of Object.entries(values)) {
    if (typeof value !== "number" || !Number.isFinite(value)) {
      throw new Error(`${key} must be a finite number.`);
    }
  }
  if (plasmaK <= 0 || urineOsm <= 0 || plasmaOsm <= 0) {
    throw new Error("Plasma potassium and both osmolalities must be positive.");
  }
  if (urineK < 0 || (urineNa !== null && urineNa < 0)) {
    throw new Error("Urine potassium and sodium cannot be negative.");
  }
  if (urineCr !== null && urineCr <= 0) {
    throw new Error("Urine creatinine must be positive.");
  }
  const ttkg = (urineK * plasmaOsm) / (urineOsm * plasmaK);
  if (!Number.isFinite(ttkg)) throw new Error("Result exceeds the supported numeric range.");
  const assumptionsMet = urineOsm >= plasmaOsm && urineNa !== null && urineNa >= 25;
  const warnings = [
    "TTKG is a disputed historical estimate: medullary urea recycling violates a key assumption.",
  ];
  if (urineOsm < plasmaOsm) warnings.push("Urine osmolality must be at least plasma osmolality.");
  if (urineNa === null) warnings.push("Urine sodium is needed to check distal sodium delivery.");
  else if (urineNa < 25) warnings.push("Urine sodium below 25 mEq/L violates the traditional prerequisites.");
  const context = plasmaK < 3.5 ? "Hypokalemia" : plasmaK > 5 ? "Hyperkalemia" : "Normokalemia";
  let historical = "Not classified during normokalemia.";
  if (plasmaK < 3.5) {
    historical = ttkg < 2 ? "Historical range: potassium conservation" :
      ttkg <= 4 ? "Historical range: indeterminate" : "Historical range: possible renal potassium wasting";
  } else if (plasmaK > 5) {
    historical = ttkg < 6 ? "Historical range: reduced renal potassium secretion" :
      ttkg <= 10 ? "Historical range: indeterminate" : "Historical range: increased potassium secretion";
  }
  let urineKCr = null;
  let urineKCrInterpretation = null;
  if (urineCr !== null) {
    urineKCr = urineK / urineCr * 100; // urine K (mEq/L) / urine Cr (mg/dL) => mEq/g
    if (!Number.isFinite(urineKCr)) throw new Error("K/Cr ratio exceeds the numeric range.");
    urineKCrInterpretation = context !== "Hypokalemia"
      ? "Interpret the spot K/Cr ratio in the appropriate clinical context."
      : urineKCr < 13 ? "Below 13 mEq/g: renal potassium conservation is more likely."
      : urineKCr > 13 ? "Above 13 mEq/g: renal potassium wasting is possible."
      : "At the 13 mEq/g threshold; interpret with other findings.";
  }
  return { ttkg, context, historical, assumptionsMet, warnings, urineKCr, urineKCrInterpretation };
}
