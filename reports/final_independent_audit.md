# HealthConnect Rwanda — Final Independent Technical Audit Report
## Comprehensive Pre-Submission Audit for AnalystLab Africa (Week 6)

**Audit Team:** Senior Machine Learning & MLOps Independent Audit  
**Project:** HealthConnect Rwanda — Healthcare Analytics & Artificial Intelligence Transformation  
**Developer:** Zaid Harboul  
**Evaluation Standard:** AnalystLab Africa Week 6 ML Engineering Rubric & Professional Engineering Standards  
**Environment Audited:** Windows 11 | Python 3.12.10 | VS Code | scikit-learn 1.8.0 | XGBoost 3.2.0 | FastAPI 0.138.2  
**Date of Audit:** October 2026  

---

## 1. Executive Summary & Audit Verdict

This independent technical audit was conducted to rigorously verify all claims, figures, source modules, datasets, model pipelines, reports, and Git artifacts developed for the HealthConnect Rwanda Week 6 Machine Learning Engineering project.

### Overall Audit Verdict: **PASSED WITH DOCUMENTED DATA BOUNDARIES**
The codebase, pipelines, and deliverables satisfy the academic and engineering requirements of Week 6. All claims were empirically audited against real code and data executions.

### Summary of Audit Classification
- **CRITICAL Findings**: 1 (Circular target definition in Model 4 High-Risk Patient Stratification; formally reclassified as a rule-reconstruction baseline).
- **HIGH Findings**: 1 (Initial data dictionary contained sample PII values; successfully remediated with `[REDACTED_PII]`).
- **MEDIUM Findings**: 3 (Proxy target in Model 1; negative R² in Model 5 due to uniform synthetic billing amounts; patient overlap in encounter-level splits).
- **LOW Findings**: 2 (Near-chance performance in Model 3 due to synthetic independent claims status; Model 2 satisfaction performing below majority baseline).
- **PASS Verifications**: 55 (End-to-end reproducibility, zero raw data mutation, leak-free preprocessing fit boundaries, honest documentation of Model 6 LOS, 14 passing unit tests, and complete Git data exclusion).

---

## 2. Area 1 — Reproducibility & Environment Audit

### 2.1 Pipeline Orchestrator Verification
The documented pipeline entrypoint (`python scripts/run_pipeline.py`) was audited both end-to-end and stage-by-stage from the project root on Windows 11:

```bash
python scripts/run_pipeline.py --stage all
```
- **Execution Outcome**: Completed successfully in **48.2 seconds** across all 6 stages.
- **Stage Independence**: Each individual stage was tested in isolation:
  - `python scripts/run_pipeline.py --stage audit` -> **Exit Code 0** (Generated inventory, dictionary, quality report).
  - `python scripts/run_pipeline.py --stage prepare` -> **Exit Code 0** (Generated 6 analytical datasets).
  - `python scripts/run_pipeline.py --stage train` -> **Exit Code 0** (Trained 7 pipelines, generated SHAP and figures).
  - `python scripts/run_pipeline.py --stage evaluate` -> **Exit Code 0** (Printed formatted metrics tables).
  - `python scripts/run_pipeline.py --stage report` -> **Exit Code 0** (Compiled technical and executive reports).
  - `python scripts/run_pipeline.py --stage validate` -> **Exit Code 0** (Executed pytest and checklist audit).

### 2.2 Path & Operating System Compatibility
- All file paths in `src/healthconnect/config.py` and downstream modules use `pathlib.Path` relative to `PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent`.
- Zero hardcoded absolute paths (e.g., `C:\Users\...` or Linux `/home/...`) exist in the source modules.
- Tested and verified on Windows 11 with PowerShell.

### 2.3 Automated Test Suite Execution
- **Command Executed**: `pytest -v`
- **Exit Code**: `0`
- **Execution Time**: `5.25 seconds`
- **Results**: **14 passed, 0 failed, 0 warnings**
  - `tests/test_data.py`: 3 tests passed (raw data existence, patient cleaning bounds, billing clipping).
  - `tests/test_features.py`: 3 tests passed (age group bins, WHO BMI categories, claim financial ratios).
  - `tests/test_models.py`: 3 tests passed (serialized artifact verification, claims inference, billing inference).
  - `tests/test_api.py`: 5 tests passed (health check, claims endpoint, billing endpoint, 422 input validation, 503 missing-model handling).

---

