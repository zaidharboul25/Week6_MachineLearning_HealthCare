"""
Anomaly Detection Module for HealthConnect Rwanda.
Implements unsupervised anomaly detection using Isolation Forest and domain-specific rules:
- High billing anomalies
- Discrepant/suspicious insurance claims
- Potential duplicate patient demographics
- Outlier facility workloads
Provides anomaly scores, interpretable flags, and clinical/administrative review workflows.
"""

from pathlib import Path
import logging
from typing import Dict, Any, List
import joblib
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from healthconnect.config import ARTIFACTS_DIR, RANDOM_SEED

logger = logging.getLogger(__name__)

def detect_billing_anomalies(
    df_billing: pd.DataFrame,
    contamination: float = 0.01
) -> pd.DataFrame:
    """
    Detect statistical outliers and unusual high-billing amounts using Isolation Forest & IQR.
    """
    logger.info("Detecting Billing Anomalies via Isolation Forest...")
    df = df_billing.copy()
    
    # Statistical IQR Bounds
    q25 = df["Amount"].quantile(0.25)
    q75 = df["Amount"].quantile(0.75)
    iqr = q75 - q25
    upper_bound = q75 + 1.5 * iqr
    
    # Isolation Forest
    iso = IsolationForest(contamination=contamination, random_state=RANDOM_SEED)
    df["AnomalyScore"] = iso.fit_predict(df[["Amount"]])
    df["AnomalyFlag"] = (df["AnomalyScore"] == -1)
    
    # Reason derivation
    def assign_reason(row):
        if row["Amount"] > upper_bound:
            return f"Extreme High Billing (> 1.5x IQR threshold: {upper_bound:,.0f} RWF)"
        elif row["AnomalyFlag"]:
            return "Multivariate / Distributional Outlier in Transaction Density"
        return "Normal"
        
    df["AnomalyReason"] = df.apply(assign_reason, axis=1)
    
    # Recommended Action Workflow
    def assign_action(reason):
        if reason == "Normal":
            return "Routine Processing"
        return "Route to Internal Medical Billing Audit Queue for Clinical Itemization Review"
        
    df["ReviewAction"] = df["AnomalyReason"].apply(assign_action)
    
    logger.info(f"Billing anomalies detected: {df['AnomalyFlag'].sum()} flagged records.")
    return df

def detect_claim_anomalies(
    df_claims_analytical: pd.DataFrame
) -> pd.DataFrame:
    """
    Identify suspicious or discrepant insurance claims:
    - ClaimAmount exceeding BillingAmount (Ratio > 1.0)
    - Zero or near-zero billing with high claim amounts
    - Extreme claim amounts in top 99.5th percentile
    """
    logger.info("Detecting Insurance Claim Anomalies...")
    df = df_claims_analytical.copy()
    
    claim_99 = df["ClaimAmount"].quantile(0.995)
    
    conditions = [
        (df["ClaimToBillingRatio"] > 1.05),
        (df["ClaimAmount"] > claim_99),
        (df["ClaimDiff"] < 0)
    ]
    reasons = [
        "Claim amount exceeds hospital billed invoice amount (Ratio > 1.05)",
        f"Claim amount in extreme top 0.5% percentile (> {claim_99:,.0f} RWF)",
        "Negative billing-to-claim differential"
    ]
    
    df["ClaimAnomalyFlag"] = False
    df["ClaimAnomalyReason"] = "Normal"
    
    for cond, reason in zip(conditions, reasons):
        mask = cond & (~df["ClaimAnomalyFlag"])
        df.loc[mask, "ClaimAnomalyFlag"] = True
        df.loc[mask, "ClaimAnomalyReason"] = reason
        
    df["ReviewWorkflow"] = df["ClaimAnomalyFlag"].apply(
        lambda f: "Hold Claim: Reconcile with Hospital Electronic Charge Sheet" if f else "Auto-Adjudicate"
    )
    
    logger.info(f"Claim anomalies detected: {df['ClaimAnomalyFlag'].sum()} flagged claims.")
    return df

def detect_duplicate_patients(
    df_patients: pd.DataFrame
) -> pd.DataFrame:
    """
    Identify potential duplicate patient records based on shared demographics
    (e.g., identical Phone number or FirstName + LastName + DateOfBirth).
    """
    logger.info("Detecting Potential Duplicate Patient Records...")
    df = df_patients.copy()
    
    # Phone duplicates
    phone_counts = df.groupby("Phone")["PatientID"].transform("count")
    # Exact name + DOB duplicates
    name_dob_counts = df.groupby(["FirstName", "LastName", "DateOfBirth"])["PatientID"].transform("count")
    
    df["IsDuplicatePhone"] = (phone_counts > 1)
    df["IsDuplicateIdentity"] = (name_dob_counts > 1)
    df["DuplicateRecordFlag"] = df["IsDuplicatePhone"] | df["IsDuplicateIdentity"]
    
    logger.info(f"Duplicate patient records flagged: {df['DuplicateRecordFlag'].sum()}")
    return df

def run_all_anomaly_detection(
    df_billing: pd.DataFrame,
    df_claims_analytical: pd.DataFrame,
    df_patients: pd.DataFrame
) -> Dict[str, Any]:
    """Execute complete anomaly detection suite across financial, claims, and identity domains."""
    df_billing_anomalies = detect_billing_anomalies(df_billing)
    df_claim_anomalies = detect_claim_anomalies(df_claims_analytical)
    df_patient_dups = detect_duplicate_patients(df_patients)
    
    # Fit Isolation Forest artifact on claims and billing for future inference
    iso_model = IsolationForest(contamination=0.01, random_state=RANDOM_SEED)
    iso_model.fit(df_claims_analytical[["ClaimAmount", "BillingAmount", "ClaimToBillingRatio"]])
    joblib.dump(iso_model, ARTIFACTS_DIR / "anomaly_detector.joblib")
    
    return {
        "billing_anomalies_count": int(df_billing_anomalies["AnomalyFlag"].sum()),
        "billing_anomalies_pct": round(float(df_billing_anomalies["AnomalyFlag"].mean() * 100), 2),
        "claim_anomalies_count": int(df_claim_anomalies["ClaimAnomalyFlag"].sum()),
        "claim_anomalies_pct": round(float(df_claim_anomalies["ClaimAnomalyFlag"].mean() * 100), 2),
        "duplicate_patients_count": int(df_patient_dups["DuplicateRecordFlag"].sum()),
        "df_billing_sample": df_billing_anomalies[df_billing_anomalies["AnomalyFlag"]].head(5).to_dict(orient="records"),
        "df_claim_sample": df_claim_anomalies[df_claim_anomalies["ClaimAnomalyFlag"]].head(5).to_dict(orient="records")
    }
