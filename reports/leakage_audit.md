# HealthConnect Rwanda — Data Leakage & Target Validity Audit Report

**Auditor:** Independent Technical Audit Team  
**Developer:** Zaid Harboul  
**Project:** HealthConnect Rwanda — Week 6 Machine Learning Engineering  
**Date:** October 2026  
**Audit Scope:** Feature construction, target definitions, temporal horizons, patient overlap, and preprocessing fit boundaries across all 6 models.

---

## 1. Executive Summary & Findings Matrix

| Model / Problem | Target Analyzed | Input Features | Leakage / Validity Risk | Severity Classification | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Model 1: Admission Triage** | `IsEmergencyVisit` | Clinical encounter & demographics | Target is an acute care encounter proxy, not inpatient bed admission | **MEDIUM** | VERIFIED |
| **Model 2: Patient Satisfaction** | `SatisfactionClass` | Encounter & facility workloads | Survey comment text correctly excluded; features show near-zero mutual information with rating | **LOW** | VERIFIED |
| **Model 3: Insurance Claim Status** | `TargetStatus` | `ClaimAmount`, `BillingAmount`, ratios, provider | Pre-decision variables only; synthetic target exhibits 50/50 coin-flip distribution | **LOW** | VERIFIED |
| **Model 4: High-Risk Stratification** | `HighRiskTarget` | `Age`, `BMI`, `ChronicCondition`, appointment count | **Circular Target Derivation**: Target is defined by exact rule on input features, resulting in artificial 0.994 ROC-AUC | **CRITICAL** | VERIFIED |
| **Model 5: Revenue Regression** | `Amount` | Demographics, doctor experience, diagnosis, severity | Post-settlement payments correctly excluded; target is uniform noise resulting in negative R² (-0.0297) | **MEDIUM** | VERIFIED |
| **Model 6: Length of Stay (LOS)** | Inpatient Days | N/A | No admission or discharge timestamps exist in 27 CSVs; correctly marked as UNSUPPORTED | **PASS** | VERIFIED |
| **Patient Split Overlap** | Multiple encounters | Demographics & encounter features | 510 patients have >1 appointment; random split allows patient demographics in train & test | **MEDIUM** | VERIFIED |
| **Preprocessing Fit Boundaries** | All pipelines | `ColumnTransformer` & `Pipeline` | Scalers and OneHotEncoders are fitted strictly on `X_train` | **PASS** | VERIFIED |

---

## 2. In-Depth Model-by-Model Leakage Audits

### 2.1 Model 4: High-Risk Patient Stratification (CRITICAL FINDING)
- **Code Inspected**: `src/healthconnect/features/engineer.py` (`build_risk_stratification_dataset`) and `src/healthconnect/models/classifier.py`.
- **Target Derivation**:
  ```python
  is_high_risk = (
      ((df["HasChronicCondition"] == 1) & ((df["Age"] >= 60) | (df["BMI"] >= 30))) |
      (df["SevereDiagnosisCount"] >= 1) |
      (df["HistoricalApptCount"] >= 3)
  )
  df["HighRiskTarget"] = is_high_risk.astype(int)
  ```
- **Input Features Fed to Model**:
  ```python
  m4_num = ["Age", "BMI", "HistoricalApptCount", "TotalBilledAmount"]
  m4_cat = ["Gender", "MaritalStatus", "Occupation", "Education", "InsuranceID", "ChronicCondition", "BloodGroup"]
  ```
- **Audit Diagnosis**:
  The target variable `HighRiskTarget` is a deterministic boolean combination of `Age`, `BMI`, `ChronicCondition`, and `HistoricalApptCount`. These exact variables are provided as input features to the classification algorithms. Consequently, Decision Trees and tree ensembles trivially achieve **95.6% accuracy and 0.9936 ROC-AUC** by simply reconstructing the if-else branch conditions programmed into the target.
