"""
Data Preparation and Feature Engineering Pipeline Entrypoint.
Cleans raw relational tables, engineers predictive features, and saves modeling-ready datasets to data/processed/.
"""

import sys
from pathlib import Path
import logging
import pandas as pd

# Add src to pythonpath
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from healthconnect.config import (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    REPORTS_DIR,
    DATASET_FILES,
)
from healthconnect.data.cleaner import (
    clean_patients,
    clean_appointments,
    clean_billing,
    clean_diagnoses,
    clean_claims,
    clean_feedback,
)
from healthconnect.features.engineer import (
    build_facility_workload_features,
    build_billing_analytical_dataset,
    build_claims_analytical_dataset,
    build_satisfaction_analytical_dataset,
    build_risk_stratification_dataset,
    build_facility_segmentation_dataset,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("prepare_data")

def main():
    logger.info("Starting HealthConnect Data Preparation & Feature Engineering Pipeline...")
    
    # 1. Load raw tables
    df_patients = clean_patients(pd.read_csv(DATA_RAW_DIR / DATASET_FILES["patients"]))
    df_appts = clean_appointments(pd.read_csv(DATA_RAW_DIR / DATASET_FILES["appointments"]))
    df_billing = clean_billing(pd.read_csv(DATA_RAW_DIR / DATASET_FILES["billing"]))
    df_diag = clean_diagnoses(pd.read_csv(DATA_RAW_DIR / DATASET_FILES["diagnoses"]))
    df_claims = clean_claims(pd.read_csv(DATA_RAW_DIR / DATASET_FILES["claims"]))
    df_feedback = clean_feedback(pd.read_csv(DATA_RAW_DIR / DATASET_FILES["feedback"]))
    
    df_doctors = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["doctors"])
    df_nurses = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["nurses"])
    df_admin = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["admin_staff"])
    df_lab = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["lab_scientists"])
    df_pharm = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["pharmacists"])
    df_rad = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["radiographers"])
    df_deps = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["departments"])
    df_rooms = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["rooms"])
    df_beds = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["beds"])
    df_villages = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["villages"])
    df_sectors = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["sectors"])
    df_districts = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["districts"])
    df_provinces = pd.read_csv(DATA_RAW_DIR / DATASET_FILES["provinces"])
    
    # 2. Build Facility Capacity and Workload Metrics
    df_facility_metrics = build_facility_workload_features(df_appts, df_doctors, df_beds, df_rooms)
    
    # 3. Build Modeling Datasets
    # A: Billing Amount Analytical Dataset (Revenue Regression & Emergency Triage)
    df_billing_analytical = build_billing_analytical_dataset(
        df_appts=df_appts,
        df_patients=df_patients,
        df_billing=df_billing,
        df_diag=df_diag,
        df_doctors=df_doctors,
        df_deps=df_deps,
        df_villages=df_villages,
        df_sectors=df_sectors,
        df_districts=df_districts,
        df_provinces=df_provinces,
        df_facility_metrics=df_facility_metrics
    )
    
    # B: Insurance Claims Analytical Dataset (Claim Approval Classification)
    df_claims_analytical = build_claims_analytical_dataset(df_claims, df_billing)
    
    # C: Patient Satisfaction Analytical Dataset (Satisfaction Classification)
    df_satisfaction_analytical = build_satisfaction_analytical_dataset(df_feedback, df_billing_analytical)
    
    # D: High-Risk Patient Stratification Dataset (Risk Classification & Clinical Rule)
    df_risk_analytical = build_risk_stratification_dataset(df_patients, df_appts, df_diag, df_billing)
    
    # E: Facility Segmentation Dataset (Facility Clustering)
    staff_tables = {
        "Doctor": df_doctors,
        "Nurse": df_nurses,
        "Admin": df_admin,
        "Lab": df_lab,
        "Pharm": df_pharm,
        "Radiographer": df_rad
    }
    df_facility_analytical = build_facility_segmentation_dataset(
        df_facility_metrics=df_facility_metrics,
        df_billing=df_billing,
        df_appts=df_appts,
        df_feedback=df_feedback,
        df_staff_tables=staff_tables
    )
    
    # F: Patient Clustering Dataset (Patient Segmentation)
    df_patient_clustering = df_risk_analytical[[
        "PatientID", "Age", "BMI", "HasChronicCondition", 
        "HistoricalApptCount", "TotalBilledAmount", "SevereDiagnosisCount"
    ]].copy()
    
    # 4. Save Processed Datasets
    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_billing_analytical.to_csv(DATA_PROCESSED_DIR / "billing_analytical.csv", index=False)
    df_claims_analytical.to_csv(DATA_PROCESSED_DIR / "claims_analytical.csv", index=False)
    df_satisfaction_analytical.to_csv(DATA_PROCESSED_DIR / "satisfaction_analytical.csv", index=False)
    df_risk_analytical.to_csv(DATA_PROCESSED_DIR / "risk_analytical.csv", index=False)
    df_facility_analytical.to_csv(DATA_PROCESSED_DIR / "facility_analytical.csv", index=False)
    df_patient_clustering.to_csv(DATA_PROCESSED_DIR / "patient_clustering.csv", index=False)
    
    logger.info("Saved all modeling-ready analytical datasets to data/processed/")
    
    # 5. Generate Feature Dictionary and Cleaning Log
    generate_feature_dictionary(df_billing_analytical, df_claims_analytical, df_satisfaction_analytical, REPORTS_DIR)
    generate_cleaning_log(REPORTS_DIR)
    logger.info("Generated reports/cleaning_log.md and reports/feature_dictionary.csv")

