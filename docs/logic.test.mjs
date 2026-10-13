import test from "node:test";
import assert from "node:assert/strict";
import { assess } from "./logic.mjs";

const input = { urineK: 5, plasmaK: 2.5, plasmaOsm: 285, urineOsm: 400, urineNa: 30, urineCr: 100 };

test("TTKG formula and K/Cr units", () => {
  const out = assess(input);
  assert.ok(Math.abs(out.ttkg - 1.425) < 1e-10);
  assert.equal(out.urineKCr, 5);
  assert.equal(out.context, "Hypokalemia");
  assert.equal(out.assumptionsMet, true);
});

test("renal wasting threshold is 13 mEq/g, not 200", () => {
  const out = assess({ ...input, urineK: 25 });
  assert.equal(out.urineKCr, 25);
  assert.match(out.urineKCrInterpretation, /wasting/);
});

test("threshold boundary and absent optional results", () => {
  assert.match(assess({ ...input, urineK: 13 }).urineKCrInterpretation, /threshold/);
  const out = assess({ urineK: 5, plasmaK: 2.5, plasmaOsm: 285, urineOsm: 400 });
  assert.equal(out.urineKCr, null);
  assert.equal(out.assumptionsMet, false);
});

test("urine osmolality and sodium prerequisites", () => {
  assert.equal(assess({ ...input, urineOsm: 250 }).assumptionsMet, false);
  assert.equal(assess({ ...input, urineNa: 24 }).assumptionsMet, false);
  assert.equal(assess({ ...input, urineNa: 25, urineOsm: 285 }).assumptionsMet, true);
});

test("potassium status boundaries", () => {
  assert.equal(assess({ ...input, plasmaK: 3.5 }).context, "Normokalemia");
  assert.equal(assess({ ...input, plasmaK: 5 }).context, "Normokalemia");
  assert.equal(assess({ ...input, plasmaK: 5.1 }).context, "Hyperkalemia");
});

test("invalid values are rejected", () => {
  for (const v of [NaN, Infinity, -Infinity, 0, -1]) {
    assert.throws(() => assess({ ...input, plasmaK: v }));
  }
  assert.throws(() => assess({ ...input, urineK: -1 }));
  assert.throws(() => assess({ ...input, urineNa: -1 }));
  assert.throws(() => assess({ ...input, urineCr: 0 }));
  assert.throws(() => assess({ ...input, urineOsm: 0 }));
  assert.throws(() => assess({ ...input, plasmaOsm: Infinity }));
});
