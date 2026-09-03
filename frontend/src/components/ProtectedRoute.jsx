import { Navigate, Outlet, useLocation } from "react-router-dom";

function ProtectedRoute() {
    const token = localStorage.getItem("access_token");
    const location = useLocation();

    if (!token) {
        const loginPath = location.pathname.startsWith("/caretaker")
            ? "/caretaker/login"
            : "/patient/login";
        return <Navigate to={loginPath} replace state={{ from: location }} />;
    }

    return <Outlet />;
}

export default ProtectedRoute;
