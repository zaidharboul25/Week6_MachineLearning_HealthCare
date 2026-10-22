"""
Explainable AI (XAI) Module for HealthConnect Rwanda.
Provides:
- Global feature importance extraction
- SHAP summary and local explanation generation
- Local prediction breakdown
- Clinical & statistical caveats on interpretability
"""

from pathlib import Path
import logging
from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import shap
    SHAP_AVAILABLE = True
except Exception:
    SHAP_AVAILABLE = False

from healthconnect.config import FIGURES_DIR, RANDOM_SEED

logger = logging.getLogger(__name__)

def extract_feature_importances(
    pipeline: Any,
    feature_names: List[str] = None
) -> pd.DataFrame:
    """
    Extract feature importances from tree-based or linear models in a fitted pipeline.
    """
    model = pipeline.steps[-1][1]
    preprocessor = pipeline.named_steps.get("preprocessor")
    
    # Get feature names after one-hot encoding
    if preprocessor is not None and hasattr(preprocessor, "get_feature_names_out"):
        transformed_names = preprocessor.get_feature_names_out()
    else:
        transformed_names = [f"feat_{i}" for i in range(model.n_features_in_)] if hasattr(model, "n_features_in_") else []

    importances = None
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.abs(model.coef_).flatten()

    if importances is not None and len(importances) == len(transformed_names):
        df_imp = pd.DataFrame({
            "feature": transformed_names,
            "importance": importances
        }).sort_values(by="importance", ascending=False).reset_index(drop=True)
        return df_imp
    else:
        return pd.DataFrame(columns=["feature", "importance"])

def generate_shap_explanations(
    pipeline: Any,
    X_sample: pd.DataFrame,
    task_name: str,
    output_fig_path: Path
) -> Dict[str, Any]:
    """
    Generate SHAP summary plot and feature rankings.
    Includes robust fallback if SHAP TreeExplainer fails.
    """
    logger.info(f"Generating SHAP explanations for {task_name}...")
    preprocessor = pipeline.named_steps.get("preprocessor")
    model = pipeline.steps[-1][1]
    
    if preprocessor is not None:
        X_trans = preprocessor.transform(X_sample)
        feature_names = preprocessor.get_feature_names_out()
    else:
        X_trans = X_sample.values
        feature_names = [f"feat_{i}" for i in range(X_trans.shape[1])]

    # Convert to clean feature names (strip 'num__', 'cat__')
    clean_names = [n.replace("num__", "").replace("cat__", "") for n in feature_names]

    explanation_data = {"method": "None", "top_features": []}

    if SHAP_AVAILABLE:
        try:
            # TreeExplainer for tree models
            if hasattr(model, "feature_importances_"):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_trans[:200])
                
                # For classification, pick positive or main class
                if isinstance(shap_values, list) and len(shap_values) > 1:
                    shap_vals_to_plot = shap_values[1]
                elif hasattr(shap_values, "shape") and len(shap_values.shape) == 3:
                    shap_vals_to_plot = shap_values[:, :, 1]
                else:
                    shap_vals_to_plot = shap_values

                plt.figure(figsize=(10, 6))
                shap.summary_plot(
                    shap_vals_to_plot,
                    X_trans[:200],
                    feature_names=clean_names,
                    max_display=12,
                    show=False
                )
                plt.title(f"SHAP Summary: {task_name}", fontsize=12, fontweight="bold")
                plt.tight_layout()
                plt.savefig(output_fig_path, dpi=300)
                plt.close()
                
                # Compute mean absolute SHAP values for top features
                mean_abs_shap = np.abs(shap_vals_to_plot).mean(axis=0)
                top_indices = np.argsort(mean_abs_shap)[::-1][:10]
                explanation_data["method"] = "SHAP TreeExplainer"
                explanation_data["top_features"] = [
                    {"feature": clean_names[i], "mean_abs_shap": round(float(mean_abs_shap[i]), 4)}
                    for i in top_indices
                ]
                logger.info(f"Successfully generated SHAP plot: {output_fig_path}")
                return explanation_data
        except Exception as e:
            logger.warning(f"SHAP TreeExplainer encountered error: {e}. Falling back to permutation/model feature importances.")

    # Fallback to model feature importances
    df_imp = extract_feature_importances(pipeline)
    if not df_imp.empty:
        plt.figure(figsize=(10, 6))
        top_10 = df_imp.head(10).sort_values("importance", ascending=True)
        clean_top_names = [n.replace("num__", "").replace("cat__", "") for n in top_10["feature"]]
        plt.barh(clean_top_names, top_10["importance"], color="#2b5c8f")
        plt.xlabel("Model Feature Importance", fontsize=11)
        plt.title(f"Global Feature Importance: {task_name}", fontsize=12, fontweight="bold")
        plt.tight_layout()
        plt.savefig(output_fig_path, dpi=300)
        plt.close()
        
        explanation_data["method"] = "Model Native Feature Importance"
        explanation_data["top_features"] = [
            {"feature": row["feature"].replace("num__", "").replace("cat__", ""), "importance": round(float(row["importance"]), 4)}
            for _, row in df_imp.head(10).iterrows()
        ]

    return explanation_data
