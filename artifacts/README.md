# HealthConnect Rwanda Model & Pipeline Artifacts

This directory stores trained scikit-learn pipelines, model configurations, feature metadata, and encoders.

## Storage Governance & Privacy
- **Zero Patient Data Leakage**: Serialized pipeline artifacts contain only mathematical weights, transformation schemas, and feature metadata. No raw patient records or PII are embedded within serialized models.
- Model artifacts are tracked locally and excluded from public version control via `.gitignore`.
- Trained artifacts include:
  - `billing_regressor.joblib`: Revenue/Billing amount prediction model.
  - `claims_classifier.joblib`: Insurance claim approval classification model.
  - `satisfaction_classifier.joblib`: Patient satisfaction tier classification model.
  - `risk_classifier.joblib`: Patient clinical risk stratification model.
  - `facility_clusterer.joblib`: Facility operational segmentation model.
  - `patient_clusterer.joblib`: Patient clinical and utilization clustering model.
  - `anomaly_detector.joblib`: Isolation Forest multi-faceted anomaly detection model.
