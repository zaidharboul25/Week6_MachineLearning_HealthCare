# HealthConnect Rwanda — Explainable AI (XAI) & Model Interpretability Report

**Author:** Zaid Harboul  
**Role:** Senior Machine Learning Engineer  
**Program:** AnalystLab Africa — Week 6  

---

## 1. The Imperative for Model Transparency in Healthcare

In clinical medicine and healthcare administration, "black-box" machine learning predictions pose significant patient safety, financial, and ethical risks. Healthcare providers, hospital administrators, and insurance adjudicators cannot responsibly act on automated predictions without understanding the underlying factors driving the model's output.

Explainable AI (XAI) bridges the gap between predictive performance and clinical accountability by providing:
1. **Global Interpretability**: Understanding which features generally dominate model decision-making across the entire patient population.
2. **Local Interpretability**: Deconstructing individual predictions to show exactly how specific clinical features increased or decreased a patient's risk score or claim approval probability.
3. **Auditing for Bias & Leakage**: Detecting whether spurious correlations or target-leaking proxies are improperly driving model decisions.

---

## 2. Methodology: SHAP (SHapley Additive exPlanations)

We implemented SHAP based on cooperative game theory (Shapley values). SHAP fairly allocates the credit or blame for a prediction among all input features, satisfying mathematical properties of local accuracy, missingness, and consistency.

Where tree ensembles (Random Forest, Gradient Boosting, XGBoost) were utilized, `shap.TreeExplainer` was applied to compute exact Shapley values across test cohorts.

---

## 3. Global Explainability Findings

### 3.1 Insurance Claim Status Classification
The top 5 most influential features identified by SHAP for claim adjudication were:
- **`Provider_RSSB`**: Mean absolute SHAP value = `0.0055`
- **`ClaimDiff`**: Mean absolute SHAP value = `0.0038`
- **`BillingAmount`**: Mean absolute SHAP value = `0.0036`
- **`ClaimToBillingRatio`**: Mean absolute SHAP value = `0.0033`
- **`ClaimAmount`**: Mean absolute SHAP value = `0.0008`
- **`Provider_Radiant`**: Mean absolute SHAP value = `0.0`
- **`IsFullClaim`**: Mean absolute SHAP value = `0.0`
- **`Provider_Private`**: Mean absolute SHAP value = `0.0`
- **`Provider_MMI`**: Mean absolute SHAP value = `0.0`

**Interpretation**:
- `Provider`: The underwriting rules and contractual billing schedules of specific insurance providers (e.g. RSSB vs Private insurers) heavily influence claim adjudication outcomes.
- `ClaimToBillingRatio` & `ClaimDiff`: The ratio between the requested reimbursement amount and the hospital invoiced charges is a primary determinant of whether a claim is immediately approved or flagged for further verification.

### 3.2 Hospital Billing & Revenue Regression
The top 5 most influential features identified for encounter billing amount prediction were:
- **`Age`**: Mean absolute SHAP value = `2547.6213`
- **`Month`**: Mean absolute SHAP value = `2435.7327`
- **`DoctorExperience`**: Mean absolute SHAP value = `2288.3256`
- **`DepartmentWorkload`**: Mean absolute SHAP value = `1994.4079`
- **`BMI`**: Mean absolute SHAP value = `1927.3353`
- **`MaritalStatus_Single`**: Mean absolute SHAP value = `1818.586`
- **`FacilityApptVolume`**: Mean absolute SHAP value = `1150.9639`
- **`MaritalStatus_Widowed`**: Mean absolute SHAP value = `1103.7261`
- **`PatientToDoctorRatio`**: Mean absolute SHAP value = `926.2762`
- **`Severity_Mild`**: Mean absolute SHAP value = `880.2877`

**Interpretation**:
- `Age` & `BMI`: Patient demographic and physiological vulnerability correlate with the complexity of diagnostic workups and medication regimens.
- `DoctorExperience`: Senior physicians frequently handle higher-acuity, specialized cases involving advanced interventions.
- `DepartmentWorkload`: Clinical departments handling higher encounter densities reflect higher resource utilization.

---

## 4. Visual Artifacts
- **Insurance Claims SHAP Summary**: [shap_claims_classifier.png](file:///reports/figures/shap_claims_classifier.png)
- **Billing Regression SHAP Summary**: [shap_billing_regression.png](file:///reports/figures/shap_billing_regression.png)

---

## 5. Critical Clinical & Statistical Limitations of Explanations

1. **Correlation Does Not Establish Causation**: High SHAP attribution indicates statistical association within historical observational data. It does NOT imply that modifying a feature (e.g., altering billing ratios) will biologically or clinically alter the outcome.
2. **Data Bias & Historical Disparities**: If historical claims adjudication exhibited regional or socioeconomic disparities, the model will inherit and reflect these biases in its explanations.
3. **Feature Correlation / Multicollinearity**: When clinical features are correlated (e.g., `Age` and `ChronicCondition`), Shapley values can distribute importance across correlated features, occasionally reducing the apparent impact of individual variables.
4. **Clinical Governance Safeguard**: XAI outputs must always be interpreted alongside clinical notes, lab investigations, and physician judgment.
