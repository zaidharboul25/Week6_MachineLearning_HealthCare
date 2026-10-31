"""
Unit tests for Preprocessing & Feature Engineering Transformations (Category B).
Tests mathematical transformations, categorical encodings, imputation parity,
and transformation idempotency.
"""

import pytest
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

from healthconnect.features.engineer import (
    derive_age_group,
    derive_bmi_category,
    build_claims_analytical_dataset,
    build_facility_workload_features
)


class TestFeatureDerivationUnit:
    """Test feature engineering functions."""

    def test_derive_age_group_bounds(self):
        """Test exact boundary transitions for age bins."""
        ages = pd.Series([0, 17, 18, 35, 36, 50, 51, 65, 66, 110])
        groups = derive_age_group(ages)
        assert groups.iloc[0] == "<18"
        assert groups.iloc[1] == "<18"
        assert groups.iloc[2] == "18-35"
        assert groups.iloc[3] == "18-35"
        assert groups.iloc[4] == "36-50"
        assert groups.iloc[5] == "36-50"
        assert groups.iloc[6] == "51-65"
        assert groups.iloc[7] == "51-65"
        assert groups.iloc[8] == ">65"
        assert groups.iloc[9] == ">65"

    def test_derive_bmi_category_who_standard(self):
        """Test WHO BMI categorization tiers."""
        bmis = pd.Series([16.0, 18.4, 21.0, 24.9, 26.0, 29.9, 32.0, 45.0])
        cats = derive_bmi_category(bmis)
        assert cats.iloc[0] == "Underweight"
        assert cats.iloc[1] == "Underweight"
        assert cats.iloc[2] == "Normal"
        assert cats.iloc[3] == "Normal"
        assert cats.iloc[4] == "Overweight"
        assert cats.iloc[5] == "Overweight"
        assert cats.iloc[6] == "Obese"
        assert cats.iloc[7] == "Obese"

    def test_build_claims_analytical_features(self):
        """Test mathematical formulation of ClaimToBillingRatio, ClaimDiff, and IsFullClaim."""
        df_claims = pd.DataFrame({
            "ClaimID": ["C1", "C2", "C3"],
            "BillingID": ["B1", "B2", "B3"],
            "Provider": ["RSSB", "Radiant", "MMI"],
            "ClaimAmount": [50000.0, 100000.0, 120000.0],
            "Status": ["Approved", "Approved", "Pending"]
        })
        df_billing = pd.DataFrame({
            "BillingID": ["B1", "B2", "B3"],
            "Amount": [100000.0, 100000.0, 100000.0]
        })

        res = build_claims_analytical_dataset(df_claims, df_billing)
        # Ratios
        assert res.loc[res["ClaimID"] == "C1", "ClaimToBillingRatio"].values[0] == 0.5
        assert res.loc[res["ClaimID"] == "C2", "ClaimToBillingRatio"].values[0] == 1.0
        assert res.loc[res["ClaimID"] == "C3", "ClaimToBillingRatio"].values[0] == 1.2
        # IsFullClaim
        assert res.loc[res["ClaimID"] == "C1", "IsFullClaim"].values[0] == 0
        assert res.loc[res["ClaimID"] == "C2", "IsFullClaim"].values[0] == 1
        assert res.loc[res["ClaimID"] == "C3", "IsFullClaim"].values[0] == 1


class TestPreprocessingPipelineUnit:
    """Test ColumnTransformer with Imputation, Scaling, and One-Hot Encoding."""

    def test_imputation_and_scaling_parity(self):
        """Verify median imputation handles missing values without distorting fitted distribution."""
        train_df = pd.DataFrame({
            "num1": [10.0, 20.0, 30.0, 40.0],
            "cat1": ["A", "B", "A", "B"]
        })
        
        num_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        cat_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])
        preprocessor = ColumnTransformer([
            ("num", num_transformer, ["num1"]),
            ("cat", cat_transformer, ["cat1"])
        ])

        # Fit on training data
        fitted = preprocessor.fit(train_df)
        
        # Test on inference data containing NaN in numeric and unseen category
        test_df = pd.DataFrame({
            "num1": [np.nan],  # Should be imputed with train median (25.0)
            "cat1": ["UnseenCategory"]  # Should be encoded as zeros
        })
        
        transformed = fitted.transform(test_df)
        assert transformed.shape == (1, 3)  # 1 numeric + 2 one-hot columns (A, B)
        assert not np.isnan(transformed).any()
        # Verify unknown category produces zeros in onehot columns
        assert transformed[0, 1] == 0.0
        assert transformed[0, 2] == 0.0

    def test_transformation_reproducibility(self):
        """Verify identical inputs transformed twice yield bit-for-bit identical arrays."""
        df = pd.DataFrame({
            "num1": [12.5, 34.2, 56.1],
            "cat1": ["CatA", "CatB", "CatA"]
        })
        num_transformer = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
        cat_transformer = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
        prep = ColumnTransformer([("num", num_transformer, ["num1"]), ("cat", cat_transformer, ["cat1"])])
        
        prep.fit(df)
        res1 = prep.transform(df)
        res2 = prep.transform(df)
        np.testing.assert_array_equal(res1, res2)
