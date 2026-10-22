# HealthConnect Rwanda — Automated Test Suite Results

**Test Framework:** pytest  
**Status:** PASS (100% Success)  
**Execution Timestamp:** October 2026  

---

## 1. Test Execution Summary

```text
............                                                             [100%]
============================== warnings summary ===============================
deployment\app.py:44
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:44: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    @app.on_event("startup")

..\..\..\AppData\Local\Programs\Python\Python312\Lib\site-packages\fastapi\applications.py:4675
  C:\Users\zaidh\AppData\Local\Programs\Python\Python312\Lib\site-packages\fastapi\applications.py:4675: DeprecationWarning: 
          on_event is deprecated, use lifespan event handlers instead.
  
          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).
          
    return self.router.on_event(event_type)  # ty: ignore[deprecated]

deployment\app.py:82
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:82: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Provider: str = Field(..., example="RSSB", description="Insurance provider (RSSB, Radiant, MMI, Private)")

deployment\app.py:83
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:83: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    ClaimAmount: float = Field(..., gt=0, example=85000.0, description="Requested reimbursement amount in RWF")

deployment\app.py:84
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:84: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    BillingAmount: float = Field(..., gt=0, example=90000.0, description="Total hospital invoiced billing amount in RWF")

deployment\app.py:93
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:93: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Age: int = Field(..., ge=0, le=120, example=45)

deployment\app.py:94
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:94: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    BMI: float = Field(..., ge=10.0, le=60.0, example=24.5)

deployment\app.py:95
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:95: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    DoctorExperience: int = Field(..., ge=0, le=50, example=12)

deployment\app.py:96
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:96: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    FacilityApptVolume: int = Field(..., ge=0, example=250)

deployment\app.py:97
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:97: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    PatientToDoctorRatio: float = Field(..., ge=0, example=14.5)

deployment\app.py:98
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:98: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    BedToDoctorRatio: float = Field(..., ge=0, example=6.2)

deployment\app.py:99
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:99: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    DepartmentWorkload: int = Field(..., ge=0, example=45)

deployment\app.py:100
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:100: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Month: int = Field(..., ge=1, le=12, example=4)

deployment\app.py:101
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:101: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    VisitType: str = Field(..., example="Consultation")

deployment\app.py:102
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:102: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Diagnosis: str = Field(..., example="Hypertension")

deployment\app.py:103
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:103: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Severity: str = Field(..., example="Moderate")

deployment\app.py:104
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:104: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Gender: str = Field(..., example="Female")

deployment\app.py:105
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:105: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    MaritalStatus: str = Field(..., example="Married")

deployment\app.py:106
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:106: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Occupation: str = Field(..., example="Teacher")

deployment\app.py:107
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:107: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    Education: str = Field(..., example="University")

deployment\app.py:108
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:108: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    InsuranceID: str = Field(..., example="INS001")

deployment\app.py:109
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:109: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    ChronicCondition: str = Field(..., example="Hypertension")

deployment\app.py:110
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:110: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    DepartmentName: str = Field(..., example="Internal Medicine")

deployment\app.py:111
  C:\Users\zaidh\Desktop\Stage_number_2\week5\deployment\app.py:111: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.13/migration/
    ProvinceName: str = Field(..., example="Kigali City")

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
12 passed, 24 warnings in 4.82s
```

---

## 2. Tested Functional Domains
- **Data Loading & Schema Invariants**: Validated presence of 27 raw datasets and boundary constraints on patient and billing data.
- **Feature Engineering Transformations**: Validated age categorizations, WHO BMI tiers, and financial ratios.
- **Model Inference Integrity**: Validated serialization and inference for classification, regression, clustering, and anomaly detection pipelines.
- **FastAPI Endpoints**: Validated `/health`, `/predict/claims`, and `/predict/billing` requests and Pydantic validation.
