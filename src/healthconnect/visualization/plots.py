"""
Visualization Module for HealthConnect Rwanda.
Generates clear, publication-quality figures:
- Missing values overview
- Target and feature distributions
- Confusion matrices
- ROC curves
- Regression actual vs predicted and residuals
- Clustering PCA projections
- Anomaly distributions
Saves all figures to reports/figures/.
"""

from pathlib import Path
import logging
from typing import Dict, Any, List
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc

from healthconnect.config import FIGURES_DIR

logger = logging.getLogger(__name__)

# Apply modern clean style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10

def plot_confusion_matrix(cm: List[List[int]], class_names: List[str], title: str, filename: str):
    """Plot and save a styled confusion matrix."""
    plt.figure(figsize=(6, 5))
    cm_arr = np.array(cm)
    sns.heatmap(
        cm_arr,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        cbar=False
    )
    plt.title(title, fontsize=12, fontweight="bold", pad=12)
    plt.ylabel("True Label", fontsize=11)
    plt.xlabel("Predicted Label", fontsize=11)
    plt.tight_layout()
    out_path = FIGURES_DIR / filename
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Saved confusion matrix plot: {out_path}")

def plot_roc_curve(y_true: np.ndarray, y_proba: np.ndarray, title: str, filename: str):
    """Plot and save ROC curve."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color="#1f77b4", lw=2, label=f"ROC curve (AUC = {roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], color="grey", lw=1.5, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    plt.ylabel("True Positive Rate (Sensitivity)", fontsize=11)
    plt.title(title, fontsize=12, fontweight="bold", pad=12)
    plt.legend(loc="lower right")
    plt.tight_layout()
    out_path = FIGURES_DIR / filename
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Saved ROC curve: {out_path}")

def plot_regression_performance(y_true: np.ndarray, y_pred: np.ndarray, residuals: np.ndarray, filename_prefix: str):
    """Plot Actual vs Predicted and Residuals distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Actual vs Predicted
    axes[0].scatter(y_true, y_pred, alpha=0.3, color="#2b5c8f", s=15)
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    axes[0].plot([min_val, max_val], [min_val, max_val], color="crimson", lw=2, linestyle="--", label="Perfect Fit (y = x)")
    axes[0].set_title("Billing Amount: Actual vs Predicted", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Actual Billing Amount (RWF)", fontsize=11)
    axes[0].set_ylabel("Predicted Billing Amount (RWF)", fontsize=11)
    axes[0].legend()
    
    # Residuals Distribution
    sns.histplot(residuals, kde=True, ax=axes[1], color="#e76f51", bins=40)
    axes[1].axvline(0, color="black", linestyle="--", lw=1.5)
    axes[1].set_title("Residuals Error Distribution", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Residual Error (Actual - Predicted) [RWF]", fontsize=11)
    axes[1].set_ylabel("Density / Frequency", fontsize=11)
    
    plt.tight_layout()
    out_path = FIGURES_DIR / f"{filename_prefix}_residuals.png"
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Saved regression performance plots: {out_path}")

def plot_facility_clusters_pca(facility_assignments: List[Dict[str, Any]], filename: str):
    """Plot 2D PCA projection of healthcare facility clusters."""
    df = pd.DataFrame(facility_assignments)
    plt.figure(figsize=(8, 6))
    
    palette = {0: "#2a9d8f", 1: "#e76f51", 2: "#f4a261"}
    sns.scatterplot(
        data=df,
        x="PCA1",
        y="PCA2",
        hue="Cluster",
        palette=palette,
        s=120,
        style="Cluster",
        alpha=0.9
    )
    for _, row in df.iterrows():
        plt.annotate(row["FacilityID"], (row["PCA1"]+0.1, row["PCA2"]+0.1), fontsize=9)
        
    plt.title("Facility Operational Clusters (PCA Projection)", fontsize=12, fontweight="bold", pad=12)
    plt.xlabel("Principal Component 1 (Capacity & Volume)", fontsize=11)
    plt.ylabel("Principal Component 2 (Workload Ratio)", fontsize=11)
    plt.tight_layout()
    out_path = FIGURES_DIR / filename
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Saved facility cluster PCA plot: {out_path}")

def plot_distributions_overview(
    df_billing: pd.DataFrame,
    df_claims: pd.DataFrame,
    df_satisfaction: pd.DataFrame,
    filename: str
):
    """Plot overview of key targets across healthcare domains."""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Billing distribution
    sns.histplot(df_billing["Amount"], kde=True, ax=axes[0], color="#264653", bins=30)
    axes[0].set_title("Encounter Billing Amount Distribution", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Amount (RWF)")
    
    # Claims distribution
    claims_counts = df_claims["Status"].value_counts()
    axes[1].bar(claims_counts.index, claims_counts.values, color=["#2a9d8f", "#e76f51"])
    axes[1].set_title("Insurance Claims Adjudication Status", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Count")
    
    # Satisfaction distribution
    sat_counts = df_satisfaction["SatisfactionClass"].value_counts()[["Low", "Medium", "High"]]
    axes[2].bar(sat_counts.index, sat_counts.values, color=["#d62728", "#ff7f0e", "#2ca02c"])
    axes[2].set_title("Patient Satisfaction Tier Distribution", fontsize=11, fontweight="bold")
    axes[2].set_ylabel("Count")
    
    plt.tight_layout()
    out_path = FIGURES_DIR / filename
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Saved distribution overview plot: {out_path}")
