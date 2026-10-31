"""
HealthConnect Rwanda — Production Machine Learning Inference API.
Built with FastAPI and Pydantic for high-throughput, secure, type-safe model serving.

Endpoints:
- GET  /health: System operational health check and model loading status.
- POST /predict/claims: Predict insurance claim approval status.
- POST /predict/billing: Predict anticipated healthcare encounter billing amount.
- POST /predict/satisfaction: Predict patient experience satisfaction tier.

Compliance Notice:
This API is an analytical decision-support prototype. It does NOT make autonomous
clinical decisions or expose identifiable patient health records (PII).
"""

from pathlib import Path
import logging
from typing import Dict, Any, List, Optional
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("healthconnect-api")

# Directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
from contextlib import asynccontextmanager

ARTIFACTS_DIR = BASE_DIR / "artifacts"

# Global model store
models: Dict[str, Any] = {}

def load_models():
    """Load serialized model pipelines on server startup."""
    logger.info("Initializing HealthConnect model pipelines...")
    try:
        claims_path = ARTIFACTS_DIR / "claims_classifier.joblib"
        if claims_path.exists():
            models["claims"] = joblib.load(claims_path)
            logger.info("Loaded claims_classifier.joblib")

        billing_path = ARTIFACTS_DIR / "billing_regressor.joblib"
        if billing_path.exists():
            models["billing"] = joblib.load(billing_path)
            logger.info("Loaded billing_regressor.joblib")

        sat_path = ARTIFACTS_DIR / "satisfaction_classifier.joblib"
        if sat_path.exists():
            models["satisfaction"] = joblib.load(sat_path)
            logger.info("Loaded satisfaction_classifier.joblib")

        triage_path = ARTIFACTS_DIR / "admission_triage_classifier.joblib"
        if triage_path.exists():
            models["triage"] = joblib.load(triage_path)
            logger.info("Loaded admission_triage_classifier.joblib")

    except Exception as e:
        logger.error(f"Error loading models: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_models()
    yield

# Initialize FastAPI application
app = FastAPI(
    title="HealthConnect Rwanda ML Inference Service",
    description="Enterprise Machine Learning Serving Layer for Healthcare Analytics & Decision Support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ----------------------------------------------------------------------
# Pydantic Schemas for Input Validation & Serialization
# ----------------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: List[str]
    environment: str

class ClaimsPredictionRequest(BaseModel):
    Provider: str = Field(..., description="Insurance provider (RSSB, Radiant, MMI, Private)")
    ClaimAmount: float = Field(..., gt=0, description="Requested reimbursement amount in RWF")
    BillingAmount: float = Field(..., gt=0, description="Total hospital invoiced billing amount in RWF")

class ClaimsPredictionResponse(BaseModel):
    prediction_label: str
    prediction_code: int
    probability_approved: float
    recommendation: str

class BillingPredictionRequest(BaseModel):
    Age: int = Field(..., ge=0, le=120)
    BMI: float = Field(..., ge=10.0, le=60.0)
    DoctorExperience: int = Field(..., ge=0, le=50)
    FacilityApptVolume: int = Field(..., ge=0)
    PatientToDoctorRatio: float = Field(..., ge=0)
    BedToDoctorRatio: float = Field(..., ge=0)
    DepartmentWorkload: int = Field(..., ge=0)
    Month: int = Field(..., ge=1, le=12)
    VisitType: str = Field(...)
    Diagnosis: str = Field(...)
    Severity: str = Field(...)
    Gender: str = Field(...)
    MaritalStatus: str = Field(...)
    Occupation: str = Field(...)
    Education: str = Field(...)
    InsuranceID: str = Field(...)
    ChronicCondition: str = Field(...)
    DepartmentName: str = Field(...)
    ProvinceName: str = Field(...)

class BillingPredictionResponse(BaseModel):
    predicted_billing_amount_rwf: float
    confidence_interval_lower_rwf: float
    confidence_interval_upper_rwf: float
    notes: str

class TriagePredictionRequest(BaseModel):
    Age: int = Field(..., ge=0, le=120)
    BMI: float = Field(..., ge=10.0, le=70.0)
    DoctorExperience: int = Field(..., ge=0, le=50)
    FacilityApptVolume: int = Field(..., ge=0)
    PatientToDoctorRatio: float = Field(..., ge=0)
    Gender: str = Field(...)
    MaritalStatus: str = Field(...)
    Occupation: str = Field(...)
    Education: str = Field(...)
    InsuranceID: str = Field(...)
    ChronicCondition: str = Field(...)
    Severity: str = Field(...)
    DepartmentName: str = Field(...)
    ProvinceName: str = Field(...)

class TriagePredictionResponse(BaseModel):
    prediction_label: str
    is_emergency: int
    probability_emergency: Optional[float]
    recommendation: str

class SatisfactionPredictionRequest(BaseModel):
    Age: int = Field(..., ge=0, le=120)
    BMI: float = Field(..., ge=10.0, le=70.0)
    Amount: float = Field(..., ge=0)
    DoctorExperience: int = Field(..., ge=0, le=50)
    PatientToDoctorRatio: float = Field(..., ge=0)
    DepartmentWorkload: int = Field(..., ge=0)
    VisitType: str = Field(...)
    Severity: str = Field(...)
    Diagnosis: str = Field(...)
    Gender: str = Field(...)
    InsuranceID: str = Field(...)
    DepartmentName: str = Field(...)

class SatisfactionPredictionResponse(BaseModel):
    predicted_satisfaction_tier: str
    predicted_code: int
    recommendation: str

# ----------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
def health_check():
    """Service health and model readiness probe."""
    return HealthResponse(
        status="Healthy",
        version="1.0.0",
        models_loaded=list(models.keys()),
        environment="Production (Rwanda-MOH Analytics Layer)"
    )

@app.post("/predict/claims", response_model=ClaimsPredictionResponse)
def predict_claim_approval(req: ClaimsPredictionRequest):
    """Predict whether an incoming insurance claim will be Approved or Pending."""
    if "claims" not in models:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Claims model unavailable")

    # Compute engineered features
    ratio = round(req.ClaimAmount / max(req.BillingAmount, 1.0), 4)
    diff = round(req.BillingAmount - req.ClaimAmount, 2)
    is_full = int(req.ClaimAmount >= req.BillingAmount)

    input_df = pd.DataFrame([{
        "ClaimAmount": req.ClaimAmount,
        "BillingAmount": req.BillingAmount,
        "ClaimToBillingRatio": ratio,
        "ClaimDiff": diff,
        "IsFullClaim": is_full,
        "Provider": req.Provider
    }])

    pipe = models["claims"]
    pred = int(pipe.predict(input_df)[0])
    proba = float(pipe.predict_proba(input_df)[0][1])

    label = "Approved" if pred == 1 else "Pending"
    rec = "Proceed with automated payment clearance" if pred == 1 else "Route to manual claim verification queue"

    return ClaimsPredictionResponse(
        prediction_label=label,
        prediction_code=pred,
        probability_approved=round(proba, 4),
        recommendation=rec
    )

@app.post("/predict/billing", response_model=BillingPredictionResponse)
def predict_encounter_billing(req: BillingPredictionRequest):
    """Predict expected clinical billing charge for an encounter."""
    if "billing" not in models:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Billing model unavailable")

    input_dict = req.model_dump()
    input_df = pd.DataFrame([input_dict])

    pipe = models["billing"]
    pred = float(pipe.predict(input_df)[0])
    pred = max(0.0, round(pred, 2))

    # 95% Confidence interval based on test RMSE (~82,993 RWF)
    rmse = 82993.0
    lower = max(0.0, round(pred - 1.96 * rmse, 2))
    upper = round(pred + 1.96 * rmse, 2)

    return BillingPredictionResponse(
        predicted_billing_amount_rwf=pred,
        confidence_interval_lower_rwf=lower,
        confidence_interval_upper_rwf=upper,
        notes="Forecasted total encounter cost before insurance co-pay application."
    )

@app.post("/predict/triage", response_model=TriagePredictionResponse)
def predict_admission_triage(req: TriagePredictionRequest):
    """Predict acute care triage status (Emergency vs Routine encounter)."""
    if "triage" not in models:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Triage model unavailable")

    input_df = pd.DataFrame([req.model_dump()])
    pipe = models["triage"]
    pred = int(pipe.predict(input_df)[0])
    
    proba = None
    if hasattr(pipe, "predict_proba"):
        try:
            proba = round(float(pipe.predict_proba(input_df)[0][1]), 4)
        except Exception:
            proba = None

    label = "Emergency" if pred == 1 else "Routine"
    rec = "Expedite to acute clinical resuscitation bay" if pred == 1 else "Direct to outpatient standard consultation queue"

    return TriagePredictionResponse(
        prediction_label=label,
        is_emergency=pred,
        probability_emergency=proba,
        recommendation=rec
    )

@app.post("/predict/satisfaction", response_model=SatisfactionPredictionResponse)
def predict_patient_satisfaction(req: SatisfactionPredictionRequest):
    """Predict patient satisfaction tier (Low, Medium, High)."""
    if "satisfaction" not in models:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Satisfaction model unavailable")

    input_df = pd.DataFrame([req.model_dump()])
    pipe = models["satisfaction"]
    pred = pipe.predict(input_df)[0]
    
    tier_map = {0: "Low", 1: "Medium", 2: "High"}
    if isinstance(pred, (int, np.integer)):
        tier_label = tier_map.get(int(pred), str(pred))
        code = int(pred)
    else:
        tier_label = str(pred)
        code = 1

    rec = "Engage patient advocacy liaison for experience follow-up" if tier_label == "Low" else "Standard discharge communication protocol"

    return SatisfactionPredictionResponse(
        predicted_satisfaction_tier=tier_label,
        predicted_code=code,
        recommendation=rec
    )
