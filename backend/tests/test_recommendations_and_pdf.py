"""
Unit tests for Healthcare Recommendations, Treatment Suggestions,
and PDF Report Generation.
MedAssist-AI Milestone 4
"""

from app.treatment_data import TREATMENT_DATA, get_treatment_suggestions
from app.report_generator import generate_prediction_report_pdf


def test_treatment_suggestions_exact_match():
    """Verify treatment data returns specific recommendations for mapped diseases."""
    treatment = get_treatment_suggestions("Diabetes")
    assert treatment is not None
    assert treatment["category"] == "Metabolic"
    assert len(treatment["suggestions"]) == 4
    assert "dietary_advice" in treatment
    assert "when_to_see_doctor" in treatment


def test_treatment_suggestions_fallback():
    """Verify fallback response for unmapped disease names."""
    fallback = get_treatment_suggestions("Uncommon Disease XYZ")
    assert fallback is not None
    assert fallback["category"] == "General"
    assert len(fallback["suggestions"]) > 0


def test_all_41_diseases_covered():
    """Verify all 41 diseases have curated treatment suggestions."""
    assert len(TREATMENT_DATA) == 41
    for disease, data in TREATMENT_DATA.items():
        assert "category" in data
        assert "suggestions" in data
        assert len(data["suggestions"]) >= 3
        assert "dietary_advice" in data
        assert "when_to_see_doctor" in data


def test_pdf_report_generation():
    """Verify PDF report generation produces valid, non-empty binary content."""
    patient_info = {
        "full_name": "Test Patient",
        "email": "test@example.com",
        "gender": "Male",
        "date_of_birth": "1990-01-01",
        "blood_group": "O+",
        "height_cm": 175.0,
        "weight_kg": 70.0,
    }
    symptoms = [
        {"symptom_name": "headache", "severity": "Mild"},
        {"symptom_name": "high_fever", "severity": "Moderate"},
    ]
    top_conditions = [
        {
            "condition": "Common Cold",
            "model_score": 85.5,
            "description": "Viral infection of the upper respiratory tract.",
            "precautions": ["Rest", "Drink fluids", "Steam inhalation"],
        }
    ]
    risk_data = {
        "predicted_outcome": "Negative",
        "positive_model_score": 25.0,
        "negative_model_score": 75.0,
        "blood_pressure": "Normal",
        "cholesterol_level": "Normal",
    }
    recommendations = [
        "Drink at least 2-3 litres of water daily",
        "Avoid cold drinks",
    ]

    pdf_bytes = generate_prediction_report_pdf(
        patient_info=patient_info,
        symptoms=symptoms,
        prediction_data="Common Cold",
        top_conditions=top_conditions,
        risk_data=risk_data,
        recommendations=recommendations,
    )

    assert pdf_bytes is not None
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500  # Valid PDF is several kilobytes
    assert pdf_bytes.startswith(b"%PDF")  # Valid PDF file header