- **Scientific & Clinical Reality**:
  The raw `HC_Patients.csv` dataset contains NO clinical outcome ground-truth label (e.g., 30-day readmission, acute decompensation, mortality, or emergency hospitalization). 100% of patients have `Status == 'Active'`.
- **Remediation & Recommendation**:
  1. Formally document that Model 4 is a **Rule-Reconstruction Heuristic Baseline**, NOT a clinically validated prospective outcome predictor.
  2. The high metric (0.994 AUC) must be explicitly flagged as an artifact of deterministic target derivation rather than superior machine learning generalization.
  3. For real-world deployment, hospital information systems must record actual clinical adverse outcomes (e.g., emergency readmissions within 30 days) to train an un-leaked predictive classifier.

---

### 2.2 Model 1: Hospital Admission / Acute Care Triage (MEDIUM FINDING)
- **Code Inspected**: `src/healthconnect/features/engineer.py` (`IsEmergencyVisit`) and `src/healthconnect/models/classifier.py`.
- **Target Derivation**:
  ```python
  df["IsEmergencyVisit"] = (df["VisitType"] == "Emergency").astype(int)
  ```
- **Audit Diagnosis**:
  The business objective defined in the assignment specifications is to predict whether a patient will be admitted to the hospital. However, across all 27 supplied CSV files, there is NO inpatient admission registry, NO bed assignment transaction log, and NO admission status flag.
  The model predicts whether an encounter is an Emergency visit (`IsEmergencyVisit`) versus a Consultation or Follow-up. While acute emergency encounters frequently correlate with inpatient admission need, labeling this task as "Hospital Admission Prediction" constitutes a proxy target limitation.
- **Remediation**:
  Maintain explicit documentation stating that `IsEmergencyVisit` is an operational triage proxy for acute care necessity, and that true admission prediction is constrained by database schema omissions.

---

### 2.3 Model 3: Insurance Claim Status Classification (LOW FINDING)
- **Code Inspected**: `src/healthconnect/features/engineer.py` (`build_claims_analytical_dataset`).
- **Target & Predictors**:
  - Target: `TargetStatus` (`Approved`: 21,008; `Pending`: 21,028).
  - Predictors: `Provider`, `ClaimAmount`, `BillingAmount`, `ClaimToBillingRatio`, `ClaimDiff`, `IsFullClaim`.
- **Audit Diagnosis**:
  1. *Temporal Horizon*: All predictor features (`ClaimAmount`, `BillingAmount`, `Provider`) are established prior to claim adjudication and are legally present on the initial claim submission form.
  2. *Data Leakage Check*: An empirical correlation analysis between predictors and `TargetStatus` showed near-zero correlation across all fields:
     - `ClaimAmount`: r = +0.0024
     - `BillingAmount`: r = +0.0030
     - `ClaimToBillingRatio`: r = -0.0018
     - `Provider` approval rates: RSSB (50.9%), MMI (49.6%), Private (49.3%), Radiant (50.1%).
  3. The status label was generated as an independent 50/50 Bernoulli distribution. Models achieve ~51.0% accuracy and ~0.514 ROC-AUC, demonstrating zero target leakage and reflecting the true information-theoretic limit of the dataset.

---

### 2.4 Model 2: Patient Satisfaction Classification (LOW FINDING)
- **Code Inspected**: `src/healthconnect/features/engineer.py` (`build_satisfaction_analytical_dataset`).
- **Target & Predictors**:
  - Target: `SatisfactionClass` (`Low`, `Medium`, `High`) derived from survey `Rating` (1 to 5).
  - Predictors: Encounter type, patient demographics, doctor experience, department workload, billing amount.
- **Leakage Prevention Verification**:
  The free-text survey comment (`Comment`: 'Poor', 'Average', 'Good', 'Excellent') was submitted simultaneously with `Rating`. The pipeline **correctly dropped `Comment` from input features**, successfully preventing direct label leakage.
- **Baseline Comparison Audit**:
  Because patient survey ratings in `HC_Patient_Feedback.csv` are uniformly distributed noise independent of doctor experience or department workloads (correlations r < 0.02), all trained models achieved accuracies of 35.5% - 38.4%, which is slightly below the naive majority class baseline (40.9% for Low satisfaction). This is an honest empirical outcome reflecting uncorrupted feature evaluation.

