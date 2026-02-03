/**
 * API Service for communicating with Django backend.
 * Handles JWT authentication and all API requests.
 */
import axios from 'axios';

// Use environment variable for API URL in production, fallback to localhost for dev
const API_BASE_URL = import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL}/api`
    : 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
                    refresh: refreshToken,
                });

                const { access } = response.data;
                localStorage.setItem('access_token', access);

                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (refreshError) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// Authentication
export const login = async (username, password) => {
    const response = await axios.post(`${API_BASE_URL}/token/`, {
        username,
        password,
    });
    return response.data;
};

export const register = async (username, email, password, role = 'viewer') => {
    const response = await axios.post(`${API_BASE_URL}/register/`, {
        username,
        email,
        password,
        role,
    });
    return response.data;
};

// CSV Upload
export const uploadCSV = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

// Get Summary
export const getSummary = async () => {
    const response = await api.get('/summary/');
    return response.data;
};

// Get History
export const getHistory = async () => {
    const response = await api.get('/history/');
    return response.data;
};

// Get Dataset Detail
export const getDatasetDetail = async (datasetId) => {
    const response = await api.get(`/dataset/${datasetId}/`);
    return response.data;
};

// Generate Report
export const generateReport = (datasetId) => {
    // Return the API endpoint - the component will handle the authenticated request
    return `${API_BASE_URL}/report/${datasetId}/`;
};

export default api;
