import difflib
from pathlib import Path

import joblib
import pandas as pd

from app.train_disease_model import normalize_symptom


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "disease_prediction_model.pkl"
)

FEATURES_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "disease_features.pkl"
)

DESCRIPTION_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "Disease_Symptom_Prediction"
    / "symptom_Description.csv"
)

PRECAUTION_PATH = (
    PROJECT_ROOT
    / "datasets"
    / "Disease_Symptom_Prediction"
    / "symptom_precaution.csv"
)


# --------------------------------------------------
# Load or Auto-train model & features
# --------------------------------------------------

if not MODEL_PATH.exists() or not FEATURES_PATH.exists():
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    from app.train_disease_model import train_and_evaluate
    train_and_evaluate()

model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURES_PATH)

description_df = pd.read_csv(DESCRIPTION_PATH, encoding="latin1")
precaution_df = pd.read_csv(PRECAUTION_PATH, encoding="latin1")



# --------------------------------------------------
# Medical Synonym & Common Typo Alias Dictionary
# --------------------------------------------------

SYMPTOM_ALIASES: dict[str, list[str]] = {
    # Fever and temperature
    "fever": ["high_fever", "mild_fever"],
    "fewer": ["high_fever", "mild_fever"],
    "fevr": ["high_fever", "mild_fever"],
    "high_fever": ["high_fever"],
    "mild_fever": ["mild_fever"],
    "temperature": ["high_fever"],
    "pyrexia": ["high_fever"],
    # Nausea and vomiting
    "nausea": ["nausea"],
    "nausia": ["nausea"],
    "nauseous": ["nausea"],
    "queasy": ["nausea"],
    "vomit": ["vomiting"],
    "vomiting": ["vomiting"],
    "throwing_up": ["vomiting"],
    # Pain and aches
    "headache": ["headache"],
    "head_ache": ["headache"],
    "migraine": ["headache"],
    "head_pain": ["headache"],
    "stomach_pain": ["stomach_pain", "abdominal_pain"],
    "stomach_ache": ["stomach_pain", "abdominal_pain"],
    "belly_pain": ["abdominal_pain"],
    "abdominal_pain": ["abdominal_pain"],
    "tummy_ache": ["stomach_pain"],
    "body_pain": ["muscle_pain", "joint_pain"],
    "body_ache": ["muscle_pain", "joint_pain"],
    "muscle_pain": ["muscle_pain"],
    "joint_pain": ["joint_pain"],
    "back_pain": ["back_pain"],
    "neck_pain": ["neck_pain"],
    "chest_pain": ["chest_pain"],
    # Respiratory & Cold
    "cough": ["cough"],
    "cold": ["chills", "continuous_sneezing", "runny_nose"],
    "sneezing": ["continuous_sneezing"],
    "continuous_sneezing": ["continuous_sneezing"],
    "runny_nose": ["runny_nose"],
    "breathlessness": ["breathlessness"],
    "shortness_of_breath": ["breathlessness"],
    "breathing_problem": ["breathlessness"],
    "chills": ["chills"],
    "shivering": ["shivering", "chills"],
    # Fatigue & Weakness
    "fatigue": ["fatigue"],
    "tired": ["fatigue"],
    "exhaustion": ["fatigue"],
    "weakness": ["fatigue", "lethargy"],
    "lethargy": ["lethargy"],
    "malaise": ["malaise", "fatigue"],
    # Digestive & Bowel
    "diarrhea": ["diarrhoea"],
    "diarrhoea": ["diarrhoea"],
    "loose_motion": ["diarrhoea"],
    "loose_motions": ["diarrhoea"],
    "constipation": ["constipation"],
    "acidity": ["acidity"],
    "gas": ["passage_of_gases"],
    "indigestion": ["indigestion"],
    # Skin & Allergy
    "itching": ["itching"],
    "itchy": ["itching"],
    "itch": ["itching"],
    "skin_rash": ["skin_rash"],
    "rash": ["skin_rash"],
    "red_spots": ["red_spots_over_body"],
    "yellow_skin": ["yellowish_skin"],
    "yellowish_skin": ["yellowish_skin"],
    "yellow_eyes": ["yellowing_of_eyes"],
    "yellowing_of_eyes": ["yellowing_of_eyes"],
    # Neurological / Balance
    "dizziness": ["dizziness"],
    "dizzy": ["dizziness"],
    "vertigo": ["loss_of_balance", "unsteadiness"],
    "loss_of_balance": ["loss_of_balance"],
    "unsteadiness": ["unsteadiness"],
    # Appetite & Weight
    "loss_of_appetite": ["loss_of_appetite"],
    "no_appetite": ["loss_of_appetite"],
    "weight_loss": ["weight_loss"],
    "weight_gain": ["weight_gain"],
    "excessive_hunger": ["excessive_hunger"],
    # Urinary
    "burning_urination": ["burning_micturition"],
    "burning_micturition": ["burning_micturition"],
    "dark_urine": ["dark_urine"],
    "yellow_urine": ["yellow_urine"],
}


