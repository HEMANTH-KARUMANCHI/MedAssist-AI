-- MedAssist AI — Comprehensive Database Initialization Script
-- Automatically executed on PostgreSQL container startup

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'patient',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patient_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    phone VARCHAR(20),
    blood_group VARCHAR(10),
    height_cm NUMERIC(5, 2),
    weight_kg NUMERIC(5, 2),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_patient_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS caretaker_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    profession VARCHAR(100) NOT NULL,
    organization VARCHAR(150),
    years_of_experience INTEGER,
    specialization VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_caretaker_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS patient_symptoms (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    symptom_name VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_symptom_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS disease_predictions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    predicted_disease VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_disease_prediction_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS patient_risk_assessments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    fever VARCHAR(10),
    cough VARCHAR(10),
    fatigue VARCHAR(10),
    difficulty_breathing VARCHAR(10),
    age INTEGER,
    gender VARCHAR(20),
    blood_pressure VARCHAR(20),
    cholesterol_level VARCHAR(20),
    predicted_outcome VARCHAR(50),
    positive_model_score NUMERIC(5, 2),
    negative_model_score NUMERIC(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_risk_assessment_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS patient_reports (
    id SERIAL PRIMARY KEY,
    patient_user_id INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    stored_file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    file_size INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_report_patient_user
        FOREIGN KEY (patient_user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS patient_assignments (
    id SERIAL PRIMARY KEY,
    patient_user_id INTEGER NOT NULL,
    caretaker_user_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'Active',
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP,
    CONSTRAINT fk_patient
        FOREIGN KEY (patient_user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_caretaker
        FOREIGN KEY (caretaker_user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_patient
        UNIQUE (patient_user_id)
);