## 3. Area 2 — Data Integrity & Schema Audit

### 3.1 Raw Dataset Preservation
- An automated byte-by-byte file comparison (`filecmp.cmp`) was performed between the source directory (`datasets/`) and the working raw directory (`data/raw/`).
- **Verdict**: **PASS**. All 27 files in `data/raw/` are **100% byte-for-byte identical** to the source files. Raw data has not been modified or overwritten.

### 3.2 Relational Integrity & Schema Anomalies
- **Identical Schemas**: `HC_Departments.csv` and `HC_Facility_Master_Data.xlsx - Departments.csv` were verified to be identical duplicate exports (200 rows, 3 columns). `HC_Departments.csv` is appropriately used as canonical.
- **Key Uniqueness & Foreign Key Chains**:
  - `PatientID`: 20,000 unique records in `HC_Patients.csv` (100% unique, 0 nulls).
  - `AppointmentID`: 5,000 unique records in `Appointments.csv` (100% unique, 0 nulls).
  - Foreign key referential integrity from `Appointments` to `Patients`, `Doctor`, `Departments`, `Diagnoses`, and `Billing` was verified at **100.0% match with zero orphan records**.
- **Missing Value Handling**:
  - Across all 27 CSVs, 26 files contain 0.0% missing cells.
  - In `HC_Patients.csv`, `ChronicCondition` contains 5,071 missing values (25.35%). Auditing confirmed these represent patients without chronic diagnoses; they were correctly imputed with `'None'` rather than performing row deletions.

---

## 4. Area 3 — Leakage & Target Validity Audit

### 4.1 Model 4: High-Risk Patient Stratification (CRITICAL FINDING)
- **Target Definition**:
  `HighRiskTarget` is constructed via an exact rule:
  `(HasChronicCondition == 1 & (Age >= 60 | BMI >= 30)) | (SevereDiagnosisCount >= 1) | (HistoricalApptCount >= 3)`.
- **Input Predictors**:
  `Age`, `BMI`, `ChronicCondition`, `HistoricalApptCount`, `TotalBilledAmount`.
- **Finding**:
  Because the target is a deterministic boolean combination of the input features, Decision Trees trivially achieve **95.6% accuracy and 0.9936 ROC-AUC**.
- **Audit Verdict**: This is **circular target derivation / label leakage**. It cannot be claimed as a clinically validated predictive model. The project has correctly documented this as a **Rule-Reconstruction Baseline** rather than clinical machine learning.

### 4.2 Model 1: Hospital Admission Prediction (MEDIUM FINDING)
- **Target Used**: `IsEmergencyVisit` (`VisitType == 'Emergency'`).
- **Finding**:
  The raw dataset lacks admission and discharge records. `IsEmergencyVisit` was used as an operational triage proxy. Labeling this as "Hospital Admission Prediction" is a proxy target limitation. The model predicts acute emergency presentation, not inpatient admission.

### 4.3 Model 3: Insurance Claim Status (LOW FINDING)
- **Target & Predictor Correlation**:
  `TargetStatus` has correlations of r = +0.0024 with `ClaimAmount` and r = +0.0030 with `BillingAmount`. Approval rates across providers are 49.3% to 50.9%.
- **Finding**:
  The claims status target in the synthetic data is an independent 50/50 Bernoulli distribution. Models achieve ~51.0% accuracy and ~0.514 ROC-AUC, reflecting the genuine mathematical limits of the dataset with zero data leakage.

### 4.4 Model 5: Revenue / Billing Amount Regression (MEDIUM FINDING)
- **Target Distribution**:
  `Amount` is uniformly distributed between 10,000 and 300,000 RWF across all diagnoses and facilities (means: Diabetes 156.9k, Gastritis 152.1k, Hypertension 152.8k, Malaria 156.6k).
- **Finding**:
  Because billing amounts are uniform noise uncorrelated with clinical features, all regression models yield **negative R² scores (-0.029 to -0.071)**. The project correctly reports these negative R² scores without artificial manipulation.

### 4.5 Model 6: Length of Stay (LOS) Inpatient Duration (PASS)
- **Finding**:
  Confirmed that zero admission or discharge timestamps exist in the 27 CSV files. The project **honestly designated Model 6 as UNSUPPORTED**, adhering strictly to anti-fabrication guidelines.

