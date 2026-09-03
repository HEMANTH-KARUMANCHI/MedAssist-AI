"""
AI Model Validation & Performance Testing Script
MedAssist-AI Milestone 4

Validates performance metrics, accuracy, precision, recall,
F1-scores, and feature importances for both:
1. Disease Prediction Model (Random Forest - 41 classes, 131 features)
2. Patient Risk Assessment Model (Random Forest Pipeline - Binary outcome)
"""

import json
from pathlib import Path
import re

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
MODELS_DIR = BACKEND_DIR / "models"
DATASETS_DIR = PROJECT_ROOT / "datasets"

DISEASE_DATASET = DATASETS_DIR / "Disease_Symptom_Prediction" / "dataset.csv"
DISEASE_MODEL_PATH = MODELS_DIR / "disease_prediction_model.pkl"
DISEASE_FEATURES_PATH = MODELS_DIR / "disease_features.pkl"

RISK_DATASET = DATASETS_DIR / "Disease_symptom_and_patient_profile_dataset.csv"
RISK_MODEL_PATH = MODELS_DIR / "patient_risk_model.pkl"

OUTPUT_REPORT_PATH = MODELS_DIR / "validation_report.json"


def normalize_symptom(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def normalize_disease(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).strip())


from app.train_disease_model import load_augmented_dataset


def validate_disease_model():
    print("\n" + "=" * 70)
    print("  VALIDATING AI MODEL 1: DISEASE PREDICTION")
    print("=" * 70)

    # 1. Load Augmented Dataset
    df, feature_names = load_augmented_dataset()
    x_df = df[feature_names]
    y_series = df["Disease"]
    print(f"Total evaluated dataset samples: {len(df)}")
    print(f"Disease classes: {y_series.nunique()} classes")
    print(f"Symptom features: {len(feature_names)} features")

    # 2. Load Model & Features
    model = joblib.load(DISEASE_MODEL_PATH)
    print(f"Loaded model: {type(model).__name__}")

    # Stratified Split (80/20)
    x_train, x_test, y_train, y_test = train_test_split(
        x_df, y_series, test_size=0.2, random_state=42, stratify=y_series
    )

    # Evaluation on test split and full dataset
    y_pred_test = model.predict(x_test)
    y_pred_all = model.predict(x_df)

    test_acc = accuracy_score(y_test, y_pred_test)
    test_f1 = f1_score(y_test, y_pred_test, average="weighted")
    overall_acc = accuracy_score(y_series, y_pred_all)

    # 5-fold cross validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, x_df, y_series, cv=cv, scoring="accuracy")

    # Feature importances
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    top_features = [
        {"feature": feature_names[idx], "importance": round(float(importances[idx]), 4)}
        for idx in sorted_idx[:10]
    ]

    print(f"\n[Test Split Accuracy]      : {test_acc * 100:.2f}%")
    print(f"[Weighted F1-Score]        : {test_f1 * 100:.2f}%")
    print(f"[Full Dataset Accuracy]    : {overall_acc * 100:.2f}%")
    print(f"[5-Fold Cross-Val Mean]    : {cv_scores.mean() * 100:.2f}% (std: {cv_scores.std() * 100:.2f}%)")
    print("\nTop 5 Influential Symptoms:")
    for feat in top_features[:5]:
        print(f"  - {feat['feature']:<30}: {feat['importance'] * 100:.2f}%")

    return {
        "model_name": "Disease Prediction Model",
        "algorithm": "RandomForestClassifier",
        "classes": len(model.classes_),
        "features_count": len(feature_names),
        "test_accuracy": round(float(test_acc), 4),
        "test_f1_score": round(float(test_f1), 4),
        "overall_accuracy": round(float(overall_acc), 4),
        "cross_val_accuracy_mean": round(float(cv_scores.mean()), 4),
        "cross_val_accuracy_std": round(float(cv_scores.std()), 4),
        "top_features": top_features,
    }