def resolve_symptom_features(symptom_input: str) -> list[str]:
    """Resolve user-entered symptom text to matching canonical feature names using aliases and fuzzy matching."""
    normalized = normalize_symptom(symptom_input)

    # 1. Direct feature match
    if normalized in feature_names:
        return [normalized]

    # 2. Alias dictionary lookup
    if normalized in SYMPTOM_ALIASES:
        return [f for f in SYMPTOM_ALIASES[normalized] if f in feature_names]

    # 3. Check for partial substring match in feature_names
    substring_matches = [f for f in feature_names if normalized in f or f in normalized]
    if substring_matches:
        return substring_matches[:2]

    # 4. Fuzzy closest match using difflib
    close_matches = difflib.get_close_matches(normalized, feature_names, n=2, cutoff=0.6)
    if close_matches:
        return close_matches

    # 5. Fuzzy match on alias keys
    close_alias_keys = difflib.get_close_matches(normalized, list(SYMPTOM_ALIASES.keys()), n=1, cutoff=0.6)
    if close_alias_keys:
        return [f for f in SYMPTOM_ALIASES[close_alias_keys[0]] if f in feature_names]

    return []


def _build_input_dataframe(symptoms: list[str]) -> pd.DataFrame:
    """Construct 131-feature binary vector from input symptom list with alias resolution."""
    input_data = {feature_name: 0 for feature_name in feature_names}

    for symptom in symptoms:
        resolved_features = resolve_symptom_features(symptom)
        for feature in resolved_features:
            if feature in input_data:
                input_data[feature] = 1

    return pd.DataFrame([input_data], columns=feature_names)


# --------------------------------------------------
# Prediction Endpoints
# --------------------------------------------------

def predict_disease(symptoms: list[str]) -> str:
    """Predict primary disease using retrained Random Forest classifier."""
    input_df = _build_input_dataframe(symptoms)
    return str(model.predict(input_df)[0])


def get_disease_description(disease: str) -> str | None:
    """Retrieve disease clinical overview from description dataset."""
    matches = description_df[
        description_df["Disease"].astype(str).str.strip().str.lower()
        == str(disease).strip().lower()
    ]
    if matches.empty:
        return None
    return str(matches.iloc[0]["Description"])


def get_disease_precautions(disease: str) -> list[str]:
    """Retrieve clinical precaution measures from precaution dataset."""
    matches = precaution_df[
        precaution_df["Disease"].astype(str).str.strip().str.lower()
        == str(disease).strip().lower()
    ]
    if matches.empty:
        return []

    row = matches.iloc[0]
    precautions: list[str] = []
    for column in precaution_df.columns:
        if column.lower().startswith("precaution"):
            value = row[column]
            if pd.notna(value):
                text_val = str(value).strip()
                if text_val:
                    precautions.append(text_val)

    return precautions


def predict_top_conditions(symptoms: list[str], top_n: int = 3) -> list[dict]:
    """Calculate top-N differential diagnosis probabilities with confidence percentages and precautions."""
    input_df = _build_input_dataframe(symptoms)
    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_

    ranked_indices = probabilities.argsort()[::-1][:top_n]
    predictions = []

    for index in ranked_indices:
        disease = str(classes[index])
        score = round(float(probabilities[index]) * 100, 2)
        predictions.append(
            {
                "condition": disease,
                "model_score": score,
                "description": get_disease_description(disease),
                "precautions": get_disease_precautions(disease),
            }
        )

    return predictions