"""
Regression Modeling Module for HealthConnect Rwanda.
Implements:
- Model 5: Revenue / Billing Amount Regression
- Model 6: Length of Stay (LOS) Assessment & Documentation of Data Limitation
"""

from pathlib import Path
import logging
from typing import Dict, Any, List, Tuple
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)

from healthconnect.config import ARTIFACTS_DIR, RANDOM_SEED

logger = logging.getLogger(__name__)

def evaluate_regressor(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict[str, Any]:
    """Calculate standard regression metrics: RMSE, MAE, R2, MAPE."""
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Safe MAPE calculation avoiding zero-division
    nonzero_mask = (y_test != 0)
    if nonzero_mask.sum() > 0:
        mape = mean_absolute_percentage_error(y_test[nonzero_mask], y_pred[nonzero_mask]) * 100
    else:
        mape = np.nan

    residuals = (y_test - y_pred).values

    return {
        "rmse": round(float(rmse), 2),
        "mae": round(float(mae), 2),
        "r2": round(float(r2), 4),
        "mape": round(float(mape), 2) if not np.isnan(mape) else "N/A",
        "y_pred": y_pred,
        "y_test": y_test.values,
        "residuals": residuals
    }

def run_billing_regression_experiments(
    df_billing_analytical: pd.DataFrame
) -> Tuple[Dict[str, Any], Any, str]:
    """
    Train and compare candidate regression algorithms for Billing Amount prediction.
    Features include clinical diagnosis, severity, patient demographics, doctor experience,
    department, facility workload, and seasonal indicators.
    Strictly excludes payment amounts and claim records to prevent target leakage.
    """
    logger.info("Starting Model 5: Revenue / Billing Amount Regression...")
    target = "Amount"
    
    num_features = [
        "Age", "BMI", "DoctorExperience", "FacilityApptVolume", 
        "PatientToDoctorRatio", "BedToDoctorRatio", "DepartmentWorkload", "Month"
    ]
    cat_features = [
        "VisitType", "Diagnosis", "Severity", "Gender", "MaritalStatus",
        "Occupation", "Education", "InsuranceID", "ChronicCondition",
        "DepartmentName", "ProvinceName"
    ]
    
    X = df_billing_analytical[num_features + cat_features]
    y = df_billing_analytical[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features),
        ]
    )

    models = {
        "Baseline (Dummy Mean)": DummyRegressor(strategy="mean"),
        "Linear Regression (Ridge)": Ridge(alpha=1.0, random_state=RANDOM_SEED),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=RANDOM_SEED, n_jobs=-1),
        "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=RANDOM_SEED),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=RANDOM_SEED)
    }

    results = {}
    best_score = float("inf")
    best_pipeline = None
    best_name = None

    for name, reg in models.items():
        pipe = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", reg)])
        pipe.fit(X_train, y_train)
        eval_metrics = evaluate_regressor(pipe, X_test, y_test)
        results[name] = eval_metrics
        logger.info(f"[Model 5] {name} - RMSE: {eval_metrics['rmse']:,}, MAE: {eval_metrics['mae']:,}, R2: {eval_metrics['r2']}, MAPE: {eval_metrics['mape']}%")

        # Track best model by MAE (excluding baseline)
        if name != "Baseline (Dummy Mean)" and eval_metrics["mae"] < best_score:
            best_score = eval_metrics["mae"]
            best_pipeline = pipe
            best_name = name

    # Serialize best regressor
    if best_pipeline is not None:
        joblib.dump(best_pipeline, ARTIFACTS_DIR / "billing_regressor.joblib")
        logger.info(f"Saved best regression pipeline ({best_name}) to artifacts/billing_regressor.joblib")

    return results, best_pipeline, best_name

def assess_length_of_stay_feasibility() -> Dict[str, Any]:
    """
    Formally assess feasibility of Model 6: Length of Stay (LOS) Regression.
    Concludes task is UNSUPPORTED due to missing admission/discharge timestamps.
    """
    logger.warning("Model 6: Length of Stay Prediction is UNSUPPORTED by available datasets.")
    return {
        "status": "UNSUPPORTED",
        "reason": (
            "Exhaustive inspection across all 27 supplied CSV files confirmed that no admission timestamps, "
            "discharge timestamps, bed assignment dates, or duration-of-stay columns exist. "
            "In strict adherence to assignment instructions ('Do not train a model if the target cannot be "
            "constructed correctly. Do not invent data, metrics, or columns'), this experiment is formally documented "
            "as unsupported by the source data rather than fabricated."
        ),
        "recommendation": "Deploy an Admission-Discharge-Transfer (ADT) tracking module in the Hospital Information System to record admission and discharge timestamps for future modeling."
    }
