# TTKG Calculator — Transtubular Potassium Gradient

> **Nephrology** — Renal Potassium Handling Assessment

## Overview

Real clinical calculator for evaluating renal potassium handling using the transtubular potassium gradient (TTKG), urine K/Cr ratio, and transtubular sodium gradient (TTNaG) to differentiate renal vs extrarenal causes of hypo- and hyperkalemia.

**References:** West ML et al. (NEJM 1986), Kamel KS et al. (Kidney Int 2002)

## Formulas Implemented

| Calculator | Formula |
|:-----------|:--------|
| **TTKG** | (UK × POsm) / (UOsm × PK) |
| **Urine K/Cr** | UK / UCr (mEq/g) |
| **TTNaG** | (UNa × POsm) / (UOsm × PNa) |

## CLI Usage

```bash
# TTKG in hypokalemia
python ttkg_calc.py ttkg --urine-k 15 --plasma-osm 285 --urine-osm 400 --plasma-k 2.8

# TTKG in hyperkalemia
python ttkg_calc.py ttkg --urine-k 30 --plasma-osm 290 --urine-osm 350 --plasma-k 6.5

# Urine K/Cr ratio
python ttkg_calc.py k-cr --urine-k 25 --urine-cr 100

# Transtubular Na gradient
python ttkg_calc.py ttnag --urine-na 20 --plasma-na 140 --urine-osm 400 --plasma-osm 285

# Full potassium assessment
python ttkg_calc.py full --urine-k 15 --plasma-k 2.8 --plasma-osm 285 --urine-osm 400 --urine-cr 80
```

## Python API

```python
from ttkg_calc import calc_ttkg, calc_urine_k_cr_ratio, full_potassium_assessment

# TTKG in hypokalemia
result = calc_ttkg(urine_k=15, plasma_osm=285, urine_osm=400, plasma_k=2.8)
print(result["ttkg"])  # ~3.8
print(result["interpretation"])  # "Indeterminate"

# Full assessment
full = full_potassium_assessment(urine_k=15, plasma_k=2.8,
                                  plasma_osm=285, urine_osm=400, urine_cr=80)
```

## Interpretation Guide

### Hypokalemia (K < 3.5)
| TTKG | Interpretation |
|:-----|:---------------|
| < 2 | Appropriate K conservation (extrarenal loss) |
| > 4 | Inappropriate K wasting (renal cause) |

### Hyperkalemia (K > 5.0)
| TTKG | Interpretation |
|:-----|:---------------|
| < 6 | Inappropriate K retention (hypoaldosteronism) |
| > 10 | Appropriate K excretion (extrarenal cause) |

## License

MIT License.
