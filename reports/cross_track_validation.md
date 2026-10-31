# HealthConnect Clinic Experience Lab — Cross-Track Interface Validation
**Collaboration Stream:** Data Science $\longleftrightarrow$ Machine Learning Engineering  
**Document Control:** HC-W7-CROSS-DS-MLE-01  
**Author:** Zaid Harboul (Lead Machine Learning Engineer)  
**Partner Track:** Data Science Track (HC-POD Modeling Stream)  
**Target System:** HealthConnect Rwanda Patient & Claims Prediction Stack  
**Date:** October 2026  

---

## 1. Context & Collaborative Scope

In the HealthConnect Clinic Experience Lab project, the **Data Science track** focuses on exploratory data analysis, hypothesis formulation, algorithm selection, statistical modeling, and feature importance analysis. The **Machine Learning Engineering track** is responsible for operationalizing those analytical models: building reproducible data pipelines, handling missing values, standardizing encodings, constructing high-throughput API endpoints, and validating system robustness.

During Week 7, our primary cross-track validation objective was to **establish, test, and harden the interface contract between the Data Science model specification and the ML Engineering production serving pipeline**.

> [!NOTE]
> **Integrity Disclosure:** The technical experiments, schema validations, and unit/integration tests documented herein were implemented and verified locally using synthetic, anonymized test fixtures conforming to the HealthConnect schema. This technical validation represents the engineering verification of the Data Science $\to$ ML Engineering contract.

---

## 2. Technical Interface Contract Specification

### Dependency Tested:
* **Component:** Insurance Claim Approval Classifier (`claims_classifier.joblib`) and Encounter Billing Regressor (`billing_regressor.joblib`).
* **Source Interface:** Data Science feature selection and model training specifications.
* **Consuming Interface:** ML Engineering data ingestion, schema validation layer (`src/healthconnect/data/validator.py`), and FastAPI inference service (`deployment/app.py`).

### Information Exchanged:

| Flow Direction | Artifact / Specification | Content & Format | Purpose |
| :--- | :--- | :--- | :--- |
| **Data Science $\to$ MLE** | Feature Schema Definition | Feature list: `[ClaimAmount, BillingAmount, ClaimToBillingRatio, ClaimDiff, IsFullClaim, Provider]` | Dictates expected input tensors and column names for inference |
| **Data Science $\to$ MLE** | Decision Threshold Policy | Binary threshold $\tau = 0.50$ on calibrated class probability $P(\text{Approved})$ | Dictates automated clearance vs manual review routing |
| **MLE $\to$ Data Science** | Pydantic Request Model | `ClaimsPredictionRequest` (JSON schema with `gt=0` constraints) | Ensures raw inputs from external clinic systems are sanitized |
| **MLE $\to$ Data Science** | Pipeline Feature Transformer | `ColumnTransformer` with `SimpleImputer` and `OneHotEncoder(handle_unknown='ignore')` | Solves missing value and unseen category crashes at serving time |

---

## 3. Collaborative Validation Scenarios & Observed Evidence

### Scenario 1: Exact Feature Alignment & Order Invariance
* **Objective:** Verify that the feature vector ingested by the serving pipeline perfectly mirrors the feature vector learned by the Data Science classifier.
* **Test Implementation:** `tests/validation/test_cross_track_validation.py::test_ds_mle_claims_feature_contract`
* **Expected Result:** Exact set match ($1:1$) across all 6 features: `ClaimAmount`, `BillingAmount`, `ClaimToBillingRatio`, `ClaimDiff`, `IsFullClaim`, `Provider`.
* **Observed Result:** **PASS**. The pipeline ColumnTransformer inspects exactly those 6 columns; all transformers bind without dimension mismatch.
* **Evidence:** Test execution output confirmed in test registry `TC_CRX_01`.

