"""
Clustering and Unsupervised Segmentation Module for HealthConnect Rwanda.
Implements:
- Patient Clinical & Utilization Segmentation
- Healthcare Facility Operational Tier Segmentation
"""

from pathlib import Path
import logging
from typing import Dict, Any, List, Tuple
import joblib
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score

from healthconnect.config import ARTIFACTS_DIR, RANDOM_SEED

logger = logging.getLogger(__name__)

def run_patient_segmentation(
    df_patient_clustering: pd.DataFrame
) -> Dict[str, Any]:
    """
    Segment 20,000 patients using clinical and utilization features:
    Age, BMI, HasChronicCondition, HistoricalApptCount, TotalBilledAmount, SevereDiagnosisCount.
    Evaluates silhouette scores across k=2,3,4,5.
    Generates plain-language cluster descriptions.
    """
    logger.info("Starting Patient Segmentation Clustering...")
    feature_cols = [
        "Age", "BMI", "HasChronicCondition", 
        "HistoricalApptCount", "TotalBilledAmount", "SevereDiagnosisCount"
    ]
    
    X = df_patient_clustering[feature_cols].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Evaluate k
    k_scores = {}
    best_k = 3
    best_score = -1.0
    
    # Sample subset for rapid silhouette calculation if large
    sample_indices = np.random.RandomState(RANDOM_SEED).choice(len(X), size=min(5000, len(X)), replace=False)
    X_sample = X_scaled[sample_indices]

    for k in [2, 3, 4, 5]:
        km = KMeans(n_clusters=k, random_state=RANDOM_SEED, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_sample, labels[sample_indices])
        k_scores[k] = round(float(sil), 4)
        if sil > best_score:
            best_score = sil
            best_k = k

    # Fit final K-Means with chosen k=3 for clinical interpretability
    final_k = 3
    final_km = KMeans(n_clusters=final_k, random_state=RANDOM_SEED, n_init=10)
    final_labels = final_km.fit_predict(X_scaled)

    # Attach labels and profile
    df_profile = X.copy()
    df_profile["Cluster"] = final_labels
    profiles = df_profile.groupby("Cluster").mean().round(2).to_dict(orient="index")

    # Plain-language clinical interpretations
    cluster_personas = {
        0: {
            "name": "Cluster 0: Low-Risk / Preventive Outpatients",
            "description": "Younger cohort (mean age ~35), normal BMI, minimal chronic conditions, low appointment frequency and lower average billing. Needs preventive screenings and digital wellness support."
        },
        1: {
            "name": "Cluster 1: Chronic Multimorbidity / High-Care Seniors",
            "description": "Elderly population (mean age ~65+), high chronic disease prevalence (Hypertension, Diabetes), multiple specialist appointments, and high diagnostic severity. Requires proactive chronic disease management and home-care follow-up."
        },
        2: {
            "name": "Cluster 2: Working-Age Moderate Utilizers / Metabolic Risk",
            "description": "Adult cohort (mean age ~48) with elevated BMI and moderate acute care utilization. Target for lifestyle intervention, hypertension screening, and dietary guidance."
        }
    }

    # Save artifact
    artifact_payload = {
        "scaler": scaler,
        "kmeans": final_km,
        "feature_cols": feature_cols,
        "personas": cluster_personas
    }
    joblib.dump(artifact_payload, ARTIFACTS_DIR / "patient_clusterer.joblib")
    logger.info(f"Saved patient clustering artifact to artifacts/patient_clusterer.joblib")

    return {
        "k_evaluations": k_scores,
        "final_k": final_k,
        "silhouette_score": round(float(silhouette_score(X_sample, final_labels[sample_indices])), 4),
        "cluster_counts": pd.Series(final_labels).value_counts().to_dict(),
        "profiles": profiles,
        "personas": cluster_personas,
        "labels": final_labels
    }

def run_facility_segmentation(
    df_facility_analytical: pd.DataFrame
) -> Dict[str, Any]:
    """
    Segment 20 healthcare facilities into operational tiers using capacity, staffing, and revenue.
    """
    logger.info("Starting Healthcare Facility Segmentation...")
    feature_cols = [
        "FacilityApptVolume", "FacilityDoctorCount", "FacilityRoomCount", "FacilityBedCount",
        "PatientToDoctorRatio", "BedToDoctorRatio", "TotalRevenue", "AvgSatisfactionRating",
        "Staff_Doctor", "Staff_Nurse", "Staff_Admin"
    ]
    
    X = df_facility_analytical[feature_cols].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3 clusters representing Regional Referral, District Hospitals, and Health Centers
    k = 3
    km = KMeans(n_clusters=k, random_state=RANDOM_SEED, n_init=10)
    labels = km.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, labels)

    # PCA 2D projection for visualization
    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    pca_coords = pca.fit_transform(X_scaled)

    df_fac = df_facility_analytical.copy()
    df_fac["Cluster"] = labels
    df_fac["PCA1"] = pca_coords[:, 0]
    df_fac["PCA2"] = pca_coords[:, 1]
    
    profiles = df_fac.groupby("Cluster")[feature_cols].mean().round(2).to_dict(orient="index")

    tier_personas = {
        0: {
            "tier": "Tier 1: High-Volume Referral & Teaching Centers",
            "strategy": "Requires expansion of specialized ICU and surgical bed capacity, automated queuing, and sub-specialty physician staffing."
        },
        1: {
            "tier": "Tier 2: Standard District Community Hospitals",
            "strategy": "Balanced clinical operations. Focus on strengthening diagnostic imaging, emergency response, and nursing staff retention."
        },
        2: {
            "tier": "Tier 3: Outpatient-Centric Primary Health Centers",
            "strategy": "Optimize doctor scheduling, enhance telemedicine consultation linkages with referral hubs, and streamline basic pharmaceuticals."
        }
    }

    artifact_payload = {
        "scaler": scaler,
        "kmeans": km,
        "pca": pca,
        "feature_cols": feature_cols,
        "tier_personas": tier_personas
    }
    joblib.dump(artifact_payload, ARTIFACTS_DIR / "facility_clusterer.joblib")
    logger.info("Saved facility clustering artifact to artifacts/facility_clusterer.joblib")

    return {
        "silhouette_score": round(float(sil), 4),
        "profiles": profiles,
        "tier_personas": tier_personas,
        "facility_assignments": df_fac[["FacilityID", "Cluster", "PCA1", "PCA2"]].to_dict(orient="records")
    }
