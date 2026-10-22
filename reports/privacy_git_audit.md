# HealthConnect Rwanda — Privacy, PII & Version Control Security Audit

**Auditor:** Independent Technical Audit Team  
**Developer:** Zaid Harboul  
**Project:** HealthConnect Rwanda — Week 6 Machine Learning Engineering  
**Date:** October 2026  
**Audit Standard:** Healthcare Data Minimization & Technical Governance Guidelines (Rwanda Law No. 058/2021)

---

## 1. Executive Summary & Security Verdict

| Audit Domain | Assessment Criteria | Verified Finding | Status |
| :--- | :--- | :--- | :--- |
| **Raw Healthcare Data** | No raw patient or hospital CSVs tracked in Git | `data/raw/` and `datasets/` excluded via `.gitignore` | **PASS** |
| **Processed Healthcare Data** | No analytical patient datasets tracked in Git | `data/processed/` excluded via `.gitignore` | **PASS** |
| **Model Binaries & Weights** | No serialized `.joblib` / `.pkl` models tracked in Git | `artifacts/*.joblib` excluded via `.gitignore` | **PASS** |
| **Secrets & Credentials** | No `.env`, API keys, or database credentials tracked | Only `.env.example` template tracked | **PASS** |
| **Data Dictionary Sanitization**| No sample PII values exposed in tracked documentation | Initial sample phone numbers & names sanitized to `[REDACTED_PII]` | **PASS** |
| **Remote Git Safety** | No unauthorized push to remote GitHub repositories | Checked `git remote -v`: No unauthorized remote configured | **PASS** |
| **Legal Compliance Claims** | Verification of claims regarding Rwanda Law No. 058/2021 | Technical safeguards verified; formal legal certification unverified | **MEDIUM** |

---

## 2. Git Tracking & Exclusion Verification

A comprehensive inspection of the Git index (`git ls-files`) was conducted against the repository root.

### 2.1 Tracked Files Breakdown (75 files total)
- **Configuration & Build (6 files)**: `.gitignore`, `.env.example`, `pyproject.toml`, `requirements.txt`, `LICENSE`, `README.md`.
- **Source Modules (18 files)**: `src/healthconnect/` package (config, data audit, cleaner, feature engineering, classification, regression, clustering, anomaly, XAI, plotting).
- **Notebooks (7 files)**: `notebooks/01_*.ipynb` through `07_*.ipynb`.
- **Deployment Assets (4 files)**: `deployment/app.py`, `deployment/architecture.md`, `deployment/architecture_diagram.mmd`, `deployment/Dockerfile`.
- **Unit & Integration Tests (5 files)**: `tests/` (`test_api.py`, `test_data.py`, `test_features.py`, `test_models.py`, `__init__.py`).
- **Pipeline Scripts (8 files)**: `scripts/` (`audit_data.py`, `prepare_data.py`, `train_models.py`, `evaluate_models.py`, `generate_reports.py`, `validate_deliverables.py`, `generate_notebooks.py`, `run_pipeline.py`).
- **Reports & Visualizations (27 files)**: Markdown reports, metrics JSON, high-resolution figures in `reports/figures/`, and sanitized metadata CSVs.

### 2.2 Excluded Files Verification
```bash
git status --ignored -s
```
- `!! data/raw/` (Contains all 27 raw healthcare CSV files) — **CONFIRMED EXCLUDED**
- `!! data/processed/` (Contains all 6 processed analytical datasets) — **CONFIRMED EXCLUDED**
- `!! datasets/` (Original source data archive) — **CONFIRMED EXCLUDED**
- `!! artifacts/*.joblib` (7 serialized model pipeline binaries) — **CONFIRMED EXCLUDED**
- `!! .pytest_cache/`, `!! __pycache__/` — **CONFIRMED EXCLUDED**

---

## 3. Personally Identifiable Information (PII) Audit & Remediation

### 3.1 PII Inventory in Raw Datasets
The following sensitive columns were identified in `HC_Patients.csv`:
- `FirstName`, `LastName`: Direct patient names.
- `DateOfBirth`: Precise date of birth.
- `Phone`: Personal mobile phone numbers (e.g., `250788000000.0`).
- `EmergencyContact`: Contact names.

In staff tables (`HC_Doctor.csv`, `HC_Nurse.csv`, `HC_Administrative_Staff.csv`):
- `FirstName`, `LastName`: Direct employee names.

### 3.2 Audit Finding on Tracked Metadata (Remediated)
- **Initial Finding**: `reports/data_dictionary.csv` originally extracted the first 3 distinct values of each column for documentation purposes. For columns flagged as `is_pii == True`, this resulted in sample names (e.g. `Patrick`, `Emmanuel`), birthdates (`1/1/2007`), and phone numbers appearing in the tracked CSV.
- **Severity**: **HIGH**.
- **Remediation Implemented**:
  `src/healthconnect/data/audit.py` was updated with a privacy filter:
  ```python
  if is_pii:
      samples_str = "[REDACTED_PII]"
  ```
  The data audit was re-executed. All 27 PII columns in `reports/data_dictionary.csv` now display `[REDACTED_PII]`. No individual patient or employee identifiers exist in tracked repository files.

---

## 4. Legal Compliance Claim Clarification

- **Claim in Project Reports**: *"In strict compliance with Rwanda Law No. 058/2021 relating to the protection of personal data and privacy..."*
- **Audit Assessment**:
  1. *Technical Safeguards*: The project adheres to core data minimization, de-identification, and security principles (excluding raw records, hashing/dropping direct IDs, non-root Docker execution, and role-based access architecture).
  2. *Regulatory Disclaimer*: Under academic and technical auditing guidelines, claims of formal legal compliance cannot be certified by automated code inspection alone. Full legal compliance requires formal Data Protection Officer (DPO) registration, institutional ethics review board (IRB) approval, and regulatory licensing by the National Cyber Security Authority (NCSA) of Rwanda.
- **Recommendation**:
  Qualify all compliance statements in project reports to indicate that technical architectural safeguards are implemented in alignment with statutory principles, pending formal regulatory review.

---

## 5. Remote Repository Audit

- **Check**: Checked `git remote -v`.
- **Result**: No remote tracking URL is configured.
- **Verification**: The repository exists purely on the local Windows 11 development machine. No code, metadata, or models have been pushed to any public or private remote repository without user authorization.
