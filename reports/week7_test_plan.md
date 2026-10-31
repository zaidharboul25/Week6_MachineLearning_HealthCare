# HealthConnect Clinic Experience Lab — Week 7 Formal ML Test Plan
**Document ID:** HC-W7-ML-TESTPLAN-01  
**Project:** Improving Patient Appointment Attendance and Healthcare Support Using Data and AI  
**Track:** Machine Learning Engineering  
**Lead Engineer:** Zaid Harboul  
**Organization:** AnalystLab Africa Experience Lab Internship Programme  
**Target Environment:** Windows 11, Python 3.12, scikit-learn 1.8, XGBoost 3.2, FastAPI 0.138, Pytest 9.1  

---

## 1. Executive Summary & Test Strategy

During Week 6, the HealthConnect Machine Learning Engineering team successfully integrated the initial analytical pipelines, connecting relational patient datasets to predictive models for insurance claims approval, billing amount regression, admission triage, and patient experience classification. 

Week 7 shifts focus from initial component integration to **systematic verification, reliability engineering, fault injection, edge-case hardening, and end-to-end validation**. This Test Plan formalizes the testing methodology across five core functional dimensions:
1. **Data Ingestion & Integrity Testing (Category A)**
2. **Preprocessing & Feature Engineering Testing (Category B)**
3. **Model Invariants & Contract Testing (Category C)**
4. **Integration & API Serving Testing (Category D)**
5. **Robustness & Fault Tolerance Testing (Category E)**

---

## 2. Test Architecture & Directory Structure

Tests are organized into a strict three-tier hierarchical architecture conforming to enterprise Python standards:

```text
tests/
├── conftest.py                           # Shared fixtures & synthetic healthcare datasets (Zero PII)
├── unit/
│   ├── test_data_unit.py                 # Category A: Data cleaning, type casting, schema validation
│   ├── test_preprocessing_unit.py        # Category B: Feature engineering, scaling, one-hot encoding
│   └── test_model_unit.py                # Category C: Model contracts, probabilities, metrics
├── integration/
│   ├── test_pipeline_integration.py      # Category D: Chained execution (Raw -> Clean -> Prep -> Infer)
│   └── test_api_integration.py           # Category D: FastAPI HTTP endpoints (/health, /predict/*)
└── validation/
    ├── test_cross_track_validation.py    # Category D: Data Science -> ML Engineering interface contracts
    ├── test_reproducibility_validation.py# Category B/C: Bit-for-bit determinism across repeated executions
    └── test_robustness_validation.py     # Category E: Malformed data, NaNs, novel categories, hostile payloads
```

---

## 3. Comprehensive Test Categories & Acceptance Criteria

### Category A: Data Ingestion & Schema Tests
* **Objective:** Ensure data ingested from external sources, databases, or API payloads conforms to required column definitions, valid data types, and realistic domain bounds before entering analytical pipelines.
* **Scope & Scenarios:**
  - Mandatory column verification across all 4 modeling schemas (Claims, Billing, Triage, Satisfaction).
  - Type-safety checks: ensuring numeric columns can be cast safely and rejecting corrupted strings.
  - Value boundary auditing: patient Age $\in [0, 120]$, BMI $\in [10.0, 70.0]$, Doctor Experience $\in [0, 50]$.
  - Financial sanity: Billing and Claim amounts $\ge 0.0$ RWF.
  - String normalization: automated trimming of leading/trailing whitespace across categorical variables.
* **Acceptance Criteria:** Missing required columns trigger explicit `HealthConnectSchemaError`. Empty datasets trigger `HealthConnectDataError`. Boundary violations in cleaning functions are safely clipped without dropping rows.

### Category B: Preprocessing & Feature Engineering Tests
* **Objective:** Verify that feature transformations, mathematical derivations, scaling, and encodings are mathematically correct, reproducible, and leak-free.
* **Scope & Scenarios:**
  - Demographic binning: Exact boundary validation for WHO BMI classifications and 5-tier age groups.
  - Derived financial features: Calculation of `ClaimToBillingRatio = ClaimAmount / BillingAmount`, `ClaimDiff = BillingAmount - ClaimAmount`, and boolean flag `IsFullClaim`.
  - Imputation & scaling parity: Verifying that `SimpleImputer` replaces missing values using median/mode parameters learned during training, preventing inference crashes.
  - One-Hot Encoding: Ensuring novel, unseen categorical levels at inference time produce zero-vectors without throwing index errors (`handle_unknown="ignore"`).
