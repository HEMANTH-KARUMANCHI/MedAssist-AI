from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.dataset_loader import load_all_datasets
from app.database import init_db_tables
from app.auth import router as auth_router
from app.patient import router as patient_router
from app.caretaker import router as caretaker_router
from app.analytics import router as analytics_router


app = FastAPI(
    title="MedAssist AI API",
    description="AI-Powered Disease Prediction, Patient Risk Assessment & Healthcare Analytics API",
    version="1.0.0"
)

# CORS Configuration - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": f"Server Error: {str(exc)}"},
        headers={"Access-Control-Allow-Origin": "*"}
    )


@app.on_event("startup")
def on_startup():
    init_db_tables()


app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(caretaker_router)
app.include_router(analytics_router)

@app.get("/")
def read_root():
    return {"message": "MedAssist AI API is running"}


@app.get("/datasets/summary")
def get_dataset_summary():
    patient_profile, disease_dataset, symptom_severity = load_all_datasets()

    return {
        "patient_profile_dataset": {
            "rows": patient_profile.shape[0],
            "columns": patient_profile.shape[1]
        },
        "disease_prediction_dataset": {
            "rows": disease_dataset.shape[0],
            "columns": disease_dataset.shape[1]
        },
        "symptom_severity_dataset": {
            "rows": symptom_severity.shape[0],
            "columns": symptom_severity.shape[1]
        }
    }
