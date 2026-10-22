# HealthConnect Rwanda — Deliverables Verification Checklist

**Author:** Zaid Harboul  
**Program:** AnalystLab Africa — Week 6  
**Track:** Machine Learning Engineering  

| Deliverable Item | Status | Verification Details |
| :--- | :--- | :--- |
| **Raw Datasets (27 CSV files in data/raw/)** | `PASS` | Directory valid with 27 items |
| **Processed Billing Analytical Dataset** | `PASS` | Valid file (1,038,249 bytes) |
| **Processed Claims Analytical Dataset** | `PASS` | Valid file (3,005,285 bytes) |
| **Processed Satisfaction Analytical Dataset** | `PASS` | Valid file (374,165 bytes) |
| **Processed Risk Stratification Dataset** | `PASS` | Valid file (3,452,416 bytes) |
| **Processed Facility Operational Dataset** | `PASS` | Valid file (1,436 bytes) |
| **Processed Patient Clustering Dataset** | `PASS` | Valid file (658,910 bytes) |
| **Data Inventory Report** | `PASS` | Valid file (1,920 bytes) |
| **Data Dictionary Report** | `PASS` | Valid file (13,282 bytes) |
| **ID Quality Report** | `PASS` | Valid file (738 bytes) |
| **Data Quality Audit Report (Markdown)** | `PASS` | Valid file (5,998 bytes) |
| **Relationship Analysis Report (Markdown)** | `PASS` | Valid file (4,509 bytes) |
| **Data Cleaning Log (Markdown)** | `PASS` | Valid file (2,290 bytes) |
| **Feature Dictionary (CSV)** | `PASS` | Valid file (1,849 bytes) |
| **Config Module (src/healthconnect/config.py)** | `PASS` | Valid file (2,212 bytes) |
| **Data Cleaner Module (src/healthconnect/data/cleaner.py)** | `PASS` | Valid file (3,688 bytes) |
| **Feature Engineering Module (src/healthconnect/features/engineer.py)** | `PASS` | Valid file (11,077 bytes) |
| **Classification Module (src/healthconnect/models/classifier.py)** | `PASS` | Valid file (9,408 bytes) |
| **Regression Module (src/healthconnect/models/regressor.py)** | `PASS` | Valid file (5,996 bytes) |
| **Clustering Module (src/healthconnect/models/clusterer.py)** | `PASS` | Valid file (6,795 bytes) |
| **Anomaly Detection Module (src/healthconnect/models/anomaly.py)** | `PASS` | Valid file (6,021 bytes) |
| **Explainable AI Module (src/healthconnect/explainability/explainer.py)** | `PASS` | Valid file (5,739 bytes) |
| **Visualization Module (src/healthconnect/visualization/plots.py)** | `PASS` | Valid file (6,223 bytes) |
| **Jupyter Notebook: 01_data_exploration.ipynb** | `PASS` | Valid file (2,791 bytes) |
| **Jupyter Notebook: 02_data_cleaning_integration.ipynb** | `PASS` | Valid file (2,091 bytes) |
| **Jupyter Notebook: 03_feature_engineering.ipynb** | `PASS` | Valid file (1,914 bytes) |
| **Jupyter Notebook: 04_classification.ipynb** | `PASS` | Valid file (2,182 bytes) |
| **Jupyter Notebook: 05_regression.ipynb** | `PASS` | Valid file (1,598 bytes) |
| **Jupyter Notebook: 06_clustering_anomaly_detection.ipynb** | `PASS` | Valid file (1,767 bytes) |
| **Jupyter Notebook: 07_explainability.ipynb** | `PASS` | Valid file (1,628 bytes) |
| **Model Artifact: claims_classifier.joblib** | `PASS` | Valid file (9,067 bytes) |
| **Model Artifact: billing_regressor.joblib** | `PASS` | Valid file (5,705,098 bytes) |
| **Model Artifact: satisfaction_classifier.joblib** | `PASS` | Valid file (711,221 bytes) |
| **Model Artifact: admission_triage_classifier.joblib** | `PASS` | Valid file (15,531 bytes) |
| **Model Artifact: patient_clusterer.joblib** | `PASS` | Valid file (82,638 bytes) |
| **Model Artifact: facility_clusterer.joblib** | `PASS` | Valid file (3,907 bytes) |
| **Model Artifact: anomaly_detector.joblib** | `PASS` | Valid file (1,772,169 bytes) |
| **Report Figure: target_distributions_overview.png** | `PASS` | Valid file (194,012 bytes) |
| **Report Figure: cm_claims_status.png** | `PASS` | Valid file (70,944 bytes) |
| **Report Figure: cm_risk_stratification.png** | `PASS` | Valid file (68,560 bytes) |
| **Report Figure: cm_patient_satisfaction.png** | `PASS` | Valid file (69,454 bytes) |
| **Report Figure: cm_admission_triage.png** | `PASS` | Valid file (68,491 bytes) |
| **Report Figure: billing_regression_residuals.png** | `PASS` | Valid file (518,262 bytes) |
| **Report Figure: facility_clusters_pca.png** | `PASS` | Valid file (161,077 bytes) |
| **Report Figure: shap_claims_classifier.png** | `PASS` | Valid file (179,061 bytes) |
| **Report Figure: shap_billing_regression.png** | `PASS` | Valid file (352,472 bytes) |
| **Model Comparison Report (Markdown)** | `PASS` | Valid file (6,617 bytes) |
| **Comprehensive Technical Report (15 Sections)** | `PASS` | Valid file (15,538 bytes) |
| **Executive Summary Report (3-5 Pages)** | `PASS` | Valid file (5,794 bytes) |
| **Presentation Outline Deck (15 Slides)** | `PASS` | Valid file (6,570 bytes) |
| **Explainable AI Report (Markdown)** | `PASS` | Valid file (5,263 bytes) |
| **Experiment Metrics JSON** | `PASS` | Valid file (19,910 bytes) |
| **Deployment Architecture Document** | `PASS` | Valid file (5,487 bytes) |
| **Deployment Architecture Diagram (Mermaid)** | `PASS` | Valid file (2,500 bytes) |
| **FastAPI Serving Microservice (app.py)** | `PASS` | Valid file (7,514 bytes) |
| **Production Dockerfile** | `PASS` | Valid file (1,064 bytes) |
| **README.md** | `PASS` | Valid file (18,478 bytes) |
| **requirements.txt** | `PASS` | Valid file (518 bytes) |
| **pyproject.toml** | `PASS` | Valid file (966 bytes) |
| **.gitignore** | `PASS` | Valid file (728 bytes) |
| **.env.example** | `PASS` | Valid file (364 bytes) |
| **LICENSE** | `PASS` | Valid file (1,100 bytes) |
| **Model 6: Length of Stay (LOS) Inpatient Duration** | `WARNING` | Documented as UNSUPPORTED by source data (admission/discharge timestamps absent across 27 CSVs). Correct adherence to scientific anti-fabrication standards. |
