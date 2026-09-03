# 🏥 MedAssist AI — Intelligent Healthcare Assistant & Clinical Decision Support System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.x-61DAFB.svg?style=flat&logo=React&logoColor=black)](https://reactjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg?style=flat&logo=PostgreSQL&logoColor=white)](https://www.postgresql.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3.0-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![Pytest](https://img.shields.io/badge/Tests-10%20Passed-brightgreen.svg?style=flat&logo=pytest&logoColor=white)](https://pytest.org)

**MedAssist AI** is an end-to-end, full-stack intelligent healthcare platform designed to empower patients and assist medical professionals. It leverages machine learning to predict potential diseases from symptoms, evaluate clinical risk factors, recommend personalized treatment options, generate downloadable clinical reports, and provide interactive healthcare analytics with caretaker collaboration.

---

## 🌟 Key Features

### 1. 🤖 AI Disease Prediction Engine
- Analyzes patient-reported symptoms across **131 clinical features**.
- Accurately predicts across **41 distinct disease classes** with **100% test accuracy** and **100% 5-fold cross-validation score**.
- Computes ranked differential diagnosis probabilities and displays the top 3 potential conditions with percentage confidence.

### 2. ⚠️ Clinical Patient Risk Assessment
- Assesses key vital signs and risk factors (Age, Gender, Blood Pressure, Cholesterol, Fever, Cough, Fatigue, Dyspnea).
- Scikit-Learn pipeline with numerical standardization and categorical encoding.
- **92.16% test accuracy**, **97.69% ROC-AUC**, and **100% Recall for high-risk patients** (0 false negatives for clinical safety).

### 3. 💊 Evidence-Based Treatment Suggestions & Health Advisory
- Automatically maps predicted diseases to comprehensive medical recommendations:
  - **Primary medications & dosages**
  - **Dietary guidelines & restrictions**
  - **Rest & recovery protocols**
  - **Precautionary measures & warning signs**
- Synthesizes risk level and disease diagnosis into an actionable **Health Advisory** with clinical urgency indicators (`High Risk / Immediate Medical Attention`, `Moderate Risk / Doctor Consultation`, `Low Risk / Home Care`).

### 4. 📄 Automated Clinical PDF Report Generation
- Generates professional, publication-ready PDF medical reports using `fpdf2`.
- Includes patient profile data, symptom records, AI disease prediction confidence, risk stratification scores, medications, and clinical disclaimers.

### 5. 📊 Interactive Health Analytics Dashboard
- Visualizes patient health trends using **Recharts**:
  - **Prediction Activity & Health Severity Over Time** (Interactive Line Chart)
  - **Most Frequently Diagnosed Conditions** (Horizontal Bar Chart)
  - **Common Symptoms Breakdown** (Bar Chart)
  - **Risk Stratification Distribution** (Area Chart)
  - Summary metric cards (Total Predictions, High Risk Alerts, Recorded Symptoms, Active Caretaker).

### 6. 🤝 Caretaker Collaboration & Patient Monitoring
- Dedicated **Caretaker Portal** for doctors, nurses, and family caretakers.
- Allows caretakers to view assigned patients, inspect historical predictions, monitor risk levels, review uploaded medical records, and update professional profiles.

---

## 🏗️ System Architecture

```
                                  +-----------------------------+
                                  |     User Web Browser        |
                                  | (Patient & Caretaker Views) |
                                  +--------------+--------------+
                                                 |
                                     HTTP Requests (Port 3000)
                                                 v
                                  +-----------------------------+
                                  |     Nginx Web Server        |
                                  | (React SPA Static Hosting)  |
                                  +--------------+--------------+
                                                 |
                                     REST API Calls (Port 8000)
                                                 v
                                  +-----------------------------+
                                  |     FastAPI Backend API     |
                                  | (JWT Auth, Endpoints, CORS) |
                                  +------+---------------+------+
                                         |               |
                    +--------------------+               +--------------------+
                    |                                                         |
                    v                                                         v
    +-------------------------------+                         +-------------------------------+
    |      PostgreSQL Database      |                         |      Machine Learning Engine  |
    | (Users, Profiles, Symptoms,   |                         | - Disease Classifier (RF)     |
    |  Predictions, Reports, Assocs)|                         | - Risk Pipeline (Scaler + RF) |
    +-------------------------------+                         +-------------------------------+
```

---

## 📊 Machine Learning Model Benchmarks

| Metric | Disease Prediction Model | Patient Risk Assessment Model |
| :--- | :--- | :--- |
| **Model Type** | `RandomForestClassifier` | `Pipeline(StandardScaler, OneHotEncoder, RF)` |
| **Input Features** | 131 binary symptom features | 8 clinical features (Age, BP, Cholesterol, etc.) |
| **Target Classes** | 41 disease categories | Binary (`High Risk` vs `Low Risk`) |
| **Test Accuracy** | **100.00%** | **92.16%** |
| **F1-Score** | **100.00%** | **92.86%** |
| **Recall (Positive)** | **100.00%** | **100.00% (0 False Negatives)** |
| **ROC-AUC Score** | **1.0000** | **97.69%** |
| **5-Fold Cross-Val** | **100.00%** | **91.80%** |

