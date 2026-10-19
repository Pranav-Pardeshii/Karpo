"""
Crop Recommendation Model Training and Inference Module.
Trains Random Forest and XGBoost classifiers, evaluates metrics, selects the superior model,
computes feature importances and confusion matrices, and provides an inference class for real-time recommendations.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from xgboost import XGBClassifier

from crop_advisory.config import (
    CROP_REC_FEATURES,
    CROP_REC_MODEL_FILENAME,
    CROP_REC_PREPROCESSOR_FILENAME,
    get_artifact_path,
)
from crop_advisory.domain.crop_mapping import get_crop_metadata
from crop_advisory.exceptions import ModelNotFoundError
from crop_advisory.ml.feature_validation import validate_soil_climate_input
from crop_advisory.ml.model_loader import ModelLoader, default_model_loader
from crop_advisory.ml.preprocessing import (
    get_crop_rec_splits,
    load_and_clean_crop_rec_data,
)


def train_and_evaluate_crop_models(
    artifacts_dir: Optional[Union[str, Path]] = None, random_state: int = 42
) -> Dict[str, Any]:
    """
    Trains both Random Forest and XGBoost classifiers on Crop_recommendation.csv.
    Evaluates both models, selects the best, saves artifacts, and returns comprehensive metrics.
    """
    save_dir = Path(artifacts_dir) if artifacts_dir else get_artifact_path("").parent
    save_dir.mkdir(parents=True, exist_ok=True)

    df = load_and_clean_crop_rec_data()
    X_train, X_test, y_train, y_test, label_encoder, scaler = get_crop_rec_splits(
        df=df, test_size=0.2, random_state=random_state
    )

    classes = label_encoder.classes_

    # 1. Train Random Forest Classifier
    rf_model = RandomForestClassifier(
        n_estimators=100, max_depth=15, min_samples_split=3, random_state=random_state, n_jobs=1
    )
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)

    rf_acc = accuracy_score(y_test, rf_preds)
    rf_prec = precision_score(y_test, rf_preds, average="weighted", zero_division=0)
    rf_rec = recall_score(y_test, rf_preds, average="weighted", zero_division=0)
    rf_f1 = f1_score(y_test, rf_preds, average="weighted", zero_division=0)

    # 2. Train XGBoost Classifier
    xgb_model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="mlogloss",
        random_state=random_state,
        n_jobs=1,
    )
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)

    xgb_acc = accuracy_score(y_test, xgb_preds)
    xgb_prec = precision_score(y_test, xgb_preds, average="weighted", zero_division=0)
    xgb_rec = recall_score(y_test, xgb_preds, average="weighted", zero_division=0)
    xgb_f1 = f1_score(y_test, xgb_preds, average="weighted", zero_division=0)

    # Compare and select best
    if xgb_f1 > rf_f1:
        best_name = "XGBoost Classifier"
        best_model = xgb_model
        best_preds = xgb_preds
        best_metrics = {
            "accuracy": xgb_acc,
            "precision": xgb_prec,
            "recall": xgb_rec,
            "f1_score": xgb_f1,
        }
        best_importances = dict(zip(CROP_REC_FEATURES, xgb_model.feature_importances_.tolist()))
    else:
        best_name = "Random Forest Classifier"
        best_model = rf_model
        best_preds = rf_preds
        best_metrics = {
            "accuracy": rf_acc,
            "precision": rf_prec,
            "recall": rf_rec,
            "f1_score": rf_f1,
        }
        best_importances = dict(zip(CROP_REC_FEATURES, rf_model.feature_importances_.tolist()))

    cm = confusion_matrix(y_test, best_preds)
    cr = classification_report(
        y_test, best_preds, target_names=classes, output_dict=True, zero_division=0
    )

    # Save artifacts
    model_path = save_dir / CROP_REC_MODEL_FILENAME
    preproc_path = save_dir / CROP_REC_PREPROCESSOR_FILENAME
    joblib.dump(best_model, model_path)
    preprocessor_bundle = {
        "scaler": scaler,
        "label_encoder": label_encoder,
        "features": CROP_REC_FEATURES,
        "classes": classes.tolist(),
        "model_name": best_name,
    }
    joblib.dump(preprocessor_bundle, preproc_path)

    return {
        "rf_metrics": {
            "accuracy": rf_acc,
            "precision": rf_prec,
            "recall": rf_rec,
            "f1_score": rf_f1,
        },
        "xgb_metrics": {
            "accuracy": xgb_acc,
            "precision": xgb_prec,
            "recall": xgb_rec,
            "f1_score": xgb_f1,
        },
        "best_model_name": best_name,
        "best_metrics": best_metrics,
        "feature_importances": best_importances,
        "confusion_matrix": cm.tolist(),
        "classes": classes.tolist(),
        "classification_report": cr,
        "test_sample_count": len(y_test),
        "model_path": str(model_path),
        "preprocessor_path": str(preproc_path),
    }


class CropRecommender:
    """
    Inference helper for Crop Recommendation.
    Loads saved model and preprocessor to generate top recommendations with probabilities.
    """

    def __init__(
        self,
        model_path: Optional[Union[str, Path]] = None,
        preprocessor_path: Optional[Union[str, Path]] = None,
        loader: Optional[ModelLoader] = None,
    ):
        self.model_path = Path(model_path) if model_path else None
        self.preprocessor_path = Path(preprocessor_path) if preprocessor_path else None
        self.loader = loader or default_model_loader
        self.model = None
        self.preprocessor = None
        self._load()

    def _load(self) -> None:
        if self.model_path and self.preprocessor_path:
            if not self.model_path.exists() or not self.preprocessor_path.exists():
                raise ModelNotFoundError(
                    f"Model or preprocessor file not found at '{self.model_path}'. "
                    "Please run train_models.py first."
                )
            self.model = joblib.load(self.model_path)
            self.preprocessor = joblib.load(self.preprocessor_path)
        else:
            self.model = self.loader.load_crop_recommendation_model()
            self.preprocessor = self.loader.load_crop_recommendation_preprocessor()

    def predict(
        self,
        n: float,
        p: float,
        k: float,
        temperature: float,
        humidity: float,
        ph: float,
        rainfall: float,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """
        Recommends best crops given soil nutrients and environmental parameters.
        Returns top recommendation, top-k ranking with probabilities, and agronomic insights.
        """
        # Feature validation
        validate_soil_climate_input(
            n=n, p=p, k=k, temperature=temperature, humidity=humidity, ph=ph, rainfall=rainfall
        )

        scaler = self.preprocessor["scaler"]
        classes = self.preprocessor["classes"]

        # Strictly ordered feature array matching training schema
        input_arr = np.array([[n, p, k, temperature, humidity, ph, rainfall]], dtype=float)
        input_scaled = scaler.transform(input_arr)

        probabilities = self.model.predict_proba(input_scaled)[0]
        top_indices = np.argsort(probabilities)[::-1][:top_k]

        recommendations: List[Dict[str, Any]] = []
        for idx in top_indices:
            crop_label = str(classes[idx])
            prob = float(probabilities[idx])
            meta = get_crop_metadata(crop_label)
            recommendations.append(
                {
                    "crop": crop_label,
                    "display_name": meta.get("display_name", crop_label.title()),
                    "category": meta.get("category", "Field Crop"),
                    "confidence_score": round(prob * 100.0, 2),
                    "probability": round(prob, 4),
                    "description": meta.get("description", ""),
                }
            )

        primary = recommendations[0]

        # Soil nutrient diagnostics
        nutrient_notes = []
        if n < 40:
            nutrient_notes.append(
                "Low Soil Nitrogen (N): Consider legume cover crops or urea supplementation."
            )
        elif n > 120:
            nutrient_notes.append(
                "High Soil Nitrogen (N): Suitable for heavy-foliage crops; minimize nitrogenous fertilizers."
            )

        if p < 25:
            nutrient_notes.append(
                "Low Phosphorus (P): Superphosphate (SSP/DAP) recommended for strong root development."
            )
        if k < 25:
            nutrient_notes.append(
                "Low Potassium (K): Muriate of Potash (MOP) recommended for disease resistance."
            )

        if ph < 5.5:
            nutrient_notes.append("Acidic Soil (pH < 5.5): Agricultural lime application advised.")
        elif ph > 8.0:
            nutrient_notes.append(
                "Alkaline Soil (pH > 8.0): Gypsum or organic compost advised to balance pH."
            )

        return {
            "primary_crop": primary["crop"],
            "display_name": primary["display_name"],
            "confidence_percent": primary["confidence_score"],
            "category": primary["category"],
            "description": primary["description"],
            "recommendations": recommendations,
            "soil_advisory_notes": nutrient_notes,
            "model_used": self.preprocessor.get("model_name", "Classification Model"),
        }