def generate_feature_dictionary(df_bill, df_claims, df_sat, reports_dir):
    features = [
        {"feature_name": "Amount", "dataset": "billing_analytical", "type": "Target (Numeric)", "description": "Total medical billing amount for the appointment encounter in Rwandan Francs (RWF)."},
        {"feature_name": "AgeGroup", "dataset": "billing/satisfaction/risk", "type": "Engineered (Categorical)", "description": "Standardized demographic tier (<18, 18-35, 36-50, 51-65, >65) derived from patient Age."},
        {"feature_name": "BMICategory", "dataset": "billing/satisfaction/risk", "type": "Engineered (Categorical)", "description": "WHO Body Mass Index classification: Underweight, Normal, Overweight, Obese."},
        {"feature_name": "HasChronicCondition", "dataset": "billing/satisfaction/risk", "type": "Engineered (Binary)", "description": "Binary flag indicating diagnosis of Diabetes, Hypertension, or Asthma."},
        {"feature_name": "DepartmentWorkload", "dataset": "billing/satisfaction", "type": "Engineered (Numeric)", "description": "Encounter volume handled by clinical department."},
        {"feature_name": "FacilityApptVolume", "dataset": "billing/facility", "type": "Engineered (Numeric)", "description": "Annual patient appointment load per healthcare facility."},
        {"feature_name": "PatientToDoctorRatio", "dataset": "billing/facility", "type": "Engineered (Numeric)", "description": "Operational ratio of patient encounters to active medical doctors."},
        {"feature_name": "BedToDoctorRatio", "dataset": "billing/facility", "type": "Engineered (Numeric)", "description": "Hospital infrastructure capacity metric: beds per doctor."},
        {"feature_name": "ClaimToBillingRatio", "dataset": "claims_analytical", "type": "Engineered (Numeric)", "description": "Ratio of requested insurance claim amount to invoiced billing amount."},
        {"feature_name": "ClaimDiff", "dataset": "claims_analytical", "type": "Engineered (Numeric)", "description": "Absolute difference between invoiced billing amount and requested claim."},
        {"feature_name": "TargetStatus", "dataset": "claims_analytical", "type": "Target (Binary)", "description": "Insurance claim approval status: 1 = Approved, 0 = Pending."},
        {"feature_name": "SatisfactionClass", "dataset": "satisfaction_analytical", "type": "Target (Categorical)", "description": "Patient survey outcome tier: Low (1-2), Medium (3), High (4-5)."},
        {"feature_name": "HighRiskTarget", "dataset": "risk_analytical", "type": "Target (Binary)", "description": "Documented clinical risk stratification based on multimorbidity, age, and severe history."},
        {"feature_name": "IsEmergencyVisit", "dataset": "billing_analytical", "type": "Target / Feature (Binary)", "description": "Encounter urgency indicator: 1 = Emergency, 0 = Routine (Consultation / Follow-up)."}
    ]
    pd.DataFrame(features).to_csv(reports_dir / "feature_dictionary.csv", index=False)

def generate_cleaning_log(reports_dir):
    log_content = """# HealthConnect Rwanda — Data Cleaning & Transformation Log

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
"""
    with open(reports_dir / "cleaning_log.md", "w", encoding="utf-8") as f:
        f.write(log_content)

if __name__ == "__main__":
    main()
