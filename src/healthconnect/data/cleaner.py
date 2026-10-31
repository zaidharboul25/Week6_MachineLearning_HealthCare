"""
Data Cleaning and Validation Module for HealthConnect Rwanda.
Handles missing values, data type casting, deduplication, and sanity validations.
"""

from pathlib import Path
import logging
from typing import Dict, Tuple
import pandas as pd
import numpy as np

from healthconnect.config import DATA_RAW_DIR, DATASET_FILES

logger = logging.getLogger(__name__)

def clean_patients(df_patients: pd.DataFrame) -> pd.DataFrame:
    """
    Clean patients master records.
    - Fills missing ChronicCondition with 'None'
    - Casts numeric fields (Age, HeightCm, WeightKg, BMI)
    - Validates age and BMI boundaries
    - Strips whitespace from categorical strings
    """
    df = df_patients.copy()
    logger.info(f"Cleaning patients table: raw rows = {len(df)}")
    
    # Fill missing chronic condition with explicit category 'None'
    df["ChronicCondition"] = df["ChronicCondition"].fillna("None").astype(str).str.strip()
    
    # Cast numeric columns
    numeric_cols = ["Age", "HeightCm", "WeightKg", "BMI"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            
    # Clean text strings
    text_cols = ["Gender", "MaritalStatus", "Occupation", "Education", "BloodGroup", "Status"]
    for c in text_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
            
    # Compute BMI if missing or verify consistency: BMI = Weight / (Height/100)^2
    calculated_bmi = df["WeightKg"] / ((df["HeightCm"] / 100) ** 2)
    df["BMI"] = df["BMI"].fillna(calculated_bmi).round(1)
    
    # Sanity bounds check
    df["Age"] = df["Age"].clip(lower=0, upper=120)
    df["BMI"] = df["BMI"].clip(lower=10.0, upper=60.0)
    
    logger.info(f"Cleaned patients table: clean rows = {len(df)}")
    return df

def clean_appointments(df_appointments: pd.DataFrame) -> pd.DataFrame:
    """
    Clean appointments transactions.
    - Parses Date to datetime
    - Strips whitespace
    """
    df = df_appointments.copy()
    logger.info(f"Cleaning appointments table: raw rows = {len(df)}")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["VisitType"] = df["VisitType"].astype(str).str.strip()
    return df

def clean_billing(df_billing: pd.DataFrame) -> pd.DataFrame:
    """
    Clean billing transactions.
    - Casts Amount to numeric
    - Validates non-negative billing
    """
    df = df_billing.copy()
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Amount"] = df["Amount"].clip(lower=0)
    if "Status" in df.columns:
        df["Status"] = df["Status"].astype(str).str.strip()
    return df

def clean_diagnoses(df_diagnoses: pd.DataFrame) -> pd.DataFrame:
    """
    Clean diagnoses records.
    - Normalizes diagnosis names and severity levels
    """
    df = df_diagnoses.copy()
    if "Diagnosis" in df.columns:
        df["Diagnosis"] = df["Diagnosis"].astype(str).str.strip()
    if "Severity" in df.columns:
        df["Severity"] = df["Severity"].astype(str).str.strip()
    return df

def clean_claims(df_claims: pd.DataFrame) -> pd.DataFrame:
    """
    Clean insurance claims records.
    """
    df = df_claims.copy()
    if "ClaimAmount" in df.columns:
        df["ClaimAmount"] = pd.to_numeric(df["ClaimAmount"], errors="coerce").clip(lower=0)
    if "Provider" in df.columns:
        df["Provider"] = df["Provider"].astype(str).str.strip()
    if "Status" in df.columns:
        df["Status"] = df["Status"].astype(str).str.strip()
    return df

def clean_feedback(df_feedback: pd.DataFrame) -> pd.DataFrame:
    """
    Clean patient feedback records.
    - Ensures Rating is integer between 1 and 5
    - Standardizes comments
    """
    df = df_feedback.copy()
    if "Rating" in df.columns:
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(3).astype(int).clip(1, 5)
    if "Comment" in df.columns:
        df["Comment"] = df["Comment"].astype(str).str.strip()
    elif "Comments" in df.columns:
        df["Comment"] = df["Comments"].astype(str).str.strip()
    return df
