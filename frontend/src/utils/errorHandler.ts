import axios, { AxiosError } from 'axios';
import type { IApiError, IErrorDetail } from '@/types/api.types';

export interface IParsedError {
  message: string;
  errors: IErrorDetail[];
  statusCode: number;
}

function parseApiError(error: AxiosError<IApiError>): IParsedError {
  const statusCode = error.response?.status ?? 0;
  const responseData = error.response?.data;

  if (responseData && typeof responseData === 'object') {
    return {
      message: responseData.message ?? 'An error occurred',
      errors: responseData.errors ?? [],
      statusCode,
    };
  }

  return {
    message: getDefaultMessageForStatus(statusCode),
    errors: [],
    statusCode,
  };
}

function getDefaultMessageForStatus(status: number): string {
  const messages: Record<number, string> = {
    400: 'Bad request. Please check your input.',
    401: 'Your session has expired. Please log in again.',
    403: 'You do not have permission to perform this action.',
    404: 'The requested resource was not found.',
    409: 'A conflict occurred. The resource may already exist.',
    422: 'Validation failed. Please check your input.',
    429: 'Too many requests. Please slow down.',
    500: 'An internal server error occurred.',
    502: 'Service temporarily unavailable.',
    503: 'Service temporarily unavailable.',
  };
  return messages[status] ?? 'An unexpected error occurred.';
}

export function handleError(error: unknown, customMessage?: string): IParsedError {
  if (axios.isAxiosError(error)) {
    const parsed = parseApiError(error as AxiosError<IApiError>);
    if (customMessage) {
      parsed.message = customMessage;
    }
    return parsed;
  }

  if (error instanceof Error) {
    return { message: customMessage ?? error.message, errors: [], statusCode: 0 };
  }

  return { message: customMessage ?? 'An unexpected error occurred.', errors: [], statusCode: 0 };
}
