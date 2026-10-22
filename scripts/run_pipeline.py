"""
HealthConnect Rwanda — Single Entry-Point Pipeline Orchestrator.
Supports running end-to-end pipeline or individual stages:
- audit: Profile raw data and generate data dictionary / relationship reports.
- prepare: Clean raw datasets and engineer predictive features.
- train: Train all classification, regression, clustering, and anomaly models.
- evaluate: Print metrics summaries across all trained models.
- report: Generate technical report, executive summary, presentation, and XAI report.
- validate: Run automated test suite and check all required deliverables.
- all: Execute complete end-to-end pipeline sequentially.

Usage:
    python scripts/run_pipeline.py --stage all
    python scripts/run_pipeline.py --stage audit
"""

import sys
import argparse
from pathlib import Path
import subprocess

# Add src and project root to pythonpath
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root))

from healthconnect.config import (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    REPORTS_DIR,
    METRICS_DIR,
    ARTIFACTS_DIR
)

def run_audit():
    print("\n>>> [STAGE 1/6] EXECUTING DATA AUDIT...")
    from healthconnect.data.audit import audit_all
    audit_all()
    print(">>> Stage 1 (Audit) Completed Successfully.")

def run_prepare():
    print("\n>>> [STAGE 2/6] EXECUTING DATA PREPARATION & FEATURE ENGINEERING...")
    inventory_file = REPORTS_DIR / "data_inventory.csv"
    if not inventory_file.exists():
        print("Warning: Audit has not been executed yet. Running audit first...")
        run_audit()

    from scripts.prepare_data import main as prepare_main
    prepare_main()
    print(">>> Stage 2 (Prepare) Completed Successfully.")

def run_train():
    print("\n>>> [STAGE 3/6] EXECUTING MODEL TRAINING & EVALUATION...")
    processed_bill = DATA_PROCESSED_DIR / "billing_analytical.csv"
    if not processed_bill.exists():
        print("Error: Processed datasets missing in data/processed/. Run `python scripts/run_pipeline.py --stage prepare` first.")
        sys.exit(1)

    from scripts.train_models import main as train_main
    train_main()
    print(">>> Stage 3 (Train) Completed Successfully.")

def run_evaluate():
    print("\n>>> [STAGE 4/6] PRINTING MODEL EVALUATION REPORT...")
    metrics_file = METRICS_DIR / "experiment_metrics.json"
    if not metrics_file.exists():
        print("Error: Metrics file not found in reports/metrics/. Run `python scripts/run_pipeline.py --stage train` first.")
        sys.exit(1)

    from scripts.evaluate_models import main as eval_main
    eval_main()
    print(">>> Stage 4 (Evaluate) Completed Successfully.")

def run_report():
    print("\n>>> [STAGE 5/6] GENERATING COMPREHENSIVE REPORTS & PRESENTATION...")
    metrics_file = METRICS_DIR / "experiment_metrics.json"
    if not metrics_file.exists():
        print("Error: Metrics file not found. Run `python scripts/run_pipeline.py --stage train` first.")
        sys.exit(1)

    from scripts.generate_reports import main as report_main
    report_main()
    print(">>> Stage 5 (Report) Completed Successfully.")

def run_validate():
    print("\n>>> [STAGE 6/6] VALIDATING ALL DELIVERABLES & RUNNING TESTS...")
    from scripts.validate_deliverables import main as val_main
    val_main()
    print(">>> Stage 6 (Validate) Completed Successfully.")

def main():
    parser = argparse.ArgumentParser(description="HealthConnect Rwanda ML Pipeline Orchestrator")
    parser.add_argument(
        "--stage",
        type=str,
        default="all",
        choices=["all", "audit", "prepare", "train", "evaluate", "report", "validate"],
        help="Pipeline stage to execute (default: all)"
    )
    args = parser.parse_args()

    stage = args.stage.lower()
    print(f"================================================================================")
    print(f"       HEALTHCONNECT RWANDA PIPELINE — STAGE: {stage.upper()}                   ")
    print(f"================================================================================")

    if stage == "audit":
        run_audit()
    elif stage == "prepare":
        run_prepare()
    elif stage == "train":
        run_train()
    elif stage == "evaluate":
        run_evaluate()
    elif stage == "report":
        run_report()
    elif stage == "validate":
        run_validate()
    elif stage == "all":
        run_audit()
        run_prepare()
        run_train()
        run_evaluate()
        run_report()
        run_validate()
        print("\n================================================================================")
        print("       >>> FULL END-TO-END PIPELINE EXECUTED SUCCESSFULLY! <<<                 ")
        print("================================================================================")

if __name__ == "__main__":
    main()
