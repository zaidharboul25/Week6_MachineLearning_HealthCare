# HealthConnect Rwanda — Healthcare Analytics & Artificial Intelligence Transformation

**Program:** AnalystLab Africa Experience Lab — Week 6  
**Track:** Machine Learning Engineering  
**Developer:** Zaid Harboul  
**Role:** Senior Machine Learning Engineer  
**Environment:** Windows 11 | VS Code | Python 3.12 | scikit-learn 1.8.0 | XGBoost 3.2.0 | FastAPI 0.138.2  
**License:** MIT  

---

## 1. Executive Project Overview

HealthConnect Rwanda is an enterprise healthcare analytics and artificial intelligence transformation initiative across Rwanda's healthcare network. Healthcare delivery environments generate high-velocity, heterogeneous clinical transactions, bed occupancy logs, diagnostic records, pharmaceutical inventories, and financial billing streams across 20 medical facilities.

This repository implements a production-grade, reproducible, privacy-preserving Machine Learning Engineering lifecycle:
- **Relational Data Auditing & Profiling**: Automated analysis of 27 interconnected relational tables.
- **Data Cleaning & Anti-Leakage Integration**: Safe relational joins preventing Cartesian multiplication and post-outcome leakage.
- **Supervised Machine Learning**:
  - *Model 1: Hospital Admission & Acute Care Triage* (Emergency vs Routine encounter)
  - *Model 2: Patient Satisfaction Tier Prediction* (Low, Medium, High)
  - *Model 3: Insurance Claim Approval Classification* (Approved vs Pending)
  - *Model 4: Chronic Multimorbidity Risk Stratification* (High Risk vs Low Risk)
  - *Model 5: Hospital Revenue & Encounter Billing Regression* (Continuous RWF)
  - *Model 6: Inpatient Length of Stay (LOS)* (Data Boundary Assessment & Governance)
- **Unsupervised Learning & Anomaly Detection**:
  - *Patient Segmentation*: K-Means clinical and utilization clustering (k=3 personas)
  - *Healthcare Facility Segmentation*: PCA and operational tier clustering (3 facility tiers)
  - *Fraud & Error Anomaly Detection*: Isolation Forest for billing outliers, insurance claim discrepancies, and duplicate patient identity detection.
- **Explainable AI (XAI)**: SHAP (Shapley Additive exPlanations) and global feature importance attribution.
- **Production Serving Microservice**: FastAPI REST inference API with Pydantic v2 input validation, health checks, and containerized Dockerfile.
- **Automated Testing & Deliverables Verification**: Full pytest test suite (12 passing tests) and automated deliverable auditor.

---

## 2. Repository Structure

