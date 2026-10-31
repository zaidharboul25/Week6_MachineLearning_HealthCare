"""
Classification Modeling Module for HealthConnect Rwanda.
Implements:
- Model 1: Hospital Admission / Acute Care Triage Prediction
- Model 2: Patient Satisfaction Classification (Low, Medium, High)
- Model 3: Insurance Claim Approval Classification (Approved vs Pending)
- Model 4: High-Risk Patient Stratification (High Risk vs Low Risk)
"""

from pathlib import Path
import logging
from typing import Dict, Any, List, Tuple
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from healthconnect.config import ARTIFACTS_DIR, RANDOM_SEED

logger = logging.getLogger(__name__)

def evaluate_classifier(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    is_multiclass: bool = False
) -> Dict[str, Any]:
    """Calculate comprehensive classification metrics."""
    y_pred = model.predict(X_test)
    y_proba = None
    roc_auc = np.nan
    try:
        y_proba = model.predict_proba(X_test)
        if is_multiclass:
            roc_auc = roc_auc_score(y_test, y_proba, multi_class="ovr", average="weighted")
        else:
            roc_auc = roc_auc_score(y_test, y_proba[:, 1])
    except Exception:
        pass

    avg_mode = "weighted" if is_multiclass else "binary"
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average=avg_mode, zero_division=0)
    rec = recall_score(y_test, y_pred, average=avg_mode, zero_division=0)
    f1 = f1_score(y_test, y_pred, average=avg_mode, zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()

    return {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4) if not np.isnan(roc_auc) else "N/A",
        "confusion_matrix": cm,
        "y_pred": y_pred,
        "y_test": y_test.values
    }

def train_and_compare_classifiers(
    X: pd.DataFrame,
    y: pd.Series,
    numeric_features: List[str],
    categorical_features: List[str],
    task_name: str,
    is_multiclass: bool = False
) -> Tuple[Dict[str, Any], Any, str]:
    """
    Train, cross-validate, and compare candidate classification models.
    Returns:
        metrics_dict: metrics across algorithms
        best_pipeline: top fitted pipeline
        best_name: name of the best performing algorithm
    """
    logger.info(f"Starting classification comparison for: {task_name}")
    from sklearn.preprocessing import LabelEncoder
    label_encoder = None
    if is_multiclass or y.dtype == "object":
        label_encoder = LabelEncoder()
        y_encoded = pd.Series(label_encoder.fit_transform(y), index=y.index)
    else:
        y_encoded = y

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=RANDOM_SEED, stratify=y_encoded
    )

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_SEED),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=RANDOM_SEED),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=RANDOM_SEED, n_jobs=-1),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, max_depth=4, random_state=RANDOM_SEED),
        "XGBoost": XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=RANDOM_SEED, eval_metric="mlogloss" if is_multiclass else "logloss")
    }

    results = {}
    best_score = -1.0
    best_pipeline = None
    best_name = None

    for name, clf in models.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", clf)])
        pipe.fit(X_train, y_train)
        eval_metrics = evaluate_classifier(pipe, X_test, y_test, is_multiclass=is_multiclass)
        if label_encoder is not None:
            eval_metrics["classes"] = list(label_encoder.classes_)
        results[name] = eval_metrics
        logger.info(f"[{task_name}] {name} - Acc: {eval_metrics['accuracy']}, F1: {eval_metrics['f1']}, ROC-AUC: {eval_metrics['roc_auc']}")

        # Track best model by F1 score
        if eval_metrics["f1"] > best_score:
            best_score = eval_metrics["f1"]
            best_pipeline = pipe
            best_name = name

    return results, best_pipeline, best_name

