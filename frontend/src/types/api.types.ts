export interface IErrorDetail {
  field: string | null;
  message: string;
}

export interface IMeta {
  page: number | null;
  page_size: number | null;
  total: number | null;
  total_pages: number | null;
}

export interface IApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data: T | null;
  errors: IErrorDetail[] | null;
  meta: IMeta | null;
}

export interface IApiError {
  success: false;
  message: string;
  data: null;
  errors: IErrorDetail[] | null;
  meta: null;
}

export type TApiMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface IRequestOptions {
  customErrorMessage?: string;
  showSuccessToast?: boolean;
  showErrorToast?: boolean;
  successMessage?: string;
}
