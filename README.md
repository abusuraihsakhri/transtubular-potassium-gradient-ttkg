# Transtubular Potassium Gradient TTKG

> **Domain:** Clinical Nephrology & Electrolyte Physiology
> **References:** West ML et al. (NEJM 1986), Kamel KS et al. (Kidney Int 2002)

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

Transtubular Potassium Gradient (TTKG) Calculator for clinical assessment of renal potassium handling.

Real implementations for:
- TTKG = (UK × POsm) / (UOsm × PK)
- Interpretation for hypo- and hyperkalemia
- Aldosterone assessment
- Urine K/Cr ratio
- Transtubular Na gradient (TTNaG)

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

---

## 💻 CLI Quickstart & Usage

### Installation
```bash
pip install pydantic fastapi uvicorn pytest
```

### 1. Calculate TTKG
```bash
python cli.py ttkg --urine-k 60 --plasma-osm 285 --urine-osm 300 --plasma-k 4.0
```

### 2. Calculate Urine K/Cr Ratio
```bash
python cli.py k-cr --urine-k 25 --urine-cr 100
```

### 3. Calculate TTNaG
```bash
python cli.py ttnag --urine-na 50 --plasma-na 140 --urine-osm 300 --plasma-osm 285
```

### 4. Full Assessment
```bash
python cli.py full --urine-k 5 --plasma-k 2.5 --plasma-osm 285 --urine-osm 400 --urine-cr 100
```

### 5. Enterprise Supervisor Audit
```bash
python cli.py audit --task-id TASK-001 --primary-metric 12.0
```

### 6. Verify Audit Trail
```bash
python cli.py verify-audit
```

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances (`llama3`, `mistral`), Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Active Learning Bayesian Calibration:** Dynamic tracker updating worker reliability weights and monitoring Brier calibration drift.
* **FastAPI & Prometheus Telemetry:** Exposes OpenAPI 3.1 REST endpoints and operational Prometheus metrics (`/metrics`).

### Environment Variables

| Variable | Description | Required |
|:---------|:------------|:---------|
| `AUDIT_SECRET_KEY` | HMAC-SHA256 key for audit trail integrity | Recommended (generated if unset) |
| `MODEL_PROVIDER` | LLM provider (`mock`, `ollama`, `claude`, `openai`) | No (default: `mock`) |

---

## 🧪 Testing & Verification

Run the automated test suite:

```bash
pytest -v
```

Execute high-throughput batch simulation benchmarks:

```bash
python simulator.py 100
```

---

## 🐳 Container Deployment

```bash
docker build -t transtubular-potassium-gradient-ttkg .
docker run -p 8000:8000 --env AUDIT_SECRET_KEY=your-secure-key transtubular-potassium-gradient-ttkg
```

Or using Docker Compose:

```bash
cp .env.example .env
# Edit .env to set AUDIT_SECRET_KEY
docker-compose up -d
```

---

## 📁 Project Structure

```
transtubular-potassium-gradient-ttkg/
├── ttkg_calc.py          # Core calculation engine + CLI
├── cli.py                # CLI entry point
├── enrichment.py         # Enrichment engine suite
├── simulator.py          # High-throughput simulation
├── agents/               # Enterprise agent framework
│   ├── base.py           # PHI guard, audit trail, security
│   ├── models.py         # Pydantic schemas
│   ├── supervisor.py     # Multi-agent orchestrator
│   ├── workers.py        # Specialized domain workers
│   ├── llm_factory.py    # LLM provider factory
│   ├── api.py            # FastAPI REST server
│   ├── metrics.py        # Prometheus metrics
│   ├── streamer.py       # WebSocket telemetry
│   └── learning.py       # Bayesian calibration engine
├── tests/                # Test suite
├── web/                  # Operations console UI
├── Dockerfile
├── docker-compose.yml
└── openapi_spec.json
```
