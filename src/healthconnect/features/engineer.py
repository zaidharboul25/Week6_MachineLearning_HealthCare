"""
Feature Engineering Module for HealthConnect Rwanda.
Transforms raw cleaned relational tables into machine-learning-ready analytical datasets
with defensible engineered features and strict target leakage prevention.
"""

from pathlib import Path
import logging
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def derive_age_group(age: pd.Series) -> pd.Series:
    """Categorize age into standard demographic groups."""
    bins = [-1, 17, 35, 50, 65, 150]
    labels = ["<18", "18-35", "36-50", "51-65", ">65"]
    return pd.cut(age, bins=bins, labels=labels).astype(str)

def derive_bmi_category(bmi: pd.Series) -> pd.Series:
    """Categorize BMI according to WHO standards."""
    bins = [-1, 18.5, 24.9, 29.9, 100]
    labels = ["Underweight", "Normal", "Overweight", "Obese"]
    return pd.cut(bmi, bins=bins, labels=labels).astype(str)

def build_facility_workload_features(
    df_appts: pd.DataFrame,
    df_doctors: pd.DataFrame,
    df_beds: pd.DataFrame,
    df_rooms: pd.DataFrame
) -> pd.DataFrame:
    """
    Compute facility-level capacity and operational workload metrics.
    """
    facility_appts = df_appts.groupby("FacilityID").size().rename("FacilityApptVolume")
    facility_doctors = df_doctors.groupby("FacilityID").size().rename("FacilityDoctorCount")
    facility_rooms = df_rooms.groupby("FacilityID").size().rename("FacilityRoomCount")
    
    # Rooms to beds mapping
    bed_room = df_beds.merge(df_rooms[["RoomID", "FacilityID"]], on="RoomID", how="left")
    facility_beds = bed_room.groupby("FacilityID").size().rename("FacilityBedCount")
    
    fac_df = pd.concat([facility_appts, facility_doctors, facility_rooms, facility_beds], axis=1).fillna(0).reset_index()
    fac_df["PatientToDoctorRatio"] = (fac_df["FacilityApptVolume"] / np.maximum(fac_df["FacilityDoctorCount"], 1)).round(2)
    fac_df["BedToDoctorRatio"] = (fac_df["FacilityBedCount"] / np.maximum(fac_df["FacilityDoctorCount"], 1)).round(2)
    return fac_df

def build_billing_analytical_dataset(
    df_appts: pd.DataFrame,
    df_patients: pd.DataFrame,
    df_billing: pd.DataFrame,
    df_diag: pd.DataFrame,
    df_doctors: pd.DataFrame,
    df_deps: pd.DataFrame,
    df_villages: pd.DataFrame,
    df_sectors: pd.DataFrame,
    df_districts: pd.DataFrame,
    df_provinces: pd.DataFrame,
    df_facility_metrics: pd.DataFrame
) -> pd.DataFrame:
    """
    Build modeling dataset for Revenue / Billing Amount Prediction (Model 5).
    Grain: Appointment encounter (APT000001 - APT005000).
    Target: Amount (Billing amount).
    Leakage Prevention: Excludes post-settlement payment methods and claims.
    """
    logger.info("Building Billing Analytical Dataset...")
    # Base merge: Appointments + Billing (1:1)
    df = df_appts.merge(df_billing[["AppointmentID", "Amount"]], on="AppointmentID", how="inner")
    
    # Merge Diagnoses (1:1)
    df = df.merge(df_diag[["AppointmentID", "Diagnosis", "Severity"]], on="AppointmentID", how="left")
    
    # Merge Patient Demographics
    patient_cols = ["PatientID", "Age", "Gender", "MaritalStatus", "Occupation", "Education", 
                    "InsuranceID", "BloodGroup", "BMI", "ChronicCondition", "VillageID"]
    df = df.merge(df_patients[patient_cols], on="PatientID", how="left")
    
    # Geographic hierarchy enrichment
    geo = df_villages.merge(df_sectors, on="SectorID", how="left") \
                     .merge(df_districts, on="DistrictID", how="left") \
                     .merge(df_provinces, on="ProvinceID", how="left")
    df = df.merge(geo[["VillageID", "DistrictName", "ProvinceName"]], on="VillageID", how="left")
    
    # Department Name
    df = df.merge(df_deps[["DepartmentID", "DepartmentName"]], on="DepartmentID", how="left")
    
    # Doctor experience
    df = df.merge(df_doctors[["StaffID", "YearsExperience"]].rename(columns={"StaffID": "DoctorID", "YearsExperience": "DoctorExperience"}),
                  on="DoctorID", how="left")
    
    # Facility operational metrics
    df = df.merge(df_facility_metrics, on="FacilityID", how="left")
    
    # Feature engineering
    df["AgeGroup"] = derive_age_group(df["Age"])
    df["BMICategory"] = derive_bmi_category(df["BMI"])
    df["HasChronicCondition"] = (df["ChronicCondition"] != "None").astype(int)
    
    # Temporal indicators from Date
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Quarter"] = df["Date"].dt.quarter
    df["IsWeekend"] = df["DayOfWeek"].isin([5, 6]).astype(int)
    
    # Department workload
    dept_workload = df.groupby("DepartmentID")["AppointmentID"].transform("count")
    df["DepartmentWorkload"] = dept_workload
    
    # Acute/Emergency encounter indicator (Model 1 proxy)
    df["IsEmergencyVisit"] = (df["VisitType"] == "Emergency").astype(int)
    
    # Drop raw IDs that cause data leakage / memorization
    drop_cols = ["Date", "VillageID", "PatientID", "DoctorID"]
    df_clean = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    logger.info(f"Billing Analytical Dataset built: Shape = {df_clean.shape}")
    return df_clean

