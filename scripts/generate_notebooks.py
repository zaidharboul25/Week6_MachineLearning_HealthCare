"""
Generate 7 structured, reproducible Jupyter Notebooks calling healthconnect modules.
"""

import json
from pathlib import Path

notebooks_dir = Path("notebooks")
notebooks_dir.mkdir(parents=True, exist_ok=True)

def make_cell(cell_type, source):
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [s + "\n" for s in source.split("\n")]
    }

def make_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [s + "\n" for s in source.split("\n")]
    }

def write_nb(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.12"},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(notebooks_dir / filename, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Created notebooks/{filename}")

# Notebook 1: Data Exploration
nb1_cells = [
    make_cell("markdown", "# HealthConnect Rwanda — 01. Exploratory Data Analysis (EDA)\n**Author:** Zaid Harboul  \n**Track:** Machine Learning Engineering | AnalystLab Africa — Week 6\n\nThis notebook performs comprehensive profiling of the 27 relational healthcare datasets."),
    make_code_cell("import sys\nfrom pathlib import Path\nproject_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(project_root / 'src'))\n\nimport pandas as pd\nfrom healthconnect.config import DATA_RAW_DIR, REPORTS_DIR\nfrom healthconnect.data.audit import audit_all\n\nprint('Project Root:', project_root)"),
    make_cell("markdown", "## 1. Execute Complete Data Audit\nProfile all 27 files, inspect rows, columns, duplicate rows, missingness, and primary key validity."),
    make_code_cell("audit_results = audit_all()\ndf_inventory = pd.read_csv(REPORTS_DIR / 'data_inventory.csv')\ndf_inventory.head(10)"),
    make_cell("markdown", "## 2. Inspect Target Distributions\nInspect key targets: Billing amounts, claims adjudication status, and patient satisfaction ratings."),
    make_code_cell("df_bill = pd.read_csv(DATA_RAW_DIR / 'HC_Billing.csv')\ndf_claims = pd.read_csv(DATA_RAW_DIR / 'Insurance_Claims.csv')\ndf_fb = pd.read_csv(DATA_RAW_DIR / 'HC_Patient_Feedback.csv')\n\nprint('Billing Amount Stats:\\n', df_bill['Amount'].describe())\nprint('\\nClaims Status Breakdown:\\n', df_claims['Status'].value_counts())\nprint('\\nFeedback Rating Distribution:\\n', df_fb['Rating'].value_counts())")
]
write_nb("01_data_exploration.ipynb", nb1_cells)

# Notebook 2: Data Cleaning & Integration
nb2_cells = [
    make_cell("markdown", "# HealthConnect Rwanda — 02. Data Cleaning & Integration\n**Author:** Zaid Harboul\n\nIntegrates master and transactional tables into safe, leak-free analytical grains."),
    make_code_cell("import sys\nfrom pathlib import Path\nproject_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(project_root / 'src'))\n\nimport pandas as pd\nfrom healthconnect.config import DATA_RAW_DIR, REPORTS_DIR\n\ndf_id = pd.read_csv(REPORTS_DIR / 'id_quality.csv')\ndf_id"),
    make_cell("markdown", "## Referential Integrity & Join Validation\nValidates that join cardinalities are strictly 1:1 or N:1 without row explosion."),
    make_code_cell("appts = pd.read_csv(DATA_RAW_DIR / 'HC_Clinical_Transactions.xlsx - Appointments.csv')\npats = pd.read_csv(DATA_RAW_DIR / 'HC_Patients.csv')\nbill = pd.read_csv(DATA_RAW_DIR / 'HC_Billing.csv')\n\nprint('Appointments matches in Patients:', appts['PatientID'].isin(pats['PatientID']).mean() * 100, '%')\nprint('Appointments matches in Billing:', appts['AppointmentID'].isin(bill['AppointmentID']).mean() * 100, '%')")
]
write_nb("02_data_cleaning_integration.ipynb", nb2_cells)

# Notebook 3: Feature Engineering
nb3_cells = [
    make_cell("markdown", "# HealthConnect Rwanda — 03. Feature Engineering\n**Author:** Zaid Harboul\n\nEngineers clinical, demographic, operational, and financial features across analytical datasets."),
    make_code_cell("import sys\nfrom pathlib import Path\nproject_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(project_root / 'src'))\n\nimport pandas as pd\nfrom healthconnect.config import DATA_PROCESSED_DIR, REPORTS_DIR\n\ndf_feat_dict = pd.read_csv(REPORTS_DIR / 'feature_dictionary.csv')\ndf_feat_dict"),
    make_cell("markdown", "## Inspect Processed Analytical Datasets\nReview the shapes and columns of generated modeling datasets."),
    make_code_cell("df_bill_analytical = pd.read_csv(DATA_PROCESSED_DIR / 'billing_analytical.csv')\nprint('Billing Analytical Shape:', df_bill_analytical.shape)\nprint('Engineered Columns:', [c for c in df_bill_analytical.columns if 'Ratio' in c or 'Workload' in c or 'Group' in c])")
]
write_nb("03_feature_engineering.ipynb", nb3_cells)

