import { Link, useLocation, useNavigate } from "react-router-dom";
import { FaHospital, FaUserCircle, FaSignOutAlt, FaArrowLeft } from "react-icons/fa";
import { useToast } from "../context/ToastContext";

import "../styles/AppShell.css";

function Navbar() {
    const { pathname } = useLocation();
    const navigate = useNavigate();
    const { showToast } = useToast();

    const isCaretaker = pathname.startsWith("/caretaker");
    const dashboardPath = isCaretaker
        ? "/caretaker/dashboard"
        : "/patient/dashboard";

    const isDashboard = pathname === "/patient/dashboard" || pathname === "/caretaker/dashboard";

    const handleLogout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("token_type");
        showToast("Logged out successfully.", "info");
        navigate(isCaretaker ? "/caretaker/login" : "/patient/login");
    };

    return (
        <header className="app-navbar">
            <div className="app-navbar__left">
                <Link to={dashboardPath} className="app-navbar__brand">
                    <FaHospital />
                    <span>MedAssist AI</span>
                </Link>

                {!isDashboard && (
                    <Link to={dashboardPath} className="app-navbar__back-link">
                        <FaArrowLeft />
                        <span>Back to Dashboard</span>
                    </Link>
                )}
            </div>

            <div className="app-navbar__right">
                <Link to={isCaretaker ? "/caretaker/profile" : "/patient/profile"} className="app-navbar__profile">
                    <FaUserCircle />
                    <span>{isCaretaker ? "Caretaker Portal" : "Patient Portal"}</span>
                </Link>

                <button
                    onClick={handleLogout}
                    className="app-navbar__logout-btn"
                    title="Sign Out / Exit"
                >
                    <FaSignOutAlt />
                    <span>Exit</span>
                </button>
            </div>
        </header>
    );
}

export default Navbar;
