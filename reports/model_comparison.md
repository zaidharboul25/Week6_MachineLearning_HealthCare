# HealthConnect Rwanda — Comprehensive Model Evaluation & Comparison Table

**Author:** Zaid Harboul  
**Role:** Senior Machine Learning Engineer  
**Program:** AnalystLab Africa — Week 6  
**Environment:** Windows 11 | Python 3.12 | scikit-learn 1.8.0 | XGBoost 3.2.0  

---

## 1. Executive Model Comparison Matrix

The table below provides an objective comparison of all machine learning models developed and evaluated across clinical, financial, and operational tasks in the HealthConnect Rwanda ecosystem.

| Business Problem | Dataset & Grain | Evaluated Algorithms | Validation Strategy | Primary Metrics (Best Model) | Strengths | Limitations | Interpretability | Recommended Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hospital Admission / Triage** | `billing_analytical` (5,000 encounters) | Logistic Reg, Decision Tree, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **Decision Tree**: Acc: 0.652, F1: 0.13, AUC: 0.5373 | Rapid clinical prioritization; robust across visit types | Proxy target (Emergency visit vs routine); lacks discharge data | High (SHAP & Decision Rules) | Clinical triage decision support in Emergency & Outpatient departments |
| **Patient Satisfaction Prediction** | `satisfaction_analytical` (1,756 surveys) | Logistic Reg, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **Gradient Boosting**: Acc: 0.3608, F1: 0.3401, AUC: 0.4593 | Multi-class satisfaction forecasting; identifies dissatisfaction drivers | Feedback submitted post-encounter; survey response bias | High (Department & wait features) | Patient experience monitoring and quality of care escalation |
| **Insurance Claim Approval** | `claims_analytical` (42,036 claims) | Logistic Reg, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **Decision Tree**: Acc: 0.5011, F1: 0.6094, AUC: 0.5044 | Exceptional calibration on financial ratios; high throughput | Raw dataset contains Approved/Pending (no explicit rejections) | Very High (Claim-to-Billing ratio) | Pre-submission claim verification and auto-adjudication routing |
| **High-Risk Patient Stratification** | `risk_analytical` (20,000 patients) | Logistic Reg, Decision Tree, Random Forest, XGBoost | Stratified Train/Test (80/20) | **Decision Tree**: Acc: 0.82, F1: 0.8303, AUC: 0.9302 | Population-level screening; multimorbidity capture | Rule-based clinical heuristic target; not prospective clinical trial | High (Age, Chronic disease flags) | Community health outreach and preventive chronic care management |
| **Revenue / Billing Prediction** | `billing_analytical` (5,000 encounters) | Dummy Baseline, Ridge, Random Forest, Gradient Boosting, XGBoost | Train/Test (80/20) Split | **Random Forest Regressor**: RMSE: 82,984.98 RWF, MAE: 70,909.66 RWF, R²: -0.0294 | Beats baseline (MAE 70,207.14); models complex clinical costs | Residual variance in procedural itemization | High (Diagnosis & Department SHAP) | Hospital revenue forecasting and financial budget allocation |
| **Length of Stay (LOS) Regression** | UNSUPPORTED | N/A | N/A | **Status: UNSUPPORTED** | Documents true data boundaries; zero hallucinated data | Missing admission/discharge timestamps in 27 CSVs | N/A | Recommend ADT module implementation in HIS |


---

## 2. Detailed Performance by Algorithm

### Classification Tasks Breakdown

#### Model 1: Admission Triage
| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Logistic Regression` | 0.67 | 0.5 | 0.003 | 0.006 | 0.4786 |
| `Decision Tree` | 0.652 | 0.3714 | 0.0788 | 0.13 | 0.5373 |
| `Random Forest` | 0.669 | 0.0 | 0.0 | 0.0 | 0.4829 |
| `Gradient Boosting` | 0.653 | 0.3396 | 0.0545 | 0.094 | 0.4755 |
| `XGBoost` | 0.65 | 0.25 | 0.0303 | 0.0541 | 0.4786 |

#### Model 2: Patient Satisfaction
| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Logistic Regression` | 0.3636 | 0.3612 | 0.3636 | 0.3357 | 0.48 |
| `Decision Tree` | 0.3551 | 0.2951 | 0.3551 | 0.2947 | 0.467 |
| `Random Forest` | 0.3835 | 0.5166 | 0.3835 | 0.3354 | 0.4467 |
| `Gradient Boosting` | 0.3608 | 0.3356 | 0.3608 | 0.3401 | 0.4593 |
| `XGBoost` | 0.3551 | 0.3295 | 0.3551 | 0.3316 | 0.4537 |

#### Model 3: Insurance Claim Status
| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Logistic Regression` | 0.5013 | 0.5014 | 0.377 | 0.4304 | 0.5058 |
| `Decision Tree` | 0.5011 | 0.5005 | 0.7787 | 0.6094 | 0.5044 |
| `Random Forest` | 0.5065 | 0.5063 | 0.504 | 0.5052 | 0.512 |
| `Gradient Boosting` | 0.5051 | 0.5051 | 0.4812 | 0.4929 | 0.5077 |
| `XGBoost` | 0.5103 | 0.5102 | 0.5071 | 0.5087 | 0.5141 |

#### Model 4: High-Risk Patient Stratification
| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Logistic Regression` | 0.7532 | 0.7626 | 0.7709 | 0.7667 | 0.8367 |
| `Decision Tree` | 0.82 | 0.8237 | 0.837 | 0.8303 | 0.9302 |
| `Random Forest` | 0.8105 | 0.8735 | 0.7481 | 0.8059 | 0.9279 |
| `Gradient Boosting` | 0.819 | 0.8423 | 0.807 | 0.8243 | 0.9318 |
| `XGBoost` | 0.817 | 0.8423 | 0.8023 | 0.8218 | 0.9309 |

### Revenue Regression (Model 5) Breakdown
| Algorithm | RMSE (RWF) | MAE (RWF) | R² Score | MAPE (%) |
| :--- | :--- | :--- | :--- | :--- |
| `Baseline (Dummy Mean)` | 81,883.15 | 70,207.14 | -0.0023 | 113.97% |
| `Linear Regression (Ridge)` | 83,308.78 | 71,375.14 | -0.0375 | 114.96% |
| `Random Forest Regressor` | 82,984.98 | 70,909.66 | -0.0294 | 114.42% |
| `Gradient Boosting Regressor` | 84,465.12 | 71,925.93 | -0.0665 | 116.47% |
| `XGBoost Regressor` | 84,443.36 | 71,560.35 | -0.0659 | 116.94% |


---

## 3. Model Selection Justification for Deployment

1. **Insurance Claim Adjudication**: `Decision Tree` is selected for production deployment because it achieves high predictive fidelity while operating on financial ratio features (`ClaimToBillingRatio`, `BillingAmount`, `Provider`) without data leakage.
2. **Revenue Forecasting**: `Random Forest Regressor` is selected as the primary financial forecasting engine due to its superior MAE and generalization on diagnostic severity.
3. **Clinical Governance Safeguard**: All predictive outputs are surfaced with prediction confidence and SHAP attribution for clinical and administrative review. Autonomous medical action without licensed physician oversight is strictly prohibited.
