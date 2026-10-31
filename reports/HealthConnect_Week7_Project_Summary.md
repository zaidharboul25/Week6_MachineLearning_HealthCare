# HealthConnect Clinic Experience Lab — Week 7 Project Summary
**Document Control:** HC-W7-PROJ-SUM-01  
**Programme:** AnalystLab Africa Experience Lab Internship Programme  
**Project Title:** Improving Patient Appointment Attendance and Healthcare Support Using Data and AI  
**Track:** Machine Learning Engineering  
**Lead Engineer:** Zaid Harboul  
**Week:** Week 7 — Testing, Refinement & End-to-End Validation  
**Date:** October 2026  

---

## 1. What You Planned to Test
The testing plan targeted five comprehensive dimensions of the HealthConnect ML pipeline:
1. **Data Ingestion & Integrity:** Checking column schemas, data types, missing values, duplicates, and domain boundaries across all 27 raw datasets and processed analytical tables.
2. **Preprocessing Transformations:** Validating mathematical accuracy of age binning, WHO BMI classifications, financial ratios (`ClaimToBillingRatio`, `ClaimDiff`), one-hot encodings, and scaling parameters.
3. **Model Invariants & Contracts:** Verifying deserialization, input/output tensor shapes, probability calibrations ($\sum P = 1.0$), non-negative regression bounds, and metric calculation functions across all 7 serialized artifacts.
4. **Integration & API Serving Layer:** Verifying component chaining (`Data \to Cleaning \to Feature Eng \to Model \to Prediction`) and live FastAPI endpoints (`/health`, `/predict/claims`, `/predict/billing`, `/predict/triage`, `/predict/satisfaction`), including HTTP 422 and 503 error handling.
5. **Robustness & Fault Tolerance:** Testing behavior under hostile inputs: injected NaNs, unseen categories, extreme out-of-range clinical values, and empty DataFrames.

---

## 2. What You Actually Tested
We implemented and executed an automated testing hierarchy comprising **65 test cases in Pytest** across three designated test tiers (`tests/unit/`, `tests/integration/`, `tests/validation/`), along with a dedicated **9-step End-to-End Validation Orchestrator** (`scripts/run_e2e_validation.py`). Every single model, cleaning module, feature engineering function, and API endpoint was exercised.

---

## 3. Most Important Testing Results
* **100% Final Suite Pass Rate:** All 65 automated Pytest tests passed successfully within 7.05 seconds.
* **100% End-to-End Execution:** All 9 stages of the E2E validation script completed successfully without unhandled errors.
* **Deterministic Reproducibility:** Inferences repeated across 5 consecutive cycles produced bit-for-bit identical classifications and floating-point regression outputs within $2.91 \times 10^{-11}$ tolerance.
* **Robust Serving Layer:** Live HTTP tests confirmed that FastAPI handles normal requests with 200 OK, malformed inputs with 422 Unprocessable Entity, and missing models with 503 Service Unavailable without leaking internal system traces.

---

## 4. Issues or Weaknesses Identified
During initial testing, 7 specific technical issues and 1 architectural data limitation were discovered:
1. **Missing Imputation in Pipelines:** In Week 6, `ColumnTransformer` lacked imputation; incoming NaNs in numeric features caused a catastrophic `ValueError: Input contains NaN` during inference.
2. **Unexposed Endpoints in API:** `deployment/app.py` loaded `satisfaction_classifier` and `admission_triage_classifier` in memory but lacked exposed route handlers for them.
3. **Data Cleaner KeyError:** `clean_billing` crashed with an unhandled `KeyError: 'Status'` if the optional `Status` column was omitted.
4. **Cleaner Plural Column Mismatch:** `clean_feedback` crashed when datasets used `'Comments'` instead of `'Comment'`.
5. **Missing Dependency Import:** `/predict/satisfaction` crashed with `NameError: name 'np' is not defined`.
6. **Feature Count Incompatibilities in Model Tests:** Test fixtures passed 3 features to `patient_clusterer` (which expects 6) and 2 features to `anomaly_detector` (which expects 3).
7. **Strict Equality Float Failure:** Floating-point noise ($2.91 \times 10^{-11}$) caused a strict bitwise equality assertion failure in reproducibility checks.
8. **Length of Stay Data Limitation:** Model 6 (LOS) cannot be trained or validated due to the complete absence of admission and discharge timestamps in raw clinical files.

---

## 5. Improvements & Refinements Made
1. **Imputation Hardening:** Embedded `SimpleImputer(strategy="median")` for numeric features and `SimpleImputer(strategy="most_frequent")` for categorical features across all classification and regression pipelines; retrained and re-serialized all artifacts.
2. **FastAPI Expansion:** Added `/predict/triage` and `/predict/satisfaction` endpoints with strict Pydantic schemas (`TriagePredictionRequest`, `SatisfactionPredictionRequest`).
3. **Cleaner Resilience:** Added column existence guards (`if 'Status' in df.columns:`) across all cleaner functions in `src/healthconnect/data/cleaner.py`.
4. **Data Validator Module:** Created `src/healthconnect/data/validator.py` with formal `MODEL_FEATURE_SCHEMAS`, boundary checks, and custom exception hierarchy (`HealthConnectSchemaError`, `HealthConnectDataError`).
5. **Assertion Tolerance:** Upgraded reproducibility assertions to scientific numerical tolerance (`abs(diff) < 1e-6`).

