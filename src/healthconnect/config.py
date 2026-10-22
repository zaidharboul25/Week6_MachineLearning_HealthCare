"""
Configuration management for HealthConnect Rwanda Machine Learning Pipeline.
Handles paths, random seeds, schema definitions, and experiment settings.
"""

from pathlib import Path
import os

# Project Root is two levels up from this file: src/healthconnect/config.py -> project_root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Core Directories
DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_INTERIM_DIR = DATA_DIR / "interim"
DATA_PROCESSED_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
METRICS_DIR = REPORTS_DIR / "metrics"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DEPLOYMENT_DIR = PROJECT_ROOT / "deployment"

# Reproducibility
RANDOM_SEED = 42

# Canonical Raw Dataset Filenames
DATASET_FILES = {
    "countries": "HCCountries.csv",
    "provinces": "HC_Provinces.csv",
    "districts": "HC_Districts.csv",
    "sectors": "HC_Sectors.csv",
    "villages": "HC_Villages.csv",
    "ownership": "HC_Ownership_Types.csv",
    "departments": "HC_Departments.csv",
    "departments_dup": "HC_Facility_Master_Data.xlsx - Departments.csv",
    "services": "HC_Services.csv",
    "equipment": "HC_Medical_Equipment.csv",
    "rooms": "HC_Rooms.csv",
    "beds": "HC_Beds.csv",
    "specialties": "HC_Medical_Specialties.csv",
    "doctors": "HC_Doctor.csv",
    "nurses": "HC_Nurse.csv",
    "pharmacists": "Pharmacist.csv",
    "lab_scientists": "Laboratory_Scientist.csv",
    "radiographers": "HC_Radiographer.csv",
    "admin_staff": "HC_Administrative_Staff.csv",
    "patients": "HC_Patients.csv",
    "appointments": "HC_Clinical_Transactions.xlsx - Appointments.csv",
    "diagnoses": "HC_Diagnoses.csv",
    "billing": "HC_Billing.csv",
    "payments": "HC_Payments.csv",
    "claims": "Insurance_Claims.csv",
    "feedback": "HC_Patient_Feedback.csv",
    "revenue_summary": "HC_Revenue_Summary.csv"
}

# Ensure all critical working directories exist
for directory in [
    DATA_RAW_DIR,
    DATA_INTERIM_DIR,
    DATA_PROCESSED_DIR,
    ARTIFACTS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    METRICS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)