def validate_risk_model():
    print("\n" + "=" * 70)
    print("  VALIDATING AI MODEL 2: PATIENT RISK ASSESSMENT")
    print("=" * 70)

    # 1. Load Data
    raw = pd.read_csv(RISK_DATASET)
    clean_df = raw.drop(columns=["Disease"]).drop_duplicates()
    print(f"Total raw records: {len(raw)}")
    print(f"Unique clean records: {len(clean_df)}")

    target = "Outcome Variable"
    x = clean_df.drop(columns=[target])
    y = clean_df[target]

    # 2. Load Pipeline
    pipeline = joblib.load(RISK_MODEL_PATH)
    print(f"Loaded Pipeline with steps: {list(pipeline.named_steps.keys())}")

    # Train / Test split consistent with training
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    y_pred = pipeline.predict(x_test)
    y_proba = pipeline.predict_proba(x_test)[:, 1]  # positive class probability

    # Convert positive/negative to binary for ROC-AUC
    y_test_bin = (y_test == "Positive").astype(int)

    acc = accuracy_score(y_test, y_pred)
    bal_acc = balanced_accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label="Positive")
    rec = recall_score(y_test, y_pred, pos_label="Positive")
    f1 = f1_score(y_test, y_pred, pos_label="Positive")
    auc = roc_auc_score(y_test_bin, y_proba)
    cm = confusion_matrix(y_test, y_pred, labels=["Negative", "Positive"]).tolist()

    # 5-fold cross validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, x, y, cv=cv, scoring="accuracy")

    # Feature importances from pipeline
    rf_model = pipeline.named_steps["model"]
    preprocessor = pipeline.named_steps["preprocessor"]
    transformed_feature_names = list(preprocessor.get_feature_names_out())
    importances = rf_model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    top_risk_drivers = [
        {"feature": transformed_feature_names[i], "importance": round(float(importances[i]), 4)}
        for i in sorted_idx[:8]
    ]

    print(f"\n[Accuracy]                 : {acc * 100:.2f}%")
    print(f"[Balanced Accuracy]        : {bal_acc * 100:.2f}%")
    print(f"[Precision (Positive)]     : {prec * 100:.2f}%")
    print(f"[Recall (Positive)]        : {rec * 100:.2f}%")
    print(f"[F1-Score]                 : {f1 * 100:.2f}%")
    print(f"[ROC-AUC Score]            : {auc * 100:.2f}%")
    print(f"[5-Fold Cross-Val Mean]    : {cv_scores.mean() * 100:.2f}%")
    print(f"[Confusion Matrix]         : TN={cm[0][0]}, FP={cm[0][1]}, FN={cm[1][0]}, TP={cm[1][1]}")

    print("\nTop Risk Driver Features:")
    for feat in top_risk_drivers[:5]:
        print(f"  - {feat['feature']:<30}: {feat['importance'] * 100:.2f}%")

    return {
        "model_name": "Patient Risk Assessment Model",
        "algorithm": "RandomForestClassifier (ColumnTransformer Pipeline)",
        "features": list(x.columns),
        "test_accuracy": round(float(acc), 4),
        "balanced_accuracy": round(float(bal_acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc_score": round(float(auc), 4),
        "cross_val_accuracy_mean": round(float(cv_scores.mean()), 4),
        "confusion_matrix": {
            "true_negative": cm[0][0],
            "false_positive": cm[0][1],
            "false_negative": cm[1][0],
            "true_positive": cm[1][1],
        },
        "top_risk_drivers": top_risk_drivers,
    }


def main():
    print("=" * 70)
    print("      MEDASSIST AI - COMPREHENSIVE MODEL VALIDATION REPORT")
    print("=" * 70)

    disease_report = validate_disease_model()
    risk_report = validate_risk_model()

    final_report = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "disease_prediction_model": disease_report,
        "patient_risk_model": risk_report,
    }

    with open(OUTPUT_REPORT_PATH, "w") as f:
        json.dump(final_report, f, indent=2)

    print("\n" + "=" * 70)
    print(f"Validation report saved successfully to:\n  {OUTPUT_REPORT_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()