Validation metrics generated via `backend/validate_models.py` and exported to `backend/models/validation_report.json`.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite, React Router v6, Axios, Lucide React Icons, Recharts, Custom Glassmorphism CSS with Mobile Responsiveness.
- **Backend**: FastAPI, Python 3.10, Uvicorn, Pydantic v2, Python-JOSE (JWT), Native Bcrypt.
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib.
- **PDF Engine**: `fpdf2` with sanitized Latin-1 encoding and clinical layout templates.
- **Database**: PostgreSQL 15 with automated startup schema verification and auto-migrations.
- **DevOps & Containerization**: Docker, Docker Compose, Nginx, Pytest test suite.

---

## 🚀 Quickstart Guide

### Method A: One-Command Docker Setup (Recommended)

1. Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running.
2. Clone this repository and navigate to the project root:
   ```bash
   git clone https://github.com/HEMANTH-KARUMANCHI/MedAssist-AI.git
   cd MedAssist-AI
   ```
3. Start the multi-container platform:
   ```bash
   docker compose up --build
   ```
4. Access the applications:
   - **Frontend App**: [http://localhost:3000](http://localhost:3000)
   - **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Method B: Manual Local Development Setup

#### 1. Database Setup
Ensure PostgreSQL is running locally on port `5432` with a database named `medassist_ai` (or adjust `.env`).

#### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create & activate Python virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows
# source venv/bin/activate # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run database table initialization
python -c "from app.database import init_db_tables; init_db_tables()"

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

#### 3. Frontend Setup
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Automated Testing

Run the automated test suite covering AI models, top conditions inference, treatment mappings, and PDF generation:

```bash
cd backend
pytest -v
```

**Test Coverage Summary:**
- `test_disease_feature_names_loaded` — Verifies feature vector integrity.
- `test_disease_prediction_basic` — Evaluates Random Forest inference.
- `test_disease_prediction_top_conditions` — Tests top-3 differential diagnosis calculation.
- `test_disease_metadata_helpers` — Tests severity and precautions retrieval.
- `test_patient_risk_assessment_positive` — Tests clinical risk classification pipeline.
- `test_patient_risk_assessment_missing_fields` — Tests graceful fallback handling.
- `test_treatment_suggestions_exact_match` — Verifies treatments for all 41 diseases.
- `test_pdf_report_generation` — Validates binary PDF creation and metadata.

---

## 📁 Repository Structure

```
MedAssist-AI/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI application entrypoint & middleware
│   │   ├── auth.py                  # JWT authentication & bcrypt security
│   │   ├── database.py              # PostgreSQL connection & auto-migrations
│   │   ├── schemas.py               # Pydantic request/response schemas
│   │   ├── patient.py               # Patient endpoints (symptoms, prediction, advisory)
│   │   ├── caretaker.py             # Caretaker portal endpoints & profile management
│   │   ├── analytics.py             # Health trend aggregations & Recharts endpoints
│   │   ├── treatment_data.py        # 41 disease clinical treatment dictionary
│   │   ├── report_generator.py      # Automated PDF report builder (fpdf2)
│   │   └── dataset_loader.py        # Dataset ingestion utilities
│   ├── models/
│   │   ├── disease_prediction_model.pkl
│   │   ├── disease_features.pkl
│   │   ├── patient_risk_model.pkl
│   │   └── validation_report.json   # Exported ML performance benchmarks
│   ├── scripts/
│   │   └── init_db.sql              # Master database schema script
│   ├── tests/
│   │   ├── conftest.py              # Pytest client fixtures
│   │   ├── test_ai_models.py        # AI inference unit tests
│   │   └── test_recommendations_and_pdf.py # Treatment & PDF unit tests
│   ├── validate_models.py           # ML validation & benchmarking script
│   ├── requirements.txt             # Python dependencies
│   ├── pytest.ini                   # Pytest configuration
│   └── Dockerfile                   # Backend Docker container specification
├── frontend/
│   ├── src/
│   │   ├── components/              # Reusable UI components & layouts
│   │   ├── context/                 # React Context (Toast notifications)
│   │   ├── pages/
│   │   │   ├── Patient/             # Patient views (Dashboard, Symptoms, Prediction, Advisory, Reports, Analytics)
│   │   │   └── caretaker/           # Caretaker views (Dashboard, Profile, Patient Monitoring)
│   │   ├── services/                # Axios API service clients
│   │   ├── styles/                  # Responsive glassmorphism CSS
│   │   ├── App.jsx                  # Main application routes & protected guards
│   │   └── main.jsx                 # React root mounting
│   ├── nginx.conf                   # Production Nginx reverse proxy configuration
│   ├── package.json                 # Node.js dependencies
│   └── Dockerfile                   # Frontend Docker container specification
├── datasets/                        # Training & testing medical datasets (CSV)
├── docker-compose.yml               # Multi-container orchestration
├── .env.example                     # Environment variables template
└── README.md                        # Master project documentation
```

---

## 🔒 Security & Privacy

- **Password Hashing**: Native `bcrypt` with automatic 72-byte safe truncation.
- **Token Security**: Stateless JWT (HS256) with 30-minute expiration.
- **Role-Based Access Control (RBAC)**: Strict separation between `patient` and `caretaker` route authorization.
- **Sanitized Reports**: Medical report exports sanitize input and format clinical disclaimers.

---

## 📜 License & Disclaimers

This project is developed for educational and clinical decision support purposes. **MedAssist AI is not a substitute for professional medical diagnosis or emergency treatment.** Always consult a qualified healthcare provider for medical conditions.
