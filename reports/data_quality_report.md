# HealthConnect Rwanda — Data Quality Audit Report

**Author:** Zaid Harboul  
**Role:** Senior Machine Learning Engineer  
**Project:** HealthConnect Rwanda — Healthcare Analytics & Artificial Intelligence Transformation  
**Program:** AnalystLab Africa — Week 6  
**Environment:** Windows 11 | Python 3.12 | scikit-learn 1.8.0  

---

## 1. Executive Summary & Inventory Overview

The HealthConnect Rwanda relational database represents an enterprise healthcare ecosystem in Rwanda spanning clinical transactions, infrastructure, medical staffing, financial billing, insurance reimbursements, and patient satisfaction surveys.

An exhaustive automated audit of all **27 CSV files** in the dataset was conducted.

### Table Inventory Summary
| File Name | Rows | Columns | Size (Bytes) | Missing Pct (%) | Duplicate Rows | Candidate Primary Key |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `HC_Administrative_Staff.csv` | 80 | 10 | 8,106 | 0.0% | 0 | `StaffID` |
| `HC_Beds.csv` | 2,000 | 3 | 54,024 | 0.0% | 0 | `BedID` |
| `HC_Billing.csv` | 60,000 | 4 | 2,220,751 | 0.0% | 0 | `BillingID` |
| `HC_Clinical_Transactions.xlsx - Appointments.csv` | 5,000 | 7 | 310,039 | 0.0% | 0 | `AppointmentID` |
| `HC_Departments.csv` | 200 | 3 | 5,163 | 0.0% | 0 | `DepartmentID` |
| `HC_Diagnoses.csv` | 60,000 | 4 | 2,431,317 | 0.0% | 0 | `DiagnosisID` |
| `HC_Districts.csv` | 30 | 3 | 747 | 0.0% | 0 | `DistrictID` |
| `HC_Doctor.csv` | 350 | 10 | 27,479 | 0.0% | 0 | `StaffID` |
| `HC_Facility_Master_Data.xlsx - Departments.csv` | 200 | 3 | 5,158 | 0.0% | 0 | `DepartmentID` |
| `HC_Medical_Equipment.csv` | 200 | 4 | 8,571 | 0.0% | 0 | `EquipmentID` |
| `HC_Medical_Specialties.csv` | 200 | 3 | 5,479 | 0.0% | 0 | `SpecialtyID` |
| `HC_Nurse.csv` | 700 | 10 | 49,067 | 0.0% | 0 | `StaffID` |
| `HC_Ownership_Types.csv` | 4 | 2 | 93 | 0.0% | 0 | `OwnershipID` |
| `HC_Patient_Feedback.csv` | 21,064 | 4 | 610,386 | 0.0% | 0 | `FeedbackID` |
| `HC_Patients.csv` | 20,000 | 19 | 2,786,822 | 1.33% | 0 | `PatientID` |
| `HC_Payments.csv` | 60,000 | 4 | 2,151,757 | 0.0% | 0 | `PaymentID` |
| `HC_Provinces.csv` | 5 | 3 | 149 | 0.0% | 0 | `ProvinceID` |
| `HC_Radiographer.csv` | 30 | 10 | 2,611 | 0.0% | 0 | `StaffID` |
| `HC_Revenue_Summary.csv` | 12 | 3 | 310 | 0.0% | 0 | `None` |
| `HC_Rooms.csv` | 400 | 4 | 15,884 | 0.0% | 0 | `RoomID` |
| `HC_Sectors.csv` | 120 | 3 | 2,567 | 0.0% | 0 | `SectorID` |
| `HC_Services.csv` | 400 | 3 | 15,679 | 0.0% | 0 | `ServiceID` |
| `HC_Villages.csv` | 480 | 3 | 11,447 | 0.0% | 0 | `VillageID` |
| `HCCountries.csv` | 1 | 6 | 89 | 0.0% | 0 | `CountryID` |
| `Insurance_Claims.csv` | 42,036 | 5 | 1,899,268 | 0.0% | 0 | `ClaimID` |
| `Laboratory_Scientist.csv` | 40 | 10 | 4,094 | 0.0% | 0 | `StaffID` |
| `Pharmacist.csv` | 50 | 10 | 4,093 | 0.0% | 0 | `StaffID` |


---

## 2. Critical Findings & Schema Anomalies

### 2.1 Identical Schema & Duplicate Table Detection
- **`HC_Departments.csv` vs `HC_Facility_Master_Data.xlsx - Departments.csv`**:
  - The audit confirmed that these two files are **100% byte-for-byte identical in row counts (200 rows, 3 columns) and content**.
  - **Resolution**: `HC_Departments.csv` is maintained as the primary canonical department registry. `HC_Facility_Master_Data.xlsx - Departments.csv` is classified as an export duplicate.

### 2.2 Appointment Horizon & Transactional Coverage
- `HC_Clinical_Transactions.xlsx - Appointments.csv` contains **5,000 appointment encounters** spanning `APT000001` through `APT005000`.
- Meanwhile, `HC_Billing.csv` and `HC_Diagnoses.csv` contain **60,000 transactions** (`APT000001` through `APT060000`), representing an expanded 12-month transaction log.
- `HC_Patient_Feedback.csv` covers **21,064 records** with appointment IDs up to `APT059999`.
- **Integration Rule**: Downstream analytical pipelines must perform controlled inner and left joins, explicitly documenting cohort sizes and preventing Cartesian record multiplication.

### 2.3 Target Variable Analysis & Availability
- **Patient Satisfaction**: `HC_Patient_Feedback.csv` provides `Rating` (1 to 5) and `Comment` ('Poor', 'Average', 'Good', 'Excellent'). Mapped to Low (1-2), Medium (3), and High (4-5) classes.
- **Insurance Claims**: `Insurance_Claims.csv` contains 42,036 claims. Classes observed: `Pending` (21,028) and `Approved` (21,008). **'Rejected' status is not present in raw data**, requiring documented binary classification.
- **Billing Amount**: `HC_Billing.csv` contains 60,000 continuous billing records (mean 155,157 RWF, std 83,840 RWF) with zero missingness.
- **Hospital Admissions & Length of Stay (LOS)**: No explicit admission registry, admission timestamp, or discharge timestamp exists in the 27 CSVs. Length of Stay modeling is documented as unsupported by available data. Acute/Emergency encounter triage is modeled using `VisitType == 'Emergency'` as a transparent proxy.

---

## 3. Missing Value Analysis & Treatment Decisions

| Table | Column | Null Count | Null % | Domain Interpretation & Strategy |
| :--- | :--- | :--- | :--- | :--- |
| `HC_Patients.csv` | `ChronicCondition` | 5,071 | 25.35% | Patients with no diagnosed chronic condition. Handled by imputing `'None'` category rather than row deletion. |
| All other 26 files | All columns | 0 | 0.00% | Complete records with zero null values across master and transactional tables. |

---

## 4. Personally Identifiable Information (PII) Protection

The following sensitive patient columns were identified in `HC_Patients.csv`:
- `FirstName`, `LastName`: Direct personal names.
- `Phone`, `EmergencyContact`: Contact information.
- `DateOfBirth`: Precise birthdate.

**Governance Directive**: Direct identifiers are excluded from all feature engineering, modeling pipelines, Git repositories, and API payloads. Only pseudo-anonymized IDs (`PatientID`) and derived demographic features (`Age`, `AgeGroup`, `BMI`) are processed.