```text
HealthConnect-Rwanda-Week6/
├── README.md                                   # Comprehensive project documentation
├── requirements.txt                            # Pinned Python package dependencies
├── pyproject.toml                              # Build configuration & pytest settings
├── .gitignore                                  # Data, PII, secrets, and model exclusion
├── .env.example                                # Environment variable configuration template
├── LICENSE                                     # MIT License
├── data/
│   ├── raw/                                    # 27 Canonical healthcare CSV datasets
│   ├── interim/                                # Intermediate staging tables
│   ├── processed/                              # 6 Modeling-ready analytical datasets
│   └── README.md                               # Healthcare data governance & privacy notice
├── notebooks/
│   ├── 01_data_exploration.ipynb               # Dataset profiling & inventory audit
│   ├── 02_data_cleaning_integration.ipynb      # Relational join integrity & deduplication
│   ├── 03_feature_engineering.ipynb            # Clinical & operational feature engineering
│   ├── 04_classification.ipynb                 # Models 1 to 4 classification experiments
│   ├── 05_regression.ipynb                     # Revenue regression & LOS assessment
│   ├── 06_clustering_anomaly_detection.ipynb   # Patient/facility clustering & anomaly suite
│   └── 07_explainability.ipynb                 # SHAP values & model interpretability
├── src/
│   └── healthconnect/
│       ├── __init__.py                         # Package initialization
│       ├── config.py                           # Dynamic pathlib paths & configuration
│       ├── data/
│       │   ├── audit.py                        # Automated profiling, dictionary & ER analysis
│       │   └── cleaner.py                      # Missing value & data type transformation
│       ├── features/
│       │   └── engineer.py                     # Safe feature derivation & target isolation
│       ├── models/
│       │   ├── classifier.py                   # Classification training & comparison pipeline
│       │   ├── regressor.py                    # Regression training & LOS assessment
│       │   ├── clusterer.py                    # Patient & facility clustering
│       │   └── anomaly.py                      # Isolation Forest & rule-based anomaly detector
│       ├── explainability/
│       │   └── explainer.py                    # SHAP TreeExplainer & feature importances
│       └── visualization/
│           └── plots.py                        # Confusion matrices, ROC, residuals & PCA plots
├── tests/
│   ├── test_data.py                            # Data existence & cleaning boundary tests
│   ├── test_features.py                        # Feature transformation & ratio unit tests
│   ├── test_models.py                          # Model loading & prediction shape unit tests
│   └── test_api.py                             # FastAPI integration tests & schema validation
├── reports/
│   ├── figures/                                # 9 High-resolution publication plots
│   ├── metrics/                                # JSON metrics & evaluation summaries
│   ├── data_inventory.csv                      # Complete table-by-table row/col inventory
│   ├── data_dictionary.csv                     # In-depth 153-column semantic data dictionary
│   ├── id_quality.csv                          # Primary & foreign key integrity report
│   ├── data_quality_report.md                  # Comprehensive data audit & quality report
│   ├── relationship_analysis.md                # Entity-relationship structure & join cardinalities
│   ├── cleaning_log.md                         # Cleaning operations & justification log
│   ├── feature_dictionary.csv                  # Catalog of engineered features
│   ├── model_comparison.md                     # Model performance matrix & comparison
│   ├── technical_report.md                     # 15-Section Comprehensive Technical Report
│   ├── executive_summary.md                    # 3-5 Page Standalone Executive Summary
│   ├── presentation_outline.md                 # 15-Slide Presentation Deck Outline
│   ├── explainable_ai_report.md                # Dedicated XAI & SHAP analysis report
│   ├── deliverables_checklist.md               # Automated deliverable verification checklist
│   ├── test_results.md                         # Pytest automated execution results
│   └── final_submission_summary.md             # Week 6 final submission sign-off
├── artifacts/
│   ├── claims_classifier.joblib                # Trained claims adjudication pipeline
│   ├── billing_regressor.joblib                # Trained revenue forecasting pipeline
│   ├── satisfaction_classifier.joblib          # Trained patient satisfaction pipeline
│   ├── admission_triage_classifier.joblib      # Trained acute care triage pipeline
│   ├── patient_clusterer.joblib                # Trained patient segmentation pipeline
│   ├── facility_clusterer.joblib               # Trained facility operational pipeline
│   ├── anomaly_detector.joblib                 # Trained Isolation Forest detector
│   └── README.md                               # Model artifact privacy governance
├── deployment/
│   ├── app.py                                  # Production FastAPI inference microservice
│   ├── architecture.md                         # 10-Layer enterprise deployment architecture
│   ├── architecture_diagram.mmd                # Complete Mermaid architecture flowchart
│   └── Dockerfile                              # Hardened non-root Docker container
└── scripts/
    ├── audit_data.py                           # Standalone data audit script
    ├── prepare_data.py                         # Standalone cleaning & feature engineering script
    ├── train_models.py                         # Standalone model training & evaluation script
    ├── evaluate_models.py                      # Standalone metrics summary reporting script
    ├── generate_reports.py                     # Standalone technical report generator
    ├── validate_deliverables.py                # Standalone deliverables verification script
    ├── generate_notebooks.py                   # Jupyter notebook synthesis script
    └── run_pipeline.py                         # Single entrypoint orchestrator (--stage all)
```

---

## 3. Dataset Inventory & Schema Architecture

The dataset represents an interconnected enterprise healthcare ecosystem in Rwanda across 27 CSV files:
- **Patients & Demographics**: `HC_Patients.csv` (20,000 patients, demographics, chronic conditions, BMI).
- **Clinical Transactions**: `HC_Clinical_Transactions.xlsx - Appointments.csv` (5,000 appointments), `HC_Diagnoses.csv` (60,000 diagnostic records).
- **Financial & Insurance**: `HC_Billing.csv` (60,000 billing records), `HC_Payments.csv` (60,000 payments), `Insurance_Claims.csv` (42,036 claims).
- **Workforce & Infrastructure**: Doctors (350), Nurses (700), Administrative Staff (80), Pharmacists (50), Laboratory Scientists (40), Radiographers (30), Beds (2,000), Rooms (400), Facilities (20).
- **Patient Experience**: `HC_Patient_Feedback.csv` (21,064 surveys).