---

## 6. Retesting Results
Following implementation of the fixes, the entire suite was re-executed:
* `tests/integration/test_api_integration.py`: 8 passed (was 1 failed)
* `tests/integration/test_pipeline_integration.py`: 2 passed (was 1 failed)
* `tests/unit/test_data_unit.py`: 9 passed (was 1 failed)
* `tests/unit/test_model_unit.py`: 15 passed (was 2 failed)
* `tests/unit/test_preprocessing_unit.py`: 5 passed (was 1 failed)
* `tests/validation/test_reproducibility_validation.py`: 3 passed (was 1 failed)
* **Total Retest Result:** **65 / 65 PASSED (100% Success)**.

---

## 7. Which Track(s) You Collaborated With
Primary cross-track collaboration occurred with the **Data Science Track** (HC-POD Modeling Stream).

---

## 8. What Was Tested Collaboratively
We tested the formal interface contract between Data Science modeling specifications and the ML Engineering serving pipeline:
* Expected feature names, types, and column counts for claims approval and billing regression.
* Automated handling of derived features (`ClaimToBillingRatio`, `ClaimDiff`, `IsFullClaim`).
* Enforcement of the operational decision threshold policy ($\tau = 0.50$).
* Behavior under simulated contract violations (omitted features, unexpected data types).

---

## 9. What Changed as a Result
* Formally codified `MODEL_FEATURE_SCHEMAS` in `src/healthconnect/data/validator.py` to eliminate feature mismatch risks.
* Moved the computation of derived ratios inside the serving layer handler (`deployment/app.py`), relieving client applications from having to calculate model-specific ratios.
* Documented collaborative interface evidence in `reports/cross_track_validation.md` and `reports/week7_cross_track_evidence.md`.

---

## 10. Key Findings or Validation Outcomes
* The machine learning serving stack is now fully resilient against hostile and degraded inputs (NaNs, unseen categories, extreme values).
* The claims classifier accurately routes high-probability claims to automated clearance and low-probability claims to manual verification.
* The billing regressor provides reliable cost forecasts accompanied by a 95% statistical confidence interval ($[\text{Forecast} - 1.96 \times \text{RMSE}, \text{Forecast} + 1.96 \times \text{RMSE}]$).

---

## 11. Major Challenges Encountered
* **Handling Missing Values Without Data Leakage:** Implementing imputation inside the scikit-learn pipeline rather than as a global pandas operation ensured that imputation medians are strictly fitted on training splits and applied safely to inference payloads.
* **Balancing Strict Validation with API Usability:** Designing Pydantic schemas that validate essential clinical boundaries while allowing flexibility for derived fields.

---

## 12. Important Decisions Made
* **Decided to Retrain & Re-serialize All Models:** Rather than writing ad-hoc imputation logic in the API, we updated the model definitions in `classifier.py` and `regressor.py` to include `SimpleImputer` directly inside the serialized pipelines.
* **Decided to Formally Document Model 6 (LOS) as Unsupported:** Preserved engineering integrity by documenting the absence of admission/discharge timestamps rather than creating synthetic proxy dates.

---

## 13. Remaining Limitations
* **Model 6 (Length of Stay):** Cannot be modeled due to raw data limitations.
* **Patient Satisfaction Predictability:** Multiclass accuracy is ~38% because synthetic feedback ratings have near-uniform distribution across demographic features.

---

## 14. Remaining Issues or Dependencies
* Dependency on upstream operational databases to provide valid patient and appointment IDs in production.
* Need for real-world clinician and administrative feedback on the $\tau = 0.50$ claims decision threshold.

---

## 15. Your Contribution to the Overall HealthConnect Project
As Senior Machine Learning Engineer, Zaid Harboul:
* Engineered a hardened, enterprise-grade ML inference API serving 4 predictive models with full input validation and confidence intervals.
* Constructed a 65-test automated testing framework achieving 100% pass rate.
* Developed an automated 9-step End-to-End Validation Orchestrator.
* Codified interface contracts protecting the system from data drift and schema mismatch.
* Eliminated crash vulnerabilities through pipeline-embedded median and mode imputation.

---

## 16. What Must Be Completed Before Week 8
1. Package the serving layer into a finalized containerized deployment (review `deployment/Dockerfile`).
2. Coordinate with Cloud Engineering for deployment to staging/production hosting.
3. Integrate with Generative AI assistant to provide real-time appointment and billing predictions via conversational interfaces.
4. Prepare final project presentation and end-of-internship demonstration.

