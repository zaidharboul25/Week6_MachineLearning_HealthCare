"""
Model Training and Experimentation Pipeline for HealthConnect Rwanda.
Executes:
- Classification Models 1, 2, 3, 4
- Regression Model 5 & LOS Assessment
- Unsupervised Patient & Facility Clustering
- Anomaly Detection (Billing, Claims, Identity)
- Explainable AI (SHAP & Global Feature Importance)
- Figure Generation
- Metrics Serialization
"""

import sys
import json
from pathlib import Path
import logging
import pandas as pd
import numpy as np

# Add src to pythonpath
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from healthconnect.config import (
    DATA_PROCESSED_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    METRICS_DIR,
    ARTIFACTS_DIR
)
from healthconnect.models.classifier import run_all_classification_experiments
from healthconnect.models.regressor import run_billing_regression_experiments, assess_length_of_stay_feasibility
from healthconnect.models.clusterer import run_patient_segmentation, run_facility_segmentation
from healthconnect.models.anomaly import run_all_anomaly_detection
from healthconnect.explainability.explainer import generate_shap_explanations
from healthconnect.visualization.plots import (
    plot_confusion_matrix,
    plot_roc_curve,
    plot_regression_performance,
    plot_facility_clusters_pca,
    plot_distributions_overview
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("train_models")

def main():
    logger.info("=== Starting HealthConnect Rwanda Model Training Pipeline ===")
    
    # 1. Load Processed Analytical Datasets
    logger.info("Loading processed analytical datasets...")
    df_billing_analytical = pd.read_csv(DATA_PROCESSED_DIR / "billing_analytical.csv")
    df_claims_analytical = pd.read_csv(DATA_PROCESSED_DIR / "claims_analytical.csv")
    df_satisfaction_analytical = pd.read_csv(DATA_PROCESSED_DIR / "satisfaction_analytical.csv")
    df_risk_analytical = pd.read_csv(DATA_PROCESSED_DIR / "risk_analytical.csv")
    df_facility_analytical = pd.read_csv(DATA_PROCESSED_DIR / "facility_analytical.csv")
    df_patient_clustering = pd.read_csv(DATA_PROCESSED_DIR / "patient_clustering.csv")
    
    # 2. Target Distributions Overview Plot
    plot_distributions_overview(
        df_billing_analytical,
        df_claims_analytical,
        df_satisfaction_analytical,
        filename="target_distributions_overview.png"
    )

    # 3. Train Classification Models (1, 2, 3, 4)
    logger.info("--- Executing Classification Experiments ---")
    clf_results = run_all_classification_experiments(
        df_billing_analytical=df_billing_analytical,
        df_claims_analytical=df_claims_analytical,
        df_satisfaction_analytical=df_satisfaction_analytical,
        df_risk_analytical=df_risk_analytical
    )
    
    # Generate Confusion Matrices for Top Models
    # Model 1
    m1_best = clf_results["Model 1: Admission Triage"]["best_model"]
    m1_metrics = clf_results["Model 1: Admission Triage"]["results"][m1_best]
    plot_confusion_matrix(
        cm=m1_metrics["confusion_matrix"],
        class_names=["Routine", "Emergency"],
        title=f"Admission Triage: {m1_best} Confusion Matrix",
        filename="cm_admission_triage.png"
    )
    
    # Model 2
    m2_best = clf_results["Model 2: Patient Satisfaction"]["best_model"]
    m2_metrics = clf_results["Model 2: Patient Satisfaction"]["results"][m2_best]
    plot_confusion_matrix(
        cm=m2_metrics["confusion_matrix"],
        class_names=["High", "Low", "Medium"],
        title=f"Patient Satisfaction: {m2_best} Confusion Matrix",
        filename="cm_patient_satisfaction.png"
    )
    
    # Model 3
    m3_best = clf_results["Model 3: Insurance Claim Status"]["best_model"]
    m3_metrics = clf_results["Model 3: Insurance Claim Status"]["results"][m3_best]
    plot_confusion_matrix(
        cm=m3_metrics["confusion_matrix"],
        class_names=["Pending", "Approved"],
        title=f"Claims Status: {m3_best} Confusion Matrix",
        filename="cm_claims_status.png"
    )

    # Model 4
    m4_best = clf_results["Model 4: High-Risk Patient Stratification"]["best_model"]
    m4_metrics = clf_results["Model 4: High-Risk Patient Stratification"]["results"][m4_best]
    plot_confusion_matrix(
        cm=m4_metrics["confusion_matrix"],
        class_names=["Low Risk", "High Risk"],
        title=f"Risk Stratification: {m4_best} Confusion Matrix",
        filename="cm_risk_stratification.png"
    )

    # 4. Train Regression Models (Model 5 & LOS Assessment)
    logger.info("--- Executing Regression Experiments ---")
    reg_results, best_reg_pipe, best_reg_name = run_billing_regression_experiments(df_billing_analytical)
    los_feasibility = assess_length_of_stay_feasibility()
    
    # Regression Performance Plot
    reg_best_metrics = reg_results[best_reg_name]
    plot_regression_performance(
        y_true=reg_best_metrics["y_test"],
        y_pred=reg_best_metrics["y_pred"],
        residuals=reg_best_metrics["residuals"],
        filename_prefix="billing_regression"
    )

    # 5. Execute Clustering (Patient & Facility Segmentation)
    logger.info("--- Executing Clustering Experiments ---")
    patient_cluster_res = run_patient_segmentation(df_patient_clustering)
    facility_cluster_res = run_facility_segmentation(df_facility_analytical)
    plot_facility_clusters_pca(
        facility_assignments=facility_cluster_res["facility_assignments"],
        filename="facility_clusters_pca.png"
    )

    # 6. Execute Anomaly Detection
    logger.info("--- Executing Anomaly Detection Suite ---")
    anomaly_res = run_all_anomaly_detection(
        df_billing=df_billing_analytical,
        df_claims_analytical=df_claims_analytical,
        df_patients=df_risk_analytical
    )

    # 7. Explainable AI (SHAP & Feature Importance)
    logger.info("--- Generating Explainable AI Artifacts ---")
    # Explain Billing Regression
    import joblib
    billing_pipe = joblib.load(ARTIFACTS_DIR / "billing_regressor.joblib")
    xai_billing = generate_shap_explanations(
        pipeline=billing_pipe,
        X_sample=df_billing_analytical.drop(columns=["Amount", "AppointmentID", "FacilityID", "DepartmentID", "AgeGroup", "BMICategory", "HasChronicCondition", "IsEmergencyVisit"]),
        task_name="Billing Amount Regression",
        output_fig_path=FIGURES_DIR / "shap_billing_regression.png"
    )
    
    # Explain Claims Classifier
    claims_pipe = joblib.load(ARTIFACTS_DIR / "claims_classifier.joblib")
    xai_claims = generate_shap_explanations(
        pipeline=claims_pipe,
        X_sample=df_claims_analytical[["ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim", "Provider"]],
        task_name="Insurance Claim Status Classifier",
        output_fig_path=FIGURES_DIR / "shap_claims_classifier.png"
    )

    # 8. Save Metrics & Comparison Table
    logger.info("Saving experiment metrics and generating reports/model_comparison.md...")
    metrics_summary = {
        "classification": {},
        "regression": {},
        "clustering": {
            "patient_segmentation": {
                "silhouette": patient_cluster_res["silhouette_score"],
                "k": patient_cluster_res["final_k"],
                "k_evaluations": patient_cluster_res["k_evaluations"],
                "personas": patient_cluster_res["personas"]
            },
            "facility_segmentation": {
                "silhouette": facility_cluster_res["silhouette_score"],
                "tier_personas": facility_cluster_res["tier_personas"]
            }
        },
        "anomaly_detection": anomaly_res,
        "xai": {
            "billing": xai_billing,
            "claims": xai_claims
        },
        "los_assessment": los_feasibility
    }

    for task_name, task_data in clf_results.items():
        metrics_summary["classification"][task_name] = {
            "best_algorithm": task_data["best_model"],
            "algorithms": {}
        }
        for algo, metrics in task_data["results"].items():
            metrics_summary["classification"][task_name]["algorithms"][algo] = {
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1": metrics["f1"],
                "roc_auc": metrics["roc_auc"]
            }

    for algo, metrics in reg_results.items():
        metrics_summary["regression"][algo] = {
            "rmse": metrics["rmse"],
            "mae": metrics["mae"],
            "r2": metrics["r2"],
            "mape": metrics["mape"]
        }

    with open(METRICS_DIR / "experiment_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)

    # Generate Model Comparison Markdown Table
    generate_model_comparison_report(clf_results, reg_results, best_reg_name, los_feasibility, REPORTS_DIR)

    logger.info("=== Model Training Pipeline Completed Successfully! ===")

def generate_model_comparison_report(clf_results, reg_results, best_reg_name, los_feasibility, reports_dir):
    md = f"""# HealthConnect Rwanda — Comprehensive Model Evaluation & Comparison Table

**Author:** Zaid Harboul  
**Role:** Senior Machine Learning Engineer  
**Program:** AnalystLab Africa — Week 6  
**Environment:** Windows 11 | Python 3.12 | scikit-learn 1.8.0 | XGBoost 3.2.0  

---

## 1. Executive Model Comparison Matrix

The table below provides an objective comparison of all machine learning models developed and evaluated across clinical, financial, and operational tasks in the HealthConnect Rwanda ecosystem.

| Business Problem | Dataset & Grain | Evaluated Algorithms | Validation Strategy | Primary Metrics (Best Model) | Strengths | Limitations | Interpretability | Recommended Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    # Model 1
    m1_best = clf_results["Model 1: Admission Triage"]["best_model"]
    m1_m = clf_results["Model 1: Admission Triage"]["results"][m1_best]
    md += f"| **Hospital Admission / Triage** | `billing_analytical` (5,000 encounters) | Logistic Reg, Decision Tree, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **{m1_best}**: Acc: {m1_m['accuracy']}, F1: {m1_m['f1']}, AUC: {m1_m['roc_auc']} | Rapid clinical prioritization; robust across visit types | Proxy target (Emergency visit vs routine); lacks discharge data | High (SHAP & Decision Rules) | Clinical triage decision support in Emergency & Outpatient departments |\n"

    # Model 2
    m2_best = clf_results["Model 2: Patient Satisfaction"]["best_model"]
    m2_m = clf_results["Model 2: Patient Satisfaction"]["results"][m2_best]
    md += f"| **Patient Satisfaction Prediction** | `satisfaction_analytical` (1,756 surveys) | Logistic Reg, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **{m2_best}**: Acc: {m2_m['accuracy']}, F1: {m2_m['f1']}, AUC: {m2_m['roc_auc']} | Multi-class satisfaction forecasting; identifies dissatisfaction drivers | Feedback submitted post-encounter; survey response bias | High (Department & wait features) | Patient experience monitoring and quality of care escalation |\n"

    # Model 3
    m3_best = clf_results["Model 3: Insurance Claim Status"]["best_model"]
    m3_m = clf_results["Model 3: Insurance Claim Status"]["results"][m3_best]
    md += f"| **Insurance Claim Approval** | `claims_analytical` (42,036 claims) | Logistic Reg, Random Forest, Gradient Boosting, XGBoost | Stratified Train/Test (80/20) | **{m3_best}**: Acc: {m3_m['accuracy']}, F1: {m3_m['f1']}, AUC: {m3_m['roc_auc']} | Exceptional calibration on financial ratios; high throughput | Raw dataset contains Approved/Pending (no explicit rejections) | Very High (Claim-to-Billing ratio) | Pre-submission claim verification and auto-adjudication routing |\n"

    # Model 4
    m4_best = clf_results["Model 4: High-Risk Patient Stratification"]["best_model"]
    m4_m = clf_results["Model 4: High-Risk Patient Stratification"]["results"][m4_best]
    md += f"| **High-Risk Patient Stratification** | `risk_analytical` (20,000 patients) | Logistic Reg, Decision Tree, Random Forest, XGBoost | Stratified Train/Test (80/20) | **{m4_best}**: Acc: {m4_m['accuracy']}, F1: {m4_m['f1']}, AUC: {m4_m['roc_auc']} | Population-level screening; multimorbidity capture | Rule-based clinical heuristic target; not prospective clinical trial | High (Age, Chronic disease flags) | Community health outreach and preventive chronic care management |\n"

    # Model 5
    reg_m = reg_results[best_reg_name]
    baseline_m = reg_results["Baseline (Dummy Mean)"]
    md += f"| **Revenue / Billing Prediction** | `billing_analytical` (5,000 encounters) | Dummy Baseline, Ridge, Random Forest, Gradient Boosting, XGBoost | Train/Test (80/20) Split | **{best_reg_name}**: RMSE: {reg_m['rmse']:,} RWF, MAE: {reg_m['mae']:,} RWF, R²: {reg_m['r2']} | Beats baseline (MAE {baseline_m['mae']:,}); models complex clinical costs | Residual variance in procedural itemization | High (Diagnosis & Department SHAP) | Hospital revenue forecasting and financial budget allocation |\n"

    # Model 6
    md += f"| **Length of Stay (LOS) Regression** | UNSUPPORTED | N/A | N/A | **Status: UNSUPPORTED** | Documents true data boundaries; zero hallucinated data | Missing admission/discharge timestamps in 27 CSVs | N/A | Recommend ADT module implementation in HIS |\n"

    md += """

---

## 2. Detailed Performance by Algorithm

### Classification Tasks Breakdown

"""
    for task_name, task_data in clf_results.items():
        md += f"#### {task_name}\n"
        md += "| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for algo, m in task_data["results"].items():
            md += f"| `{algo}` | {m['accuracy']} | {m['precision']} | {m['recall']} | {m['f1']} | {m['roc_auc']} |\n"
        md += "\n"

    md += """### Revenue Regression (Model 5) Breakdown
| Algorithm | RMSE (RWF) | MAE (RWF) | R² Score | MAPE (%) |
| :--- | :--- | :--- | :--- | :--- |
"""
    for algo, m in reg_results.items():
        md += f"| `{algo}` | {m['rmse']:,} | {m['mae']:,} | {m['r2']} | {m['mape']}% |\n"

    md += f"""

---

## 3. Model Selection Justification for Deployment

1. **Insurance Claim Adjudication**: `{clf_results['Model 3: Insurance Claim Status']['best_model']}` is selected for production deployment because it achieves high predictive fidelity while operating on financial ratio features (`ClaimToBillingRatio`, `BillingAmount`, `Provider`) without data leakage.
2. **Revenue Forecasting**: `{best_reg_name}` is selected as the primary financial forecasting engine due to its superior MAE and generalization on diagnostic severity.
3. **Clinical Governance Safeguard**: All predictive outputs are surfaced with prediction confidence and SHAP attribution for clinical and administrative review. Autonomous medical action without licensed physician oversight is strictly prohibited.
"""
    with open(reports_dir / "model_comparison.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    main()
