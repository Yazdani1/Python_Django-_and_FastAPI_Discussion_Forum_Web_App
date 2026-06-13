import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

interface IRetryConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

export const apiClient = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const status = error.response?.status;
    const config = error.config as IRetryConfig | undefined;

    if (status === 401 && config && !config._retry) {
      config._retry = true;
      try {
        await axios.post(`${BASE_URL}/api/v1/auth/refresh`, {}, { withCredentials: true });
        return apiClient.request(config);
      } catch {
        // Refresh failed — reject silently; AuthContext handles this on initial load
        // and ProtectedRoute redirects unauthenticated users to login
      }
    }

    return Promise.reject(error);
  },
);
