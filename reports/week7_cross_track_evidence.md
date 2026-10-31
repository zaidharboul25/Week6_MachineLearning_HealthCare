# HealthConnect Rwanda — Week 7 Cross-Track Evidence Log
**Track:** Machine Learning Engineering  
**Stream:** HC-POD Technical Validation (Data Science $\longleftrightarrow$ ML Engineering)  
**Author:** Zaid Harboul  
**Status:** Validated & Verified  

---

## 1. Traceability & Interface Contract Specification

The interface contract between the Data Science model specification and the ML Engineering serving pipeline is formalized directly in code at `src/healthconnect/data/validator.py`:

```python
MODEL_FEATURE_SCHEMAS: Dict[str, Dict[str, List[str]]] = {
    "claims": {
        "required_columns": [
            "ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim", "Provider"
        ],
        "numeric_columns": ["ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim"],
        "categorical_columns": ["Provider"]
    },
    "billing": {
        "required_columns": [
            "Age", "BMI", "DoctorExperience", "FacilityApptVolume",
            "PatientToDoctorRatio", "BedToDoctorRatio", "DepartmentWorkload", "Month",
            "VisitType", "Diagnosis", "Severity", "Gender", "MaritalStatus",
            "Occupation", "Education", "InsuranceID", "ChronicCondition",
            "DepartmentName", "ProvinceName"
        ],
        ...
    }
}
```

---

## 2. Test Execution Logs & Evidence

### Test Execution 1: Feature Contract Verification
* **Test:** `tests/validation/test_cross_track_validation.py::TestCrossTrackInterfaceContracts::test_ds_mle_claims_feature_contract`
* **Log Output:**
  ```text
  PASSED tests/validation/test_cross_track_validation.py::TestCrossTrackInterfaceContracts::test_ds_mle_claims_feature_contract
  ```
* **Verification Detail:** The column transformer in `claims_classifier.joblib` requires exactly 6 features matching the Data Science specification: `ClaimAmount`, `BillingAmount`, `ClaimToBillingRatio`, `ClaimDiff`, `IsFullClaim`, and `Provider`. Verified in memory.

### Test Execution 2: Missing Ratio Detection (Hostile Input)
* **Test:** `tests/validation/test_cross_track_validation.py::TestCrossTrackInterfaceContracts::test_ds_mle_contract_detects_missing_ratio_feature`
* **Log Output:**
  ```text
  PASSED tests/validation/test_cross_track_validation.py::TestCrossTrackInterfaceContracts::test_ds_mle_contract_detects_missing_ratio_feature
  ```
* **Verification Detail:** Passing a DataFrame without `ClaimToBillingRatio` raised `HealthConnectSchemaError("Missing required columns for model 'claims': ['ClaimDiff', 'ClaimToBillingRatio', 'IsFullClaim']")`. Caught and verified.

### Test Execution 3: Decision Boundary Threshold Contract
* **Test:** `tests/validation/test_cross_track_validation.py::TestCrossTrackInterfaceContracts::test_ds_mle_probability_threshold_contract`
* **Log Output:**
  ```text
  PASSED tests/validation/test_cross_track_validation.py::TestCrossTrackInterfaceContracts::test_ds_mle_probability_threshold_contract
  ```
* **Verification Detail:** Prediction binary class exactly tracks $P(\text{Approved}) \ge 0.50$. Calibrated probabilities conform to unit simplex ($P(\text{Approved}) + P(\text{Pending}) = 1.0$).

---

## 3. Engineering Improvements Summary

1. **Autonomous Feature Derivation in Serving Layer:**  
   Raw HTTP clients only supply `Provider`, `ClaimAmount`, and `BillingAmount`. `deployment/app.py` autonomously engineers the derived features (`ClaimToBillingRatio`, `ClaimDiff`, `IsFullClaim`), isolating external clients from model-internal feature transformations.
2. **Standardized Pydantic Request Validation:**  
   Invalid values such as negative claim amounts or zero billing amounts are intercepted at the HTTP boundary with HTTP 422 before reaching the model pipeline.
3. **Imputation Safeguards:**  
   `SimpleImputer` embedded in the ColumnTransformer ensures that inference never crashes due to unexpected NaNs.