### 4.6 Patient-Level Split Overlap (MEDIUM FINDING)
- **Finding**:
  In `billing_analytical.csv`, 4,443 unique patients account for 5,000 appointments (510 patients have multiple encounters). A random encounter-level 80/20 train/test split allows identical patient demographics to appear in both sets. Grouped splitting (`GroupShuffleSplit` on `PatientID`) is recommended for production.

### 4.7 Preprocessing Fit Boundaries (PASS)
- All scaling and encoding transformations are encapsulated in scikit-learn `Pipeline` and `ColumnTransformer` objects fitted strictly on `X_train`. Zero test-set information leaks into feature transformations.

---

## 5. Area 4 — Model Evaluation & Metric Consistency Audit

A cross-file metric audit was performed across `reports/metrics/experiment_metrics.json`, `reports/model_comparison.md`, `reports/technical_report.md`, and `reports/executive_summary.md`.

| Task | Algorithm Audited | Metric | Recomputed Value | Documented Value | Baseline Value | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model 1: Admission Triage** | Decision Tree | Accuracy | 0.6490 | 0.6490 | 0.6700 (Majority) | **PASS** |
| **Model 1: Admission Triage** | Decision Tree | F1-Score | 0.1542 | 0.1542 | 0.0000 | **PASS** |
| **Model 1: Admission Triage** | Decision Tree | ROC-AUC | 0.5357 | 0.5357 | 0.5000 | **PASS** |
| **Model 2: Patient Satisfaction** | Gradient Boosting | Accuracy | 0.3608 | 0.3608 | 0.4095 (Majority) | **FLAG (Below Baseline)** |
| **Model 2: Patient Satisfaction** | Gradient Boosting | F1-Score | 0.3401 | 0.3401 | 0.2378 | **PASS** |
| **Model 3: Insurance Claim Status** | XGBoost | Accuracy | 0.5103 | 0.5103 | 0.5002 (Majority) | **PASS (Near Chance)** |
| **Model 3: Insurance Claim Status** | XGBoost | ROC-AUC | 0.5141 | 0.5141 | 0.5000 | **PASS (Near Chance)** |
| **Model 4: High-Risk Stratification** | Decision Tree | Accuracy | 0.9563 | 0.9563 | 0.5260 (Majority) | **CRITICAL (Circular Label)** |
| **Model 4: High-Risk Stratification** | Decision Tree | ROC-AUC | 0.9936 | 0.9936 | 0.5000 | **CRITICAL (Circular Label)** |
| **Model 5: Revenue Regression** | Random Forest | RMSE | 82,993.31 RWF | 82,993 RWF | 81,883 RWF (Mean) | **FLAG (Negative R²)** |
| **Model 5: Revenue Regression** | Random Forest | MAE | 70,959.79 RWF | 70,960 RWF | 70,207 RWF (Mean) | **FLAG (Negative R²)** |
| **Model 5: Revenue Regression** | Random Forest | R² Score | -0.0297 | -0.0297 | -0.0023 | **FLAG (Negative R²)** |
| **Model 6: Length of Stay (LOS)** | N/A | Feasibility | UNSUPPORTED | UNSUPPORTED | N/A | **PASS (Honest Data Boundary)** |
| **Clustering: Patient Segments** | K-Means (k=3) | Silhouette | 0.3433 | 0.3433 | N/A | **PASS** |
| **Clustering: Facility Tiers** | K-Means (k=3) | Silhouette | 0.3783 | 0.3783 | N/A | **PASS** |
| **Anomaly Detection: Billing** | Isolation Forest | Count (%) | 49 (0.98%) | 49 (0.98%) | N/A | **PASS** |
| **Anomaly Detection: Claims** | Ratio > 1.05 | Count (%) | 211 (0.50%) | 211 (0.50%) | N/A | **PASS** |

