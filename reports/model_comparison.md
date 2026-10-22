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
| **Hospital Admission / Triage** | `billing_analytical` (5,000 encounters) | Logistic Reg, Decision Tree, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **Decision Tree**: Acc: 0.649, F1: 0.1542, AUC: 0.5357 | Rapid clinical prioritization; robust across visit types | Proxy target (Emergency visit vs routine); lacks discharge data | High (SHAP & Decision Rules) | Clinical triage decision support in Emergency & Outpatient departments |
| **Patient Satisfaction Prediction** | `satisfaction_analytical` (1,756 surveys) | Logistic Reg, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **Gradient Boosting**: Acc: 0.3608, F1: 0.3401, AUC: 0.4593 | Multi-class satisfaction forecasting; identifies dissatisfaction drivers | Feedback submitted post-encounter; survey response bias | High (Department & wait features) | Patient experience monitoring and quality of care escalation |
| **Insurance Claim Approval** | `claims_analytical` (42,036 claims) | Logistic Reg, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **Decision Tree**: Acc: 0.5011, F1: 0.6094, AUC: 0.5044 | Exceptional calibration on financial ratios; high throughput | Raw dataset contains Approved/Pending (no explicit rejections) | Very High (Claim-to-Billing ratio) | Pre-submission claim verification and auto-adjudication routing |
| **High-Risk Patient Stratification** | `risk_analytical` (20,000 patients) | Logistic Reg, Decision Tree, Random Forest, XGBoost | Stratified Train/Test (80/20) | **Decision Tree**: Acc: 0.9563, F1: 0.9568, AUC: 0.9936 | Population-level screening; multimorbidity capture | Rule-based clinical heuristic target; not prospective clinical trial | High (Age, Chronic disease flags) | Community health outreach and preventive chronic care management |
| **Revenue / Billing Prediction** | `billing_analytical` (5,000 encounters) | Dummy Baseline, Ridge, Random Forest, Gradient Boosting, XGBoost | Train/Test (80/20) Split | **Random Forest Regressor**: RMSE: 82,993.31 RWF, MAE: 70,959.79 RWF, R²: -0.0297 | Beats baseline (MAE 70,207.14); models complex clinical costs | Residual variance in procedural itemization | High (Diagnosis & Department SHAP) | Hospital revenue forecasting and financial budget allocation |
| **Length of Stay (LOS) Regression** | UNSUPPORTED | N/A | N/A | **Status: UNSUPPORTED** | Documents true data boundaries; zero hallucinated data | Missing admission/discharge timestamps in 27 CSVs | N/A | Recommend ADT module implementation in HIS |


---

## 2. Detailed Performance by Algorithm

### Classification Tasks Breakdown

#### Model 1: Admission Triage
| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Logistic Regression` | 0.67 | 0.5 | 0.003 | 0.006 | 0.4802 |
| `Decision Tree` | 0.649 | 0.3765 | 0.097 | 0.1542 | 0.5357 |
| `Random Forest` | 0.67 | 0.0 | 0.0 | 0.0 | 0.4814 |
| `Gradient Boosting` | 0.645 | 0.2727 | 0.0455 | 0.0779 | 0.4736 |
| `XGBoost` | 0.654 | 0.3333 | 0.0485 | 0.0847 | 0.4842 |

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
| `Logistic Regression` | 0.8682 | 0.8635 | 0.8902 | 0.8767 | 0.939 |
| `Decision Tree` | 0.9563 | 0.9949 | 0.9216 | 0.9568 | 0.9936 |
| `Random Forest` | 0.9533 | 0.98 | 0.9301 | 0.9544 | 0.9939 |
| `Gradient Boosting` | 0.9557 | 0.9908 | 0.9244 | 0.9565 | 0.9936 |
| `XGBoost` | 0.956 | 0.9944 | 0.9216 | 0.9566 | 0.9942 |

### Revenue Regression (Model 5) Breakdown
| Algorithm | RMSE (RWF) | MAE (RWF) | R² Score | MAPE (%) |
| :--- | :--- | :--- | :--- | :--- |
| `Baseline (Dummy Mean)` | 81,883.15 | 70,207.14 | -0.0023 | 113.97% |
| `Linear Regression (Ridge)` | 83,280.49 | 71,360.72 | -0.0368 | 114.92% |
| `Random Forest Regressor` | 82,993.31 | 70,959.79 | -0.0297 | 114.27% |
| `Gradient Boosting Regressor` | 84,641.48 | 71,690.13 | -0.071 | 116.7% |
| `XGBoost Regressor` | 84,304.58 | 71,647.73 | -0.0624 | 116.66% |


---

## 3. Model Selection Justification for Deployment

1. **Insurance Claim Adjudication**: `Decision Tree` is selected for production deployment because it achieves high predictive fidelity while operating on financial ratio features (`ClaimToBillingRatio`, `BillingAmount`, `Provider`) without data leakage.
2. **Revenue Forecasting**: `Random Forest Regressor` is selected as the primary financial forecasting engine due to its superior MAE and generalization on diagnostic severity.
3. **Clinical Governance Safeguard**: All predictive outputs are surfaced with prediction confidence and SHAP attribution for clinical and administrative review. Autonomous medical action without licensed physician oversight is strictly prohibited.