* **Acceptance Criteria:** Feature arrays generated during repeated runs must be bit-for-bit identical ($L_\infty \text{ norm} = 0.0$). Shape and column order must remain invariant between training and inference.

### Category C: Model Contracts & Prediction Invariants
* **Objective:** Verify that all 7 serialized machine learning artifacts deserialize cleanly and produce well-formed, bounded predictions and calibrated probabilities.
* **Scope & Scenarios:**
  - Model deserialization: Validation of `claims_classifier.joblib`, `billing_regressor.joblib`, `satisfaction_classifier.joblib`, `admission_triage_classifier.joblib`, `patient_clusterer.joblib`, `facility_clusterer.joblib`, and `anomaly_detector.joblib`.
  - Prediction contracts: Regression outputs strictly $> 0$ RWF; binary classification outputs $\in \{0, 1\}$; multiclass satisfaction outputs $\in \{\text{"Low"}, \text{"Medium"}, \text{"High"}\}$.
  - Probability calibration: For classification models exposing `predict_proba()`, verifying that $\sum_{k} P(y=k|X) = 1.0 \pm 10^{-6}$ and individual probabilities lie in $[0.0, 1.0]$.
  - Evaluation metric functions: Validating correctness of `evaluate_classifier()` (Accuracy, Precision, Recall, F1, ROC-AUC) and `evaluate_regressor()` (RMSE, MAE, $R^2$, MAPE).
* **Acceptance Criteria:** Zero unhandled exceptions during inference on valid payloads. 100% of serialized model files load within $< 500\text{ ms}$.

### Category D: Integration & Serving Layer Tests
* **Objective:** Verify the seamless interoperability of chained pipeline stages and the production HTTP serving layer built with FastAPI.
* **Scope & Scenarios:**
  - End-to-end component chaining: `Raw Tables \to Data Cleaner \to Feature Engineer \to Schema Validator \to Model Predict \to Decision Output`.
  - Service readiness probe: `GET /health` returning HTTP 200, operational status `"Healthy"`, and list of loaded models.
  - Serving endpoints: `POST /predict/claims`, `POST /predict/billing`, `POST /predict/triage`, `POST /predict/satisfaction`.
  - Error code compliance: HTTP 422 for schema/type validation failures; HTTP 503 for missing model artifacts.
* **Acceptance Criteria:** All valid requests return HTTP 200 with structured JSON response payloads. All malformed requests return HTTP 422 with actionable diagnostic details without leaking internal system traces.

### Category E: Robustness & Fault Tolerance Tests
* **Objective:** Validate system resilience under adverse operating conditions, corrupted inputs, network/disk failures, and hostile payloads.
* **Scope & Scenarios:**
  - Missing numeric values: Payloads containing `NaN` in key numeric fields (`BMI`, `DoctorExperience`, `PatientToDoctorRatio`).
  - Unseen categories: Ingestion of novel diagnosis strings, foreign provinces, or unknown insurance carriers.
  - Boundary stress: Payloads with maximum plausible ages ($120$), massive appointment volumes ($50,000$), or zero-amount claims.
  - Empty datasets: Ingestion of zero-row DataFrames.
* **Acceptance Criteria:** Pipeline handles missing values and novel categories gracefully via built-in imputers and encoders without unhandled crashes. Corrupted schemas raise controlled custom domain exceptions (`HealthConnectSchemaError`).

---

## 4. Test Execution & Reporting Protocol

| Execution Level | Tool / Framework | Frequency | Target Pass Rate | Output Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Unit Testing** | `pytest tests/unit/` | Per commit / modification | 100% | Console logs, test registry |
| **Integration Testing**| `pytest tests/integration/`| Nightly / PR review | 100% | FastAPI TestClient logs |
| **Validation Testing** | `pytest tests/validation/` | Pre-release | 100% | Determinism metrics, diff logs |
| **End-to-End Orchestrator**| `python scripts/run_e2e_validation.py` | Weekly sign-off | 100% | `week7_e2e_validation_results.csv` |

All test cases, executions, defects, and retests are formally logged in `reports/week7_test_results.csv` and `reports/week7_issue_log.csv`.