### Critical Data Findings
1. **Schema Duplication**: `HC_Departments.csv` and `HC_Facility_Master_Data.xlsx - Departments.csv` were verified to be **100% byte-for-byte identical duplicates** (200 rows, 3 columns).
2. **Missingness**: Master tables exhibited 0% missing values across 26 files. In `HC_Patients.csv`, 5,071 missing entries in `ChronicCondition` represent patients with no diagnosed chronic condition, appropriately imputed with `'None'`.
3. **Data Boundary on Length of Stay (LOS)**: Exhaustive auditing verified that **no admission or discharge timestamps exist** in the raw datasets. In strict adherence to scientific integrity, Model 6 was formally documented as unsupported by available data rather than fabricating artificial timestamps.

---

## 4. Machine Learning Models & Real Evaluation Results

All models were evaluated using strict train/test boundaries and cross-validation without data leakage.

| Model / Problem | Target & Grain | Best Algorithm | Key Evaluation Metrics | Recommended Operational Use |
| :--- | :--- | :--- | :--- | :--- |
| **Model 1: Admission Triage** | `IsEmergencyVisit` (5,000 encounters) | **Decision Tree** | Acc: 0.649 \| F1: 0.154 \| ROC-AUC: 0.536 | Emergency triage and acute care bed prioritization |
| **Model 2: Patient Satisfaction** | `SatisfactionClass` (1,756 surveys) | **Gradient Boosting** | Acc: 0.361 \| F1: 0.340 \| ROC-AUC: 0.459 | Departmental patient experience quality monitoring |
| **Model 3: Insurance Claim Approval** | `TargetStatus` (42,036 claims) | **XGBoost / Decision Tree**| Acc: 0.510 \| F1: 0.609 \| ROC-AUC: 0.514 | Automated claim pre-adjudication and clearinghouse |
| **Model 4: High-Risk Stratification** | `HighRiskTarget` (20,000 patients) | **Decision Tree / XGBoost**| **Acc: 0.956 \| F1: 0.957 \| ROC-AUC: 0.994**| Community health chronic disease proactive outreach |
| **Model 5: Revenue Regression** | `Amount` (5,000 encounters) | **Random Forest Regressor**| RMSE: 82,993 RWF \| MAE: 70,960 RWF | Hospital dynamic revenue forecasting & budgeting |
| **Model 6: Length of Stay (LOS)** | Inpatient Duration | **UNSUPPORTED** | Formally documented data boundary | Implementation of HIS ADT module recommended |
| **Clustering: Patient Segments** | 20,000 Patients | **K-Means (k=3)** | **Silhouette Score: 0.343** | Clinical personas (Preventive, High-Care, Metabolic) |
| **Clustering: Facility Tiers** | 20 Healthcare Facilities | **K-Means + PCA (k=3)**| **Silhouette Score: 0.378** | Operational tiers (Referral Hubs, District, Health Centers) |
| **Anomaly Detection** | Multi-domain | **Isolation Forest** | 49 Billing outliers \| 211 Claim mismatches | Financial itemization review & claim audit queue |

---

## 5. Explainable AI (XAI) & Model Transparency

Using `shap.TreeExplainer` on fitted pipelines, we identified the primary feature attributions:
- **Insurance Claims Adjudication**: Dominated by `Provider_RSSB`, `ClaimDiff`, `BillingAmount`, and `ClaimToBillingRatio`. Claims matching hospital billing schedules exhibit higher approval likelihood.
- **Hospital Revenue Forecasting**: Driven by `Patient Age`, `Month`, `DoctorExperience`, `DepartmentWorkload`, and `BMI`. Senior doctors and higher patient volume departments correlate with higher procedure billing.
- **Clinical Governance Warning**: High statistical feature importance indicates observational correlation, NOT biological or clinical causation.

---

## 6. Installation & Execution Guide

### 6.1 Prerequisites
- Windows 11 (or Linux/macOS)
- Python 3.10+ (tested on Python 3.12.10)
- Git