def build_claims_analytical_dataset(
    df_claims: pd.DataFrame,
    df_billing: pd.DataFrame
) -> pd.DataFrame:
    """
    Build modeling dataset for Insurance Claim Status Classification (Model 3).
    Grain: ClaimID.
    Target: Status ('Approved' -> 1, 'Pending' -> 0).
    """
    logger.info("Building Claims Analytical Dataset...")
    df = df_claims.merge(df_billing[["BillingID", "Amount"]].rename(columns={"Amount": "BillingAmount"}),
                         on="BillingID", how="inner")
    
    # Financial ratio features
    df["ClaimToBillingRatio"] = (df["ClaimAmount"] / np.maximum(df["BillingAmount"], 1.0)).round(4)
    df["ClaimDiff"] = (df["BillingAmount"] - df["ClaimAmount"]).round(2)
    df["IsFullClaim"] = (df["ClaimAmount"] >= df["BillingAmount"]).astype(int)
    
    # Target encoding
    # Observed raw classes: 'Approved' (21,008) and 'Pending' (21,028)
    df["TargetStatus"] = (df["Status"] == "Approved").astype(int)
    
    logger.info(f"Claims Analytical Dataset built: Shape = {df.shape}")
    return df

def build_satisfaction_analytical_dataset(
    df_feedback: pd.DataFrame,
    df_billing_analytical: pd.DataFrame
) -> pd.DataFrame:
    """
    Build modeling dataset for Patient Satisfaction Prediction (Model 2).
    Grain: Feedback submission linked to encounter.
    Target: SatisfactionClass ('Low', 'Medium', 'High').
    """
    logger.info("Building Patient Satisfaction Analytical Dataset...")
    # Link feedback to clinical analytical dataset on AppointmentID
    df = df_feedback.merge(df_billing_analytical, on="AppointmentID", how="inner")
    
    # Derive Target:
    # Rating 1-2: Low | Rating 3: Medium | Rating 4-5: High
    def map_satisfaction(rating: int) -> str:
        if rating <= 2:
            return "Low"
        elif rating == 3:
            return "Medium"
        else:
            return "High"
            
    df["SatisfactionClass"] = df["Rating"].apply(map_satisfaction)
    
    # Leakage prevention: Exclude 'Rating' and 'Comment' from input features
    df_clean = df.drop(columns=["FeedbackID", "Rating", "Comment"])
    logger.info(f"Satisfaction Analytical Dataset built: Shape = {df_clean.shape}")
    return df_clean

