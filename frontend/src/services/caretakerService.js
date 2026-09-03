import api from "./api";

// Create Caretaker Profile
export const createCaretakerProfile = async (profileData) => {

    const response = await api.post(
        "/caretaker/profile",
        profileData
    );

    return response.data;

};

// Get Caretaker Profile
export const getCaretakerProfile = async () => {

    const response = await api.get(
        "/caretaker/profile"
    );

    return response.data;

};

// Update Caretaker Profile
export const updateCaretakerProfile = async (profileData) => {

    const response = await api.put(
        "/caretaker/profile",
        profileData
    );

    return response.data;

};



export const getAssignedPatients = async () => {

    const response = await api.get(
        "/caretaker/patients"
    );

    return response.data;

};


// Get details of an assigned patient
export const getPatientDetails = async (patientUserId) => {
    const response = await api.get(`/caretaker/patients/${patientUserId}`);
    return response.data;
};

// Get Caretaker Analytics
export const getCaretakerAnalytics = async () => {
    const response = await api.get("/caretaker/analytics");
    return response.data;
};

// Create Clinical Care Plan
export const createCarePlan = async (planData) => {
    const response = await api.post("/caretaker/care-plans", planData);
    return response.data;
};

// Get Care Plans
export const getCarePlans = async (patientId = null) => {
    const url = patientId ? `/caretaker/care-plans?patient_id=${patientId}` : "/caretaker/care-plans";
    const response = await api.get(url);
    return response.data;
};

// Delete Care Plan
export const deleteCarePlan = async (planId) => {
    const response = await api.delete(`/caretaker/care-plans/${planId}`);
    return response.data;
};