### Scenario 2: Simulated Schema Drift & Mismatch Detection
* **Objective:** Test how the ML serving pipeline behaves if upstream Data Science or operational data providers omit an engineered feature (e.g. passing raw amounts but omitting `ClaimToBillingRatio`).
* **Test Implementation:** `tests/validation/test_cross_track_validation.py::test_ds_mle_contract_detects_missing_ratio_feature`
* **Expected Result:** Pipeline must intercept the malformed payload early, prevent a silent scikit-learn internal crash, and raise an informative `HealthConnectSchemaError` naming the missing column.
* **Observed Result:** **PASS**. `HealthConnectSchemaError` raised: *"Missing required columns for model 'claims': ['ClaimToBillingRatio', 'ClaimDiff', 'IsFullClaim']"*.
* **Finding & Action:** Identified that raw API clients cannot be expected to pre-calculate `ClaimToBillingRatio`.
  - **Refinement Applied:** In `deployment/app.py`, the ML Engineering serving layer automatically calculates `ClaimToBillingRatio = ClaimAmount / max(BillingAmount, 1.0)`, `ClaimDiff = BillingAmount - ClaimAmount`, and `IsFullClaim = int(ClaimAmount >= BillingAmount)` inside the endpoint handler before passing the data to the model.
* **Retest Result:** Validated in `tests/integration/test_api_integration.py::test_predict_claims_success` (Status: PASS).

### Scenario 3: Decision Threshold Calibration & Contract Enforcement
* **Objective:** Ensure the serving layer strictly enforces the Data Science operational threshold policy ($\tau = 0.50$).
* **Test Implementation:** `tests/validation/test_cross_track_validation.py::test_ds_mle_probability_threshold_contract`
* **Expected Result:** If $P(\text{Approved}) \ge 0.50$, prediction must equal 1 (`Approved`), triggering automated payment clearance; if $< 0.50$, prediction must equal 0 (`Pending`), routing the claim to the manual verification queue.
* **Observed Result:** **PASS**. Binary predictions strictly conform to probability thresholding across all evaluation records.

---

## 4. Impact on the HealthConnect Project

1. **Elimination of Target & Serving Skew:** By establishing explicit schema definitions (`MODEL_FEATURE_SCHEMAS`) in `src/healthconnect/data/validator.py`, data drift and column ordering mismatches between modeling and serving were eliminated.
2. **Robustness Against Missing Data:** Integrating `SimpleImputer` into the scikit-learn pipeline resolved the risk of inference crashes when incoming clinical records contain missing attributes.
3. **Automated Administrative Workflow:** Claims with high confidence ($P \ge 0.50$) can be cleared automatically, while borderline claims are routed with clear diagnostic recommendation strings (`recommendation: "Route to manual claim verification queue"`).

---

## 5. Summary Matrix (Test $\to$ Finding $\to$ Action $\to$ Retest $\to$ Outcome)

| Step | Detail |
| :--- | :--- |
| **Collaborating Track** | Data Science $\longleftrightarrow$ Machine Learning Engineering |
| **Dependency Tested** | Claims & Billing feature schemas and serving interface |
| **Component Tested** | `src/healthconnect/data/validator.py`, `deployment/app.py`, `artifacts/claims_classifier.joblib` |
| **Information Received** | Feature lists, boundary distributions, probability decision thresholds ($\tau=0.50$) |
| **Information Provided** | Pydantic validation schemas, automated ratio derivations, error response codes (422/503) |
| **Testing Activity** | Unit & integration tests in `test_cross_track_validation.py` & `test_api_integration.py` |
| **Issue Identified** | API clients lacked automated ratio calculation; missing numerical values triggered pipeline crashes |
| **Action Taken** | Added ratio engineering directly into API route; embedded `SimpleImputer` into pipeline ColumnTransformer |
| **Retest Result** | **100% PASS** across all cross-track tests (`TC_CRX_01`, `TC_CRX_02`, `TC_CRX_03`) |
| **Evidence Path** | `reports/week7_cross_track_evidence.md`, `reports/week7_test_results.csv` |
| **Project Impact** | Seamless Data Science to ML Engineering interoperability, zero-crash serving layer |