def build_risk_stratification_dataset(
    df_patients: pd.DataFrame,
    df_appts: pd.DataFrame,
    df_diag: pd.DataFrame,
    df_billing: pd.DataFrame
) -> pd.DataFrame:
    """
    Build dataset for High-Risk Patient Stratification (Model 4).
    Grain: PatientID (20,000 patients).
    Defines transparent, documented clinical risk rules:
    High Risk if:
      - Has diagnosed chronic condition (Diabetes, Hypertension, Asthma) AND (Age >= 60 OR BMI >= 30)
      OR
      - Has experienced Severe diagnosis
      OR
      - Frequent healthcare utilizer (> 3 appointments)
    """
    logger.info("Building Patient Risk Stratification Dataset...")
    df = df_patients.copy()
    
    # Aggregate patient clinical history from appointments
    appt_counts = df_appts.groupby("PatientID").size().rename("HistoricalApptCount")
    
    # Severity history
    appt_diag = df_appts.merge(df_diag, on="AppointmentID", how="left")
    severe_counts = appt_diag[appt_diag["Severity"] == "Severe"].groupby("PatientID").size().rename("SevereDiagnosisCount")
    
    # Total billing history
    appt_bill = df_appts.merge(df_billing, on="AppointmentID", how="left")
    total_billed = appt_bill.groupby("PatientID")["Amount"].sum().rename("TotalBilledAmount")
    
    df = df.merge(appt_counts, on="PatientID", how="left").fillna({"HistoricalApptCount": 0})
    df = df.merge(severe_counts, on="PatientID", how="left").fillna({"SevereDiagnosisCount": 0})
    df = df.merge(total_billed, on="PatientID", how="left").fillna({"TotalBilledAmount": 0})
    
    df["AgeGroup"] = derive_age_group(df["Age"])
    df["BMICategory"] = derive_bmi_category(df["BMI"])
    df["HasChronicCondition"] = (df["ChronicCondition"] != "None").astype(int)
    
    # Ground-truth clinical risk rule (Transparent Heuristic)
    is_high_risk = (
        ((df["HasChronicCondition"] == 1) & ((df["Age"] >= 60) | (df["BMI"] >= 30))) |
        (df["SevereDiagnosisCount"] >= 1) |
        (df["HistoricalApptCount"] >= 3)
    )
    df["HighRiskTarget"] = is_high_risk.astype(int)
    
    logger.info(f"Patient Risk Dataset built: Shape = {df.shape}, High Risk Count = {df['HighRiskTarget'].sum()} ({df['HighRiskTarget'].mean()*100:.1f}%)")
    return df

def build_facility_segmentation_dataset(
    df_facility_metrics: pd.DataFrame,
    df_billing: pd.DataFrame,
    df_appts: pd.DataFrame,
    df_feedback: pd.DataFrame,
    df_staff_tables: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    """
    Build facility-level operational dataset for facility clustering.
    Grain: FacilityID (HF001 - HF020).
    """
    logger.info("Building Facility Operational Dataset...")
    df = df_facility_metrics.copy()
    
    # Revenue aggregation
    appt_bill = df_appts.merge(df_billing, on="AppointmentID", how="left")
    facility_rev = appt_bill.groupby("FacilityID")["Amount"].sum().rename("TotalRevenue")
    df = df.merge(facility_rev, on="FacilityID", how="left").fillna({"TotalRevenue": 0})
    
    # Average satisfaction rating
    appt_fb = df_appts.merge(df_feedback, on="AppointmentID", how="left")
    fac_sat = appt_fb.groupby("FacilityID")["Rating"].mean().round(2).rename("AvgSatisfactionRating")
    df = df.merge(fac_sat, on="FacilityID", how="left").fillna({"AvgSatisfactionRating": 3.0})
    
    # Staff counts across all roles
    for role_name, staff_df in df_staff_tables.items():
        if "FacilityID" in staff_df.columns:
            cnt = staff_df.groupby("FacilityID").size().rename(f"Staff_{role_name}")
            df = df.merge(cnt, on="FacilityID", how="left").fillna({f"Staff_{role_name}": 0})
            
    logger.info(f"Facility Operational Dataset built: Shape = {df.shape}")
    return df
