import React, { createContext, useContext, useState, useCallback } from "react";
import {
    FaCheckCircle,
    FaExclamationCircle,
    FaInfoCircle,
    FaExclamationTriangle,
    FaTimes
} from "react-icons/fa";
import "../styles/Toast.css";

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
    const [toasts, setToasts] = useState([]);

    const removeToast = useCallback((id) => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
    }, []);

    const showToast = useCallback((message, type = "info", duration = 4000) => {
        const id = Date.now() + Math.random().toString(36).substring(2, 9);
        const newToast = { id, message, type };

        setToasts((prev) => [...prev, newToast]);

        if (duration > 0) {
            setTimeout(() => {
                removeToast(id);
            }, duration);
        }
    }, [removeToast]);

    const getIcon = (type) => {
        switch (type) {
            case "success":
                return <FaCheckCircle className="toast-icon" />;
            case "error":
                return <FaExclamationCircle className="toast-icon" />;
            case "warning":
                return <FaExclamationTriangle className="toast-icon" />;
            case "info":
            default:
                return <FaInfoCircle className="toast-icon" />;
        }
    };

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}
            <div className="toast-container" aria-live="polite">
                {toasts.map((t) => (
                    <div
                        key={t.id}
                        className={`toast-item toast-${t.type}`}
                        role="alert"
                    >
                        <div className="toast-content">
                            {getIcon(t.type)}
                            <span>{t.message}</span>
                        </div>
                        <button
                            className="toast-close"
                            onClick={() => removeToast(t.id)}
                            aria-label="Close notification"
                        >
                            <FaTimes />
                        </button>
                    </div>
                ))}
            </div>
        </ToastContext.Provider>
    );
}

export function useToast() {
    const context = useContext(ToastContext);
    if (!context) {
        throw new Error("useToast must be used within a ToastProvider");
    }
    return context;
}
