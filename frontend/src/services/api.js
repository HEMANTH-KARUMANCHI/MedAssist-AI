import axios from "axios";

const getBaseUrl = () => {
    if (import.meta.env.VITE_API_URL && !import.meta.env.VITE_API_URL.includes("localhost") && !import.meta.env.VITE_API_URL.includes("127.0.0.1")) {
        return import.meta.env.VITE_API_URL;
    }
    const hostname = typeof window !== "undefined" && window.location.hostname ? window.location.hostname : "127.0.0.1";
    return `http://${hostname}:8000`;
};

const api = axios.create({
    baseURL: getBaseUrl(),
});


api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");
        }
        return Promise.reject(error);
    }
);

export default api;