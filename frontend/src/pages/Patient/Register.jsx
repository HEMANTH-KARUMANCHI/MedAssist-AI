import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import {
    FaHospital,
    FaUser,
    FaEnvelope,
    FaLock,
    FaUserPlus,
    FaHeartbeat,
    FaRobot,
    FaShieldAlt,
    FaArrowLeft
} from "react-icons/fa";

import { registerUser } from "../../services/authService";
import { useToast } from "../../context/ToastContext";

import "../../styles/Patient.css";

function PatientRegister() {

    const navigate = useNavigate();
    const { showToast } = useToast();

    const [formData, setFormData] = useState({

        full_name: "",
        email: "",
        password: "",
        confirmPassword: ""

    });

    const handleChange = (e) => {

        setFormData({

            ...formData,
            [e.target.name]: e.target.value

        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        if (formData.password !== formData.confirmPassword) {

            showToast("Passwords do not match. Please re-enter.", "warning");

            return;

        }

        try {

            await registerUser({

                full_name: formData.full_name,
                email: formData.email,
                password: formData.password,
                role: "patient"

            });

            showToast("Registration Successful! Please sign in.", "success");

            navigate("/patient/login");

        }

        catch (error) {
            console.error(error);
            if (!error.response) {
                showToast("Cannot connect to server. Please ensure backend is running on port 8000.", "error");
            } else {
                showToast(error.response.data?.detail || "Registration Failed. Please try again.", "error");
            }
        }

    };

    return (

        <div className="patient-login-page">

            <div className="login-overlay"></div>

            <div className="login-wrapper">

                {/* Left */}

                <div className="login-left">

                    <div className="brand">

                        <FaHospital />

                        <span>MedAssist AI</span>

                    </div>

                    <h1>

                        Join MedAssist AI

                    </h1>

                    <p>

                        Create your patient account and experience
                        AI-powered disease prediction, secure medical
                        records, personalized healthcare
                        recommendations, and intelligent health
                        monitoring.

                    </p>

                    <div className="login-features">

                        <div className="login-feature">

                            <FaHeartbeat />

                            <span>Track Your Health</span>

                        </div>

                        <div className="login-feature">

                            <FaRobot />

                            <span>AI Disease Prediction</span>

                        </div>

                        <div className="login-feature">

                            <FaShieldAlt />

                            <span>Secure Medical Data</span>

                        </div>

                    </div>

                </div>

                {/* Right */}

                <div className="login-card">

                    <h2>

                        Patient Registration

                    </h2>

                    <p>

                        Create your account

                    </p>

                    <form onSubmit={handleSubmit}>

                        <div className="input-group">

                            <FaUser />

                            <input

                                type="text"

                                name="full_name"

                                placeholder="Full Name"

                                value={formData.full_name}

                                onChange={handleChange}

                                required

                            />

                        </div>

                        <div className="input-group">

                            <FaEnvelope />

                            <input

                                type="email"

                                name="email"

                                placeholder="Email Address"

                                value={formData.email}

                                onChange={handleChange}

                                required

                            />

                        </div>

                        <div className="input-group">

                            <FaLock />

                            <input

                                type="password"

                                name="password"

                                placeholder="Password"

                                value={formData.password}

                                onChange={handleChange}

                                required

                            />

                        </div>

                        <div className="input-group">

                            <FaLock />

                            <input

                                type="password"

                                name="confirmPassword"

                                placeholder="Confirm Password"

                                value={formData.confirmPassword}

                                onChange={handleChange}

                                required

                            />

                        </div>

                        <button

                            className="login-btn"

                            type="submit"

                        >

                            <FaUserPlus />

                            Register

                        </button>

                    </form>

                    <div className="login-links">

                        <p>

                            Already have an account?

                        </p>

                        <Link to="/patient/login">

                            Login Here

                        </Link>

                        <Link

                            to="/"

                            className="back-home"

                        >

                            <FaArrowLeft />

                            Back to Home

                        </Link>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default PatientRegister;