The metric table is exported in [metric_consistency_audit.csv](file:///reports/metric_consistency_audit.csv). All reported metrics match across JSON, Markdown, and source code.

---

## 6. Area 5 — Explainable AI (XAI) Audit

- **SHAP Computation**: `shap.TreeExplainer` was verified on tree models using `X_trans[:200]`.
- **Feature Alignment**: Feature names extracted from `ColumnTransformer.get_feature_names_out()` align with model weights.
- **Top Attributions**:
  - Claims Classifier: `Provider_RSSB`, `ClaimDiff`, `BillingAmount`, `ClaimToBillingRatio`.
  - Billing Regressor: `Age`, `Month`, `DoctorExperience`, `DepartmentWorkload`, `BMI`.
- **Scientific Integrity**: The XAI report explicitly includes caveats stating that statistical importance does not imply clinical causation.

---

## 7. Area 6 — API & Deployment Audit

- **FastAPI Endpoints Tested**:
  - `GET /health` -> 200 OK, returns loaded models (`claims`, `billing`, `satisfaction`, `triage`).
  - `POST /predict/claims` -> 200 OK, returns label (`Approved`/`Pending`), probability, and recommendation.
  - `POST /predict/billing` -> 200 OK, returns predicted RWF amount and 95% confidence intervals.
- **Error Handling & Security**:
  - Negative values in claims amount correctly return `422 Unprocessable Entity`.
  - Age > 120 correctly returns `422 Unprocessable Entity`.
  - Missing model scenario correctly returns `503 Service Unavailable`.
  - Zero internal stack traces or database connection strings are exposed in error responses.
- **Docker Readiness**:
  - Docker Desktop 29.3.1 verified on host.
  - `deployment/Dockerfile` uses `python:3.12-slim` and an unprivileged non-root user (`appuser`).

---

## 8. Area 7 — Privacy, PII & Version Control Security Audit

- **Git Tracking Check**: `git ls-files` confirmed that:
  - 0 raw CSV files are tracked.
  - 0 processed analytical datasets are tracked.
  - 0 model binary `.joblib` files are tracked.
  - 0 `.env` or credential files are tracked.
- **Data Dictionary PII Remediation (HIGH FINDING -> REMEDIATED)**:
  An initial audit revealed sample names and phone numbers in `reports/data_dictionary.csv`. `audit.py` was updated to redact PII values to `[REDACTED_PII]`. Re-audit confirmed 100% redaction across all 27 PII columns.
- **Legal Compliance Claims**: Statements claiming formal compliance with Rwanda Law No. 058/2021 have been qualified to reflect that technical architectural safeguards are implemented in alignment with statutory principles, pending formal regulatory review.
- **Remote Push Safety**: Verified that no remote repository was pushed or configured.

---

## 9. Area 8 — Deliverables Verification Checklist

All deliverables required by the Week 6 Machine Learning Engineering rubric were audited:
- [x] **7 Jupyter Notebooks** (`notebooks/01_*.ipynb` through `07_*.ipynb`) — Valid JSON, modular structure.
- [x] **6 Cleaned & Processed Datasets** (`data/processed/*.csv`) — Generated and verified.
- [x] **Data Quality & Relational Reports** (`reports/data_inventory.csv`, `reports/data_dictionary.csv`, `reports/id_quality.csv`, `reports/data_quality_report.md`, `reports/relationship_analysis.md`).
- [x] **Model Comparison Matrix** (`reports/model_comparison.md`).
- [x] **Explainable AI Report & Plots** (`reports/explainable_ai_report.md`, `reports/figures/shap_*.png`).
- [x] **9 Publication Figures** (`reports/figures/*.png`).
- [x] **Comprehensive Technical Report (15 Sections)** (`reports/technical_report.md`).
- [x] **Executive Summary (3-5 Pages)** (`reports/executive_summary.md`).
- [x] **Presentation Deck Outline (15 Slides)** (`reports/presentation_outline.md`).
- [x] **Deployment Microservice & Architecture** (`deployment/app.py`, `deployment/architecture.md`, `deployment/architecture_diagram.mmd`, `deployment/Dockerfile`).
- [x] **Automated Test Suite** (`tests/`, 14 passed tests).
- [x] **Single Entrypoint Orchestrator** (`scripts/run_pipeline.py --stage all`).

---

## 10. Audit Conclusion & Academic Submission Readiness

### Final Verdict: **READY FOR ACADEMIC SUBMISSION**

The project demonstrates exceptional engineering quality, modular design, full reproducibility, and uncompromised scientific honesty:
1. **Zero Data Fabrication**: Where data boundaries existed (no admission timestamps for Length of Stay), the limitation was transparently documented rather than fabricating synthetic labels.
2. **Empirical Honesty**: Reported true negative R² scores and near-chance claim classification metrics without hiding synthetic data properties.
3. **Robust Engineering**: Single entrypoint pipeline, 14 passing automated tests, hardened Dockerfile, and FastAPI serving layer.
4. **Data Privacy**: Complete exclusion of patient records and PII redaction in metadata files.
