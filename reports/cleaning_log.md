# HealthConnect Rwanda — Data Cleaning & Transformation Log

**Author:** Zaid Harboul  
**Role:** Senior Machine Learning Engineer  
**Program:** AnalystLab Africa — Week 6  

---

## 1. Summary of Cleaning Operations

| Dataset | Pre-Clean Rows | Post-Clean Rows | Action Taken | Clinical & Engineering Justification |
| :--- | :--- | :--- | :--- | :--- |
| `HC_Patients.csv` | 20,000 | 20,000 | Imputed `ChronicCondition` NaN with `'None'`. Validated and recalculated BMI where necessary. Clipped bounds (Age 0-120, BMI 10-60). | Avoided record deletion. Missing chronic condition indicates absence of chronic diagnosis in primary care records. |
| `HC_Clinical_Transactions.xlsx - Appointments.csv` | 5,000 | 5,000 | Converted `Date` to datetime. Extracted temporal components (`Month`, `DayOfWeek`, `Quarter`, `IsWeekend`). | Validated complete integrity. Preserves exact date metadata for chronological/stratified validation. |
| `HC_Billing.csv` | 60,000 | 60,000 | Cast `Amount` to numeric float, clipped negative values to 0. Validated payment status. | Enforces valid positive monetary transactions. |
| `Insurance_Claims.csv` | 42,036 | 42,036 | Joined to `BillingAmount`. Engineered `ClaimToBillingRatio` and `ClaimDiff`. Encoded binary target. | Target has two observed classes: `Approved` (50%) and `Pending` (50%). |
| `HC_Patient_Feedback.csv` | 21,064 | 21,064 | Mapped `Rating` (1-5) into 3 balanced categories: Low (1-2), Medium (3), High (4-5). Excluded `Comment` to prevent label leakage. | Direct alignment with Week 6 rubric for patient satisfaction prediction. |
| `HC_Diagnoses.csv` | 60,000 | 60,000 | Normalized text fields. Verified severity mapping (`Mild`, `Moderate`, `Severe`). | Diagnostic clinical severity is a key feature for billing and risk prediction. |

---

## 2. Leakage Prevention Safeguards
1. **Target Separation**: `AmountPaid` (from `HC_Payments.csv`) was strictly excluded from billing amount regression, as payments are settled post-billing.
2. **Survey Feedback Separation**: Text comments submitted alongside patient satisfaction surveys were excluded from feature inputs.
3. **Claim Settlement Isolation**: Only pre-decision claim amount and billing parameters were provided to the insurance claim classifier.
