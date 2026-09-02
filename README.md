# Transtubular Potassium Gradient TTKG

> **Domain:** Diagnostic Radiology & Medical Imaging AI  
> **Reference Guidelines & Standards:** `American College of Radiology (ACR) RADS & Fleischner Society`

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

Transtubular Potassium Gradient (TTKG) Calculator

Real implementations for:
- TTKG = (UK × POsm) / (UOsm × PK)
- Interpretation for hypo- and hyperkalemia
- Aldosterone assessment
- Urine K/Cr ratio
- Transtubular Na gradient (TTNaG)

References: West ML et al. (NEJM 1986), Kamel KS et al. (Kidney Int 2002)
Stdlib only.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Analytical Functions

- **`calc_ttkg()`**: Transtubular Potassium Gradient (TTKG).

TTKG = (UK × POsm) / (UOsm × PK)

Interpretation depends on clinical context:

In HYPOKALEMIA (K < 3.5):
    TTKG < 2: Appropriate renal K conservation (extrarenal loss)
    TTKG > 4: Inappropriate renal K wasting (renal cause)

In HYPERKALEMIA (K > 5.0):
    TTKG < 6: Inappropriate K retention (hypoaldosteronism, K-sparing diuretics)
    TTKG > 10: Appropriate renal K excretion (extrarenal cause)

Normal TTKG: 8-9

Args:
    urine_k: Urine potassium (mEq/L)
    plasma_osm: Plasma osmolality (mOsm/kg)
    urine_osm: Urine osmolality (mOsm/kg)
    plasma_k: Plasma/serum potassium (mEq/L)

Returns:
    Dict with TTKG and interpretation
- **`calc_urine_k_cr_ratio()`**: Urine K/Creatinine ratio.

Useful when urine osmolality not available.

UK/UCr (mEq/mg):
    < 13 mEq/g (or < 1.5 mEq/mmol): Appropriate K conservation
    > 200 mEq/g (or > 23 mEq/mmol): Significant K wasting

Args:
    urine_k: Urine potassium (mEq/L)
    urine_cr: Urine creatinine (mg/dL)

Returns:
    Dict with K/Cr ratio and interpretation
- **`calc_ttna_gradient()`**: Transtubular Sodium Gradient (TTNaG).

TTNaG = (UNa × POsm) / (UOsm × PNa)

Similar concept to TTKG but for sodium.
Low TTNaG (< 1): Effective Na reabsorption (volume depletion)
High TTNaG (> 3): Impaired Na reabsorption

Args:
    urine_na: Urine sodium (mEq/L)
    plasma_na: Plasma sodium (mEq/L)
    urine_osm: Urine osmolality (mOsm/kg)
    plasma_osm: Plasma osmolality (mOsm/kg)

Returns:
    Dict with TTNaG and interpretation
- **`full_potassium_assessment()`**: Complete potassium handling assessment.
- **`main()`** — calculates and validates main parameters.

---

## 📐 Mathematical Formulation & Logic

```text
  p_ttkg = sub.add_parser("ttkg", help="Calculate TTKG")
```

---

## 💻 CLI Quickstart & Usage

### 1. Guided Interactive Mode
```bash
python cli.py
```

### 2. Direct Parameterized Evaluation
```bash
python cli.py --input data.csv
```

### Parameter Reference
- `--interactive`: Launch guided terminal interactive wizard.
- `--input <path>`: Evaluate input from JSON or CSV specification.
- `--json`: Output deterministic structured results in JSON format.

### Input Data Schema

| Field | Description | Requirement |
|:------|:------------|:------------|
| `Patient_ID` | Parameter / observation metric | Required |
| `v1` | Parameter / observation metric | Required |
| `v2` | Parameter / observation metric | Required |
| `v3` | Parameter / observation metric | Required |

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active AST and regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py --tasks 1000 --concurrency 8
```

---

## 🐳 Container Deployment

```bash
docker build -t transtubular-potassium-gradient-ttkg .
docker run -p 8000:8000 transtubular-potassium-gradient-ttkg
```
