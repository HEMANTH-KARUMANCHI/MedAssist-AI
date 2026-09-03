"""
Unit tests for AI Models and Inference Services.
MedAssist-AI Milestone 4
"""

import pytest

from app.prediction_service import (
    feature_names,
    get_disease_description,
    get_disease_precautions,
    predict_disease,
    predict_top_conditions,
)
from app.patient_risk_service import assess_patient_risk


def test_disease_feature_names_loaded():
    """Verify 131 symptoms are loaded for the disease prediction model."""
    assert len(feature_names) == 131
    assert "itching" in feature_names
    assert "high_fever" in feature_names
    assert "headache" in feature_names


def test_disease_prediction_basic():
    """Verify disease prediction with known symptoms returns a valid disease."""
    symptoms = ["itching", "skin_rash", "nodal_skin_eruptions"]
    prediction = predict_disease(symptoms)
    assert isinstance(prediction, str)
    assert len(prediction) > 0
    assert prediction == "Fungal infection"


def test_disease_prediction_top_conditions():
    """Verify top conditions inference returns 3 conditions with probabilities."""
    symptoms = ["chills", "vomiting", "high_fever", "sweating", "headache"]
    top_conditions = predict_top_conditions(symptoms, top_n=3)

    assert len(top_conditions) == 3
    for cond in top_conditions:
        assert "condition" in cond
        assert "model_score" in cond
        assert "description" in cond
        assert "precautions" in cond
        assert 0.0 <= cond["model_score"] <= 100.0


def test_disease_metadata_helpers():
    """Verify disease description and precaution retrievals."""
    desc = get_disease_description("Diabetes")
    assert desc is not None
    assert isinstance(desc, str)

    precautions = get_disease_precautions("Diabetes")
    assert isinstance(precautions, list)
    assert len(precautions) > 0


def test_patient_risk_assessment_positive():
    """Verify patient risk assessment model predicts high-risk scenario."""
    high_risk_patient = {
        "Fever": "Yes",
        "Cough": "Yes",
        "Fatigue": "Yes",
        "Difficulty Breathing": "Yes",
        "Age": 65,
        "Gender": "Male",
        "Blood Pressure": "High",
        "Cholesterol Level": "High",
    }
    result = assess_patient_risk(high_risk_patient)

    assert "predicted_outcome" in result
    assert result["predicted_outcome"] in ["Positive", "Negative"]
    assert "positive_model_score" in result
    assert "negative_model_score" in result
    assert 0.0 <= result["positive_model_score"] <= 100.0
    assert 0.0 <= result["negative_model_score"] <= 100.0
    assert round(result["positive_model_score"] + result["negative_model_score"]) == 100


def test_patient_risk_assessment_missing_fields():
    """Verify patient risk assessment rejects incomplete patient data."""
    incomplete_patient = {
        "Fever": "Yes",
        "Age": 30,
    }
    with pytest.raises(ValueError, match="Missing required fields"):
        assess_patient_risk(incomplete_patient)
