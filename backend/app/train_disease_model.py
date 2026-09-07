"""Train the disease classifier from the canonical dataset with subset augmentation.

In real-world clinical usage, patients frequently report only 2–4 symptoms (sparse subsets).
Training strictly on full symptom sets causes the decision trees to overfit to presence/absence
of co-occurring symptoms. This script augments training data with combinations of length 2 to 6,
allowing the model to accurately recognize disease signatures on sparse and partial symptom reports.
"""

import itertools
import json
import random
import re
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "datasets" / "Disease_Symptom_Prediction" / "dataset.csv"
MODELS_DIR = PROJECT_ROOT / "backend" / "models"
MODEL_PATH = MODELS_DIR / "disease_prediction_model.pkl"
FEATURES_PATH = MODELS_DIR / "disease_features.pkl"
METADATA_PATH = MODELS_DIR / "disease_model_metadata.json"


def normalize_symptom(value: object) -> str:
    """Canonicalize the source spelling used by both training and inference."""
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def normalize_disease(value: object) -> str:
    text = re.sub(r"\s+", " ", str(value).strip())
    return text


def load_augmented_dataset() -> tuple[pd.DataFrame, list[str]]:
    raw = pd.read_csv(DATASET_PATH, encoding="latin1")
    symptom_columns = [column for column in raw.columns if column.startswith("Symptom_")]

    disease_symptom_map: dict[str, set[str]] = {}
    disease_unique_combinations: dict[str, list[tuple[str, ...]]] = {}

    for _, record in raw.iterrows():
        disease = normalize_disease(record["Disease"])
        symptoms = tuple(
            sorted(
                {
                    normalize_symptom(val)
                    for val in record[symptom_columns]
                    if pd.notna(val) and normalize_symptom(val)
                }
            )
        )
        if not symptoms:
            continue

        if disease not in disease_symptom_map:
            disease_symptom_map[disease] = set()
            disease_unique_combinations[disease] = []

        disease_symptom_map[disease].update(symptoms)
        if symptoms not in disease_unique_combinations[disease]:
            disease_unique_combinations[disease].append(symptoms)

    all_features = sorted({sym for syms in disease_symptom_map.values() for sym in syms})

    random.seed(42)
    np.random.seed(42)

    augmented_records: list[dict[str, int | str]] = []

    for disease, sym_combinations in disease_unique_combinations.items():
        all_syms_for_disease = list(disease_symptom_map[disease])

        # 1. Include full observed combinations multiple times for weight
        for comb in sym_combinations:
            for _ in range(8):
                row: dict[str, int | str] = {f: 0 for f in all_features}
                for s in comb:
                    row[s] = 1
                row["Disease"] = disease
                augmented_records.append(row)

        # 2. Generate partial combinations (lengths 2, 3, 4, 5, 6)
        for k in [2, 3, 4, 5, 6]:
            if len(all_syms_for_disease) >= k:
                combs = list(itertools.combinations(all_syms_for_disease, k))
                sample_size = min(len(combs), 40)
                sampled_combs = random.sample(combs, sample_size) if len(combs) > 40 else combs
                for c in sampled_combs:
                    row = {f: 0 for f in all_features}
                    for s in c:
                        row[s] = 1
                    row["Disease"] = disease
                    augmented_records.append(row)

    df_augmented = pd.DataFrame(augmented_records).drop_duplicates().reset_index(drop=True)
    return df_augmented, all_features


def train_and_evaluate() -> dict:
    df, feature_names = load_augmented_dataset()
    X = df[feature_names]
    y = df["Disease"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_features="sqrt",
        random_state=42,
        class_weight="balanced",
        n_jobs=1,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    precision = precision_score(y_test, predictions, average="macro", zero_division=0)
    recall = recall_score(y_test, predictions, average="macro", zero_division=0)
    macro_f1 = f1_score(y_test, predictions, average="macro", zero_division=0)
    acc = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)
    class_report = classification_report(y_test, predictions, zero_division=0)

    metrics = {
        "accuracy": float(acc),
        "precision": float(precision),
        "recall": float(recall),
        "macro_f1": float(macro_f1),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "total_augmented_rows": int(len(df)),
        "disease_classes": int(y.nunique()),
        "symptom_features": int(len(feature_names)),
        "random_state": 42,
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(feature_names, FEATURES_PATH)
    METADATA_PATH.write_text(
        json.dumps(
            {
                "source_dataset": str(DATASET_PATH.relative_to(PROJECT_ROOT)),
                "preprocessing": [
                    "trim and lowercase symptom values",
                    "replace non-alphanumeric runs with underscores",
                    "subset combinatoric augmentation (lengths 2-6)",
                    "stratified 80/20 train/test split on unseen data",
                ],
                "metrics": metrics,
                "classification_report": class_report,
                "confusion_matrix": conf_matrix.tolist(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"=== Model Trained on {len(df)} samples across {y.nunique()} disease classes ===")
    print(json.dumps(metrics, indent=2))
    print(f"\nSaved upgraded model: {MODEL_PATH}")
    print(f"Saved features: {FEATURES_PATH}")
    print(f"Saved metadata: {METADATA_PATH}")

    return metrics


if __name__ == "__main__":
    train_and_evaluate()
