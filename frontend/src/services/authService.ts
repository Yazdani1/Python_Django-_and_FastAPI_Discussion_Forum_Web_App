import { ApiService } from '@/api/service';
import type { IAuthUser, ILoginRequest, IRegisterRequest } from '@/types/auth.types';
import type { IApiResponse } from '@/types/api.types';

const BASE = '/api/v1/auth';

export const authService = {
  register(data: IRegisterRequest): Promise<IApiResponse<IAuthUser>> {
    return ApiService.post<IAuthUser>(`${BASE}/register`, data, {
      showSuccessToast: true,
      successMessage: 'Account created successfully!',
    });
  },

  login(data: ILoginRequest): Promise<IApiResponse<IAuthUser>> {
    return ApiService.post<IAuthUser>(`${BASE}/login`, data, {
      showSuccessToast: true,
      successMessage: 'Welcome back!',
    });
  },

  logout(): Promise<IApiResponse<null>> {
    return ApiService.post<null>(`${BASE}/logout`, undefined, {
      showErrorToast: false,
    });
  },

  getMe(): Promise<IApiResponse<IAuthUser>> {
    return ApiService.get<IAuthUser>('/api/v1/users/me', undefined, {
      showErrorToast: false,
    });
  },
};