# Notebook 4: Classification Models
nb4_cells = [
    make_cell("markdown", "# HealthConnect Rwanda — 04. Supervised Classification Models\n**Author:** Zaid Harboul\n\nEvaluates Models 1 to 4: Admission Triage, Patient Satisfaction, Insurance Claims, and High-Risk Stratification."),
    make_code_cell("import sys, json\nfrom pathlib import Path\nproject_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(project_root / 'src'))\n\nimport pandas as pd\nfrom healthconnect.config import METRICS_DIR\n\nwith open(METRICS_DIR / 'experiment_metrics.json') as f:\n    metrics = json.load(f)\n\nfor task, data in metrics['classification'].items():\n    print(f'=== {task} (Best: {data[\"best_algorithm\"]}) ===')\n    print(pd.DataFrame(data['algorithms']).T[['accuracy', 'f1', 'roc_auc']])\n    print()"),
    make_cell("markdown", "## Display Confusion Matrices\nVisualizes diagnostic performance and trade-offs."),
    make_code_cell("from IPython.display import Image, display\nfrom healthconnect.config import FIGURES_DIR\n\ndisplay(Image(filename=str(FIGURES_DIR / 'cm_claims_status.png')))\ndisplay(Image(filename=str(FIGURES_DIR / 'cm_risk_stratification.png')))")
]
write_nb("04_classification.ipynb", nb4_cells)

# Notebook 5: Regression Models
nb5_cells = [
    make_cell("markdown", "# HealthConnect Rwanda — 05. Supervised Regression Models\n**Author:** Zaid Harboul\n\nEvaluates Model 5: Revenue / Billing Amount Regression and documents Model 6 (Length of Stay) data boundaries."),
    make_code_cell("import sys, json\nfrom pathlib import Path\nproject_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(project_root / 'src'))\n\nimport pandas as pd\nfrom healthconnect.config import METRICS_DIR, FIGURES_DIR\nfrom IPython.display import Image, display\n\nwith open(METRICS_DIR / 'experiment_metrics.json') as f:\n    metrics = json.load(f)\n\nprint('=== Revenue Regression Model Performance ===')\ndf_reg = pd.DataFrame(metrics['regression']).T\nprint(df_reg)\n\ndisplay(Image(filename=str(FIGURES_DIR / 'billing_regression_residuals.png')))")
]
write_nb("05_regression.ipynb", nb5_cells)

# Notebook 6: Clustering & Anomaly Detection
nb6_cells = [
    make_cell("markdown", "# HealthConnect Rwanda — 06. Clustering & Anomaly Detection\n**Author:** Zaid Harboul\n\nImplements patient clinical segmentation, healthcare facility tier clustering, and multi-domain anomaly detection."),
    make_code_cell("import sys, json\nfrom pathlib import Path\nproject_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(project_root / 'src'))\n\nfrom healthconnect.config import METRICS_DIR, FIGURES_DIR\nfrom IPython.display import Image, display\n\nwith open(METRICS_DIR / 'experiment_metrics.json') as f:\n    metrics = json.load(f)\n\nprint('Patient Segmentation Silhouette:', metrics['clustering']['patient_segmentation']['silhouette'])\nprint('Facility Segmentation Silhouette:', metrics['clustering']['facility_segmentation']['silhouette'])\nprint('Anomaly Detection Flags:', metrics['anomaly_detection']['billing_anomalies_count'], 'billing outliers')\n\ndisplay(Image(filename=str(FIGURES_DIR / 'facility_clusters_pca.png')))")
]
write_nb("06_clustering_anomaly_detection.ipynb", nb6_cells)

# Notebook 7: Explainable AI
nb7_cells = [
    make_cell("markdown", "# HealthConnect Rwanda — 07. Model Explainability (Explainable AI)\n**Author:** Zaid Harboul\n\nInterprets complex model predictions using SHAP values, global feature importances, and clinical caveats."),
    make_code_cell("import sys, json\nfrom pathlib import Path\nproject_root = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\nsys.path.insert(0, str(project_root / 'src'))\n\nfrom healthconnect.config import FIGURES_DIR, METRICS_DIR\nfrom IPython.display import Image, display\n\nwith open(METRICS_DIR / 'experiment_metrics.json') as f:\n    metrics = json.load(f)\n\nprint('SHAP Summary for Insurance Claims Classifier:')\ndisplay(Image(filename=str(FIGURES_DIR / 'shap_claims_classifier.png')))\n\nprint('SHAP Summary for Revenue Regression Model:')\ndisplay(Image(filename=str(FIGURES_DIR / 'shap_billing_regression.png')))")
]
write_nb("07_explainability.ipynb", nb7_cells)

print("All 7 notebooks successfully generated.")
