# Transtubular Potassium Gradient (TTKG)

An educational calculator for the historical transtubular potassium gradient and spot urine potassium/creatinine ratio. Includes a Python CLI, a standalone browser calculator, automated tests, and a separate demonstration FastAPI operations console.

## Clinical limitations

**TTKG is controversial and should not be used as a stand-alone diagnostic or treatment rule.** The classical estimate assumes negligible downstream osmole reabsorption, but medullary urea recycling violates that assumption. Some nephrology authors no longer use TTKG in patients with potassium disorders. The historical prerequisites are urine osmolality at least plasma osmolality and urine sodium at least 25 mEq/L; satisfying these does not establish clinical validity.

The spot urine K/creatinine ratio is an alternative assessment. In **hypokalemia**, a ratio **above 13 mEq/g creatinine** (approximately 1.5 mEq/mmol) suggests renal potassium wasting; interpretation requires clinical context, medication and acid-base assessment. Inputs should be contemporaneous. No output is a clinical recommendation.

References: [Kamel & Halperin (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8116912/), [Palmer & Clegg (2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6390907/), [Kardalas et al. (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5881435/).

## Browser calculator

The calculator lives in `docs/` and needs only a modern browser with JavaScript modules. The interface calculates TTKG and (with optional urine creatinine) spot urine K/Cr, reports whether the classical TTKG prerequisites are satisfied, and exports JSON. It works locally without Python, Pyodide, external libraries or a backend.

For local preview:

```bash
python -m http.server 8080 --directory docs
# Open http://localhost:8080/
```

All values remain in the browser's memory and are **not uploaded or persisted**. JSON is downloaded only when explicitly requested. Do not enter identifiable patient information.

## Python CLI

```bash
python cli.py ttkg --urine-k 5 --plasma-osm 285 --urine-osm 400 --plasma-k 2.5 --urine-na 30
python cli.py k-cr --urine-k 5 --urine-cr 100
python cli.py ttnag --urine-na 30 --plasma-na 140 --urine-osm 400 --plasma-osm 285
python cli.py full --urine-k 5 --plasma-k 2.5 --plasma-osm 285 --urine-osm 400 --urine-na 30 --urine-cr 100
```

The experimental TTNaG calculation is retained for compatibility; its historical thresholds are **not validated clinical diagnostic criteria**. The CLI and browser are intended for calculation checks and education.

## Backend demonstration

The optional FastAPI server includes generic task auditing, identifier-pattern filtering, an in-memory HMAC audit log, and a deterministic mock chat adapter. These rules and thresholds are **demonstrations, not validated clinical protocols**. Model providers other than `mock` are not implemented. The identifier filter is not a substitute for a formal PHI de-identification or compliance system, and the audit trail is not persistent across restarts.

```bash
python -m pip install -r requirements-dev.txt
uvicorn agents.api:app --host 127.0.0.1 --port 8000
# Open http://127.0.0.1:8000/console/
```

Docker deployment is available using `docker build -t ttkg .` and `docker run --rm -p 8000:8000 -e AUDIT_SECRET_KEY=<secure-random-key> ttkg`. Configure the audit key using a secret management mechanism for any non-disposable environment. The API has no authentication and must **not** be exposed to untrusted networks.

## Testing

```bash
python -m pip install -r requirements-dev.txt
pytest -q
python -m compileall -q agents ttkg_calc.py cli.py
node --test docs/logic.test.mjs   # Node.js 22 or newer
```

CI covers Python 3.10–3.12 and Node.js 22. Static assets are published from `docs/` by the GitHub Pages workflow when Pages deployment is enabled.

## Structure and license

- `ttkg_calc.py`, `cli.py` — Python calculations and command-line interface
- `docs/` — offline-capable browser calculator and JavaScript tests
- `agents/`, `web/` — optional API/demo operations console
- `tests/` and `test_ttkg_calc.py` — Python tests
- `.github/workflows/` — test and Pages deployment pipelines

Requires Python 3.10+ for the CLI and a modern browser (current Chromium, Firefox or Safari) for the static interface. Licensed under [MIT](LICENSE).