---

### 2.5 Model 5: Revenue / Billing Amount Regression (MEDIUM FINDING)
- **Code Inspected**: `src/healthconnect/features/engineer.py` and `src/healthconnect/models/regressor.py`.
- **Target**: `Amount` (Billing amount in RWF).
- **Leakage Prevention Verification**:
  1. `AmountPaid` (from `HC_Payments.csv`) was strictly excluded because settlement occurs after billing generation.
  2. `ClaimAmount` and `Status` (from `Insurance_Claims.csv`) were strictly excluded.
- **Audit Diagnosis on Negative R²**:
  Empirical evaluation yielded a negative coefficient of determination across all regression models:
  - Dummy Mean Baseline: R² = -0.0023 | MAE = 70,207 RWF
  - Linear Ridge: R² = -0.0368 | MAE = 71,360 RWF
  - Random Forest Regressor: R² = -0.0297 | MAE = 70,960 RWF
  - Gradient Boosting: R² = -0.0710 | MAE = 71,690 RWF
  Diagnosis: In `HC_Billing.csv`, `Amount` is uniformly distributed between 10,000 and 300,000 RWF (mean: 155,157 RWF). The mean billing amounts across diagnoses are virtually flat: Diabetes (156,980), Gastritis (152,085), Hypertension (152,761), Malaria (156,579), Upper Respiratory Infection (153,047). When machine learning models attempt to fit non-existent patterns in uniform noise, test-set MSE slightly exceeds the global mean, yielding negative R². This is a critical finding that validates scientific honesty: the models were not artificially manipulated to show inflated R² scores.

---

### 2.6 Model 6: Length of Stay (LOS) Inpatient Duration (PASS)
- **Audit Finding**:
  Exhaustive auditing across all 27 raw CSV files verified that no admission timestamps, discharge timestamps, bed occupancy durations, or transfer logs exist.
- **Verification Status**:
  The project **correctly and honestly designated Model 6 as UNSUPPORTED**, satisfying the strict assignment rule: *"Do not train a model if the target cannot be constructed correctly. Do not invent data, metrics, or columns."*

---

## 3. Patient-Level Split Overlap Analysis

- **Investigation**: In `billing_analytical.csv`, 5,000 appointment encounters correspond to 4,443 unique patients.
  - 3,933 patients have exactly 1 appointment.
  - 466 patients have 2 appointments.
  - 41 patients have 3 appointments.
  - 3 patients have 4 appointments.
- **Leakage Assessment**:
  When performing an 80/20 train/test split at the encounter level, approximately 100 patients with multiple visits appear in both training and test partitions. Although direct identifiers (`PatientID`) are removed, identical patient demographic features (`Age`, `Gender`, `BMI`, `ChronicCondition`) are shared across splits for these repeat patients.
- **Remediation**:
  Document this finding as a **MEDIUM RISK**. For production healthcare pipelines with repeat patient encounters, `GroupShuffleSplit` or `GroupKFold` grouped on `PatientID` must be applied to ensure patient-level partition isolation.

---

## 4. Preprocessing Fit Boundary Verification

- **Code Inspected**: `src/healthconnect/models/classifier.py` and `src/healthconnect/models/regressor.py`.
- **Pipeline Implementation**:
  ```python
  X_train, X_test, y_train, y_test = train_test_split(...)
  preprocessor = ColumnTransformer(
      transformers=[
          ("num", StandardScaler(), numeric_features),
          ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
      ]
  )
  pipe = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", clf)])
  pipe.fit(X_train, y_train)
  ```
- **Audit Verdict**: **PASS**.
  Feature transformations (`StandardScaler` and `OneHotEncoder`) are fitted strictly on `X_train`. The test set `X_test` is transformed exclusively using parameters learned from training data, completely preventing data leakage across fold boundaries.