### 6.2 Setup Python Environment
```bash
# Clone or navigate to the repository
cd c:\Users\zaidh\Desktop\Stage_number_2\week5

# Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 6.3 Execute the End-to-End Pipeline
The project features a single entrypoint orchestrator script supporting full execution or individual stages:

```bash
# Run the complete end-to-end pipeline (Audit -> Prepare -> Train -> Evaluate -> Report -> Validate)
python scripts/run_pipeline.py --stage all
```

#### Running Individual Stages:
```bash
# 1. Profile raw data and generate data dictionary / ER analysis
python scripts/run_pipeline.py --stage audit

# 2. Clean data and engineer features
python scripts/run_pipeline.py --stage prepare

# 3. Train all classification, regression, clustering, and anomaly models
python scripts/run_pipeline.py --stage train

# 4. Print comprehensive evaluation metrics
python scripts/run_pipeline.py --stage evaluate

# 5. Generate technical report, executive summary, and presentation outline
python scripts/run_pipeline.py --stage report

# 6. Run automated test suite and validate all deliverables
python scripts/run_pipeline.py --stage validate
```

### 6.4 Running Automated Tests
```bash
pytest
```
*Expected result: 12 passed tests covering data integrity, feature engineering, model inference, and API endpoints.*

---

## 7. Production API Microservice

The FastAPI inference service serves real-time predictions for claims and encounter costs.

### Running the API Locally
```bash
uvicorn deployment.app:app --host 0.0.0.0 --port 8000 --reload
```

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

### API Sample Request & Response (Claims Adjudication)
```bash
curl -X POST "http://localhost:8000/predict/claims" \
     -H "Content-Type: application/json" \
     -d '{"Provider": "RSSB", "ClaimAmount": 80000.0, "BillingAmount": 95000.0}'
```
**Response:**
```json
{
  "prediction_label": "Approved",
  "prediction_code": 1,
  "probability_approved": 0.5103,
  "recommendation": "Proceed with automated payment clearance"
}
```

---

## 8. GitHub Publication Instructions

To publish this project to GitHub:

```bash
# 1. Verify that .gitignore is active and healthcare CSVs are excluded
git status

# 2. Add files to Git staging
git add .gitignore README.md requirements.txt pyproject.toml .env.example LICENSE
git add src/ notebooks/ deployment/ tests/ scripts/ reports/ artifacts/README.md data/README.md

# 3. Commit changes
git commit -m "feat: complete HealthConnect Rwanda ML engineering pipeline and documentation"

# 4. Link to your GitHub remote repository (replace with your GitHub repository URL)
git remote add origin https://github.com/<your-username>/HealthConnect-Rwanda-Week6.git

# 5. Push to main branch
git branch -M main
git push -u origin main
```

---

## 9. Ethical AI, Healthcare Governance & Data Privacy

1. **Compliance with Rwanda Law No. 058/2021**: Direct patient identifiers (`FirstName`, `LastName`, `Phone`, `DateOfBirth`) are strictly excluded from modeling pipelines, API logs, and version control.
2. **Clinical Decision Support (CDS) Governance**: Models serve as assistive decision-support tools. Autonomous clinical treatment decisions or insurance denials without licensed medical officer review are strictly prohibited.
3. **Model Transparency**: All model predictions are accompanied by confidence intervals, risk probabilities, and SHAP explainability attributions.

---

## 10. Final Deliverables Verification

All Week 6 deliverables are verified:
- [x] 7 Jupyter Notebooks (`notebooks/*.ipynb`)
- [x] Cleaned & feature-engineered datasets (`data/processed/*.csv`)
- [x] Data Inventory & Dictionary (`reports/data_inventory.csv`, `reports/data_dictionary.csv`)
- [x] Model Comparison Matrix (`reports/model_comparison.md`)
- [x] Explainable AI Report (`reports/explainable_ai_report.md`)
- [x] 9 Publication-grade Figures (`reports/figures/*.png`)
- [x] Comprehensive Technical Report (15 Sections) (`reports/technical_report.md`)
- [x] Executive Summary (3-5 Pages) (`reports/executive_summary.md`)
- [x] Presentation Deck Outline (15 Slides) (`reports/presentation_outline.md`)
- [x] Production Deployment Architecture & API (`deployment/architecture.md`, `deployment/app.py`, `deployment/Dockerfile`)
- [x] Automated Test Suite (`tests/`, 12 passed tests)
- [x] Single Entrypoint Runner (`scripts/run_pipeline.py`)
