# HealthConnect Rwanda — Executive Presentation Deck Outline
## Healthcare Analytics & AI Transformation | Machine Learning Engineering
**Presenter:** Zaid Harboul (Senior Machine Learning Engineer)  
**Program:** AnalystLab Africa — Week 6  
**Structure:** 15 Slides  

---

### Slide 1: Title & Executive Introduction
- **Title**: HealthConnect Rwanda — Enterprise Healthcare Analytics & AI Transformation
- **Subtitle**: Machine Learning Engineering Lifecycle, Operational Optimization & Decision Support
- **Lead Engineer**: Zaid Harboul
- **Context**: AnalystLab Africa Experience Lab (Week 6)

### Slide 2: The Healthcare Challenge in Rwanda
- **Context**: Rapid expansion of universal healthcare coverage and electronic clinical records.
- **Challenges**: Facility workload bottlenecks, administrative delays in insurance claim settlements, multimorbid chronic disease burden, and billing discrepancies.
- **Objective**: Build an enterprise machine learning system to transform raw transactions into actionable clinical and operational intelligence.

### Slide 3: Relational Data Foundation
- **27 Connected Enterprise Datasets**: Demographics, infrastructure, staffing, clinical transactions, billing, insurance claims, and patient feedback.
- **Relational Integrity**: 100% key uniqueness across primary identifiers; verified zero orphan records across the geographical, clinical, and financial relational chain.
- **Data Governance**: Strict anonymization and PII isolation complying with Rwanda Law No. 058/2021.

### Slide 4: Data Quality Audit & Schema Resolutions
- **Identical Schema Detection**: Identified that `HC_Departments.csv` and `HC_Facility_Master_Data.xlsx - Departments.csv` were 100% identical duplicates.
- **Missingness Strategy**: Resolved 25.35% missingness in patient chronic conditions by imputing explicit `'None'` category rather than row deletion.
- **Data Boundaries**: Verified absence of admission/discharge timestamps; documented Length of Stay as unsupported by available data.

### Slide 5: Data Integration & Leakage Prevention
- **Encounter-Level Integration**: Joined 5,000 clinical encounters to patient demographics, facility capacity, doctor experience, and diagnosis.
- **Strict Leakage Safeguards**: Excluded post-settlement payment methods and simultaneous feedback text comments from predictive features.
- **Modular Pipeline**: Packaged end-to-end cleaning and feature engineering in reusable Python modules.

### Slide 6: Feature Engineering Innovation
- **Clinical & Demographic**: Age groups, WHO BMI categories, chronic condition flags.
- **Operational Strain**: Patient-to-Doctor ratio, Department Workload, Facility Annual Encounter Volume.
- **Financial Ratios**: Claim-to-Billing ratio, billing differential, full claim indicator.
- **Temporal Signals**: Month, Quarter, Day of Week, Weekend indicator.

### Slide 7: Supervised Classification: Insurance Claim Adjudication (Model 3)
- **Problem**: Classify insurance claims into `Approved` vs `Pending` to accelerate reimbursement.
- **Results**: Compared Logistic Regression, Decision Trees, Random Forest, Gradient Boosting, and XGBoost across 42,036 claims.
- **Impact**: Enables automated clearance for consistent claims, routing ratio discrepancies to human reviewers.

### Slide 8: Supervised Classification: High-Risk Patient Stratification (Model 4)
- **Problem**: Proactively identify patients with severe chronic multimorbidity.
- **Results**: Achieved 95.6% accuracy and 0.994 ROC-AUC using tree-based classifiers.
- **Clinical Application**: Supports community health outreach and chronic disease management programs.

### Slide 9: Supervised Classification: Admission Triage & Patient Satisfaction (Models 1 & 2)
- **Admission Triage**: Modeled acute emergency encounter needs vs routine consultation.
- **Patient Satisfaction**: Classifies satisfaction into Low, Medium, High tiers, linking dissatisfaction to department workload and waiting proxies.

### Slide 10: Supervised Regression: Hospital Revenue & Billing Forecasting (Model 5)
- **Problem**: Forecast encounter medical billing charges (RWF) based on clinical severity and demographics.
- **Algorithms**: Evaluated Dummy Mean Baseline, Linear Ridge, Random Forest, Gradient Boosting, and XGBoost.
- **Key Metric**: Random Forest achieved lower error than mean baseline, providing dynamic hospital financial planning estimates.

### Slide 11: Unsupervised Intelligence: Patient & Facility Segmentation
- **Patient Segmentation**: K-Means clustering (k=3) revealed three clinical personas: *Young Preventive Outpatients*, *Multimorbid Seniors*, and *Working-Age Adults*.
- **Facility Operational Tiers**: 2D PCA projection segmented 20 hospitals into Referral Centers, District Hospitals, and Primary Clinics for regional resource allocation.

### Slide 12: Anomaly Detection: Financial Fraud & Identity Duplicate Safeguards
- **Billing Anomalies**: Flagged high-cost outliers (> 1.5x IQR) for itemized clinical charge audits.
- **Insurance Claim Mismatches**: Flagged claims where requested reimbursement exceeded hospital invoiced charges.
- **Identity Duplication**: Detected demographic collisions sharing phone numbers for master patient index deduplication.

### Slide 13: Explainable AI (XAI) & Model Transparency
- **SHAP Summary Plots**: Global feature importance and local waterfall breakdowns for claims and revenue models.
- **Top Drivers**: Identified `ClaimToBillingRatio`, `BillingAmount`, `Provider`, and `Patient Age` as primary model drivers.
- **Medical Caveat**: Explicitly communicated that statistical importance does not imply clinical causation.

### Slide 14: Production Deployment Architecture & API
- **FastAPI Microservice**: Type-safe REST endpoints (`/health`, `/predict/claims`, `/predict/billing`) with sub-25ms latency.
- **Docker Hardening**: Containerized with unprivileged non-root security.
- **End-to-End Architecture**: 10-layer enterprise architecture integrating EHR, Kafka, Feast, MLflow, and Prometheus drift monitoring.

### Slide 15: Strategic Recommendations & Conclusion
- **Operationalize Claims Pre-Adjudication**: Integrate API with Rwanda Social Security Board (RSSB) to cut adjudication cycles.
- **Implement ADT Inpatient Tracking**: Upgrade OpenMRS to log admission/discharge timestamps for true Length-of-Stay modeling.
- **Responsible Governance**: Maintain mandatory licensed clinician oversight for all predictive decision-support outputs.
