"""
Model Evaluation and Metrics Reporting Script.
Loads experiment metrics and prints detailed performance tables for all models.
"""

import sys
import json
from pathlib import Path
import pandas as pd

# Add src to pythonpath
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from healthconnect.config import METRICS_DIR, REPORTS_DIR

def main():
    metrics_path = METRICS_DIR / "experiment_metrics.json"
    if not metrics_path.exists():
        print(f"Error: Metrics file not found at {metrics_path}. Run scripts/train_models.py first.")
        sys.exit(1)

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    print("================================================================================")
    print("       HEALTHCONNECT RWANDA — COMPREHENSIVE MODEL EVALUATION REPORT             ")
    print("================================================================================")
    print("\n[1] CLASSIFICATION MODELS EVALUATION SUMMARY:")
    for task_name, task_data in metrics["classification"].items():
        print(f"\nTask: {task_name} (Top Model: {task_data['best_algorithm']})")
        df_task = pd.DataFrame(task_data["algorithms"]).T
        print(df_task[["accuracy", "precision", "recall", "f1", "roc_auc"]].to_string())

    print("\n--------------------------------------------------------------------------------")
    print("[2] REVENUE REGRESSION (MODEL 5) EVALUATION SUMMARY:")
    df_reg = pd.DataFrame(metrics["regression"]).T
    print(df_reg[["rmse", "mae", "r2", "mape"]].to_string())

    print("\n--------------------------------------------------------------------------------")
    print("[3] UNSUPPORTED TASK DOCUMENTATION (MODEL 6 - LENGTH OF STAY):")
    print(f"Status: {metrics['los_assessment']['status']}")
    print(f"Reason: {metrics['los_assessment']['reason']}")

    print("\n--------------------------------------------------------------------------------")
    print("[4] CLUSTERING EVALUATION:")
    print(f"Patient Segmentation Silhouette Score (k=3): {metrics['clustering']['patient_segmentation']['silhouette']}")
    print(f"Facility Segmentation Silhouette Score (k=3): {metrics['clustering']['facility_segmentation']['silhouette']}")

    print("\n--------------------------------------------------------------------------------")
    print("[5] ANOMALY DETECTION SUMMARY:")
    ad = metrics["anomaly_detection"]
    print(f"Billing Outliers Flagged: {ad['billing_anomalies_count']} ({ad['billing_anomalies_pct']}%)")
    print(f"Discrepant Insurance Claims Flagged: {ad['claim_anomalies_count']} ({ad['claim_anomalies_pct']}%)")
    print(f"Duplicate Patient Demographic Records: {ad['duplicate_patients_count']}")

    print("\n--------------------------------------------------------------------------------")
    print("[6] EXPLAINABLE AI (SHAP TOP INFLUENTIAL DRIVERS):")
    print("Claims Classifier Top Drivers:")
    for feat in metrics["xai"]["claims"].get("top_features", [])[:5]:
        print(f"  - {feat.get('feature')}: {feat.get('mean_abs_shap', feat.get('importance'))}")
    print("Billing Regressor Top Drivers:")
    for feat in metrics["xai"]["billing"].get("top_features", [])[:5]:
        print(f"  - {feat.get('feature')}: {feat.get('mean_abs_shap', feat.get('importance'))}")
    print("================================================================================")

if __name__ == "__main__":
    main()
