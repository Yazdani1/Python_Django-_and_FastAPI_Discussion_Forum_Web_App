import type { AxiosRequestConfig } from 'axios';
import { apiClient } from './client';
import { handleError } from '@/utils/errorHandler';
import { notificationService } from '@/utils/notificationService';
import type { IApiResponse, IRequestOptions } from '@/types/api.types';

async function request<T>(
  config: AxiosRequestConfig,
  options: IRequestOptions = {},
): Promise<IApiResponse<T>> {
  const {
    customErrorMessage,
    showSuccessToast = false,
    showErrorToast = true,
    successMessage,
  } = options;

  try {
    const response = await apiClient.request<IApiResponse<T>>(config);
    if (showSuccessToast && (successMessage ?? response.data.message)) {
      notificationService.success(successMessage ?? response.data.message);
    }
    return response.data;
  } catch (error) {
    const parsed = handleError(error, customErrorMessage);
    if (showErrorToast) {
      notificationService.error(parsed.message);
    }
    throw parsed;
  }
}

export const ApiService = {
  get<T>(url: string, params?: Record<string, unknown>, options?: IRequestOptions): Promise<IApiResponse<T>> {
    return request<T>({ method: 'GET', url, params }, options);
  },

  post<T>(url: string, data?: unknown, options?: IRequestOptions): Promise<IApiResponse<T>> {
    return request<T>({ method: 'POST', url, data }, options);
  },

  put<T>(url: string, data?: unknown, options?: IRequestOptions): Promise<IApiResponse<T>> {
    return request<T>({ method: 'PUT', url, data }, options);
  },

  patch<T>(url: string, data?: unknown, options?: IRequestOptions): Promise<IApiResponse<T>> {
    return request<T>({ method: 'PATCH', url, data }, options);
  },

  delete<T>(url: string, options?: IRequestOptions): Promise<IApiResponse<T>> {
    return request<T>({ method: 'DELETE', url }, options);
  },
};