def run_all_classification_experiments(
    df_billing_analytical: pd.DataFrame,
    df_claims_analytical: pd.DataFrame,
    df_satisfaction_analytical: pd.DataFrame,
    df_risk_analytical: pd.DataFrame
) -> Dict[str, Any]:
    """Execute all 4 classification experiments."""
    all_results = {}

    # -------------------------------------------------------------
    # MODEL 1: Admission / Acute Care Triage (IsEmergencyVisit)
    # -------------------------------------------------------------
    m1_target = "IsEmergencyVisit"
    m1_features = [
        "Age", "BMI", "DoctorExperience", "FacilityApptVolume", "PatientToDoctorRatio",
        "Gender", "MaritalStatus", "Occupation", "Education", "InsuranceID",
        "ChronicCondition", "Severity", "DepartmentName", "ProvinceName"
    ]
    m1_num = ["Age", "BMI", "DoctorExperience", "FacilityApptVolume", "PatientToDoctorRatio"]
    m1_cat = ["Gender", "MaritalStatus", "Occupation", "Education", "InsuranceID",
              "ChronicCondition", "Severity", "DepartmentName", "ProvinceName"]
    
    X1 = df_billing_analytical[m1_features]
    y1 = df_billing_analytical[m1_target]
    m1_res, m1_pipe, m1_best = train_and_compare_classifiers(
        X1, y1, m1_num, m1_cat, task_name="Model 1: Admission Triage", is_multiclass=False
    )
    joblib.dump(m1_pipe, ARTIFACTS_DIR / "admission_triage_classifier.joblib")
    all_results["Model 1: Admission Triage"] = {
        "results": m1_res, "best_model": m1_best, "target": m1_target
    }

    # -------------------------------------------------------------
    # MODEL 2: Patient Satisfaction (SatisfactionClass: Low, Med, High)
    # -------------------------------------------------------------
    m2_target = "SatisfactionClass"
    m2_num = ["Age", "BMI", "Amount", "DoctorExperience", "PatientToDoctorRatio", "DepartmentWorkload"]
    m2_cat = ["VisitType", "Severity", "Diagnosis", "Gender", "InsuranceID", "DepartmentName"]
    X2 = df_satisfaction_analytical[m2_num + m2_cat]
    y2 = df_satisfaction_analytical[m2_target]
    
    # Encode target to numeric for XGBoost compatibility if needed, or string for sklearn
    m2_res, m2_pipe, m2_best = train_and_compare_classifiers(
        X2, y2, m2_num, m2_cat, task_name="Model 2: Patient Satisfaction", is_multiclass=True
    )
    joblib.dump(m2_pipe, ARTIFACTS_DIR / "satisfaction_classifier.joblib")
    all_results["Model 2: Patient Satisfaction"] = {
        "results": m2_res, "best_model": m2_best, "target": m2_target
    }

    # -------------------------------------------------------------
    # MODEL 3: Insurance Claim Status (TargetStatus: Approved vs Pending)
    # -------------------------------------------------------------
    m3_target = "TargetStatus"
    m3_num = ["ClaimAmount", "BillingAmount", "ClaimToBillingRatio", "ClaimDiff", "IsFullClaim"]
    m3_cat = ["Provider"]
    X3 = df_claims_analytical[m3_num + m3_cat]
    y3 = df_claims_analytical[m3_target]
    
    m3_res, m3_pipe, m3_best = train_and_compare_classifiers(
        X3, y3, m3_num, m3_cat, task_name="Model 3: Insurance Claim Status", is_multiclass=False
    )
    joblib.dump(m3_pipe, ARTIFACTS_DIR / "claims_classifier.joblib")
    all_results["Model 3: Insurance Claim Status"] = {
        "results": m3_res, "best_model": m3_best, "target": m3_target
    }

    # -------------------------------------------------------------
    # MODEL 4: High-Risk Patient Stratification (HighRiskTarget)
    # -------------------------------------------------------------
    m4_target = "HighRiskTarget"
    m4_num = ["Age", "BMI", "HistoricalApptCount", "TotalBilledAmount"]
    m4_cat = ["Gender", "MaritalStatus", "Occupation", "Education", "InsuranceID", "ChronicCondition", "BloodGroup"]
    X4 = df_risk_analytical[m4_num + m4_cat]
    y4 = df_risk_analytical[m4_target]
    
    m4_res, m4_pipe, m4_best = train_and_compare_classifiers(
        X4, y4, m4_num, m4_cat, task_name="Model 4: High-Risk Patient Stratification", is_multiclass=False
    )
    joblib.dump(m4_pipe, ARTIFACTS_DIR / "risk_classifier.joblib")
    all_results["Model 4: High-Risk Patient Stratification"] = {
        "results": m4_res, "best_model": m4_best, "target": m4_target
    }

    return all_results
